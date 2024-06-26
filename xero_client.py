from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Configuration, OAuth2Token
from xero_python.api_client.api import accounting_api
from xero_python.identity import IdentityApi
import requests
import webbrowser
import json
import os

# Replace with your credentials
client_id = '31B88F29375F4310A5643DE73D4F3DE6'
client_secret = 'X4bsexN6jPVxHaFRz0Fujoh8Q1r_Brr95FhxWrBPwFCTLmJd'
redirect_uri = 'http://localhost:3000/callback'

# OAuth2 Configuration
configuration = OAuth2Configuration(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scopes=["accounting.reports.read"],
)

api_client = ApiClient(configuration)

def save_tokens(token_dict):
    with open("tokens.json", "w") as f:
        json.dump(token_dict, f)

def load_tokens():
    if os.path.exists("tokens.json"):
        with open("tokens.json", "r") as f:
            return json.load(f)
    return None

def authenticate():
    token = load_tokens()
    if not token:
        # Step 1: Get the authorization URL
        auth_url = api_client.oauth2_config.get_authorize_url()
        print(f"Open the following URL in a browser to authorize the application:\n{auth_url}")

        # Step 2: Get the authorization code from the callback
        authorization_code = input("Enter the authorization code from the callback URL: ")

        # Step 3: Exchange the authorization code for an access token
        token = api_client.oauth2_config.get_access_token(authorization_code)
        save_tokens(token)
    else:
        token = OAuth2Token(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            expires_at=token['expires_at'],
        )

    api_client.configuration.oauth2_token = token

def get_balance_sheet(organization_id):
    accounting_api_instance = accounting_api.AccountingApi(api_client)
    return accounting_api_instance.get_report_balance_sheet(organization_id)

def get_profit_loss(organization_id):
    accounting_api_instance = accounting_api.AccountingApi(api_client)
    return accounting_api_instance.get_report_profit_and_loss(organization_id)
