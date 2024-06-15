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
    code = get_code_snippet("INVOICES","READ_ALL")

    #[INVOICES:READ_ALL]
    xero_tenant_id = get_xero_tenant_id()
    accounting_api = AccountingApi(api_client)

    try:
        invoices_read = accounting_api.get_invoices(
            xero_tenant_id
        )
    except AccountingBadRequestException as exception:
        output = "Error: " + exception.reason
        json = jsonify(exception.error_data)
    else:
        output = "Total invoices found:  {}.".format(len(invoices_read.invoices)
        )
        json = serialize_model(invoices_read)
    #[/INVOICES:READ_ALL]

    return render_template(
        "output.html", title="Invoices",code=code, output=output, json=json, len = 0, set="accounting", endpoint="invoice", action="read_all"
    )
