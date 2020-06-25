import bs4 as bs
import requests
from twilio.rest import Client
import os

is_not_open = True

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

resp = requests.get("https://ttbbrighton.resurva.com/")
soup = bs.BeautifulSoup(resp.text, features="html.parser")

status = soup.find_all("h3", class_="title")
if status[0].contents[0] == '\n\t\t\tBooking is Currently Offline\t\t':
    print("IS OFFLINE")
else:
    message = client.messages \
        .create(
        body='THE BARBERS ARE OPEN!!! - https://ttbbrighton.resurva.com/',
        from_=os.environ['TWILIO_FROM_NUMBER'],
        to=os.environ['TWILIO_TO_NUMBER']
    )
