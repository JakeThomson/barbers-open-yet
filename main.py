import bs4 as bs
import requests
from twilio.rest import Client
import os
import time
import datetime as dt

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
poll_interval = (15 * 60)
count = 0

while True:
    count += 1
    try:
        resp = requests.get("https://ttbbrighton.resurva.com/")
        soup = bs.BeautifulSoup(resp.text, features="html.parser")
    except:
        message = client.messages \
            .create(
                body='Error in application.',
                from_=os.environ['TWILIO_FROM_NUMBER'],
                to=os.environ['TWILIO_TO_NUMBER']
            )
        print(f"[{dt.datetime.strftime(dt.datetime.now(), '%d/%m/%Y %H:%M', )}] poll #{count} - ERROR POLLING")
        time.sleep(poll_interval * 2)
        continue

    try:
        status = soup.find_all("h3", class_="title")
    except:
        message = client.messages \
            .create(
                body='THE BARBERS ARE OPEN!!! - https://ttbbrighton.resurva.com/',
                from_=os.environ['TWILIO_FROM_NUMBER'],
                to=os.environ['TWILIO_TO_NUMBER']
            )
        print(f"[{dt.datetime.strftime(dt.datetime.now(), '%d/%m/%Y %H:%M', )}] poll #{count} - ONLINE!!!")

        break

    if status[0].contents[0] == '\n\t\t\tBooking is Currently Offline\t\t':
        print(f"[{dt.datetime.strftime(dt.datetime.now(), '%d/%m/%Y %H:%M', )}] poll #{count} - OFFLINE")
        time.sleep(poll_interval)

    else:
        message = client.messages \
            .create(
                body='THE BARBERS ARE OPEN!!! - https://ttbbrighton.resurva.com/',
                from_=os.environ['TWILIO_FROM_NUMBER'],
                to=os.environ['TWILIO_TO_NUMBER']
            )
        print(f"[{dt.datetime.strftime(dt.datetime.now(), '%d/%m/%Y %H:%M', )}] poll #{count} - ONLINE!!!")
        break
