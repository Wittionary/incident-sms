import tkinter as tk
from twilio.rest import Client
import json

# TODO:
# Contact list (hardcode at first)
# Format/template of text (hardcode at first)
# SMS provider - so far just Twilio

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.twilioClient = self.prepTwilio()

    def create_widgets(self):
        self.twilioButton = tk.Button(self)
        self.twilioButton["text"] = "Twilio SMS"
        self.twilioButton["command"] = self.sendSMS
        self.twilioButton.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.smsContent = tk.Text(self)
        self.smsContent.pack(expand=1, side="left")

    def prepTwilio(self):
        with open("config.json") as json_data_file:
            config = json.load(json_data_file)

        accountSid = config['twilio']['accountSID']
        authToken = config['twilio']['authToken']
        client = Client(accountSid, authToken)
        return client
       

    def sendSMS(self, self.smsContent.get): # needs to take in SMS provider and format/template as params in future
        message = self.twilioClient.messages \
                .create(
                     body="Header:\n \
                        device1, device2, device3 \n\n \
                        Datasource/datapoint:\n \
                        ping alert host status\n\n \
                        Value:\n \
                        9001\n\n \
                        Et cetera",
                     from_='+1devphone',
                     to='+1mycellphone'
                 )
        print(message.sid)

root = tk.Tk()
app = Application(master=root)
app.mainloop()

