ALERT_THRESHOLDS = {
    "temperature": {
        "warning": 85.0,
        "critical": 95.0,
    },
    "rpm": {
        "warning": 2800.0,
        "critical": 3200.0,
    },
    "vibration": {
        "warning": 1.0,
        "critical": 1.8,
    },
    "pressure": {
        "warning": 90.0,
        "critical": 110.0,
    },
}

CONSUMER_GROUP_ID = "manufacturing-consumer-group"
AUTO_OFFSET_RESET = "earliest"