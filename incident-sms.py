import tkinter as tk
from twilio.rest import Client
import json
from flask import Flask, render_template, request

# TODO:
# Format/template of text (hardcode at first)
# Get clarification of need for "Associates Contacted" field so I can determine if we can remove it from text
# Add a confirmation pop-up or preview field/label with second "submit" button
# Notify user with a confirmation that a text was sent
# Add error handling for when twilio gives non-200 response


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/witt")
def witt():
    print("Hello, Witt")

def prepTwilio():
    try:
        with open("config.json") as json_data_file:
            config = json.load(json_data_file)
    except FileNotFoundError:
        print("Config file not found.")
        return

    accountSid = config['twilio']['accountSID']
    authToken = config['twilio']['authToken']
    client = Client(accountSid, authToken)
    return client

def createSMS():
    message = f"Device:\n{request.form['device']}\n\n"
    message += f"Error or Datapoint & Value:\n{request.form['errorinfo']}\n\n"
    message += f"Time Began:\n{request.form['timebegan']}\n\n"
    message += f"Associates Contacted:\n{request.form['associatescontacted']}\n\n"
    message += ("**Please join the Conference Bridge**\n"
                "Phone Number: 1-901-555-1234\n"
                "Attendee access code: 12345678\n"
                "Mobile-friendly: 901-555-1234,,,12345678#,,,#")
    
    return message

@app.route('/sendSMS', methods=['POST'])
def sendSMS(): # needs to take in SMS provider and format/template as params in future
    twilioClient = prepTwilio()

    with open("config.json") as json_data_file:
        config = json.load(json_data_file)

    fromNumber = config['twilio']['fromNumber']

    with open("clients.json") as json_data_file:
        clients = json.load(json_data_file)

    contacts = clients['Test Client']['contacts']
    
    for contact in contacts.values():
        toNumber = contact
    
        try:
            message = twilioClient.messages \
                    .create(
                        body=createSMS(),
                        from_=fromNumber,
                        to=toNumber
                    )
        except twilio.base.exceptions.TwilioRestException as err:
            print(f"Unexpected error: {err}")

        print(message.sid)
              
    #def confirmSMSmessage(self):

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
