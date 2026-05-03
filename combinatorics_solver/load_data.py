import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import joblib

# Resolve paths relative to this file so it works from any directory
_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Load your dataset 📄
df = pd.read_csv(os.path.join(_DIR, "dataset.csv"))

# 2. Separate the text and the labels ✂️
X = df["question"]
y = df["operation"]

# 3. Build and train the ML Pipeline 🧠
# SVC is much more accurate for small unbalanced datasets without getting biased by class frequencies
model = make_pipeline(TfidfVectorizer(stop_words='english', ngram_range=(1, 2)), SVC(kernel='linear', probability=True))
model.fit(X, y)

# 4. Save the trained model so we don't have to retrain it every time! 💾
joblib.dump(model, os.path.join(_DIR, "combinatorics_model.joblib"))
print("Model saved as combinatorics_model.joblib!")

# 5. Test it on a new math problem! 🎯
test_question = ["How many ways to arrange 3 books from 5?"]
prediction = model.predict(test_question)
print(f"The ML predicts you need to use: {prediction[0]}")