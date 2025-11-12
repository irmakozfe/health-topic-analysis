import pandas as pd

df = pd.read_csv("healthnews_20251030.csv")

df["published"] = pd.to_datetime(df["published"], errors="coerce")

TOPIC_KEYWORDS = {
    "Infectious disease": ["covid", "influenza", "measles", "outbreak", "vaccination"],
    "Mental health": ["mental", "addiction", "anxiety", "depression", "stress", "well-being"],
    "Nutrition and lifestyle": ["nutrition", "diet", "obesity", "exercise"],
    "Policy and system": ["healthcare", "hospital", "reform", "insurance"],
}

def detect_topic(text):
    text = str(text).lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(word in text for word in keywords):
            return topic
    return "Other"

df["topic"] = df["text"].apply(detect_topic)

topic_counts = df["topic"].value_counts()
print(topic_counts)

source_counts = df.groupby("source")["topic"].value_counts()
print(source_counts)

df["date"] = df["published"].dt.date
trend = df.groupby(["date", "topic"]).size().unstack(fill_value=0)
print(trend.tail())

df.to_csv("categorized_healthnews.csv", index=False, encoding="utf-8")
topic_counts.to_csv("topic_summary.csv")
trend.to_csv("topic_trend.csv")
