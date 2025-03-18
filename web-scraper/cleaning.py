import re
import pandas as pd

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

def clean_data(df):
    """Cleans and processes the scraped data."""
    df["description"] = df["description"].apply(clean_description)
    df["title"] = df["title"].apply(clean_title)
    df["location"] = df["location"].apply(clean_location)
    return df
