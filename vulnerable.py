"""Deliberately insecure sample code. Used as a test fixture for the scanner."""

import os
import sqlite3
import subprocess

DB_PASSWORD = "password123"
API_SECRET = "sk-live-abcd1234"


def connect_to_database():
    return f"Connecting with password: {DB_PASSWORD}"


def find_user(username):
    conn = sqlite3.connect("app.db")
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return conn.execute(query).fetchall()


def ping_host(host):
    return subprocess.check_output(f"ping -c 1 {host}", shell=True)


def read_upload(filename):
    return open(os.path.join("/var/uploads", filename)).read()
