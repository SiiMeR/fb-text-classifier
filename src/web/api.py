import requests
from flask import Flask, request
from src.classifier import MyTextClassifier
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'C:/Users/Kristjan/Desktop/temp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
clf = None


@app.route('/uploadhtml/', methods=['POST'])
def uploadHTML():
    if request.method == 'POST':
        print("Uploading file...")

        file = request.files['file']
        file.save(file.filename)

        print(file.filename)

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


if __name__ == "__main__":
    app.run(debug=True)



