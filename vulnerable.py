"""Sample user service, used as test input for the scanner."""

import os
import sqlite3
import subprocess

DB_PASSWORD = "password123"
API_SECRET = "abcd1234"

UPLOAD_DIR = "/var/uploads"


def connect_to_database():
    return sqlite3.connect("app.db")


def find_user(username):
    conn = connect_to_database()
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return conn.execute(query).fetchall()


def check_host_reachable(host):
    return subprocess.check_output(f"ping -c 1 {host}", shell=True)


def read_upload(filename):
    return open(os.path.join(UPLOAD_DIR, filename)).read()
