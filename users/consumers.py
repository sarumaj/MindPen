import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveOptions,
    LiveTranscriptionEvents,
)
from google.cloud import speech_v1 as speech
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

load_dotenv()


class TranscriptConsumerDeepgram(AsyncWebsocketConsumer):
    """
    TranscriptConsumerDeepgram is a WebSocket consumer that streams audio data to
    the Deepgram API and sends the transcription results back to the client.
    """

    async def connect(self):
        try:
            # initiate Deepgram client
            config = DeepgramClientOptions(options={"keepalive": "true"})
            self.dg_client = DeepgramClient(
                api_key=os.getenv("DEEPGRAM_API_KEY"), config=config
            )

            # to the Deepgram WebSocket endpoint
            self.dg_connection = self.dg_client.listen.asyncwebsocket.v("1")

            # register event handlers
            self.dg_connection.on(LiveTranscriptionEvents.Open, self.on_open)
            self.dg_connection.on(
                LiveTranscriptionEvents.Transcript, self.on_transcript
            )
            self.dg_connection.on(LiveTranscriptionEvents.Error, self.on_error)
            self.dg_connection.on(LiveTranscriptionEvents.Close, self.on_close)

            # options for the transcription
            self.options = LiveOptions(
                punctuate=True, interim_results=False, language="en-GB"
            )

            # Start the WebSocket connection
            await self.dg_connection.start(self.options)
            await self.accept()

        except Exception as e:
            raise Exception(f"Failed to connect to Deepgram: {e}")

    async def disconnect(self, close_code):
        if self.dg_connection:
            await self.dg_connection.finish()

    async def receive(self, bytes_data):
        # forward the audio data to Deepgram
        if self.dg_connection:
            await self.dg_connection.send(bytes_data)

    async def on_open(self, *args, **kwargs):
        print("Connection opened!")

    async def on_close(self, *args, **kwargs):
        print("Connection closed.")

    async def on_transcript(self, *args, **kwargs):
        # get the transcription result from kwargs
        result = kwargs.get("result")
        if result:
            transcript = result.channel.alternatives[0].transcript

            if transcript:
                # Send the transcript to the WebSocket client
                await self.send(transcript)

    async def on_error(self, *args, **kwargs):
        error = kwargs.get("error")
        print(f"Deepgram error: {error}")


class TranscriptConsumerGooglecloud(AsyncWebsocketConsumer):
    """
    TranscriptConsumerGooglecloud is a WebSocket consumer that streams audio data to
    the Google Cloud Speech-to-Text API and sends the transcription results back to
    the client.
    """

    async def connect(self):
        try:
            # Load Google Cloud credentials
            self.credentials = service_account.Credentials.from_service_account_file(
                os.getenv("GOOGLE_CLOUD_CREDENTIALS_FILE")
            )
            self.speech_client = speech.SpeechAsyncClient(credentials=self.credentials)

            # Accept the WebSocket connection
            await self.accept()
            print("WebSocket connection established.")

            # Create a queue to handle incoming audio data
            self.audio_queue = asyncio.Queue()

            # Start the streaming transcription task
            self.transcription_task = asyncio.create_task(self.stream_transcription())

        except Exception as e:
            print(f"Failed to connect to Google Speech-to-Text API: {e}")
            raise Exception(f"Failed to connect to Google Speech-to-Text API: {e}")

    async def disconnect(self, close_code):
        # Cancel the transcription task and close the WebSocket
        if hasattr(self, "transcription_task"):
            self.transcription_task.cancel()
        print("WebSocket connection closed.")

    async def receive(self, bytes_data):
        try:
            # Add the received audio data to the queue
            await self.audio_queue.put(bytes_data)
        except Exception as e:
            print(f"Error processing audio data: {e}")
            await self.send(f"Error: {e}")

    async def stream_transcription(self):
        """Handles streaming audio to Google Cloud Speech-to-Text API."""
        try:
            # Configure the streaming recognition settings
            self.config = speech.StreamingRecognitionConfig(
                config=speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                    sample_rate_hertz=48000,
                    language_code="en-GB",
                ),
                interim_results=False,
            )

            # Define a generator to stream audio data from the queue
            async def audio_generator():
                # Send the initial request with the streaming config
                yield speech.StreamingRecognizeRequest(streaming_config=self.config)
                while True:
                    # Get the next chunk of audio data from the queue and send it
                    chunk = await self.audio_queue.get()
                    yield speech.StreamingRecognizeRequest(audio_content=chunk)

            # Call the streaming_recognize method
            responses = await self.speech_client.streaming_recognize(
                requests=audio_generator()
            )
            async for response in responses:
                for result in filter(lambda result: result.is_final, response.results):
                    # Send the transcription result back to the WebSocket client
                    transcript = result.alternatives[0].transcript
                    print(f"Transcription result: {transcript}")
                    await self.send(transcript)

        except Exception as e:
            print(f"Error during streaming transcription: {e}")
            await self.send(f"Error: {e}")


def selectTranscriptConsumer():
    """
    Selects the appropriate TranscriptConsumer based on the available transcription
    services.
    """

    class TranscriptConsumerNoOp(AsyncWebsocketConsumer):
        async def connect(self):
            await self.accept()

        async def disconnect(self, close_code):
            pass

        async def receive(self, text_data=None, bytes_data=None):
            pass

    if os.getenv("DEEPGRAM_API_KEY"):
        return TranscriptConsumerDeepgram

    if os.getenv("GOOGLE_CLOUD_CREDENTIALS_FILE"):
        return TranscriptConsumerGooglecloud

    print("no available transcription service configured")
    return TranscriptConsumerNoOp
