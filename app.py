import os
from flask import Flask, render_template, request, session, redirect, url_for
import recursion
from uuid import uuid4
from base64 import urlsafe_b64encode
import requests
from boto.s3.connection import S3Connection
from boto.s3.key import Key

app = Flask(__name__)
app.secret_key = os.environ['SESSION_KEY']

def bucket():
    return os.environ.get('bucket', 'droste.jkrall.net')

@app.route('/')
def hello():
    return render_template('index.html', user=user())

@app.route('/', methods=['POST'])
def upload():
    f = request.files['file']
    points = [int(request.form[param]) for param in ['x1', 'y1', 'x2', 'y2']]

    bytes = recursion.renderToString(f, points)
    
    key = safe_key()

    k = Key(S3Connection().get_bucket(bucket()))
    k.key = key + ".gif"
    k.set_metadata('Content-Type', 'image/gif')
    k.set_contents_from_string(bytes)

    return redirect(url_for('view', id=key))

@app.route('/view/<id>')
def view(id):
    url = 'http://' + bucket() + '/' + id + ".gif"
    return render_template('image.html', url=url, user=user())

def safe_key():
   return urlsafe_b64encode(uuid4().bytes).rstrip("=")

@app.route('/login')
def login():
    return render_template('login.html',
        id=os.environ.get('CHZ_CLIENT_ID'),
        redirect_uri=url_for('cheez', _external=True)
    )

@app.route('/cheez')
def cheez():
    code = request.args.get('code', '')
    if not code:
        return login()
    id = os.environ.get('CHZ_CLIENT_ID')
    secret = os.environ.get('CHZ_CLIENT_SECRET')
    
    r = requests.post("https://api.cheezburger.com/oauth/access_token",
            data={'client_id': id, 'client_secret': secret, 
            'code': code, 'grant_type': 'authorization_code'})
    token_data = r.json()
    session['access_token'] = token_data['access_token']
    return redirect(url_for('hello'))

def user():
    if 'access_token' in session:
        r = requests.get('https://api.cheezburger.com/v1/me',
            params = {'access_token': session['access_token']})
        json = r.json()
        if 'items' in json:
            return json['items'][0]
    return None

if  __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

