import requests
from flask import Flask, request, redirect, url_for
from src.classifier import MyTextClassifier
from werkzeug.utils import secure_filename
import os
import json
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = APP_ROOT + "/src/web/files"

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


def filedl(url):
    r = requests.get(url)
    print(r.content)
    return r


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


# https://github.com/hartleybrody/fb-messenger-bot
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "<h1>Hello, this is fb-text-classifier.</h1>\n<p>Made by Siim Raudsepp and Kristjan Puusepp</p>", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    print("Heroku received the JSON")
    data = request.get_json()
    print("The JSON data:")
    print(data)
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                try:
                    if messaging_event.get("message"):  # someone sent us a message

                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        print("sender_id: " + sender_id)

                        try:
                            for i in messaging_event["message"]["attachments"]:
                                print("Checking if it message is a file...")
                                if i["type"] == "file":
                                    print("User sent a file")
                                    r = requests.get(i["payload"]["url"])
                                    print(r.content)
                                    continue
                                else:
                                    print("Not a file")
                                    break




                        except Exception:
                            print("Something went wrong, could not download the file")

                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"]["text"]  # the message's text
                        print("message text:" + message_text)
                        send_message(sender_id, "roger that!")

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass
                except KeyError:
                    return "oops", 200

    print("sending response: ok, 200")
    return "ok", 200


def send_message(recipient_id, message_text):

    print("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=True, threaded=True)

