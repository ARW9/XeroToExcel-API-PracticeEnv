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
