import os
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
import pandas as pd
import waitress
from config import ADMIN_USER, ADMIN_PASS, DATA_DIR, ENVIRONMENT, SECRET_KEY

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config["SECRET_KEY"] = SECRET_KEY

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


def get_data(start_time, end_time):
    df_in, df_out = read_dataframes()
    df_in = df_in.dropna()
    df_out = df_out.dropna()

    common_column = "time"

    # Convert 'time' column to timestamps
    df_in[common_column] = pd.to_datetime(df_in[common_column])
    df_out[common_column] = pd.to_datetime(df_out[common_column])

    merged_df = pd.merge(df_in, df_out, on=common_column, suffixes=("_in", "_out"))

    if start_time is not None:
        merged_df = merged_df[merged_df[common_column] >= pd.to_datetime(start_time)]
    if end_time is not None:
        merged_df = merged_df[merged_df[common_column] <= pd.to_datetime(end_time)]

    result_dict = {}
    for _, row in merged_df.iterrows():
        time: pd.Timestamp = row[common_column]
        result_dict[str(time)] = {
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
    start_time_str = request.args.get("start_time")
    end_time_str = request.args.get("end_time")
    start_time = pd.to_datetime(start_time_str) if start_time_str else None
    end_time = pd.to_datetime(end_time_str) if end_time_str else None
    data = get_data(start_time, end_time)
    return data


if __name__ == "__main__":
    if ENVIRONMENT == "prod":
        waitress.serve(app, host="0.0.0.0", port=8080)
    else:
        app.run(debug=True)
