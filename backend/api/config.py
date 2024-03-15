import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "data"

WEATHER_API = os.getenv('WEATHER_API')
ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASS = os.getenv('ADMIN_PASS')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')
ENVIRONMENT = os.getenv('ENVIRONMENT')
SECRET_KEY = os.getenv('SECRET_KEY')
HOSTNAME = os.getenv('HOSTNAME')
MQTT_PORT = int(os.getenv('MQTT_PORT'))
TOPIC = os.getenv('TOPIC')
