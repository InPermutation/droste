from flask import url_for, session
import os
import requests

def redirect_uri(id):
    redirect_uri = url_for('cheez', _external=True, id=id)
    # API includes protocol as part of URL matching. Use this to force HTTPS:
    if os.environ.get('FORCE_HTTPS') == 'True':
        redirect_uri = redirect_uri.replace('http://', 'https://')
    return redirect_uri

def auth_uri(id = None):
    cid = client_id()
    uri = redirect_uri(id)
    return "https://api.cheezburger.com/oauth/authorize?response_type=code&client_id=%s&redirect_uri=%s" % (cid, uri)

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
    r = requests.post("https://api.cheezburger.com/v1/assets",
            data={'access_token': session['access_token'],
            'content': url, 'site_id': SENOR_GIF})
    return r.json()

def start_session(code):
    tdata = token_data(code)
    session['access_token'] = tdata['access_token']

def end_session():
    session.pop('access_token', None)

def user():
    if 'access_token' in session:
        r = requests.get('https://api.cheezburger.com/v1/me',
            params = {'access_token': session['access_token']})
        json = r.json()
        if 'items' in json:
            return json['items'][0]
    return None
