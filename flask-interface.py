from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import os


app = Flask(__name__)
DATA_FILE = "data/air_quality_log.csv"

@app.route("/upload", methods=["POST"])
def upload():
    try:
        # Force parsing JSON from ESP32
        data = request.get_json(force=True)
        print(" Raw data received:", data)

        # Validate data
        if not data or "value" not in data:
            print("Missing 'value' in request")
            return jsonify({"error": "Missing 'value'"}), 400

        # Convert to float
        value = float(data["value"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create directory if it doesn't exist
        os.makedirs("data", exist_ok=True)

        # Save data to CSV
        df = pd.DataFrame([[timestamp, value]], columns=["timestamp", "value"])
        df.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False)

        print(f" Logged {timestamp} → {value:.2f} V")
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Server error:", str(e)) 
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", use_reloader=False)      #prevent multiple reloads

