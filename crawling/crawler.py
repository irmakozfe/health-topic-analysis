import os
import sys
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, UTC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SOURCES = {
    "WHO": "https://www.who.int/news",
    "Spiegel Gesundheit": "https://www.spiegel.de/gesundheit/"
}


def fetch_who():
    #Selenium
    url = SOURCES["WHO"]

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/news/item/']"))
    )
    time.sleep(2)  

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    articles = []
    for a in soup.select("a[href*='/news/item/']"):
        title = a.get_text(strip=True)
        link = "https://www.who.int" + a["href"]
        if title:
            articles.append({"source": "WHO", "title": title, "link": link})

        return articles




def fetch_spiegel():
    url = SOURCES["Spiegel Gesundheit"]
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    articles = []
    for a in soup.select("article a[href*='/gesundheit/']"):
        title = a.get_text(strip=True)
        link = a["href"]
        if link.startswith("/"):
            link = "https://www.spiegel.de" + link
        if title:
            articles.append({"source": "Spiegel Gesundheit", "title": title, "link": link})
    return articles





def save_csv(df: pd.DataFrame, out_dir: str = "."):
    os.makedirs(out_dir, exist_ok=True)
    fn = f"crawling/healthnews_by_crawling{datetime.now(UTC).strftime('%Y%m%d')}.csv"
    out_path = os.path.join(out_dir, fn)
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    return out_path



def main():
    try:
        
        all_articles = []
        all_articles += fetch_who()
        all_articles += fetch_spiegel()
   

        df = pd.DataFrame(all_articles)
        if df.empty:
            print(" No articles found. Check selectors or site availability.")
            return

        out_path = save_csv(df)
        print(f"\n Total: {len(df)} articles saved to {out_path}")
        print(df.tail(10))

    except Exception as e:
        print("Error:", repr(e))
        sys.exit(1)


if __name__ == "__main__":
    print(f"Python {sys.version.split()[0]}")
    print(f"Working Directory: {os.getcwd()}")
    main()
