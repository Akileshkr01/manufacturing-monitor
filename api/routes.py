from fastapi import APIRouter, Query
from typing import List, Optional
from db import fetch_all, fetch_one
from models import SensorReading, Alert, MachineSummary, AlertSummary

router = APIRouter()


@router.get("/readings", response_model=List[dict])
def get_readings(
    machine_id: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
):
    if machine_id:
        sql = """
            SELECT id, machine_id, temperature, rpm, vibration, pressure, recorded_at, ingested_at
            FROM sensor_readings
            WHERE machine_id = %s
            ORDER BY recorded_at DESC
            LIMIT %s
        """
        return fetch_all(sql, (machine_id, limit))
    sql = """
        SELECT id, machine_id, temperature, rpm, vibration, pressure, recorded_at, ingested_at
        FROM sensor_readings
        ORDER BY recorded_at DESC
        LIMIT %s
    """
    return fetch_all(sql, (limit,))


@router.get("/readings/latest", response_model=List[dict])
def get_latest_per_machine():
    sql = """
        SELECT DISTINCT ON (machine_id)
            id, machine_id, temperature, rpm, vibration, pressure, recorded_at, ingested_at
        FROM sensor_readings
        ORDER BY machine_id, recorded_at DESC
    """
    return fetch_all(sql)


@router.get("/readings/{machine_id}/history", response_model=List[dict])
def get_machine_history(
    machine_id: str,
    limit: int = Query(200, ge=1, le=1000),
):
    sql = """
        SELECT id, machine_id, temperature, rpm, vibration, pressure, recorded_at
        FROM sensor_readings
        WHERE machine_id = %s
        ORDER BY recorded_at DESC
        LIMIT %s
    """
    return fetch_all(sql, (machine_id, limit))


@router.get("/alerts", response_model=List[dict])
def get_alerts(
    machine_id: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
):
    conditions = []
    params = []

    if machine_id:
        conditions.append("machine_id = %s")
        params.append(machine_id)
    if severity:
        conditions.append("severity = %s")
        params.append(severity.upper())

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    params.append(limit)

    sql = """
        SELECT id, machine_id, alert_type, metric, value, threshold, severity, triggered_at, created_at
        FROM alerts
        {} 
        ORDER BY triggered_at DESC
        LIMIT %s
    """.format(where_clause)

    return fetch_all(sql, tuple(params))


@router.get("/alerts/summary", response_model=List[dict])
def get_alert_summary():
    sql = """
        SELECT
            machine_id,
            severity,
            metric,
            COUNT(*) AS total_alerts,
            MAX(triggered_at) AS latest_alert
        FROM alerts
        GROUP BY machine_id, severity, metric
        ORDER BY machine_id, severity DESC
    """
    return fetch_all(sql)


@router.get("/machines/summary", response_model=List[dict])
def get_machine_summary():
    sql = """
        SELECT
            machine_id,
            ROUND(AVG(temperature)::numeric, 2) AS avg_temperature,
            ROUND(AVG(rpm)::numeric, 2) AS avg_rpm,
            ROUND(AVG(vibration)::numeric, 4) AS avg_vibration,
            ROUND(AVG(pressure)::numeric, 2) AS avg_pressure,
            ROUND(MAX(temperature)::numeric, 2) AS max_temperature,
            ROUND(MAX(rpm)::numeric, 2) AS max_rpm,
            ROUND(MAX(vibration)::numeric, 4) AS max_vibration,
            ROUND(MAX(pressure)::numeric, 2) AS max_pressure,
            COUNT(*) AS total_readings,
            MAX(recorded_at) AS last_seen
        FROM sensor_readings
        GROUP BY machine_id
        ORDER BY machine_id
    """
    return fetch_all(sql)


@router.get("/machines/{machine_id}/summary", response_model=dict)
def get_single_machine_summary(machine_id: str):
    sql = """
        SELECT
            machine_id,
            ROUND(AVG(temperature)::numeric, 2) AS avg_temperature,
            ROUND(AVG(rpm)::numeric, 2) AS avg_rpm,
            ROUND(AVG(vibration)::numeric, 4) AS avg_vibration,
            ROUND(AVG(pressure)::numeric, 2) AS avg_pressure,
            ROUND(MAX(temperature)::numeric, 2) AS max_temperature,
            ROUND(MAX(rpm)::numeric, 2) AS max_rpm,
            ROUND(MAX(vibration)::numeric, 4) AS max_vibration,
            ROUND(MAX(pressure)::numeric, 2) AS max_pressure,
            COUNT(*) AS total_readings,
            MAX(recorded_at) AS last_seen
        FROM sensor_readings
        WHERE machine_id = %s
        GROUP BY machine_id
    """
    return fetch_one(sql, (machine_id,))


@router.get("/metrics/trend", response_model=List[dict])
def get_metric_trend(
    machine_id: Optional[str] = Query(None),
    metric: str = Query("temperature"),
    interval: str = Query("5 minutes"),
):
    valid_metrics = {"temperature", "rpm", "vibration", "pressure"}
    if metric not in valid_metrics:
        metric = "temperature"

    if machine_id:
        sql = """
            SELECT
                date_trunc('minute', recorded_at) AS time_bucket,
                machine_id,
                ROUND(AVG({})::numeric, 4) AS avg_value,
                ROUND(MAX({})::numeric, 4) AS max_value,
                ROUND(MIN({})::numeric, 4) AS min_value
            FROM sensor_readings
            WHERE machine_id = %s
            AND recorded_at >= NOW() - INTERVAL %s
            GROUP BY time_bucket, machine_id
            ORDER BY time_bucket ASC
        """.format(metric, metric, metric)
        return fetch_all(sql, (machine_id, interval))

    sql = """
        SELECT
            date_trunc('minute', recorded_at) AS time_bucket,
            machine_id,
            ROUND(AVG({})::numeric, 4) AS avg_value,
            ROUND(MAX({})::numeric, 4) AS max_value,
            ROUND(MIN({})::numeric, 4) AS min_value
        FROM sensor_readings
        WHERE recorded_at >= NOW() - INTERVAL %s
        GROUP BY time_bucket, machine_id
        ORDER BY time_bucket ASC
    """.format(metric, metric, metric)
    return fetch_all(sql, (interval,))