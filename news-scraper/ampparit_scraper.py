import os
import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# ✅ Define keywords and search URLs
KEYWORDS = ["data", "koneoppiminen", "tekoäly", "azure", "analytiikka", "power bi"]
SEARCH_URLS = [f"https://www.ampparit.com/haku?q={keyword}" for keyword in KEYWORDS]
HEADERS = {"User-Agent": "Mozilla/5.0"}
OUTPUT_FOLDER = "sinkfile"  # Change to "" if you want files saved in the same folder

async def fetch(session, url):
    """Fetches a webpage asynchronously."""
    async with session.get(url, headers=HEADERS) as response:
        return await response.text()

async def scrape_ampparit():
    """Scrapes Ampparit.com for news related to multiple keywords."""
    async with aiohttp.ClientSession() as session:
        news_list = []

        for url in SEARCH_URLS:
            html = await fetch(session, url)
            soup = BeautifulSoup(html, "html.parser")

            # 🔹 Find all news items
            articles = soup.select("div.item-text")

            for article in articles:
                # ✅ Extract headline
                headline_tag = article.find("a", class_="news-item-headline")
                headline = headline_tag.get_text(strip=True) if headline_tag else None

                # ✅ Extract company (news source)
                source_tag = article.find("span", class_="item-details__detail_source")
                company = source_tag.get_text(strip=True) if source_tag else None

                # ✅ Filter: Only save headlines that contain any of the keywords
                if headline and company and any(keyword in headline.lower() for keyword in KEYWORDS):
                    news_list.append({"company": company, "headline": headline})

        return pd.DataFrame(news_list, columns=["company", "headline"])

async def main():
    print("Starting news scraping...")
    news_data = await scrape_ampparit()

    if news_data.empty:
        print("❌ No matching news found.")
        return

    # ✅ Ensure the sinkfile folder exists before saving
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # 🇫🇮 Generate Finnish-style timestamp filename
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    output_file = os.path.join(OUTPUT_FOLDER, f"ampparit_news_{timestamp}.csv")

    news_data.to_csv(output_file, index=False, encoding="utf-8")
    print(f"✅ Scraped news saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
