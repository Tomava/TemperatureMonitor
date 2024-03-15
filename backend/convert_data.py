import csv
import json
import os
import shutil
from config import WEATHER_API, DATA_DIR, LATITUDE, LONGITUDE



def handle_inside(file):
    # Create a temporary file to store modified data
    file_path = os.path.join(DATA_DIR, file)

    temp_file_path = file_path + '.temp'

    with open(file_path, 'r') as infile, open(temp_file_path, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = ['time', 'data_time', 'temperature', 'pressure', 'humidity']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for row in reader:
            del row['raw_data']

            writer.writerow(row)

    # Replace the original file with the temporary file
    shutil.move(temp_file_path, file_path)


def handle_outside(file):
    # Create a temporary file to store modified data
    file_path = os.path.join(DATA_DIR, file)

    temp_file_path = file_path + '.temp'

    with open(file_path, 'r') as infile, open(temp_file_path, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = ['time', 'data_time', 'temperature', 'pressure', 'humidity', 'feels_like', 'dew_point', 'uv_index', 'clouds', 'wind_speed', 'wind_deg', 'weather']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for row in reader:
            if row['raw_data'] is not None:
                raw_data = json.loads(row['raw_data'].replace("'", "\""))

                # Extracting relevant information from raw_data
                row['feels_like'] = raw_data['feels_like']
                row['dew_point'] = raw_data['dew_point']
                row['uv_index'] = raw_data.get('uvi', None)
                row['clouds'] = raw_data['clouds']
                row['wind_speed'] = raw_data['wind_speed']
                row['wind_deg'] = raw_data['wind_deg']
                row['weather'] = raw_data['weather'][0]['description']
            del row['raw_data']

            # Writing the modified row to the output file
            writer.writerow(row)

    # Replace the original file with the temporary file
    shutil.move(temp_file_path, file_path)


def main():
    for file in os.listdir(DATA_DIR):
        if file.startswith("inside"):
            handle_inside(file)
        else:
            handle_outside(file)

if __name__ == "__main__":
    main()
