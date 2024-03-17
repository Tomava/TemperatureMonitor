import json
import paho.mqtt.client as mqtt
import psycopg2
from config import *
from helpers import execute_database_query, dev_log


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    dev_log(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(f"{TOPIC}/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload
    dev_log(f"MQTT: {topic} {payload}")
    data = json.loads(payload)
    timedate = data.get("time")
    data_time = data.get("data_time")
    temperature = data.get("temperature")
    pressure = data.get("pressure")
    humidity = data.get("humidity")
    if topic == f"{TOPIC}/in":
        insert_statement = f"INSERT INTO {INSIDE_TABLE} (timedate, data_time, temperature, pressure, humidity) VALUES (%s, %s, %s, %s, %s);"
        try:
            execute_database_query(
                POSTGRES_DB,
                insert_statement,
                (
                    timedate,
                    data_time,
                    temperature,
                    pressure,
                    humidity,
                )
            )
        except psycopg2.Error as e:
            dev_log(e)
    elif topic == f"{TOPIC}/out":
        feels_like = data.get("feels_like")
        dew_point = data.get("dew_point")
        uv_index = data.get("uv_index")
        clouds = data.get("clouds")
        wind_speed = data.get("wind_speed")
        wind_deg = data.get("wind_deg")
        weather = data.get("weather")
        insert_statement = f"INSERT INTO {OUTSIDE_TABLE} (timedate, data_time, temperature, pressure, humidity, feels_like, dew_point, uv_index, clouds, wind_speed, wind_deg, weather) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        try:
            execute_database_query(
                POSTGRES_DB,
                insert_statement,
                (
                    timedate,
                    data_time,
                    temperature,
                    pressure,
                    humidity,
                    feels_like,
                    dew_point,
                    uv_index,
                    clouds,
                    wind_speed,
                    wind_deg,
                    weather,
                )
            )
        except psycopg2.Error as e:
            dev_log(e)


def init_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    # Keepalive 60 seconds
    dev_log(f"{MQTT_HOSTNAME}, {MQTT_PORT}")
    # TODO: Loop here until connected??
    client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)
    
    client.loop_forever(retry_first_connection=True)
