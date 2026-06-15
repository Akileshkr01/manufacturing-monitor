import json
import os
import logging
from datetime import datetime, timezone
from kafka import KafkaConsumer
from dotenv import load_dotenv
from db import get_connection, insert_sensor_reading, insert_alert
from config import ALERT_THRESHOLDS, CONSUMER_GROUP_ID, AUTO_OFFSET_RESET

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9093")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_data")


def build_consumer():
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id=CONSUMER_GROUP_ID,
        auto_offset_reset=AUTO_OFFSET_RESET,
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )


def evaluate_alerts(event: dict) -> list:
    alerts = []
    triggered_at = event.get("recorded_at", datetime.now(timezone.utc).isoformat())

    for metric, levels in ALERT_THRESHOLDS.items():
        value = event.get(metric)
        if value is None:
            continue

        if value >= levels["critical"]:
            severity = "CRITICAL"
            threshold = levels["critical"]
        elif value >= levels["warning"]:
            severity = "WARNING"
            threshold = levels["warning"]
        else:
            continue

        alert_type = "High {} Alert".format(metric.capitalize())
        if metric == "rpm":
            alert_type = "High RPM Alert"
        elif metric == "vibration":
            alert_type = "High Vibration Alert"

        alerts.append({
            "machine_id": event["machine_id"],
            "alert_type": alert_type,
            "metric": metric,
            "value": value,
            "threshold": threshold,
            "severity": severity,
            "triggered_at": triggered_at,
        })

    return alerts


def process_event(conn, event: dict):
    insert_sensor_reading(conn, event)
    logger.info(
        "Stored | machine=%s temp=%.2f rpm=%.2f vib=%.4f pres=%.2f",
        event["machine_id"],
        event["temperature"],
        event["rpm"],
        event["vibration"],
        event["pressure"],
    )

    alerts = evaluate_alerts(event)
    for alert in alerts:
        insert_alert(conn, alert)
        logger.warning(
            "Alert | severity=%s machine=%s metric=%s value=%.4f threshold=%.4f",
            alert["severity"],
            alert["machine_id"],
            alert["metric"],
            alert["value"],
            alert["threshold"],
        )


def run():
    logger.info("Starting consumer. Broker=%s Topic=%s Group=%s", KAFKA_BROKER, KAFKA_TOPIC, CONSUMER_GROUP_ID)
    consumer = build_consumer()
    conn = get_connection()
    logger.info("PostgreSQL connection established.")

    try:
        for message in consumer:
            event = message.value
            process_event(conn, event)
    except KeyboardInterrupt:
        logger.info("Consumer stopped by user.")
    finally:
        consumer.close()
        conn.close()
        logger.info("Consumer and database connection closed.")


if __name__ == "__main__":
    run()