MACHINES = [
    "MACHINE_001",
    "MACHINE_002",
    "MACHINE_003",
    "MACHINE_004",
    "MACHINE_005",
]

SENSOR_RANGES = {
    "temperature": {
        "min": 60.0,
        "max": 110.0,
        "normal_min": 60.0,
        "normal_max": 85.0,
        "spike_probability": 0.05,
    },
    "rpm": {
        "min": 800.0,
        "max": 3600.0,
        "normal_min": 1200.0,
        "normal_max": 3000.0,
        "spike_probability": 0.04,
    },
    "vibration": {
        "min": 0.1,
        "max": 2.5,
        "normal_min": 0.1,
        "normal_max": 1.2,
        "spike_probability": 0.06,
    },
    "pressure": {
        "min": 30.0,
        "max": 130.0,
        "normal_min": 30.0,
        "normal_max": 100.0,
        "spike_probability": 0.04,
    },
}

EMIT_INTERVAL_SECONDS = 3