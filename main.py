from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import threading

app = Flask(__name__)
CORS(app)

lock = threading.Lock()  # to avoid race conditions on file write
json_file = "count.json"

def read_count():
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
            return data.get("count", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def write_count(count):
    with lock:
        with open(json_file, "w") as f:
            json.dump({"count": count}, f)

@app.route("/count", methods=["GET"])
def get_count():
    count = read_count()
    return jsonify({"count": count})

@app.route("/increment", methods=["POST"])
def increment():
    count = read_count() + 1
    write_count(count)
    return jsonify({"count": count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
