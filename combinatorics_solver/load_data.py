import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import joblib

def train_and_save_model():
    _DIR = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(_DIR, "dataset.csv"))
    X = df["question"]
    y = df["operation"]
    model = make_pipeline(TfidfVectorizer(stop_words='english', ngram_range=(1, 2)), SVC(kernel='linear', probability=True))
    model.fit(X, y)
    model_path = os.path.join(_DIR, "combinatorics_model.joblib")
    joblib.dump(model, model_path)
    print("[OK] Model trained and saved to combinatorics_model.joblib!")
    return model

if __name__ == "__main__":
    trained_model = train_and_save_model()
    test_question = ["How many ways to arrange 3 books from 5?"]
    prediction = trained_model.predict(test_question)
    print(f"The ML predicts you need to use: {prediction[0]}")