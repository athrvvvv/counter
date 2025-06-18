from flask import Flask, request, jsonify
import json
import os
from telegram import Bot

app = Flask(__name__)

COUNT_FILE = "counter_backup.json"
BOT_TOKEN = "8134005386:AAESG7GSYcibFo7E8lxubjwxjmpoyhBLlBw"
CHAT_ID = "6264741586"

bot = Bot(token=BOT_TOKEN)

def read_count():
    if not os.path.exists(COUNT_FILE):
        return 0
    with open(COUNT_FILE, "r") as f:
        data = json.load(f)
        return data.get("count", 0)

def write_count(count):
    with open(COUNT_FILE, "w") as f:
        json.dump({"count": count}, f)

@app.route("/update_count", methods=["POST"])
def update_count():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    song_title = data.get("song_title", "Unknown Song")
    device_info = data.get("device_info", "Unknown Device")

    # Read old count and increment
    count = read_count() + 1
    write_count(count)

    message = (
        f"🔔 Ringtone has been set {count} times.\n"
        f"🎵 Song Title: {song_title}\n"
        f"📱 Device Info: {device_info}"
    )

    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Count updated and Telegram message sent", "count": count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
