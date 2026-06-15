import json
import random
import time
import os
import logging
from datetime import datetime, timezone
from kafka import KafkaProducer
from dotenv import load_dotenv
from config import MACHINES, SENSOR_RANGES, EMIT_INTERVAL_SECONDS

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9093")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_data")


def build_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",
        retries=5,
        retry_backoff_ms=500,
    )


def generate_reading(metric: str) -> float:
    config = SENSOR_RANGES[metric]
    if random.random() < config["spike_probability"]:
        value = random.uniform(config["normal_max"], config["max"])
    else:
        value = random.uniform(config["normal_min"], config["normal_max"])
    return round(value, 4)


def build_event(machine_id: str) -> dict:
    return {
        "machine_id": machine_id,
        "temperature": generate_reading("temperature"),
        "rpm": generate_reading("rpm"),
        "vibration": generate_reading("vibration"),
        "pressure": generate_reading("pressure"),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }


def on_success(metadata):
    logger.info(
        "Event delivered to topic=%s partition=%d offset=%d",
        metadata.topic,
        metadata.partition,
        metadata.offset,
    )


def on_error(error):
    logger.error("Failed to deliver event: %s", error)


def run():
    logger.info("Starting sensor simulator. Broker=%s Topic=%s", KAFKA_BROKER, KAFKA_TOPIC)
    producer = build_producer()

    try:
        while True:
            for machine_id in MACHINES:
                event = build_event(machine_id)
                producer.send(KAFKA_TOPIC, value=event).add_callback(on_success).add_errback(on_error)
                logger.info("Emitted | machine=%s temp=%.2f rpm=%.2f vib=%.4f pres=%.2f",
                    event["machine_id"],
                    event["temperature"],
                    event["rpm"],
                    event["vibration"],
                    event["pressure"],
                )
            producer.flush()
            time.sleep(EMIT_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logger.info("Simulator stopped by user.")
    finally:
        producer.close()
        logger.info("Kafka producer closed.")


if __name__ == "__main__":
    run()