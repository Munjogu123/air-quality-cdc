# Air Quality CDC — Nairobi & Mombasa

This project implements a **Change Data Capture (CDC) pipeline** for measuring and analyzing **air quality data** in **Nairobi** and **Mombasa**.  
It leverages **MongoDB**, **Kafka Connect**, and **Cassandra** to capture, stream, and persist pollutant readings for long-term storage and analysis.

## Overview

The system provides a **continuous data collection pipeline** that:

- Captures **air quality sensor readings** in Nairobi & Mombasa  
- Uses **MongoDB** as the source system for raw sensor inserts  
- Streams changes into **Kafka** via the MongoDB Debezium connector  
- Persists transformed data into **Cassandra** using a Kafka sink connector  

## Key Technologies

- **MongoDB**: primary datastore for raw sensor data (replica set enabled for CDC)  
- **Kafka Connect**: manages CDC connectors (MongoDB source, Cassandra sink)  
- **Cassandra**: scalable, distributed database for analytics-ready data  
- **Python (pipeline.py)**: data extraction, transformation and loading to MongoDB

## Pipeline Workflow

1. **Sensor readings** (PM₂.₅, PM₁₀, NO₂, ozone, CO, etc.) are inserted into MongoDB.  
2. **Debezium MongoDB Connector** streams insert/update operations to Kafka topics.  
3. **Kafka Cassandra Sink Connector** consumes topics and writes to Cassandra tables.  
4. **Cassandra** stores clean, structured air quality data partitioned by city and time.

## Data Model

**Example payload:**

```json
"payload": {
  "_id": "68dbf474cc8ea5a037607bb9",
  "city": "mombasa",
  "time": "2025-09-30T00:00",
  "pm2_5": 7.0,
  "pm10": 10.1,
  "ozone": 42.0,
  "carbon_monoxide": 115.0,
  "nitrogen_dioxide": 3.4,
  "sulphur_dioxide": 2.3,
  "uv_index": 0.0
}
```

**Units:**

```json
{
    "time": "iso8601",
    "pm2_5": "μg/m³",
    "pm10": "μg/m³",
    "ozone": "μg/m³",
    "carbon_monoxide": "μg/m³",
    "nitrogen_dioxide": "μg/m³",
    "sulphur_dioxide": "μg/m³",
    "uv_index": ""
  }
```

## 🧑‍💻 Development Notes

- Use `src/keyfile.sh` to manage MongoDB replica key
- Plugins (e.g. Cassandra sink JAR) live in `src/plugins`
