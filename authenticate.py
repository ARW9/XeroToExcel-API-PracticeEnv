from flask import Flask, session, request, redirect, url_for, jsonify, render_template
from functools import wraps

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
