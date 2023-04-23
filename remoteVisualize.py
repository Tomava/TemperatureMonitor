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

LOCAL_DATA_DIR = "data"
REMOTE_DATA_DIR = "/home/pi/Temperature/data"


def fetch_files():
    print("Fetching files")
    with pysftp.Connection(SFTP_HOSTNAME, username=SFTP_USERNAME, password=SFTP_PASSWORD) as sftp:
        for i, file in enumerate(sftp.listdir(REMOTE_DATA_DIR)):
            sftp.get(f"{REMOTE_DATA_DIR}/{file}", f"{LOCAL_DATA_DIR}{os.sep}{file}")
    print(f'Successfully retrieved {i + 1} files from {REMOTE_DATA_DIR} to {LOCAL_DATA_DIR}')

def read_dataframes():
    df_ins = []
    df_outs = []
    for file in os.listdir(LOCAL_DATA_DIR):
        df = pd.read_csv(f"{LOCAL_DATA_DIR}{os.sep}{file}", sep=";")
        if file.startswith("inside"):
            df_ins.append(df)
        else:
            df_outs.append(df)
    df_in = pd.concat(df_ins)
    df_out = pd.concat(df_outs)
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
    yticks = [i for i in range(int(min(df_out[column_name].min(), df_in[column_name].min())), int(max(df_out[column_name].max(), df_in[column_name].max()) + 2), 1)]
    plt.yticks(yticks, minor=True)
    plt.grid(which='minor', alpha=0.4)


def get_values(column_name, df):
    return df[column_name].min(), df[column_name].max(), round(df[column_name].mean(), 2), df[column_name].iloc[-1]


def add_to_data(data: dict, data_name: str, column_name: str, df: pd.DataFrame):
    min_value, max_value, avg_value, current_value = get_values(column_name, df)
    data[data_name] = {
            'min': min_value,
            'max': max_value,
            'avg': avg_value,
            'current': current_value
    }


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

    data = {}

    add_to_data(data, "temperature_in", "temperature", df_in)
    add_to_data(data, "temperature_out", "temperature", df_out)
    add_to_data(data, "humidity_in", "humidity", df_in)
    add_to_data(data, "humidity_out", "humidity", df_out)
    add_to_data(data, "pressure_in", "pressure", df_in)
    add_to_data(data, "pressure_out", "pressure", df_out)

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
