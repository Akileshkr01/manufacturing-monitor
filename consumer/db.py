import os
import logging
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        dbname=os.getenv("POSTGRES_DB", "manufacturing"),
        user=os.getenv("POSTGRES_USER", "mfg_user"),
        password=os.getenv("POSTGRES_PASSWORD", "mfg_pass"),
    )


def insert_sensor_reading(conn, event: dict):
    sql = """
        INSERT INTO sensor_readings (machine_id, temperature, rpm, vibration, pressure, recorded_at)
        VALUES (%(machine_id)s, %(temperature)s, %(rpm)s, %(vibration)s, %(pressure)s, %(recorded_at)s)
    """
    with conn.cursor() as cur:
        cur.execute(sql, event)
    conn.commit()


def insert_alert(conn, alert: dict):
    sql = """
        INSERT INTO alerts (machine_id, alert_type, metric, value, threshold, severity, triggered_at)
        VALUES (%(machine_id)s, %(alert_type)s, %(metric)s, %(value)s, %(threshold)s, %(severity)s, %(triggered_at)s)
    """
    with conn.cursor() as cur:
        cur.execute(sql, alert)
    conn.commit()