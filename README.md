# Sales lead generation tool

## Business requirements

Conversion rate for sales leads has decreased, which creates a need for higher quantity of leads.

A Power BI Tool is needed to be used by the sales team of Skillio. The tool should be able to:
- List, filter and rank sales leads from multiple sources

## MVP Requirements

Power BI/analytics:
- List and filter sales leads for Skillio

Data pipeline:
- Automated pipeline
- Fabric workspace containing the data in Lakehouse/Warehouse
- Defined lead quality requirements


Data sources:
- Vainu
- Duunitori
- Use multiple sources


Documentation:
- README file
- Final presentation

## Sources

Vainu:
- Main source for company data


Job posting sites (Duunitori):
- Use existing web scraping tools
- Job posting volume, keywords

## Prospect validation
- Turnover more than 500k€
- Staff number over 10 people
- Country: FI
- Cities: "helsinki", "tampere", "vantaa", "espoo", "oulu", "turku", "lahti", "jyväskylä"

## What's included in the project and how its set up

1. Scrapers:
- Duunitori.fi scraper for scraping job postings in data engineering (code can be found in GitHub)
- Ampparit.com scraper for scraping news in IT and looking for certaing keywords (code can be found in GitHub)
- Scrapers need to be run manually and locally

2. GitHub
- Repository including code for scrapers
- Technical documentation (README)

2. Azure:
- Storage account / Data Lake: leadgeneratorstorage
- Vainu api key and storage account connection string are stored in Key Vault

3. Fabric:
- Lakehouse: lead_generator_lakehouse for bronze and silver data
- Warehouse: lead_generator_warehouse for gold data
- Notebooks for transforming and cleaning data: clean_job_postings, clean_news, vainu_api_bronze_to_lakehouse, vainu_bronze_to_silver

4. PowerBI:
- App for sales team to look for leads

5. Jira:
- Kanban board including all tasks related to the project
- Also some documentation included

