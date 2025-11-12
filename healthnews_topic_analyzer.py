
import os
import sys
from datetime import datetime, timezone
UTC = timezone.utc
import feedparser
import pandas as pd


SOURCES = {
    "WHO": "https://www.who.int/rss-feeds/news-english.xml",
    "Spiegel Gesundheit": "https://www.spiegel.de/gesundheit/index.rss",
    "Tagesschau Gesundheit": "https://www.tagesschau.de/xml/rss2?rubrik=gesundheit",
    "Deutsches Ärzteblatt": "https://www.aerzteblatt.de/rss/news.asp",
}


TOPIC_KEYWORDS = {
    "Covid": ["covid", "coronavirus"],
    "Vaccination": ["vaccine", "vaccination", "immunization", "Impfung", "Impfstoff", "impfen"],
    "Pandemic": ["pandemic", "epidemic", "Ausbruch", "Pandemie", "Epidemie"],
    "Measles" : ["measles"],
    "Influenza": ["influenza", "coughing", "Erkältung", "schnupfen", "nasenschwellung", "fieber", "nasal congestion", "fever"],
    "Depression": ["depression", "depressed", "anxiety", "angst", "depressiv", "psychisch"],
    "Addiction": ["addiction", "alcohol", "smoking", "drugs", "Sucht", "Rauchen", "Alkohol", "Drogen"],
    "Nutrition and lifestyle": ["nutrition", "diet", "obesity", "exercise", "Yoga", "Meditation"],
    "Policy and system": ["healthcare", "hospital", "reform", "insurance", "Krankenhaus", "Krankenversicherung"],
}


def fetch_sources():
    rows = []
    for name, url in SOURCES.items():
        print(f"Fetching: {name} -> {url}")
        feed = feedparser.parse(url)
        print(f"→ {name}: {len(feed.entries)} entries")

        for e in feed.entries:
            rows.append({
                "source": name,
                "title": e.get("title", ""),
                "summary": e.get("summary", ""),
                "link": e.get("link", ""),
                "published": e.get("published", e.get("updated", "")),
            })

    return pd.DataFrame(rows)


def detect_topic(text):
    text = str(text).lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(word in text for word in keywords):
            return topic
    return "Other"

def save_csv(df: pd.DataFrame, out_dir: str = "."):
    os.makedirs(out_dir, exist_ok=True)
    fn = f"csv/categorized_healthnews_{datetime.now(UTC).strftime('%d%m%Y')}.csv"
    out_path = os.path.join(out_dir, fn)

 
    columns_to_save = ["source", "published", "topic", "title", "summary", "link"]

    df.to_csv(
        out_path,
        index=False,
        encoding="utf-8-sig",   
        lineterminator="\n",    
        sep=",",
        columns=columns_to_save
    )

    return out_path

def main():
    try:
        df = fetch_sources()

        if df.empty:
            print("No entries fetched. Check RSS URLs or internet connectivity.")
            return

        df["published"] = pd.to_datetime(df["published"], errors="coerce", utc=True)
        df["text"] = df["title"].fillna("") + " " + df["summary"].fillna("")
        df["topic"] = df["text"].apply(detect_topic)

        df["date"] = df["published"].dt.date
        grouped = (
            df.groupby(["source", "date", "topic"])
              .size()
              .reset_index(name="count")
        )

        
        save_csv(df, ".")  
        grouped.to_csv("csv/healthnews_summary.csv", index=False, encoding="utf-8-sig")

        print("\Grouped summary (source + date + topic):")
        print(grouped.tail(10))

        print("\Analysis complete. Files saved:")
        print(" - categorized_healthnews_YYYYMMDD.csv (detailed records)")
        print(" - healthnews_summary.csv (aggregated summary)")

    except Exception as e:
        print(" Error:", repr(e))
        sys.exit(1)


if __name__ == "__main__":
    print(f"Python: {sys.version.split()[0]}")
    print(f"Current Directory: {os.getcwd()}")
    main()
