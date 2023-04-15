import pandas as pd
import matplotlib.pyplot as plt
import os

DIR_PATH = "data"
FILE1 = f"{DIR_PATH}{os.sep}sensor.csv"
FILE2 = f"{DIR_PATH}{os.sep}outside.csv"

def read_dataframes():
    # Load data from CSV files
    df1 = pd.read_csv(FILE1, sep=";")
    df2 = pd.read_csv(FILE2, sep=";")
    return df1, df2


def create_plot(column_name, column_title, df1, df2):
    # Plot temperature data
    fig, plot = plt.subplots(num=column_title)
    plot.plot(df1[column_name], label='Inside')
    plot.plot(df2[column_name], label='Outside')
    plot.set_xlabel('Datetime')
    plot.set_ylabel(column_title)
    plot.set_title(column_title)
    plot.legend()
    plot.grid(True)
    fig.set_size_inches(12, 7)


def main():
    df1, df2 = read_dataframes()
    # Convert 'time' column to datetime data type
    df1['time'] = pd.to_datetime(df1['time'])
    df2['time'] = pd.to_datetime(df2['time'])

    # Set 'time' column as the index for both dataframes
    df1.set_index('time', inplace=True)
    df2.set_index('time', inplace=True)
    
    create_plot("temperature", "Temperature", df1, df2)
    create_plot("humidity", "Humidity", df1, df2)
    create_plot("pressure", "Pressure", df1, df2)

    plt.show()


if __name__ == "__main__":
    main()
