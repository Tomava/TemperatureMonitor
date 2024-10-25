import smbus2
import bme280
import csv
import os
import urllib.request
import json
import datetime
from config import WEATHER_API, DATA_DIR, LATITUDE, LONGITUDE

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
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&exclude=minutely,hourly,daily,alerts&appid={WEATHER_API}&units=metric"
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
        main_data = data.get("main")
        data_time = data.get("dt")
        temperature = main_data.get("temp")
        feels_like = main_data.get("feels_like")
        pressure = main_data.get("pressure")
        humidity = main_data.get("humidity")
        clouds = data.get("clouds").get("all")
        weather = main_data.get("weather")[0].get("description")
        fetched_data.extend([data_time, temperature, pressure, humidity, feels_like, None, None, clouds, None, None, weather])
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

def main():
    sensor_data = read_sensor()
    api_data = read_api_weather_data()
    now = datetime.datetime.now()
    in_headers = ["time", "data_time", "temperature", "pressure", "humidity"]
    out_headers = ["time", "data_time", "temperature", "pressure", "humidity", "feels_like", "dew_point", "uv_index", "clouds", "wind_speed", "wind_deg", "weather"]
    write_csv(f"inside_{now.strftime('%Y-%m')}.csv", [now.isoformat()] + sensor_data, in_headers)
    write_csv(f"outside_{now.strftime('%Y-%m')}.csv", [now.isoformat()] + api_data, out_headers)

if __name__ == "__main__":
    main()
