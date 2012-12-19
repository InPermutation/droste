import os
from flask import Flask, render_template, request
from images2gif import GifWriter
import StringIO
import PIL

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    f = request.files['file']

    im = PIL.Image.open(f).convert("P")
    
    gw = GifWriter()
    fp = StringIO.StringIO()

    gw.writeGifToFile(fp, [im], [10], 0, [[0, 0]], [2])

    bytes = fp.getvalue()
    fp.close()

    return bytes, None, {"Content-Type": "image/gif"}

if  __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

