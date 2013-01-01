from flask import url_for, session
import os
import requests

def redirect_uri():
    redirect_uri = url_for('cheez', _external=True)
    # API includes protocol as part of URL matching. Use this to force HTTPS:
    if os.environ.get('FORCE_HTTPS') == 'True':
        redirect_uri = redirect_uri.replace('http://', 'https://')
    return redirect_uri

def client_id():
    return os.environ.get('CHZ_CLIENT_ID')

def client_secret():
    return os.environ.get('CHZ_CLIENT_SECRET')

def token_data():
    r = requests.post("https://api.cheezburger.com/oauth/access_token",
            data={'client_id': client_id(), 'client_secret': client_secret(), 
            'code': code, 'grant_type': 'authorization_code'})
    return r.json()
 
def start_session(code):
    token_data = token_data(code)
    session['access_token'] = token_data['access_token']

def user():
    if 'access_token' in session:
        r = requests.get('https://api.cheezburger.com/v1/me',
            params = {'access_token': session['access_token']})
        json = r.json()
        if 'items' in json:
            return json['items'][0]
    return None
