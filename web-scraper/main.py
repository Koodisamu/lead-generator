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
    cleaned_data = clean_data(raw_data)  # Clean the data and add keyword column

    if cleaned_data.empty:
        print("❌ No jobs found. Exiting...")
        return

    # 🇫🇮 Generate Finnish-style timestamp filename (DD-MM-YYYY_HH-MM-SS)
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    output_file = f"listing_{timestamp}.csv"

    output_path = os.path.join(OUTPUT_FOLDER, output_file)
    cleaned_data.to_csv(output_path, index=False)
    
    print(f"✅ Scraped and cleaned job listings saved to {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
