import os
import threading
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
import pandas as pd
import waitress
import mqtt_client
from config import *

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config["SECRET_KEY"] = SECRET_KEY

@auth.verify_password
def verify_password(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return username


def get_data(start_time, end_time):
    result_dict = {}
    # TODO: Read from database
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
    threading.Thread(target=mqtt_client.init_client).start()
    if ENVIRONMENT == "prod":
        waitress.serve(app, host="0.0.0.0", port=8080)
    else:
        app.run(debug=True)
