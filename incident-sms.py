import tkinter as tk
from twilio.rest import Client
import json

# TODO:
# Contact list (hardcode at first)
# Format/template of text (hardcode at first)
# SMS provider - so far just Twilio

# Needs to be done outside Application class so it's global?

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.twilioClient = self.prepTwilio()

    def create_widgets(self):
        #       col 0   |   col 1   | col 2
        # row 0         |           |
        # -----------------------------------
        # row 1         |           |
        # -----------------------------------
        # row 2         |           |
        # -----------------------------------
        # row 3         |           |
        # -----------------------------------


        self.twilioButton = tk.Button(self)
        self.twilioButton["text"] = "Twilio SMS"
        self.twilioButton["command"] = self.sendSMS
        self.twilioButton.grid(row=4,column=1)

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.grid(row=4,column=2)

        # label 1
        self.labelDevice = tk.Label(self, text="Device:")
        self.labelDevice.grid(row=0,column=0)

        # text field 1
        self.smsContent = tk.Entry(self)
        self.smsContent.grid(row=0,column=1)

        # label 2
        self.labelError = tk.Label(self, text="Error or Datapoint & Value:")
        self.labelError.grid(row=1,column=0)

        # label 3
        self.labelTime = tk.Label(self, text="Time Began:")
        self.labelTime.grid(row=2,column=0)

    def prepTwilio(self):
        with open("config.json") as json_data_file:
            config = json.load(json_data_file)

        accountSid = config['twilio']['accountSID']
        authToken = config['twilio']['authToken']
        client = Client(accountSid, authToken)
        return client
       

    def sendSMS(self): # needs to take in SMS provider and format/template as params in future
        with open("config.json") as json_data_file:
            config = json.load(json_data_file)

        fromNumber = config['twilio']['fromNumber']
        toNumber = config['twilio']['toNumber']
        
        message = self.twilioClient.messages \
                .create(
                     body=self.smsContent.get(),
                     from_=fromNumber,
                     to=toNumber
                 )
        print(message.sid)

root = tk.Tk()
app = Application(master=root)
app.mainloop()

