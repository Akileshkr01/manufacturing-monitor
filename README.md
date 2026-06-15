# Real-Time Manufacturing Monitoring System

A production-grade streaming pipeline that simulates industrial sensors, processes live telemetry through Apache Kafka, stores data in PostgreSQL, and visualizes machine health and alerts in a Power BI dashboard.

## System Architecture

1. **Sensor Simulator**: Generates real-time telemetry data for industrial machinery.
2. **Kafka Producer**: Publishes the generated sensor data to a dedicated Kafka topic (`sensor_data`).
3. **Apache Kafka Topic**: Acts as the message broker, decoupling producers from consumers and managing data streams.
4. **Kafka Consumer**: Consumes live messages from the Kafka topic and evaluates metrics against specific anomaly thresholds.
5. **PostgreSQL Database**: Persists raw sensor readings into the `sensor_readings` table and evaluation flags into the `alerts` table.
6. **FastAPI REST API**: Connects to the database and exposes multiple structured endpoints for reading logs, trends, and metrics.
7. **Power BI Dashboard**: Connects to the FastAPI endpoints to present analytics across fleet management, alert distribution, and asset maintenance screens.

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Streaming** | Apache Kafka 7.5.0 |
| **Backend** | Python 3.11 |
| **API** | FastAPI + Uvicorn |
| **Database** | PostgreSQL 15 |
| **Containers** | Docker + Docker Compose |
| **Visualization** | Power BI Desktop |

## Project Structure
manufacturing-monitor/
├── sensor/
│   ├── simulator.py        
│   ├── config.py           
│   ├── requirements.txt
│   └── Dockerfile
├── consumer/
│   ├── consumer.py        
│   ├── db.py              
│   ├── config.py          
│   ├── requirements.txt
│   └── Dockerfile
├── api/
│   ├── main.py            
│   ├── routes.py          
│   ├── models.py          
│   ├── db.py              
│   ├── requirements.txt
│   └── Dockerfile
├── database/
│   └── init.sql           
├── dashboard/
│   └── manufacturing_dashboard.pbix
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md