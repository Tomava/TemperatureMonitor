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
MQTT_HOSTNAME = os.getenv('MQTT_HOSTNAME')
MQTT_PORT = int(os.getenv('MQTT_PORT'))
TOPIC = os.getenv('TOPIC')
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")
INSIDE_TABLE = "inside"
OUTSIDE_TABLE = "outside"