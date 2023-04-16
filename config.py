import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API = os.getenv('WEATHER_API')
SFTP_PASSWORD = os.getenv('SFTP_PASSWORD')
SFTP_USERNAME = os.getenv('SFTP_USERNAME')
SFTP_HOSTNAME = os.getenv('SFTP_HOSTNAME')
