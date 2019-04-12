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
        self.master.title("Incident SMS")
        self.pack()
        self.create_widgets()
        self.twilioClient = self.prepTwilio()

    def create_widgets(self):
        # Make widgets dynamic after figuring out format/template file
        # Resource: https://www.python-course.eu/tkinter_layout_management.php
        #       col 0   |   col 1   | col 2
        # row 0         |           |
        # -----------------------------------
        # row 1         |           |
        # -----------------------------------
        # row 2         |           |
        # -----------------------------------
        # row 3         |           |
        # -----------------------------------

        # send SMS button
        self.twilioButton = tk.Button(self,text="Twilio SMS", fg="red", command=self.confirmSMSmessage)
        self.twilioButton.grid(row=10,column=1)

        # quit button
        self.quit = tk.Button(self, text="QUIT", command=self.master.destroy)
        self.quit.grid(row=10,column=2)

        # label 1
        self.labelDevice = tk.Label(self, text="Device:",justify=tk.LEFT)
        self.labelDevice.grid(row=0,column=0)

        # text field 1
        self.textDevice = tk.Entry(self)
        self.textDevice.grid(row=0,column=1)

        # label 2
        self.labelError = tk.Label(self, text="Error or Datapoint & Value:",justify=tk.LEFT)
        self.labelError.grid(row=1,column=0)

        # text field 2
        self.textError = tk.Entry(self)
        self.textError.grid(row=1,column=1)

        # label 3
        self.labelTime = tk.Label(self, text="Time Began:",justify=tk.LEFT)
        self.labelTime.grid(row=2,column=0)

        # text field 3
        self.textTime = tk.Entry(self)
        self.textTime.grid(row=2,column=1)

        # label 4
        self.labelAssociates = tk.Label(self, text="Associates Contacted:",justify=tk.LEFT)
        self.labelAssociates.grid(row=3,column=0)

        # text field 4
        self.textAssociates = tk.Entry(self)
        self.textAssociates.grid(row=3,column=1)

    def prepTwilio(self):
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
       
    def createSMS(self):
        # Message = label text + \n + text.get() + \n\n
        message = f"Device:\n{self.textDevice.get()}\n\n"
        message += f"Error or Datapoint & Value:\n{self.textError.get()}\n\n"
        message += f"Time Began:\n{self.textTime.get()}\n\n"
        message += f"Associates Contacted:\n{self.textAssociates.get()}\n\n"
        
        return message

    def sendSMS(self): # needs to take in SMS provider and format/template as params in future
        with open("config.json") as json_data_file:
            config = json.load(json_data_file)

        fromNumber = config['twilio']['fromNumber']
        toNumber = config['twilio']['toNumber']
        
        message = self.twilioClient.messages \
                .create(
                     body=self.createSMS(),
                     from_=fromNumber,
                     to=toNumber
                 )
        print(message.sid)
              
    def confirmSMSmessage(self):
        popup = tk.Tk()
        popup.title("Are you sure?")
        labelSMS = tk.Label(popup, text=self.createSMS())
        labelSMS.pack(side="top")
        buttonConfirm = tk.Button(popup, text="Send", command = self.sendSMS())
        buttonConfirm.pack(side=tk.LEFT)
        buttonCancel = tk.Button(popup, text="Cancel", command=popup.destroy)
        buttonCancel.pack(side=tk.RIGHT)
        popup.mainloop()

root = tk.Tk()
app = Application(master=root)
app.mainloop()

