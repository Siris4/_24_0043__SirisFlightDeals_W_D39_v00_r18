
from twilio.rest import Client
import os

# this class is responsible for sending SMS notifications with the deal flight details.
    # def check_if_Google_sheet_is_lowest_price(self):

# retrieve Twilio credentials and phone numbers from environment variables:
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
from_your_virtual_twilio_phone_number = os.environ.get("FROM_YOUR_VIRTUAL_TWILIO_PHONE_NUMBER")
to_recipient_phone_number = os.environ.get("TO_RECIPIENT_PHONE_NUMBER")

class NotificationManager:
    def __init__(self):
        self.client = Client(account_sid, auth_token)   # for Twilio SMS sending:

    def send_an_sms_text(self, message):
        # --------------------------------------- TAKE THESE OUT WHEN TESTING PHASE IS ALL FINISHED ---------------------------------------------- #
        print(f"account_sid = {account_sid}")
        print(f"auth_token = {auth_token}")
        print(f"FROM_YOUR_VIRTUAL_TWILIO_PHONE_NUMBER = {from_your_virtual_twilio_phone_number}")
        print(f"TO_RECIPIENT_PHONE_NUMBER = {to_recipient_phone_number}")
        # ---------------------------------------------------------------------------------------------------------------------------------------- #

        # check if all required variables were retrieved:
        if not all([account_sid, auth_token, from_your_virtual_twilio_phone_number, to_recipient_phone_number]):
            print("Error: One or more environment variables are not set.")
        else:
            try:
                # initialize Twilio client:
                client = Client(account_sid, auth_token)

                # compose and send the message:
                message = self.client.messages.create(
                    body=message,
                    from_=from_your_virtual_twilio_phone_number,
                    to=to_recipient_phone_number,
                    # to='recip_ph_number',  #toggle this on and the one below this toggled off, to easily swap phone numbers
                )

                # print the message status:
                print(f"Message Status: {message.status}. Yes, the text got sent :)")
                print(f"The message.sid: {message.sid}")
            except Exception as e:
                print(f"Failed to send message: {e}")

    # Optional:
    def send_an_email(self):
        pass