import csv
import os
import urllib.request
import json
import datetime
import smbus2
import bme280
import paho.mqtt.client as mqtt
from config import *

def read_sensor():
    port = 1
    address = 0x77
    bus = smbus2.SMBus(port)

    calibration_params = bme280.load_calibration_params(bus, address)

    # the sample method will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)

    data_time = data.timestamp.timestamp()
    temperature = data.temperature
    pressure = data.pressure
    humidity = data.humidity

    return [data_time, temperature, pressure, humidity]

def fetch_api_weather_data():
    """
    Fetches the weather data and returns it as a dict
    :return: dict
    """
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&exclude=minutely,hourly,daily,alerts&appid={WEATHER_API}&units=metric"
    try:
        with urllib.request.urlopen(url) as site:
            data = json.loads(site.read())
    except:
        return None
    return data

def read_api_weather_data():
    data = fetch_api_weather_data()
    fetched_data = []
    if data is not None:
        current_data = data.get("current")
        data_time = current_data.get("dt")
        temperature = current_data.get("temp")
        feels_like = current_data.get("feels_like")
        pressure = current_data.get("pressure")
        humidity = current_data.get("humidity")
        dew_point = current_data.get("dew_point")
        uv_index = current_data.get("uvi")
        clouds = current_data.get("clouds")
        wind_speed = current_data.get("wind_speed")
        wind_deg = current_data.get("wind_deg")
        weather = current_data.get("weather")[0].get("description")
        fetched_data.extend([data_time, temperature, pressure, humidity, feels_like, dew_point, uv_index, clouds, wind_speed, wind_deg, weather])
    return fetched_data

def write_csv(filename, data, headers):
    filepath = os.path.join(DATA_DIR, filename)

    # Create file only once
    if not os.path.isfile(filepath):
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(headers)
    stringified_data = []
    for row in data:
        stringified_data.append(str(row))
    with open(filepath, "a+", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        print(stringified_data)
        writer.writerows([stringified_data])

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    return


def main():
    sensor_data = read_sensor()
    api_data = read_api_weather_data()
    now = datetime.datetime.now()

    in_headers = ["time", "data_time", "temperature", "pressure", "humidity"]
    out_headers = ["time", "data_time", "temperature", "pressure", "humidity", "feels_like", "dew_point", "uv_index", "clouds", "wind_speed", "wind_deg", "weather"]
    in_data = [now.isoformat()] + sensor_data
    out_data = [now.isoformat()] + api_data

    write_csv(f"inside_{now.strftime('%Y-%m')}.csv", in_data, in_headers)
    write_csv(f"outside_{now.strftime('%Y-%m')}.csv", out_data, out_headers)

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # Keepalive 60 seconds
    mqtt_client.connect(HOSTNAME, MQTT_PORT, 60)

    mqtt_client.publish(f"{TOPIC}/in", json.dumps(in_data), qos=QOS)
    mqtt_client.publish(f"{TOPIC}/out", json.dumps(out_data), qos=QOS)


if __name__ == "__main__":
    main()
