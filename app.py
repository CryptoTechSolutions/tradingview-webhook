from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Get API Keys from Environment Variables
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"  # Change for live trading

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if not data:
        return jsonify({"error": "No data received"}), 400  # HTTP 400 for Bad Request
    
    # Print data for debugging (optional)
    print("Received Webhook Data:", data)

    # Example: Place a trade if strategy conditions are met
    stock = data.get("stock")
    direction = data.get("direction")
    trade_size = data.get("trade_size")

    if not stock or not direction or trade_size is None:
        return jsonify({"error": "Missing required fields"}), 400

    order_payload = {
        "symbol": stock,
        "qty": trade_size,
        "side": "buy" if direction == "long" else "sell",
        "type": "market",
        "time_in_force": "gtc"
    }

    # Send order to Alpaca
    alpaca_response = requests.post(
        f"{ALPACA_BASE_URL}/v2/orders",
        json=order_payload,
        headers=HEADERS
    )

    if alpaca_response.status_code == 200:
        return jsonify({"message": "Order placed successfully!", "order_details": alpaca_response.json()})
    else:
        return jsonify({"error": "Failed to place order", "details": alpaca_response.text}), 500

if __name__ == "__main__":
    app.run(debug=True)
