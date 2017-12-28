import requests
from flask import Flask, request, redirect, url_for
from src.classifier import MyTextClassifier
from werkzeug.utils import secure_filename
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = APP_ROOT + "\\files"
print("if " + APP_ROOT)
print("af " + UPLOAD_FOLDER)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
clf = None


@app.route('/uploadhtml/', methods=['POST'])
def uploadHTML():
    if request.method == 'POST':
        print("Uploading file...")

        file = request.files['file']
        file.save(file.filename)


        global clf
        clf = MyTextClassifier(file)
        print("File uploaded.")
        return "Done"
    else:
        return "Something went wrong."


@app.route('/hi/<name>')
def say_hi(name):
    return 'Hello, %s!' % name


@app.route('/findauthor/<text>/')
def findauthor(text):
    print([text])
    return clf.predictAuthor([text])[0]

@app.route('/upload/', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file

        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(path)
            file.save(path)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return "something"


if __name__ == "__main__":
    app.run(debug=True)