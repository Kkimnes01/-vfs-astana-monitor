import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

message = (
    "🤖 VFS Astana Monitor запущен!\n\n"
    "Telegram-уведомления работают ✅"
)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

response.raise_for_status()
print("Telegram message sent successfully!")
