import datetime
import psycopg2
from config import *


def dev_log(message):
    if ENVIRONMENT == "dev":
        print(
            f"{datetime.datetime.now().replace(microsecond=0).isoformat()}: {message}"
        )


def execute_database_query(database_name, statement, args, fetch=False, fetch_all=False):
    dev_log(statement)
    con = psycopg2.connect(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        host=DB_HOST,
        password=POSTGRES_PASSWORD,
        port=DB_PORT,
    )
    cur = con.cursor()
    cur.execute(statement, args)
    res = None
    if fetch_all:
        res = cur.fetchall()
    elif fetch:
        res = cur.fetchone()
    con.commit()
    cur.close()
    con.close()
    return res
