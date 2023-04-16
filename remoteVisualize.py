from flask import Flask, render_template, request
from waitress import serve
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime, timedelta
import os

DIR_PATH = "data"
FILE1 = f"{DIR_PATH}{os.sep}sensor.csv"
FILE2 = f"{DIR_PATH}{os.sep}outside.csv"

def read_dataframes():
    # Load data from CSV files
    df1 = pd.read_csv(FILE1, sep=";")
    df2 = pd.read_csv(FILE2, sep=";")
    return df1, df2


def create_plot(column_name, column_title, df1, df2, index):
    # Plot temperature data
    plt.subplot(3, 1, index)
    plt.plot(df1[column_name], label='Inside')
    plt.plot(df2[column_name], label='Outside')
    plt.xlabel('Datetime')
    plt.ylabel(column_title)
    plt.title(column_title)
    plt.legend()
    plt.grid(True)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def visualize_data():
    if request.method == 'POST':
        # Get selected time range from the form
        time_range = request.form['time_range']

        df1, df2 = read_dataframes()
        # Convert 'time' column to datetime data type
        df1['time'] = pd.to_datetime(df1['time'])
        df2['time'] = pd.to_datetime(df2['time'])

        # Set 'time' column as the index for both dataframes
        df1.set_index('time', inplace=True)
        df2.set_index('time', inplace=True)

        # Get current datetime for calculating time ranges
        now = datetime.now()

        # Define time delta for different time ranges
        if time_range == '24h':
            start_date = now - timedelta(hours=24)
        elif time_range == '3d':
            start_date = now - timedelta(days=3)
        elif time_range == '7d':
            start_date = now - timedelta(days=7)
        elif time_range == '31d':
            start_date = now - timedelta(days=31)
        elif time_range == '1y':
            start_date = now - timedelta(days=365)
        elif time_range == '3y':
            start_date = now - timedelta(days=3*365)
        elif time_range == 'all':
            start_date = df1.index.min()

        end_date = now

        # Filter data based on selected time range
        df1 = df1.loc[start_date:end_date]
        df2 = df2.loc[start_date:end_date]


        plt.figure(figsize=(12, 12))

        create_plot("temperature", "Temperature", df1, df2, 1)
        create_plot("humidity", "Humidity", df1, df2, 2)
        create_plot("pressure", "Pressure", df1, df2, 3)

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
        return render_template('index.html', plot_data=plot_data)

    else:
        return render_template('index.html')

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=50100)