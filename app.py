
import os
import time

import mysql.connector
from flask import Flask
from mysql.connector import Error

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.environ["DB_PASSWORD"],
        database=os.getenv("DB_NAME", "praktikum"),
        connection_timeout=5,
    )


@app.route("/")
def home():
    return "Halo! Aplikasi Flask + Docker + Jenkins berhasil berjalan!"


@app.route("/db")
def check_database():
    for attempt in range(5):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            database = cursor.fetchone()[0]
            cursor.close()
            connection.close()

            return f"Koneksi database berhasil! Database: {database}", 200

        except (Error, KeyError) as error:
            if attempt == 4:
                return f"Koneksi database gagal: {error}", 500
            time.sleep(2)

    return "Database tidak tersedia", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
