import os
import socket
from datetime import datetime

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "infra_demo")
DB_USER = os.getenv("DB_USER", "demo")
DB_PASSWORD = os.getenv("DB_PASSWORD", "demo123")
APP_PORT = int(os.getenv("APP_PORT", "5000"))


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS visit_log (
            id SERIAL PRIMARY KEY,
            visited_at TIMESTAMP NOT NULL DEFAULT NOW(),
            hostname VARCHAR(255) NOT NULL,
            path VARCHAR(255) NOT NULL
        );
        """
    )
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    hostname = socket.gethostname()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO visit_log (hostname, path) VALUES (%s, %s) RETURNING id, visited_at;",
        (hostname, "/"),
    )
    inserted_id, visited_at = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(
        {
            "message": "Hello, MiTAC Infra Team",
            "hostname": hostname,
            "visit_id": inserted_id,
            "visited_at": visited_at.isoformat(),
            "app_time": datetime.utcnow().isoformat() + "Z",
        }
    )


@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        db_status = "ok"
    except Exception as exc:
        return jsonify({"status": "degraded", "database": "down", "error": str(exc)}), 500

    return jsonify({"status": "ok", "database": db_status})


@app.route("/visits")
def visits():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, visited_at, hostname, path FROM visit_log ORDER BY id DESC LIMIT 10;"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = [
        {
            "id": row[0],
            "visited_at": row[1].isoformat(),
            "hostname": row[2],
            "path": row[3],
        }
        for row in rows
    ]
    return jsonify(data)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=APP_PORT)
