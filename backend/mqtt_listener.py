import paho.mqtt.client as mqtt
import json
from backend.database import insert_data

MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "smartgrid/node1/data"


def on_connect(client, userdata, flags, rc):
    print("MQTT Connected:", rc)
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        insert_data(
            data.get("voltage", 0),
            data.get("current", 0),
            data.get("power", 0),
            data.get("energy", 0)
        )

    except Exception as e:
        print("MQTT Error:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


def start_mqtt():
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()