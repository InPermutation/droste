import os
from flask import Flask, render_template, request
import recursion
from uuid import uuid4
from base64 import urlsafe_b64encode

from boto.s3.connection import S3Connection
from boto.s3.key import Key

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    f = request.files['file']
    points = [int(request.form[param]) for param in ['x1', 'y1', 'x2', 'y2']]

    bytes = recursion.renderToString(f, points)

    bucket = os.environ.get('bucket', 'droste.jkrall.net')
    k = Key(S3Connection().get_bucket(bucket))
    k.key = safe_key()
    k.set_metadata('Content-Type', 'image/gif')
    k.set_contents_from_string(bytes)

    url = 'http://' + bucket + '/' + k.key
    return render_template('image.html', url=url)

def safe_key():
   return urlsafe_b64encode(uuid4().bytes).rstrip("=") + ".gif" 

if  __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

