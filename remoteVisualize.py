from flask import Flask, render_template, request
from waitress import serve
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pysftp
import os
import webbrowser
from config import SFTP_HOSTNAME, SFTP_USERNAME, SFTP_PASSWORD

DIR_PATH = "data"
FILE1_LOCAL_PATH = f"{DIR_PATH}{os.sep}sensor.csv"
FILE2_LOCAL_PATH = f"{DIR_PATH}{os.sep}outside.csv"
FILE1_REMOTE_PATH = "/home/pi/Temperature/data/sensor.csv"
FILE2_REMOTE_PATH = "/home/pi/Temperature/data/outside.csv"


def fetch_files():
    with pysftp.Connection(SFTP_HOSTNAME, username=SFTP_USERNAME, password=SFTP_PASSWORD) as sftp:
        sftp.get(FILE1_REMOTE_PATH, FILE1_LOCAL_PATH)
        sftp.get(FILE2_REMOTE_PATH, FILE2_LOCAL_PATH)


def read_dataframes():
    # Load data from CSV files
    df_in = pd.read_csv(FILE1_LOCAL_PATH, sep=";")
    df_out = pd.read_csv(FILE2_LOCAL_PATH, sep=";")
    return df_in, df_out


def create_plot(column_name, column_title, df_in, df_out, index):
    # Plot temperature data
    plt.subplot(3, 1, index)
    plt.plot(df_in[column_name], label='Inside')
    plt.plot(df_out[column_name], label='Outside')
    plt.xlabel('Datetime')
    plt.ylabel(column_title)
    plt.title(column_title)
    plt.legend()
    plt.grid(True)


def get_values(column_name, df):
    return df[column_name].max(), df[column_name].min(), round(df[column_name].mean(), 2)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def visualize_data():
    if request.method == 'POST':
        time_range = request.form['time_range']
    else:
        time_range = '24h'

    df_in, df_out = read_dataframes()
    # Convert 'time' column to datetime data type
    df_in['time'] = pd.to_datetime(df_in['time'])
    df_out['time'] = pd.to_datetime(df_out['time'])

    # Set 'time' column as the index for both dataframes
    df_in.set_index('time', inplace=True)
    df_out.set_index('time', inplace=True)

    # Get current datetime for calculating time ranges
    now = datetime.now()

    # Define time delta for different time ranges
    if time_range == '24h':
        start_date = now - relativedelta(hours=24)
    elif time_range == '3d':
        start_date = now - relativedelta(days=3)
    elif time_range == '7d':
        start_date = now - relativedelta(days=7)
    elif time_range == '31d':
        start_date = now - relativedelta(days=31)
    elif time_range == '3M':
        start_date = now - relativedelta(months=3)
    elif time_range == '1y':
        start_date = now - relativedelta(years=1)
    elif time_range == '3y':
        start_date = now - relativedelta(years=3)
    elif time_range == 'all':
        start_date = df_in.index.min()

    end_date = now

    # Filter data based on selected time range
    df_in = df_in.loc[start_date:end_date]
    df_out = df_out.loc[start_date:end_date]


    plt.figure(figsize=(12, 12))

    create_plot("temperature", "Temperature", df_in, df_out, 1)
    create_plot("humidity", "Humidity", df_in, df_out, 2)
    create_plot("pressure", "Pressure", df_in, df_out, 3)

    max_temperature_in, min_temperature_in, avg_temperature_in = get_values("temperature", df_in)
    max_temperature_out, min_temperature_out, avg_temperature_out = get_values("temperature", df_out)
    max_humidity_in, min_humidity_in, avg_humidity_in = get_values("humidity", df_in)
    max_humidity_out, min_humidity_out, avg_humidity_out = get_values("humidity", df_out)
    max_pressure_in, min_pressure_in, avg_pressure_in = get_values("pressure", df_in)
    max_pressure_out, min_pressure_out, avg_pressure_out = get_values("pressure", df_out)

    data = {
        'temperature_in': {
            'min': min_temperature_in,
            'max': max_temperature_in,
            'avg': avg_temperature_in
        },
        'temperature_out': {
            'min': min_temperature_out,
            'max': max_temperature_out,
            'avg': avg_temperature_out
        },
        'humidity_in': {
            'min': min_humidity_in,
            'max': max_humidity_in,
            'avg': avg_humidity_in
        },
        'humidity_out': {
            'min': min_humidity_out,
            'max': max_humidity_out,
            'avg': avg_humidity_out
        },
        'pressure_in': {
            'min': min_pressure_in,
            'max': max_pressure_in,
            'avg': avg_pressure_in
        },
        'pressure_out': {
            'min': min_pressure_out,
            'max': max_pressure_out,
            'avg': avg_pressure_out
        }
    }

    # Adjust spacing between subplots
    plt.subplots_adjust(hspace=0.4)

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data= buffer.getvalue()
    buffer.close()
    # Convert the plot data to base64 encoded string
    plot_data = base64.b64encode(plot_data).decode('utf-8')
    return render_template('index.html', plot_data=plot_data, data=data)

if __name__ == "__main__":
    fetch_files()
    webbrowser.open("http://127.0.0.1:50100")
    serve(app, host="127.0.0.1", port=50100)
    #app.run(debug=True)
