import time, random, json
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    payload = {
        "device_id": "EV_BIKE_01",
        "battery": random.randint(50, 100),
        "speed": random.randint(20, 80)
    }
    client.publish("telematics/EV_BIKE_01", json.dumps(payload))
    print(f"Sent: {payload}")
    time.sleep(1)
