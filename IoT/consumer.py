# consumer.py
import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "BFR0ZXwcAX4QIJk6uFEAGrP2Q4bm8HXfp3Jh4QLjTaE247YVab_UbP_Q1IUSx_ld9Kw-2qA6Jiq3Ry-P9VSuaA=="
INFLUX_ORG = "myorg"
INFLUX_BUCKET = "iot_data"

client_db = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client_db.write_api(write_options=SYNCHRONOUS)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        
        # InfluxDB Data Point
        point = Point("telemetry") \
            .tag("device_id", data.get("device_id", "EV_BIKE_01")) \
            .field("battery", float(data.get("battery", 0))) \
            .field("speed", float(data.get("speed", 0)))
        
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print(f"Stored in InfluxDB: {data}")
    except Exception as e:
        print(f"Error processing message: {e}")

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.subscribe("#")

print("Consumer started... Listening for MQTT data")
mqtt_client.loop_forever()
