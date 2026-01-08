import pandas as pd
from langdetect import detect

def preprocess_text(text):
    if pd.isna(text):
        return ""
    return text.lower().strip()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

df = pd.read_csv("health_news_train_data.csv")

df["clean_text"] = (
    df["title"].fillna("") + " " + df["summary"].fillna("")
).apply(preprocess_text)

df["language"] = df["clean_text"].apply(detect_language)

df.to_csv("processed_health_news_train.csv", index=False)
print("Preprocessing completed.")
