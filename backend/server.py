from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.database import get_latest, get_connection, insert_data
from backend.ai_model import predict_power
from backend import mqtt_listener
import threading
import os
import time

app = Flask(__name__)

# ✅ CORS FIX (IMPORTANT for GitHub Pages)
CORS(app, resources={r"/*": {"origins": "*"}})


# ---------------- MQTT THREAD (OPTIONAL) ----------------
def run_mqtt():
    try:
        print("🚀 Starting MQTT...")
        time.sleep(2)
        mqtt_listener.start_mqtt()
    except Exception as e:
        print("❌ MQTT Error:", e)


# ---------------- HOME ----------------
@app.route("/")
def home():
    return "🚀 Smart Grid Backend Running"


# ---------------- INSERT DATA API ----------------
@app.route("/api/insert", methods=["POST"])
def insert_api():
    try:
        data = request.get_json()

        # 🔴 check if no data
        if not data:
            return jsonify({"error": "No data received"}), 400

        insert_data(
            data.get("voltage", 0),
            data.get("current", 0),
            data.get("power", 0),
            data.get("energy", 0)
        )

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("❌ Insert API Error:", e)
        return jsonify({"error": str(e)}), 500


# ---------------- LIVE DATA ----------------
@app.route("/api/data")
def api_data():
    try:
        row = get_latest()

        # 🔴 safe AI prediction
        try:
            prediction = predict_power()
        except:
            prediction = 0

        if not row:
            return jsonify({
                "voltage": 0,
                "current": 0,
                "power": 0,
                "energy": 0,
                "prediction": prediction,
                "status": "no data"
            })

        return jsonify({
            "voltage": row[0],
            "current": row[1],
            "power": row[2],
            "energy": row[3],
            "prediction": prediction
        })

    except Exception as e:
        print("❌ API Error:", e)
        return jsonify({"error": str(e)}), 500


# ---------------- HISTORY ----------------
@app.route("/api/history")
def history():
    try:
        conn = get_connection()
        if conn is None:
            return jsonify([])

        cur = conn.cursor()

        cur.execute("""
            SELECT voltage, current, power, energy, timestamp
            FROM energy
            ORDER BY id DESC
            LIMIT 100
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        rows.reverse()

        return jsonify([
            {
                "voltage": r[0],
                "current": r[1],
                "power": r[2],
                "energy": r[3],
                "time": str(r[4])
            }
            for r in rows
        ])

    except Exception as e:
        print("❌ History Error:", e)
        return jsonify([])


# ---------------- START SERVER ----------------
if __name__ == "__main__":
    print("🔥 Server starting...")

    # ⚠️ OPTIONAL: Disable if causing issues
    mqtt_thread = threading.Thread(target=run_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)