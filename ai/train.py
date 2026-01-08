import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv("processed_health_news_train.csv")

df = df.dropna(subset=["clean_text", "topic"])


X = df["clean_text"]
y = df["topic"]

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_vec = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_vec, y)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("topic_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("AI model trained and saved.")
