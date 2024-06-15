from flask import Flask, session, request, redirect, url_for, jsonify, render_template
from functools import wraps
import os
from functools import wraps
from io import BytesIO
from logging.config import dictConfig
from flask import Flask, session
from flask_oauthlib.contrib.client import OAuth, OAuth2Application
from flask_session import Session
from xero_python.accounting import AccountingApi
from xero_python.assets import AssetApi
from xero_python.project import ProjectApi
from xero_python.payrollau import PayrollAuApi
from xero_python.payrolluk import PayrollUkApi
from xero_python.payrollnz import PayrollNzApi
from xero_python.file import FilesApi
from xero_python.api_client import ApiClient, serialize
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token
from xero_python.exceptions import AccountingBadRequestException, PayrollUkBadRequestException
from xero_python.identity import IdentityApi
from xero_python.utils import getvalue
import logging_settings
from utils import jsonify, serialize_model

dictConfig(logging_settings.default_settings)

# configure main flask application
app = Flask(__name__)
app.config.from_object("default_settings")
app.config.from_pyfile("config.py", silent=True)

if app.config["ENV"] != "production":
    # allow oauth2 loop to run over http (used for local testing only)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# configure persistent session cache
Session(app)

# configure flask-oauthlib application
oauth = OAuth(app)
xero = oauth.remote_app(
    name="xero",
    version="2",
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    endpoint_url="https://api.xero.com/",
    authorization_url="https://login.xero.com/identity/connect/authorize",
    access_token_url="https://identity.xero.com/connect/token",
    refresh_token_url="https://identity.xero.com/connect/token",
    scope="offline_access openid profile email accounting.transactions "
    "accounting.transactions.read accounting.reports.read "
    "accounting.journals.read accounting.settings accounting.settings.read "
    "accounting.contacts accounting.contacts.read accounting.attachments "
    "accounting.attachments.read assets projects "
    "files "
    "payroll.employees payroll.payruns payroll.payslip payroll.timesheets payroll.settings",
)  # type: OAuth2Application


# configure xero-python sdk client
api_client = ApiClient(
    Configuration(
        debug=app.config["DEBUG"],
        oauth2_token=OAuth2Token(
            client_id=app.config["CLIENT_ID"], client_secret=app.config["CLIENT_SECRET"]
        ),
    ),
    pool_threads=1,
)

# configure token persistence and exchange point between flask-oauthlib and xero-python
@xero.tokengetter
@api_client.oauth2_token_getter
def obtain_xero_oauth2_token():
    return session.get("token")

@xero.tokensaver
@api_client.oauth2_token_saver
def store_xero_oauth2_token(token):
    session["token"] = token
    session.modified = True

app = Flask(__name__)

# Assuming xero is a properly configured instance of some Xero SDK
# Make sure to configure xero somewhere in this script or import it if it's defined elsewhere

def xero_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'xero_token' not in session:
            # Redirect to login if the token is not in session
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login")
def login():
    redirect_url = url_for("oauth_callback", _external=True)
    session["state"] = app.config["STATE"]
    try:
        response = xero.authorize(callback_uri=redirect_url, state=session["state"])
    except Exception as e:
        print(e)
        raise
    return response

@app.route("/callback")
def oauth_callback():
    if request.args.get("state") != session["state"]:
        return "Error, state doesn't match, no token for you."
    try:
        response = xero.authorized_response()
    except Exception as e:
        print(e)
        raise
    if response is None or response.get("access_token") is None:
        return "Access denied: response=%s" % response
    store_xero_oauth2_token(response)
    return redirect(url_for("index", _external=True))

@app.route("/accounting_invoice_read_all")
@xero_token_required
def accounting_invoice_read_all():
    # This function must be defined elsewhere in your application
    xero_tenant_id = get_xero_tenant_id()

    # Ensure that accounting_api and api_client are properly configured and imported
    accounting_api = AccountingApi(api_client)

    try:
        invoices_read = accounting_api.get_invoices(xero_tenant_id)
    except AccountingBadRequestException as exception:
        output = "Error: " + exception.reason
        json = jsonify(exception.error_data)
    else:
        output = "Total invoices found: {}.".format(len(invoices_read.invoices))
        json = serialize_model(invoices_read)
    return render_template(
        "output.html", title="Invoices", code=code, output=output, json=json, len=len(invoices_read.invoices), set="accounting", endpoint="invoice", action="read_all"
    )

# Make sure to define or import all the functions and classes used here:
# get_code_snippet, get_xero_tenant_id, store_xero_oauth2_token, AccountingApi, api_client, serialize_model, AccountingBadRequestException
