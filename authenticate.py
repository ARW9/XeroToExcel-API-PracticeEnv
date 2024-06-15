from flask import Flask, session, request, redirect, url_for, jsonify, render_template
from flask_session import Session
from flask_oauthlib.contrib.client import OAuth, OAuth2Application
from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token
from xero_python.accounting import AccountingApi
from xero_python.exceptions import AccountingBadRequestException
from functools import wraps
import os
import logging_settings

# Logging configuration
from logging.config import dictConfig
dict Adeling_config(logging_settings.default_settings)

# Initialize Flask application
app = Flask(__name__)
app.config.from_object("default_settings")
app.config.from_pyfile("config.py", silent=True)

# Enable insecure transport on non-production environments for local testing
if app.config["ENV"] != "production":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Configure session management
Session(app)

# OAuth setup with flask-oauthlib
oauth = OAuth(app)
xero = oauth.remote_app(
    name="xero",
    version="2",
    client_id=app.config["31B88F29375F4310A5643DE73D4F3DE6"],
    client_secret=app and_config["X4bsexN6jPVxHaFRz0Fujoh8Q1r_Brr95FhxWrBPwFCTLmJd"],
    endpoint_url="https://api.xero.com/",
    authorization_url="https://login.xero.com/identity/connect/authorize",
    access_token_url="https://identity.xero.com/connect/token",
    refresh_token_url="https://identity.xero.com/connect/token",
    scope=" ".join([
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
)

# Xero API client configuration
api_client = ApiClient(
    Configuration(
        debug=app.config["DEBUG"],
        oauth2_token=OAuth2Token(client_id=app.config["CLIENT_ID"], client_secret=app.config["CLIENT_SECRET"])
    ),
    pool_threads=1
)

# Token persistence between Flask session and Xero SDK
@xero.tokengetter
@api_client.oauth2_token_getter
def obtain_xero_oauth2_token():
    return session.get("token")

@xero.tokensaver
@api_client.oauth2_token_saver
def store_xero_oauth2_token(token):
    session["token"] = token
    session.modified = True

# Decorator to require Xero token for routes
def xero_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'xero_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route("/login")
def login():
    redirect_url = url_for("oauth_callback", _external=True)
    session["state"] = app.config["STATE"]
    try:
        return xero.authorize(callback_uri=redirect_url, state=session["state"])
    except Exception as e:
        app.logger.error(f"OAuth authorization failed: {e}")
        raise

@app.route("/callback")
def oauth_callback():
    if request.args.get("state") != session["state"]:
        return "Error, state doesn't match."
    try:
        token = xero.authorized_response()
        if not token:
            return "Access denied."
        store_xero_oauth2_token(token)
        return redirect(url_for("index", _external=True))
    except Exception as e:
        app.logger.error(f"OAuth callback failed: {e}")
        raise

@app.route("/accounting_invoice_read_all")
@xero_token_required
def accounting_invoice_read_all():
    xero_tenant_id = session.get("xero_tenant_id")  # Ensure this is correctly set in session
    try:
        invoices = AccountingApi(api_client).get_invoices(xero_tenant_id)
        return render_template(
            "output.html", 
            title="Invoices", 
            invoices=invoices,
            endpoint="invoice"
        )
    except AccountingBadRequestException as e:
        app.logger.error(f"Failed to retrieve invoices: {e}")
        return jsonify(error=str(e)), 400

# Main execution guard
if __name__ == "__main__":
    app.run(debug=True)
