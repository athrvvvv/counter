import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
DATA_FILE = "counter_backup.json"

# Your Telegram bot token and chat ID
BOT_TOKEN = "8134005386:AAESG7GSYcibFo7E8lxubjwxjmpoyhBLlBw"
CHAT_ID = "6264741586"


def load_data():
    if not os.path.exists(DATA_FILE):
        # Initialize file with zero count and empty history
        data = {"count": 0, "history": []}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
        return data
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def send_telegram_message(count, song_title, device_info):
    text = (
        f"🔔 Ringtone has been set {count} times.\n"
        f"Song: {song_title}\n"
        f"Device: {device_info}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        print(f"Telegram message sent: {text}")
    except Exception as e:
        print(f"Error sending telegram message: {e}")


@app.route("/count", methods=["GET"])
def get_count():
    data = load_data()
    return jsonify(data)


@app.route("/count", methods=["POST"])
def update_count():
    req_data = request.get_json()
    song_title = req_data.get("song_title", "Unknown Song")
    device_info = req_data.get("device_info", "Unknown Device")

    data = load_data()
    data["count"] += 1
    new_record = {
        "count": data["count"],
        "song_title": song_title,
        "device_info": device_info,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    data["history"].append(new_record)

    save_data(data)
    send_telegram_message(data["count"], song_title, device_info)

    return jsonify({"message": "Count updated", "count": data["count"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
