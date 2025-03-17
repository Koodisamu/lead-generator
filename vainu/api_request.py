import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from config import KEY_VAULT_URL, SECRET_NAME

# Vainu API Endpoint
API_URL = "https://api.vainu.io/api/v2/companies/"


# Authenticate using DefaultAzureCredential (Managed Identity, CLI, or Env Variables)
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

# Fetch the API key
secret = client.get_secret(SECRET_NAME)
API_KEY = secret.value
#print(API_KEY)
# Headers for authentication
headers = {
    "API-Key": f"{API_KEY}",
    "Content-Type": "application/json"
}

# Define API query parameters
params = {
    "country": "FI",  # Filter by Finland
    "industry": "Software",  # Example industry filter
    "employee_count_min": 50,  # Get companies with at least 50 employees
    "financials": True,  # Request financial data if available
    "limit": 10  # Number of companies to fetch
}

# Make API request
response = requests.get(API_URL, headers=headers, params=params)

# Check response status
if response.status_code == 200:
    data = response.json()
    for company in data.get("results", []):
        print(f"Company Name: {company.get('company_name')}")
        print(f"Business ID: {company.get('business_id')}")
        print(f"Industry: {company.get('industry_codes')}")
        print(f"Turn over: {company.get('turn_over', 'N/A')} €")
        print(f"Profit: {company.get('profit', 'N/A')} %")
        print("-" * 40)
else:
    print("Error:", response.status_code, response.text)
