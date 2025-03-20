import os
import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient
from config import KEY_VAULT_URL, SECRET_NAME

# ✅ Define keywords and search URLs
KEYWORDS = ["data", "koneoppiminen", "tekoäly", "azure", "analytiikka", "power bi"]
SEARCH_URLS = [f"https://www.ampparit.com/haku?q={keyword}" for keyword in KEYWORDS]
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Azure Storage details
CONTAINER_NAME = "news-data"
BLOB_FOLDER = "news_listings"

# Fetch the connection string from Azure Key Vault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
connection_string = client.get_secret(SECRET_NAME).value

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

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

                # ✅ Extract media (news source)
                source_tag = article.find("span", class_="item-details__detail_source")
                media = source_tag.get_text(strip=True) if source_tag else None

                # ✅ Filter: Only save headlines that contain any of the keywords
                if headline and media and any(keyword in headline.lower() for keyword in KEYWORDS):
                    news_list.append({"media": media, "headline": headline})

        return pd.DataFrame(news_list, columns=["media", "headline"])

async def save_to_blob(news_data):
    """Saves news data to Azure Blob Storage."""
    if news_data.empty:
        print("❌ No matching news found.")
        return

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    output_file = f"ampparit_news_{timestamp}.csv"
    blob_path = f"{BLOB_FOLDER}/{output_file}"

    # Convert DataFrame to CSV format
    csv_data = news_data.to_csv(index=False, encoding="utf-8")

    # Upload CSV to Blob Storage
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_path)
    
    try:
        blob_client.upload_blob(csv_data, overwrite=True)
        print(f"✅ Scraped news saved to Azure Blob Storage: {blob_path}")
    except Exception as e:
        print(f"Error uploading to Azure Blob Storage: {e}")

async def main():
    print("Starting news scraping...")
    news_data = await scrape_ampparit()
    await save_to_blob(news_data)

if __name__ == "__main__":
    asyncio.run(main())