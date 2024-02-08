import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "data"

WEATHER_API = os.getenv('WEATHER_API')
ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASS = os.getenv('ADMIN_PASS')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')