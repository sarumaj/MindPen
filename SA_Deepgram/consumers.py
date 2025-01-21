from django.contrib.auth import get_user
from Journaling.models import Journal
import asyncio
from deepgram import DeepgramClient
from dotenv import load_dotenv
import os

load_dotenv()


def get_last_journal_for_user(request):
    """
    fetches the most recent, unprocessed journal entry for the current user
    """
    user = get_user(request)
    if user.is_authenticated:
        journal = Journal.objects.filter(author=user, processed=False).order_by('-journal_date').first()
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


def analyze_last_journal_sentiment(request):

    # fetch the last unprocessed journal for the user
    journal = get_last_journal_for_user(request)

    if not journal:
        return None

    # perform sentiment analysis
    result = asyncio.run(analyze_sentiment_with_deepgram(journal.content))

    # add processed flag and save the journal
    journal.processed = True
    journal.save()

    return result["results"]["sentiments"]["average"]
