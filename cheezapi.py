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

def token_data(code):
    r = requests.post("https://api.cheezburger.com/oauth/access_token",
            data={'client_id': client_id(), 'client_secret': client_secret(), 
            'code': code, 'grant_type': 'authorization_code'})
    return r.json()

def submit(url):
    SENOR_GIF = 61
    #TODO: access_token expired
    #TODO: no access_token (submit anonymously? prompt for login?)
    r = requests.post("https://api.cheezburger.com/v1/assets",
            data={'access_token': session['access_token'],
            'content': url, 'site_id': SENOR_GIF})
    return r.json()

def start_session(code):
    tdata = token_data(code)
    session['access_token'] = tdata['access_token']

def user():
    if 'access_token' in session:
        r = requests.get('https://api.cheezburger.com/v1/me',
            params = {'access_token': session['access_token']})
        json = r.json()
        if 'items' in json:
            return json['items'][0]
    return None
