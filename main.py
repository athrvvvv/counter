from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow cross-origin requests if needed

# In-memory count variable (for demo only; reset on server restart)
count = 0

@app.route("/")
def home():
    return {"status": "Ringtone Counter API running"}

@app.route('/count', methods=['GET', 'POST'])
def count_route():
    global count
    if request.method == 'GET':
        return jsonify({"count": count})

    if request.method == 'POST':
        data = request.get_json()
        if not data or 'count' not in data:
            return jsonify({"error": "Missing 'count' in JSON body"}), 400

        try:
            new_count = int(data['count'])
        except:
            return jsonify({"error": "'count' must be an integer"}), 400

        count = new_count
        return jsonify({"count": count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
