from django.contrib.auth import get_user
from Journaling.models import Journal
import asyncio
from deepgram import DeepgramClient
from dotenv import load_dotenv
from django.http import JsonResponse
import os

load_dotenv()


def get_last_journal_for_user(request):
    user = get_user(request)
    if user.is_authenticated:
        # Return the most recent journal entry
        return Journal.objects.filter(author=user).order_by('-journal_date').first()
    return None


async def analyze_sentiment_with_deepgram(journal_content):
    """
    Sends the journal content to Deepgram for sentiment analysis.
    """
    # Initialize the Deepgram client
    deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))

    print(journal_content)
    # Prepare payload and options
    payload = {"buffer": journal_content}
    options = {"sentiment": True, "language": "en"}

    # Perform analysis
    response = deepgram.read.analyze.v("1").analyze_text(payload, options)

    return response.to_dict()


def analyze_last_journal_sentiment(request):
    """
    Fetches the last journal entry for the current user and analyzes its sentiment.
    """
    # Fetch the last journal for the user
    journal = get_last_journal_for_user(request)

    if not journal:
        return JsonResponse({"error": "No journal found for the current user."})

    # Get the journal content
    journal_content = journal.content

    # Perform sentiment analysis
    result = asyncio.run(analyze_sentiment_with_deepgram(journal_content))

    return result["results"]["sentiments"]["average"]
