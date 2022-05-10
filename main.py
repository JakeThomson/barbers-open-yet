import json
import re

import bs4 as bs
import requests
from twilio.rest import Client
import os
import time
import datetime as dt
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
client = Client(account_sid, auth_token)
poll_interval = (2 * 60)
from_number = os.environ['FROM_NUMBER']
to_number = os.environ['TO_NUMBER']
count = 0

last_cheapest_ticket = 106.82

while True:
    count += 1
    try:
        resp = requests.get("https://www.viagogo.co.uk/Concert-Tickets/Club-and-dance/Kaytranada-Tickets/E-150085021/")
        soup = bs.BeautifulSoup(resp.text, features="html.parser")
        pattern = re.compile("eventListings = JSON\.parse\(\"(.*)\"\);")
        match = pattern.search(str(soup)).group(1)
        match = match.replace('\\', '')
        response = json.loads(match)
    except:
        message = client.messages \
            .create(
                body='Error in application.',
                from_=from_number,
                to=to_number
            )
        print(f"[{dt.datetime.strftime(dt.datetime.now(), '%d/%m/%Y %H:%M', )}] poll #{count} - ERROR POLLING")
        time.sleep(poll_interval * 2)
        continue

    circle_seating = [item for item in response if "circle" in item['Section'].lower()]

    cheapest = circle_seating[0]['RawPrice']

    if cheapest < last_cheapest_ticket:
        message = client.messages \
            .create(
                body=f'Cheaper ticket for sale!! (£{cheapest})',
                from_=from_number,
                to=to_number
            )
        last_cheapest_ticket = cheapest
        print(f"[{dt.datetime.strftime(dt.datetime.now(), '%d/%m/%Y %H:%M', )}] poll #{count} - CHEAPER TICKETS! (£{cheapest})")
        time.sleep(poll_interval * 10)
    else:
        last_cheapest_ticket = cheapest
        print(f"[{dt.datetime.strftime(dt.datetime.now(), '%d/%m/%Y %H:%M', )}] poll #{count} - No cheaper tickets found")
        time.sleep(poll_interval)

