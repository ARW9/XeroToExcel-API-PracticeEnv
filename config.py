import os

# Basic Flask Configuration
DEBUG = True
SECRET_KEY = 'mysecretkey'

# OAuth Configuration
CLIENT_ID = '31B88F29375F4310A5643DE73D4F3DE6'  # Replace with your actual client ID
CLIENT_SECRET = 'X4bsexN6jPVxHaFRz0Fujoh8Q1r_Brr95FhxWrBPwFCTLmJd'  # Replace with your actual client secret

# Session Configuration
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False
SESSION_USE_SIGNER = True
SESSION_KEY_PREFIX = 'session:'
SESSION_FILE_DIR = os.path.expanduser('~/.my_flask_sessions')

# Ensure the session file directory exists
if not os.path.exists(SESSION_FILE_DIR):
    os.makedirs(SESSION_FILE_DIR, exist_ok=True)

# OAuth2 Provider URLs
OAUTH2_AUTHORIZATION_URL = 'https://login.xero.com/identity/connect/authorize'
OAUTH2_TOKEN_URL = 'https://identity.xero.com/connect/token'
OAUTH2_REDIRECT_URI = 'http://localhost:3000/callback'

# Logging Configuration
LOGGING_LEVEL = 'DEBUG'
LOGGING_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'

# Xero API Configuration
XERO_API_BASE_URL = 'https://api.xero.com'
XERO_TENANT_ID = 'your_tenant_id_here'

# OAuth Scope
OAUTH2_SCOPE = 'offline_access openid profile email accounting.transactions.read accounting.reports.read'
