import os

# Basic Flask Configuration
DEBUG = True  # Set to False in production
SECRET_KEY = 'mysecretkey'

# OAuth Configuration
CLIENT_ID = '31B88F29375F4310A5643DE73D4F3DE6'  # Replace with your actual client ID
CLIENT_SECRET = 'X4bsexN6jPVxHaFRz0Fujoh8Q1r_Brr95FhxWrBPwFCTLmJd'  # Replace with your actual client secret

# Session Configuration
SESSION_TYPE = 'filesystem'  # Store session data in the file system
SESSION_PERMANENT = False  # Do not make sessions permanent
SESSION_USE_SIGNER = True  # Use a signer for session data to prevent tampering
SESSION_KEY_PREFIX = 'session:'  # Prefix for session keys
SESSION_FILE_DIR = '/path/to/session/files'  # Directory where session files are stored

# OAuth2 Provider URLs
OAUTH2_AUTHORIZATION_URL = 'https://login.xero.com/identity/connect/authorize'
OAUTH2_TOKEN_URL = 'https://identity.xero.com/connect/token'
OAUTH2_REDIRECT_URI = 'http://localhost:3000/callback'  # Replace with your actual redirect URI

# Logging Configuration
LOGGING_LEVEL = 'DEBUG'  # Change to 'INFO' or 'WARNING' in production
LOGGING_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'

# Xero API Configuration
XERO_API_BASE_URL = 'https://api.xero.com'
XERO_TENANT_ID = 'your_tenant_id_here'  # Replace with your actual tenant ID if static

# OAuth Scope
OAUTH2_SCOPE = ' '.join([
    "offline_access", "openid", "profile", "email",
    "accounting.transactions", "accounting.transactions.read",
    "accounting.reports.read", "accounting.journals.read",
    "accounting.settings", "accounting.settings.read",
    "accounting.contacts", "accounting.contacts.read",
    "accounting.attachments", "accounting.attachments.read",
    "assets", "projects", "files",
    "payroll.employees", "payroll.payruns", "payroll.payslip",
    "payroll.timesheets", "payroll.settings"
])

# Ensure the directory exists or replace with an appropriate one
if not os.path.exists(SESSION_FILE_DIR):
    os.makedirs(SESSION_FILE_DIR)
