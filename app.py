from flask import Flask, request
import requests
import os
import sys

app = Flask(__name__)

# Load environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Webhook endpoint that TradingView will post to
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received data: {data}", file=sys.stdout, flush=True)  # Log the incoming data
    message = data.get("text", str(data))  # If 'text' isn't in JSON, use raw data

    if request.content_type != 'application/json':
        return 'Unsupported Media Type', 415

    data = request.json
    print(f"Received data: {data}", file=sys.stdout, flush=True)  # Log the incoming data
    message = data.get("text", str(data))  # If 'text' isn't in JSON, use raw data

    try:
        send_to_telegram(message)
        print("send_to_telegram called successfully", file=sys.stdout, flush=True)
    except Exception as e:
        print("Error in send_to_telegram:", e, file=sys.stdout, flush=True)
    return 'OK', 200

# Sends the message to Telegram
def send_to_telegram(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raises an error if status code is not 200

# Entry point for running locally
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port)
