from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_latest, get_connection, insert_data
from ai_model import predict_power
import threading
import mqtt_listener
import os
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def run_mqtt():
    print("Starting MQTT...")
    time.sleep(2)
    mqtt_listener.start_mqtt()


@app.route("/")
def home():
    return "Smart Grid Backend Running"


@app.route("/api/insert", methods=["POST"])
def insert_api():
    data = request.json

    insert_data(
        data.get("voltage", 0),
        data.get("current", 0),
        data.get("power", 0),
        data.get("energy", 0)
    )

    return jsonify({"status": "success"})


@app.route("/api/data")
def api_data():
    row = get_latest()
    prediction = predict_power()

    if not row:
        return jsonify({
            "status": "no data"
        })

    return jsonify({
        "voltage": row[0],
        "current": row[1],
        "power": row[2],
        "energy": row[3],
        "prediction": prediction
    })


@app.route("/api/history")
def history():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT voltage,current,power,energy,timestamp
        FROM energy ORDER BY id DESC LIMIT 100
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


if __name__ == "__main__":
    thread = threading.Thread(target=run_mqtt)
    thread.daemon = True
    thread.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)