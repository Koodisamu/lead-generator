import re
import pandas as pd

def load_keywords(file_path):
    # Load keywords from a text file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            keywords = [line.strip() for line in file if line.strip()]
        return keywords
    except Exception as e:
        print(f"Error loading keywords: {e}")
        return []

def clean_description(text):
    # Remove emails, phone numbers and excessive spaces from descriptions
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", "***", text)
    text = re.sub(r"\+?\d[\d -]{8,}\d", "******", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_title(title):
    # Remove unnecessary symbols and short words from job titles
    title = re.sub(r"\d+", "", title)  # Remove numbers
    title = re.sub(r"\s*\(.*?\)", "", title)  # Remove parentheses
    title = re.sub(r"\s*-\s.*", "", title)  # Remove hyphen and content after it
    title = title.replace('"', "").strip()
    return title

def clean_location(location):
    # Standardize location names
    return location.split(",")[0].strip() if location else "Unknown"

def mark_matching_jobs(df, keywords):
    # Create separate columns for each keyword, initializing with 0 and marking 1 if found
    for keyword in keywords:
        # Treating keywords with spaces as phrases and escaping any special regex characters
        escaped_keyword = re.escape(keyword)  # Escape regex special characters
        df[keyword] = 0  # Initialize column with 0
        df.loc[df["description"].str.contains(escaped_keyword, case=False, na=False), keyword] = 1
    return df

def clean_data(df):
    # Cleans and processes the scraped data, then marks keyword matches
    KEYWORDS_FILE = "web-scraper/job-keywords.txt"
    KEYWORDS = load_keywords(KEYWORDS_FILE)
    
    df["description"] = df["description"].apply(clean_description)
    df["title"] = df["title"].apply(clean_title)
    df["location"] = df["location"].apply(clean_location)
    
    # Remove hyphen from Y-tunnus
    df["y_tunnus"] = df["y_tunnus"].str.replace("-", "", regex=True)
    
    # Add keyword columns
    df = mark_matching_jobs(df, KEYWORDS)
    
    # Exclude rows that do not have any keyword match
    df = df[df[KEYWORDS].sum(axis=1) > 0]
    
    # Reorder columns
    column_order = ["y_tunnus", "company", "scrape_date", "title", "location", "description"] + KEYWORDS
    df = df[column_order]
    
    return df