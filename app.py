from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received webhook data:", data)
    message = data.get("text", str(data))
    try:
        send_to_telegram(message)
        print("send_to_telegram called successfully")
    except Exception as e:
        print("Error in send_to_telegram:", e)
    return 'OK', 200

def send_to_telegram(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    print("Sending message to Telegram:", text)
    response = requests.post(url, json=payload)
    print("Telegram API Status:", response.status_code)
    print("Telegram API Response:", response.text)
    response.raise_for_status()  # This will raise an exception if the request failed


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
