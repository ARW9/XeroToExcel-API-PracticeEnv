# xero_client.py
from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Configuration, OAuth2Token
from xero_python.api_client.api import accounting_api
import requests

# Replace with your credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'YOUR_REDIRECT_URI'

# OAuth2 Configuration
configuration = OAuth2Configuration(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
)

api_client = ApiClient(configuration)

def authenticate():
    # Implement the OAuth 2.0 flow to get an access token
    # For simplicity, this example assumes you've already obtained a valid access token.
    token = OAuth2Token(
        access_token='YOUR_ACCESS_TOKEN',
        refresh_token='YOUR_REFRESH_TOKEN',
    )
    api_client.configuration.oauth2_token = token

def get_balance_sheet(organization_id):
    accounting_api_instance = accounting_api.AccountingApi(api_client)
    return accounting_api_instance.get_report_balance_sheet(organization_id)

def get_profit_loss(organization_id):
    accounting_api_instance = accounting_api.AccountingApi(api_client)
    return accounting_api_instance.get_report_profit_and_loss(organization_id)
