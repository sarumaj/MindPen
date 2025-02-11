import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import joblib
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer


def load_data():
    df = pd.read_csv("Sentiment Analysis Dataset.csv")

    # separate sentiment and sentiment_score
    df[["Sentiment", "Sentiment_Score"]] = df["Sentiment"].str.split(",\n", expand=True)

    # extract sentiment value without extra characters
    df["Sentiment"] = df["Sentiment"].map(
        lambda x: x.split(":")[1].strip().replace('"', "").replace("}", "").strip()
    )

    df = df.drop(columns=["Sentiment_Score"])

    # balance journal entries
    positive = df[df["Sentiment"] == "positive"]
    neutral = df[df["Sentiment"] == "neutral"]
    negative = df[df["Sentiment"] == "negative"]

    positive_balanced = positive.sample(n=180, random_state=42)
    negative_balanced = negative.sample(n=180, random_state=42)

    balanced_df = pd.concat([positive_balanced, neutral, negative_balanced])
    balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
    return balanced_df


def svm_model():
    balanced_df = load_data()
    # prepare the features x and labels y
    x = balanced_df["Journals"]
    y = balanced_df["Sentiment"]

    svm_linear = SVC(kernel="linear", random_state=42)

    # pipeline contains TF-IDF() and support vectors()
    pipe = Pipeline([("tfidf", TfidfVectorizer()), ("SVM", svm_linear)])

    # evaluate the model, using 10 folds
    accuracy = cross_val_score(pipe, x, y, cv=10).mean()
    print("SVM (Linear Average Accuracy: ", accuracy)

    # Fit the pipeline on the entire dataset
    pipe.fit(x, y)

    # Save the pipeline
    joblib.dump(pipe, "svm_pipeline.joblib")


if __name__ == "__main__":
    svm_model()
