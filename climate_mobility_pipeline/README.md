# 🌦️ Climate & Mobility Data Pipeline
*A modern, cloud-native data engineering project combining weather, mobility, and real-time traffic data.*

## 🚀 Overview
This project implements a **multi-source**, **production-style data pipeline** that ingests, stores, and processes climate and mobility data using modern data engineering patterns. It integrates:

- **API ingestion** (Open-Meteo weather archive)
- **Batch ingestion** (historical mobility archive)
- **Streaming ingestion** (Kafka traffic events)
- **Cloud storage** (Azure Blob Storage)
- **Orchestration-ready design** (Airflow)
- **Transformation** (dbt models)
- **Analytics** (weather-mobility insights)

The pipeline is designed to explore real analytical questions, such as:  
**How does weather influence traffic speed, congestion, or mobility patterns?**

---

## 🌍 Data Sources

### **1. Weather API (Open‑Meteo archive)**
- Hourly temperature, precipitation, wind speed
- No API key required
- Ingested via Python
- Stored in Azure under:
```markdown
raw/weather/YYYY/MM/DD/
```

### **2. Batch Mobility Data (Taxi GPS Pings)**
- Historical `.tar.gz` archive containing a TXT mobility log
- Downloaded from Azure, extracted, parsed, and converted to Parquet
- Stored in Azure under:
```markdown
raw/mobility/external/
raw/mobility/txt/
processed/mobility/
```

### **3. Streaming Traffic Events (Kafka)**
- Simulated real‑time traffic events
- Micro-batched and stored in Azure
- Enables low-latency analytics and anomaly detection

---

## 📦 Data Availability

To keep the repository lightweight and GitHub-friendly, only **simplified sample data** is included in the `data/` directory.

The full raw datasets used by the pipeline, including weather JSON files, mobility `.tar.gz` archive, extracted TXT log, and processed Parquet output, are stored in **Azure Blob Storage** and accessed automatically during execution.

This ensures the project remains easy to clone and run locally while still demonstrating a realistic, cloud-scale data engineering workflow.

---

## 🏗️ Architecture

### **Ingestion Layer**
- Weather API ingestion (JSON → Azure)
- Batch mobility ingestion (tar.gz → TXT → Parquet → Azure)
- Kafka streaming ingestion (traffic events)

### **Storage Layer (Azure Blob Storage)**
Structured as a modern data lake:
```markdown
raw/
  weather/
  mobility/
    external/
      txt/
  traffic_stream/

processed/
  weather/
  mobility/
  traffic_stream/

curated/
  mobility_weather/
  marts/
```

### **Orchestration Layer**
- Airflow DAG orchestrating API, batch, and streaming pipelines

### **Transformation Layer**
- dbt models (staging → core → marts)
- Weather-mobility joined datasets

### **Analytics Layer**
- Dashboard exploring relationships between weather and mobility

---

## 🧪 Current Status

✔ Weather API ingestion implemented  
✔ Weather data stored locally + in Azure  
✔ Batch mobility ingestion fully implemented

  - Download archive from Azure
  - Extract TXT
  - Parse mobility log
  - Write Parquet
  - Upload raw + processed data to Azure

⬜ Kafka streaming pipeline  
⬜ Airflow orchestration  
⬜ dbt transformations  
⬜ Analytics dashboard

This README will evolve as the project grows.

---

## 📁 Repository Structure (simplified)

```markdown
climate_mobility_pipeline/
  data/
    raw/
      weather/
      mobility/
        external/
          txt/
    processed/
      mobility/

  ingestion/
    api_weather/
      fetch_weather.py
      api_client.py
      local_storage.py
      azure_upload.py
    batch_mobility/
      load_mobility.py
      acquisition.py
      extraction.py
      parse_mobility.py
      write_parquet.py

  config_loader.py
  config.yaml
  README.md
```

---

## 🎯 Purpose  
This project demonstrates the full lifecycle of a modern data engineering workflow:

- Designing multi‑source ingestion strategies
- Building modular, production‑style Python components
- Working with cloud storage and partitioned data lakes
- Preparing for orchestration and transformation layers
- Creating a pipeline that answers a real analytical question

It is part of a broader portfolio focused on **cloud‑native, scalable data engineering**.
