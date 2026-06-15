from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SensorReading(BaseModel):
    id: int
    machine_id: str
    temperature: float
    rpm: float
    vibration: float
    pressure: float
    recorded_at: datetime
    ingested_at: datetime


class Alert(BaseModel):
    id: int
    machine_id: str
    alert_type: str
    metric: str
    value: float
    threshold: float
    severity: str
    triggered_at: datetime
    created_at: datetime


class MachineSummary(BaseModel):
    machine_id: str
    avg_temperature: float
    avg_rpm: float
    avg_vibration: float
    avg_pressure: float
    max_temperature: float
    max_rpm: float
    max_vibration: float
    max_pressure: float
    total_readings: int
    last_seen: datetime


class AlertSummary(BaseModel):
    machine_id: str
    severity: str
    metric: str
    total_alerts: int
    latest_alert: datetime