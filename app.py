from flask import Flask, request, redirect, session, url_for, jsonify
import requests
import base64
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))  # Better to use a fixed secret key from env variables

# Xero credentials from environment variables for better security
CLIENT_ID = os.getenv('31B88F29375F4310A5643DE73D4F3DE6')
CLIENT_SECRET = os.getenv('GpcMKLmtoP122CpjslUFAiQFWF89CeLccQBb7JyCG06WZeEu')
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def index():
    return 'Welcome to the Xero App!'

@app.route('/login')
def login():
    scope = "offline_access openid profile email"
    scope_encoded = requests.utils.quote(scope)  # Ensure scope is URL-encoded
    # Redirect to Xero OAuth URL with URL-encoded scope
    return redirect(
        f"https://login.xero.com/identity/connect/authorize?response_type=code"
        f"&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={scope_encoded}"
    )

@app.route('/callback')
def callback():
    code = request.args.get('code')
    authorization_header_value = 'Basic ' + basekdir(base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode('utf-8'))
    response = requests.post(
        'https://identity.xero.com/connect/token',
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        },
        headers={'Authorization': authorization_header_value}
    )
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch token', 'details': response.text}), response.status_code
    session['token'] = response.json().get('access_token')
    return redirect(url_for('index'))

@app.route('/api/data')
def data():
    if 'token' not in session:
        return jsonify({'error': 'Authentication token is missing'}), 401
    headers = {'Authorization': f'Bearer {session["token"]}'}
    response = requests.get('https://api.xero.com/api.xro/2.0/Invoices', headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data', 'details': response.text}), response.status_code
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
