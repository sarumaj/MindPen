from django.contrib.auth import get_user
from Journaling.models import Journal
import asyncio
from deepgram import DeepgramClient
from google.cloud import language_v2
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

load_dotenv()


def get_last_journal_for_user(request):
    """
    fetches the most recent, unprocessed journal entry for the current user
    """
    user = get_user(request)
    if user.is_authenticated:
        journal = (
            Journal.objects.filter(author=user, processed=False)
            .order_by("-journal_date")
            .first()
        )
        if not journal:
            return None
        return journal
    return None


async def analyze_sentiment_with_deepgram(journal_content):
    """
    sends the text to Deepgram for sentiment analysis
    """

    # initialize the Deepgram client
    deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))

    # prepare payload and options
    payload = {"buffer": journal_content}
    options = {"sentiment": True, "language": "en"}

    # performs sentiment analysis
    response = deepgram.read.analyze.v("1").analyze_text(payload, options)

    return response.to_dict()


async def analyze_sentiment_with_gcloud(journal_content):
    """
    sends the text to Google Cloud Natural Language API for sentiment analysis
    """
    credentials = Credentials.from_service_account_file(
        os.getenv("GOOGLE_CLOUD_CREDENTIALS_FILE")
    )
    client = language_v2.LanguageServiceAsyncClient(credentials=credentials)

    document = language_v2.Document()
    document.content = journal_content
    document.language_code = "en"

    request = language_v2.AnalyzeSentimentRequest(
        document=document, encoding_type=language_v2.EncodingType.UTF8
    )

    response = await client.analyze_sentiment(request=request)
    score = response.document_sentiment.score
    result = {
        "results": {
            "sentiments": {
                "average": {
                    "sentiment": (
                        "neutral"
                        if abs(score) * 3.0 < 1.0
                        else "positive" if score > 0.0 else "negative"
                    ),
                    "sentiment_score": 0.0,
                },
            },
        },
    }
    return result


def analyze_last_journal_sentiment(request):
    # fetch the last unprocessed journal for the user
    journal = get_last_journal_for_user(request)
    if not journal:
        return None

    async def analyze_sentiment(journal_content):
        async def analyze_sentiment_no_op():
            return {
                "results": {
                    "sentiments": {
                        "average": {
                            "sentiment": "neutral",
                            "sentiment_score": 0.0,
                        },
                    },
                },
            }

        if os.getenv("DEEPGRAM_API_KEY"):
            return await analyze_sentiment_with_deepgram(journal_content)

        if os.getenv("GOOGLE_CLOUD_CREDENTIALS_FILE"):
            return await analyze_sentiment_with_gcloud(journal_content)

        print("no available sentiment analysis service configured")
        return await analyze_sentiment_no_op()

    # perform sentiment analysis
    result = asyncio.run(analyze_sentiment(journal.content))

    # add processed flag and save the journal
    journal.processed = True
    journal.save()

    return result["results"]["sentiments"]["average"]
