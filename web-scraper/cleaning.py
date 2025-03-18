import re
import pandas as pd

KEYWORDS = ["data", "analytics"]  # ✅ Add more keywords if needed

def clean_description(text):
    """Removes emails, phone numbers, and excessive spaces from descriptions."""
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", "***", text)
    text = re.sub(r"\+?\d[\d -]{8,}\d", "******", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_title(title):
    """Removes unnecessary symbols and short words from job titles."""
    title = re.sub(r"\d+", "", title)  # Remove numbers
    title = re.sub(r"\s*\(.*?\)", "", title)  # Remove parentheses
    title = re.sub(r"\s*-\s.*", "", title)  # Remove hyphen and content after it
    title = title.replace('"', "").strip()
    return title

def clean_location(location):
    """Standardizes location names."""
    return location.split(",")[0].strip() if location else "Unknown"

def mark_matching_jobs(df):
    """Marks jobs that contain specific keywords in the description."""
    keyword_pattern = "|".join(KEYWORDS)  # Combine keywords into a regex pattern
    df["matches_keyword"] = df["description"].str.contains(keyword_pattern, case=False, na=False).map({True: "Yes", False: "No"})
    return df

def clean_data(df):
    """Cleans and processes the scraped data, then marks keyword matches."""
    df["description"] = df["description"].apply(clean_description)
    df["title"] = df["title"].apply(clean_title)
    df["location"] = df["location"].apply(clean_location)

    # ✅ Add keyword matching column
    df = mark_matching_jobs(df)

    # ✅ Reorder columns so "matches_keyword" appears before "description"
    column_order = ["y_tunnus", "company", "scrape_date", "title", "location", "matches_keyword", "description"]
    df = df[column_order]

    return df
