from channels.generic.websocket import AsyncWebsocketConsumer
from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions, LiveTranscriptionEvents
from dotenv import load_dotenv
import os

load_dotenv()


class TranscriptConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        try:
            # initiate Deepgram client
            config = DeepgramClientOptions(options={"keepalive": "true"})
            self.dg_client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"), config=config)

            # to the Deepgram WebSocket endpoint
            self.dg_connection = self.dg_client.listen.asyncwebsocket.v("1")

            # register event handlers
            self.dg_connection.on(LiveTranscriptionEvents.Open, self.on_open)
            self.dg_connection.on(LiveTranscriptionEvents.Transcript, self.on_transcript)
            self.dg_connection.on(LiveTranscriptionEvents.Error, self.on_error)
            self.dg_connection.on(LiveTranscriptionEvents.Close, self.on_close)

            # options for the transcription
            self.options = LiveOptions(
                punctuate=True,
                interim_results=False,
                language="en-GB"
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
