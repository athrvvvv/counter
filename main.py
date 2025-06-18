from flask import Flask, jsonify
import json
import os

app = Flask(__name__)
COUNT_FILE = "counter_backup.json"

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
    # Just increment and return count, no Telegram call here
    count = read_count() + 1
    write_count(count)
    return jsonify({"count": count})

@app.route("/")
def home():
    return {"status": "Ringtone Counter API running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
