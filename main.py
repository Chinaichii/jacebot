from flask import Flask, request
from openai import OpenAI
import os
import requests

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ALLOWED_USER_ID = os.environ.get("TELEGRAM_USER_ID")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" not in data:
        return "ok"

chat_id = str(data["message"]["chat"]["id"])
user_id = str(data["message"]["from"]["id"])

if "text" not in data["message"]:
    send_message(chat_id, "⛔ Я понимаю только текстовые сообщения.")
    return "ok"

message_text = data["message"]["text"]

if user_id != ALLOWED_USER_ID:
    send_message(chat_id, "⛔ Нет доступа.")
    return "ok"


    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message_text}]
    )
    reply = response.choices[0].message.content

    send_message(chat_id, reply)
    return "ok"

@app.route('/')
def index():
    return "🔥 Jace is alive."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
