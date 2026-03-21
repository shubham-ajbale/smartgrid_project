from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_latest, get_connection, insert_data
from ai_model import predict_power
import threading
import mqtt_listener
import os

app = Flask(__name__)
CORS(app)


# ---------- OPTIONAL MQTT ----------
def run_mqtt():
    mqtt_listener.start_mqtt()


# ---------- HOME ----------
@app.route("/")
def home():
    return "Smart Grid Backend Running"


# ---------- INSERT ----------
@app.route("/api/insert", methods=["POST"])
def insert_api():
    try:
        data = request.json

        insert_data(
            data.get("voltage", 0),
            data.get("current", 0),
            data.get("power", 0),
            data.get("energy", 0)
        )

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"error": str(e)})


# ---------- LIVE ----------
@app.route("/api/data")
def api_data():
    row = get_latest()
    prediction = predict_power()

    if not row:
        return jsonify({
            "voltage": 0,
            "current": 0,
            "power": 0,
            "energy": 0,
            "prediction": 0,
            "status": "no data"
        })

    return jsonify({
        "voltage": row[0],
        "current": row[1],
        "power": row[2],
        "energy": row[3],
        "prediction": prediction
    })


# ---------- HISTORY ----------
@app.route("/api/history")
def history():
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

    data = []
    for row in rows:
        data.append({
            "voltage": row[0],
            "current": row[1],
            "power": row[2],
            "energy": row[3],
            "time": str(row[4])
        })

    return jsonify(data)


# ---------- START ----------
if __name__ == "__main__":
    print("Server starting...")

    # OPTIONAL (disable if issues on Render)
    mqtt_thread = threading.Thread(target=run_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()