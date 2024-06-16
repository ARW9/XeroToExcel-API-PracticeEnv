from flask import Flask, request, redirect, session, url_for
import requests
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

if __name__ == '__main__':
    app.run(port=5000)



@app.route('/login')
def login():
    # Redirect to Xero OAuth URL
    return redirect(
        f"https://login.xero.com/identity/connect/authorize?response_type=code"
        f"&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=offline_access accounting.transactions"
    )

@app.route('/callback')
def callback():
    code = request.args.get('code')
    response = requests.post(
        'https://identity.xero.com/connect/token',
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        },
        headers={
            'Authorization': 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        }
    )
    session['token'] = response.json()['access_token']
    return redirect(url_for('index'))
