import requests
from flask import Flask, request, redirect, url_for
from src.classifier import MyTextClassifier
from werkzeug.utils import secure_filename
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = APP_ROOT + "\\src\\web\\files"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
clf = None



@app.route('/hi/<name>')
def say_hi(name):
    return 'Hello, %s!' % name


@app.route('/findauthor/<text>/')
def findauthor(text):
    print([text])
    return clf.predictAuthor([text])[0]

@app.route('/upload/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file

        if 'file' not in request.files:
            return "No file selected"

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "No file selected"

        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            global clf
            clf = MyTextClassifier(path)
            return "File upload success"
    return "Done"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)

