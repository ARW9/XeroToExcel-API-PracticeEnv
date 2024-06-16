from flask import Flask, request, redirect, session, url_for, jsonify
import requests
import base64
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Xero credentials
CLIENT_ID = '31B88F29375F4310A5643DE73D4F3DE6'
CLIENT_SECRET = 'GpcMKLmtoP122CpjslUFAiQFWF89CeLccQBb7JyCG06WZeEu'
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def index():
    return 'Welcome to the Xero App!'

@app.route('/login')
def login():
    # Corrected scope formatting to be space-separated and URL-encoded
    scope = "offline_access openid profile email"
    # Redirect to Xero OAuth URL
    return redirect(
        f"https://login.xero.com/identity/connect/authorize?response_type=code"
        f"&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={scope}"
    )

@app.route('/callback')
def callback():
    code = request.args.get('code')
    # Correct base64 encoding for the authorization header
    authorization_header_value = 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode('utf-8')
    response = requests.post(
        'https://identity.xero.com/connect/token',
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        },
        headers={
            'Authorization': authorization_header_value
        }
    )
    session['token'] = response.json().get('access_token')
    return redirect(url_for('index'))

@app.route('/api/data')
def data():
    headers = {'Authorization': f'Bearer {session["token"]}'}
    response = requests.get('https://api.xero.com/api.xro/2.0/Invoices', headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
