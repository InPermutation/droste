import os
from flask import Flask, render_template, request
from images2gif import GifWriter
import StringIO
import PIL
import recursion

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    f = request.files['file']
    points = [int(request.form[param]) for param in ['x1', 'y1', 'x2', 'y2']]

    orig = PIL.Image.open(f)

    images = [im.convert("P") for im in recursion.gif(orig, 15, points)]
    durations = [.1 for image in images]
    loops = 0 # forever
    xys = [(0, 0) for image in images]
    disposes = [1 for image in images]

    gw = GifWriter()
    fp = StringIO.StringIO()

    gw.writeGifToFile(fp, images, durations, loops, xys, disposes)

    bytes = fp.getvalue()
    fp.close()

    return bytes, None, {"Content-Type": "image/gif"}

if  __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

