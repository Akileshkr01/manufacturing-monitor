import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        dbname=os.getenv("POSTGRES_DB", "manufacturing"),
        user=os.getenv("POSTGRES_USER", "mfg_user"),
        password=os.getenv("POSTGRES_PASSWORD", "mfg_pass"),
    )


def fetch_all(query: str, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    finally:
        conn.close()


def fetch_one(query: str, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchone()
    finally:
        conn.close()