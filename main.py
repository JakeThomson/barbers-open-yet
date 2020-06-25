import bs4 as bs
import requests

is_not_open = True

resp = requests.get("https://ttbbrighton.resurva.com/")
soup = bs.BeautifulSoup(resp.text, features="html.parser")

status = soup.find_all("h3", class_="title")
if status[0].contents[0] == '\n\t\t\tBooking is Currently Offline\t\t':
    print("IS OFFLINE")

