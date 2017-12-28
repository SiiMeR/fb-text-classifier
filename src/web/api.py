import requests
from flask import Flask, request
from src.classifier import MyTextClassifier

app = Flask(__name__)

clf = MyTextClassifier("tekst1.html")


@app.route('/hi/<name>')
def say_hi(name):
    return 'Hello, %s!' % name


@app.route('/findauthor/<text>/')
def findauthor(text):
    print([text])
    return clf.predictAuthor([text])[0]


if __name__ == "__main__":
    app.run(debug=True)



