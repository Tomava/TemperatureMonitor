import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "data"

WEATHER_API = os.getenv('WEATHER_API')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')
HOSTNAME = os.getenv('HOSTNAME')
MQTT_PORT = int(os.getenv('MQTT_PORT'))
TOPIC = os.getenv('TOPIC')
QOS = 1
