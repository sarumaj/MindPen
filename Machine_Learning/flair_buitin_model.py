# import pandas as pd
# from flair.models import TextClassifier
# from flair.data import Sentence
#
#
# def pre_process_and_train():
#     df = pd.read_csv("lemotif-data-cleaned-flat.csv")
#
#     df.columns = df.columns.str.replace("Answer.f1.", "")
#     df.columns = df.columns.str.replace("Answer.t1.", "")
#     df.columns = df.columns.str.replace(".raw", "")
#     emotions_list = ["Answer", "afraid", "angry", "anxious", "ashamed", "awkward",
#                      "bored", "calm", "confused", "disgusted", "excited", "frustrated",
#                      "happy", "jealous", "nostalgic", "proud", "sad", "satisfied", "surprised"]
#
#     topics_list = ["Answer", "exercise", "family", "food", "friends", "god", "health", "love",
#                    "recreation", "school", "sleep", "work"]
#
#     df1 = df[emotions_list]
#     df2 = df[topics_list]
#
#     df.columns = df.columns.str.replace("Answer.f1.", "")
#     df.columns = df.columns.str.replace("Answer.t1.", "")
#     df.columns = df.columns.str.replace(".raw", "")
#     journal_entries = df["Answer"]
#
#     # Flair Initialization
#     classifier = TextClassifier.load("en-sentiment")
#
#     # Flair performs sentiment analysis
#     predicted_sentiments = []
#     predicted_scores = []
#
#     for entry in journal_entries:
#         sentence = Sentence(entry)
#         classifier.predict(sentence)
#         score = sentence.labels[0].score
#         sentiment = sentence.labels[0].value
#         predicted_scores.append(score)
#         predicted_sentiments.append(sentiment)
#
#     # Combine journal entries with mood and score
#     mood = pd.DataFrame(predicted_sentiments, columns=["Sentiment"])
#     prob = pd.DataFrame(predicted_scores, columns=["Probability"])
#     combined = pd.concat([journal_entries, mood, prob], axis=1)
#     print(combined.head(2))
#
#     # Balance combined by remove excess "POSITIVE" instances
#     cond = (combined["Sentiment"] == "POSITIVE")
#     positive_rows = combined[cond]
#     positive_sample = positive_rows.sample(n=900, random_state=42)
#     new_df = combined.drop(positive_sample.index)
#
#     # Generate a CSV file of the processed data
#     new_df.to_csv("Sentiment Analysis With Two Class Labels.csv", encoding="utf-8", index=False)
#
#
# if __name__ == "__main__":
#     pre_process_and_train()