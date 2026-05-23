import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://www.manitoba.ca/education/childcare/resources/new_schools.html"

SCHOOLS = [
    "Prairie Pointe School",
    "South Winnipeg Recreation Campus"
]

BOT_TOKEN = os.getenv("8626498529:AAHIeTNVUJbsjcypaZgG3ukRPFFV_gQ5XrQ")
CHAT_ID = os.getenv("6798538852")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def extract_school_data():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")

    data = {}

    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
        if len(cols) < 2:
            continue

        school_name = cols[0]

        if school_name in SCHOOLS:
            data[school_name] = cols  # store entire row

    return data

def load_previous():
    with open("previous.json", "r") as f:
        return json.load(f)

def save_current(data):
    with open("previous.json", "w") as f:
        json.dump(data, f, indent=2)

def main():
    current = extract_school_data()
    previous = load_previous()

    changes = []

    for school in SCHOOLS:
        curr_row = current.get(school, "")
        prev_row = previous.get(school, "")

        if curr_row != prev_row:
            changes.append(f"🔔 Change detected for *{school}*\n\nPrevious:\n{prev_row}\n\nNow:\n{curr_row}")

    if changes:
        send_telegram("\n\n".join(changes))

    save_current(current)

if __name__ == "__main__":
    main()
