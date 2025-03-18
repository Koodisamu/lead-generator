import os
import asyncio
import pandas as pd
from datetime import datetime
from duunitori import scrape_duunitori
from cleaning import clean_data

OUTPUT_FOLDER = "sinkfile"

async def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print("Starting job scraping...")
    raw_data = await scrape_duunitori()  # Run the async scraper
    cleaned_data = clean_data(raw_data)  # Clean the data

    # 🇫🇮 Generate Finnish-style timestamp filename (DD-MM-YYYY_HH-MM-SS)
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    output_file = f"listing_{timestamp}.csv"

    output_path = os.path.join(OUTPUT_FOLDER, output_file)
    cleaned_data.to_csv(output_path, index=False)
    
    print(f"Scraped and cleaned job listings saved to {output_path}")

'''
IF AZURE SDK IS USED:
pip install azure-storage-blob

CODE:
from azure.storage.blob import BlobServiceClient
import asyncio
import pandas as pd
from datetime import datetime
from duunitori import scrape_duunitori
from cleaning import clean_data

# 🔹 Azure Storage Configuration
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=YOUR_ACCOUNT_NAME;AccountKey=YOUR_ACCOUNT_KEY;EndpointSuffix=core.windows.net"
AZURE_CONTAINER_NAME = "your-container-name"

async def main():
    print("Starting job scraping...")
    raw_data = await scrape_duunitori()  # Run the async scraper
    cleaned_data = clean_data(raw_data)  # Clean the data

    # 🇫🇮 Generate Finnish-style timestamp filename (DD-MM-YYYY_HH-MM-SS)
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    output_filename = f"listing_{timestamp}.csv"
    
    # 🔹 Convert DataFrame to CSV
    csv_data = cleaned_data.to_csv(index=False, encoding="utf-8")

    # 🔹 Upload to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=output_filename)

    blob_client.upload_blob(csv_data, overwrite=True)

    print(f"✅ File uploaded to Azure Blob Storage: {output_filename}")

if __name__ == "__main__":
    asyncio.run(main())


IF AZURE DATA LAKE IS USED: pip install azure-storage-file-datalake, and modify the upload part in main.py:
use DataLakeServiceClient
'''

if __name__ == "__main__":
    asyncio.run(main())  # Run the async event loop
