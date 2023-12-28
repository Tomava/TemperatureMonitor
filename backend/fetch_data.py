import smbus2
import bme280
import csv
import os
import urllib.request
import json
import datetime
from config import WEATHER_API

LATITUDE = 61.45
LONGITUDE = 23.85

def read_sensor():
    port = 1
    address = 0x77
    bus = smbus2.SMBus(port)

    calibration_params = bme280.load_calibration_params(bus, address)

    # the sample method will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)

    data_time = data.timestamp.timestamp()
    temperature = round(data.temperature, 2)
    pressure = round(data.pressure, 2)
    humidity = round(data.humidity, 2)

    # there is a handy string representation too
    #print(data)

    return [data_time, temperature, pressure, humidity, data]

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
        temperature = round(current_data.get("temp"), 2)
        pressure = round(current_data.get("pressure"), 2)
        humidity = round(current_data.get("humidity"), 2)
        fetched_data.extend([data_time, temperature, pressure, humidity, current_data])
    return fetched_data

def write_csv(filename, data):
    filepath = f"data/{filename}"
    headers = ["time", "data_time", "temperature", "pressure", "humidity", "raw_data"]
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

def main():
    sensor_data = read_sensor()
    api_data = read_api_weather_data()
    now = datetime.datetime.now()
    write_csv(f"inside_{now.strftime('%Y-%m')}.csv", [now.isoformat()] + sensor_data)
    write_csv(f"outside_{now.strftime('%Y-%m')}.csv", [now.isoformat()] + api_data)

if __name__ == "__main__":
    main()
