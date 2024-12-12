import requests
from django.conf import settings

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
CHAT_ID = settings.TELEGRAM_CHAT_ID

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

def send_telegram_photo(photo_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(photo_path, 'rb') as photo:
        data = {
            "chat_id": CHAT_ID
        }
        files = {
            "photo": photo
        }
        requests.post(url, data=data, files=files)
