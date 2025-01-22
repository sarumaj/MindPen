import asyncio
from deepgram import DeepgramClient
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))


async def analyze_sentiment_with_deepgram(journal_content):
    #  process a single journal
    payload = {"buffer": journal_content}
    options = {"sentiment": True, "language": "en"}
    response = deepgram.read.analyze.v("1").analyze_text(payload, options)
    return response["results"]["sentiments"]["average"]["sentiment"]


async def process_journal_entries(journal_entries):
    # process all journal entries
    results = {}
    for entry in journal_entries:
        sentiment = await analyze_sentiment_with_deepgram(entry)
        results[entry] = sentiment
    return results


async def process_dataset_with_deepgram():
    # the main function to handles dataset processing
    df = pd.read_csv("lemotif-data-cleaned-flat.csv")

    journal_entries = df["Answer"].tolist()

    results = await process_journal_entries(journal_entries)

    # Convert results dictionary to DataFrame
    new_df = pd.DataFrame(list(results.items()), columns=["Journals", "Sentiment"])

    # DataFrame to a CSV file
    new_df.to_csv("Sentiment Analysis Dataset.csv", encoding="utf-8", index=False)


if __name__ == "__main__":
    asyncio.run(process_dataset_with_deepgram())
