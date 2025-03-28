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
- Job posting volume, keywords

## Prospect validation
- Turnover more than 500k€
- Staff number over 10 people
- Country: FI
- Cities: "helsinki", "tampere", "vantaa", "espoo", "oulu", "turku", "lahti", "jyväskylä"

## Team members and responsibilities
- Samu Syväoja (code, Fabric, Power BI)
- Linda Ulma (code, Azure, Fabric, Power BI)
- Tomi Jolkkonen (code, Power BI)


- Onni Niemelä (client, Skillio)

## What's included in the project and how it's set up

### 1. Scrapers
- Duunitori.fi scraper for scraping job postings in data engineering (code can be found in GitHub)
- Ampparit.com scraper for scraping news in IT and looking for certaing keywords (code can be found in GitHub)
- Scrapers need to be run manually and locally

### 2. GitHub
- Repository including code for scrapers
- Technical documentation (README)

### 2. Azure
- Storage account / Data Lake: leadgeneratorstorage
- Vainu api key and storage account connection string are stored in Key Vault

### 3. Fabric
- Lakehouse: lead_generator_lakehouse for bronze, silver and gold data (news weren't used in gold data after all)
- Warehouse: lead_generator_warehouse original plan was to use warehouse for gold data, but the idea had to be ditched since there were problems with creating relationships between tables
- Notebooks for transforming and cleaning data: clean_job_postings, clean_news, vainu_api_bronze_to_lakehouse, vainu_bronze_to_silver
- Master pipeline to run all notebooks and create gold data

### 4. PowerBI
- App for sales team to look for leads

### 5. Jira
- Kanban board including all tasks related to the project
- Also some documentation included

### Overview of master pipeline
![image](https://github.com/user-attachments/assets/369ce3c4-125e-4be5-8ab4-3c865f5886bb)
1. Notebooks for fetching data and transforming data are ran simultaneously
2. Dataflows for creating gold tables of the data and loading the gold tables back to the lakehouse (if warehouse wants to be used, only destination for tables needs to be modified)
3. Two stored procedures for moving data from one schema to another in the warehouse and for creating relationships. These are currently not activated, since warehouse didn't work, but they can be used, if warehouse starts working later

### Architecture
![lead-generator architecture](https://github.com/user-attachments/assets/eae8349c-52b9-4dde-8fe2-8290c656cc13)

### Color palette for Power BI
Color palette for Power BI report can be found [here](https://coolors.co/1a2239-262d49-ef376d-fac10e-38d989-39c2f0)

## Final result
A Power BI app for ranking leads
