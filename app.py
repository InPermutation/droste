import os
from flask import Flask, render_template, request, redirect, url_for
import recursion
from uuid import uuid4
from base64 import urlsafe_b64encode
import requests
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import cheezapi

app = Flask(__name__)
app.secret_key = os.environ['SESSION_KEY']

@app.route('/')
def hello():
    return render_template('index.html', user=cheezapi.user())

def bucket():
    return os.environ.get('bucket', 'droste.jkrall.net')

@app.route('/', methods=['POST'])
def upload():
    f = request.files['file']
    points = [int(request.form[param]) for param in ['x1', 'y1', 'x2', 'y2']]

    bytes = recursion.renderToString(f, points)
    
    key = urlsafe_b64encode(uuid4().bytes).rstrip("=")

    k = Key(S3Connection().get_bucket(bucket()))
    k.key = key + ".gif"
    k.set_metadata('Content-Type', 'image/gif')
    k.set_contents_from_string(bytes)

    return redirect(url_for('view', id=key))

@app.route('/view/<id>')
def view(id):
    return render_template('image.html', bucket=bucket(), id=id, user=cheezapi.user())

@app.route('/submit/<id>')
def submit(id):
    asset = cheezapi.submit('http://' + bucket()+ '/' + id + '.gif')
    return redirect(asset['items'][0]['share_url'])

@app.route('/login')
def login():
    url = "https://api.cheezburger.com/oauth/authorize?response_type=code&client_id=%s&redirect_uri=%s" % (cheezapi.client_id(), cheezapi.redirect_uri())
    return redirect(url)

@app.route('/cheez')
def cheez():
    code = request.args.get('code', '')
    if not code:
        return redirect(uri_for('login'))
    cheezapi.start_session(code)
    return redirect(url_for('hello'))

if  __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

