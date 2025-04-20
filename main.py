import os
from flask import Flask, request
import openai
import requests

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ALLOWED_USER_ID = os.getenv("TELEGRAM_USER_ID")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" not in data:
        return "ok"

    chat_id = str(data["message"]["chat"]["id"])
    user_id = str(data["message"]["from"]["id"])
    message_text = data["message"]["text"]

    if user_id != ALLOWED_USER_ID:
        send_message(chat_id, "⛔ Нет доступа.")
        return "ok"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message_text}]
    )

    reply = response["choices"][0]["message"]["content"]
    send_message(chat_id, reply)
    return "ok"

@app.route("/")
def index():
    return "🔥 Jace is alive."

if __name__ == "__main__":
    app.run()
