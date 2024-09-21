import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import joblib


def logistic_regression_model():
    # Load the preprocessed CSV file
    df_new = pd.read_csv("Sentiment Analysis With Two Class Labels.csv")

    # Prepare the features x and labels y
    x = df_new["Answer"]
    y = df_new["Sentiment"]

    # Pipeline contains TF-IDF() and Logistic Regression()
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("lr", LogisticRegression())
    ])

    # Cross-validation evaluates the model, using 10 folds
    accuracy = cross_val_score(pipe, x, y, cv=10).mean()
    print("Logistic Regression Accuracy:", accuracy)

    # Fit the pipeline on the entire dataset
    pipe.fit(x, y)

    # Save the pipeline
    joblib.dump(pipe, "sentiment_analysis_pipeline.joblib")


if __name__ == "__main__":
    logistic_regression_model()
