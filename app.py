from flask import Flask, request
import requests
import os
import sys
import json

app = Flask(__name__)

# Load environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_TOKEN_STOCK = os.getenv('TELEGRAM_TOKEN_STOCK')
TELEGRAM_CHAT_ID_STOCK = os.getenv('TELEGRAM_CHAT_ID_STOCK')
TELEGRAM_TOKEN_PURCHASED = os.getenv('TELEGRAM_TOKEN_PURCHASED')
TELEGRAM_CHAT_ID_PURCHASED = os.getenv('TELEGRAM_CHAT_ID_PURCHASED')

# Health-check route for Render
@app.route("/", methods=["GET", "HEAD"])
def index():
    return "Service is running", 200

# Webhook endpoint that TradingView will post to
@app.route('/webhook', methods=['POST'])
def webhook():
    # 🔹 Log headers
    # print("=== HEADERS ===", file=sys.stdout, flush=True)
    # for k, v in request.headers.items():
    #    print(f"{k}: {v}", file=sys.stdout, flush=True)

    # 🔹 Log raw body
    raw_data = request.get_data(as_text=True)
    #    print("=== RAW BODY ===", file=sys.stdout, flush=True)
    #    print(raw_data, file=sys.stdout, flush=True)

    # ✅ Looser validation for Content-Type
    if "application/json" not in request.content_type.lower():
    #   print(f"Invalid Content-Type received: {request.content_type}", file=sys.stdout, flush=True)
        return 'Unsupported Media Type', 415

    # Parse JSON safely
    try:
        data = request.get_json(force=True)
    except Exception as e:
    #   print("JSON parse error:", e, file=sys.stdout, flush=True)
        return 'Bad Request - invalid JSON', 400

    #print("=== PARSED JSON ===", file=sys.stdout, flush=True)
    #print(json.dumps(data, indent=2), file=sys.stdout, flush=True)

    # 🔹 Format Telegram message with multiple lines
    type_value = data.get('type', '').capitalize()
    # print(data.get('type_value', '').capitalize(), file=sys.stdout, flush=True)
    # print(type_value, file=sys.stdout, flush=True)
    type_action = f"{data.get('type', '').capitalize()} {data.get('action', '').upper()}"
    ticker_line = data.get('ticker', 'Unknown Ticker')
    # price_line = f"Price: {data.get('price', 'N/A')}"
    telegram_message = f"{type_action}\n{ticker_line}" # \n{price_line}"

    try:
        send_to_telegram(telegram_message, type_value)
    #   print("send_to_telegram called successfully", file=sys.stdout, flush=True)
    except Exception as e:
    #   print("Error in send_to_telegram:", e, file=sys.stdout, flush=True)

    return 'OK', 200

# Sends the message to Telegram
def send_to_telegram(text, type_value):
    if type_value == 'C-':
        url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': text,
            'parse_mode': 'Markdown'
        }
    elif type_value == 'S-':
        url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN_STOCK}/sendMessage'
        payload = {
            'chat_id': TELEGRAM_CHAT_ID_STOCK,
            'text': text,
            'parse_mode': 'Markdown'
        }
    else:
        url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN_PURCHASED}/sendMessage'
        payload = {
            'chat_id': TELEGRAM_CHAT_ID_PURCHASED,
            'text': text,
            'parse_mode': 'Markdown'
        }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    
# Entry point for running locally
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
#   print(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port)
