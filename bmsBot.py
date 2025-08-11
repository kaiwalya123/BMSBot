import requests
import time

# Your Telegram bot details
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

# BookMyShow search API (change 'mumbai' to your city code if needed)
BMS_URL = "https://in.bookmyshow.com/venue/yashwantrao-chavan-natyagruha-pune/YCNP"

# Store previous state to avoid duplicate alerts
last_titles = set()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot8135341163:AAG136-ZGnzV2BxKvR8IU5TVQKghedEEnh0/sendMessage"
    payload = {"chat_id": 5897444126, "text": message}
    requests.post(url, data=payload)

def check_for_natak():
    try:
        resp = requests.get(BMS_URL)
        data = resp.json()

        # Extract Marathi Natak titles
        events = data.get("data", {}).get("events", [])
        current_titles = {event.get("EventTitle") for event in events}

        # Check if there's anything new
        new_titles = current_titles - last_titles
        if new_titles:
            for title in new_titles:
                send_telegram_message(f"🎭 New Marathi Natak Available: {title}\nBook here: https://in.bookmyshow.com")
            last_titles.update(new_titles)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    while True:
        check_for_natak()
        time.sleep(60)  # check every 1 minute
