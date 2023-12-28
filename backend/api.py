from flask import Flask
from flask_httpauth import HTTPBasicAuth
import os
import pandas as pd
from config import ADMIN_USER, ADMIN_PASS, DATA_DIR

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return username


def read_dataframes():
    df_ins = []
    df_outs = []
    for file in os.listdir(DATA_DIR):
        df = pd.read_csv(os.path.join(DATA_DIR, file), sep=";")
        if file.startswith("inside"):
            df_ins.append(df)
        else:
            df_outs.append(df)
    df_in = pd.concat(df_ins)
    df_out = pd.concat(df_outs)
    return df_in, df_out


def get_data():
    df_in, df_out = read_dataframes()
    df_in = df_in.dropna()
    df_out = df_out.dropna()

    common_column = "time"

    # Convert 'time' column to timestamps
    df_in[common_column] = pd.to_datetime(df_in[common_column])
    df_out[common_column] = pd.to_datetime(df_out[common_column])

    merged_df = pd.merge(df_in, df_out, on=common_column, suffixes=("_in", "_out"))

    result_dict = {}
    for _, row in merged_df.iterrows():
        time: pd.Timestamp = row[common_column]
        result_dict[str(time.timestamp())] = {
            "in": {
                "humidity": row["humidity_in"],
                "pressure": row["pressure_in"],
                "temperature": row["temperature_in"],
            },
            "out": {
                "humidity": row["humidity_out"],
                "pressure": row["pressure_out"],
                "temperature": row["temperature_out"],
            },
        }
    return result_dict


@app.get("/temperature")
@auth.login_required
def temperature_get():
    data = get_data()
    return data


if __name__ == "__main__":
    app.run(debug=True)
