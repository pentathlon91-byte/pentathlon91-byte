# 🌦️ Climate & Mobility Data Pipeline  
*A modern data engineering project combining weather, mobility, and real‑time traffic data.*

## 🚀 Overview  
This project is a **cloud‑native data pipeline** that collects, stores, and processes climate and mobility data from multiple sources. It demonstrates modern data engineering practices, including:

- API ingestion  
- Batch ingestion  
- Streaming ingestion  
- Cloud storage  
- Orchestration  
- Data modeling  

The pipeline is designed to explore real analytical questions such as:  
**How does weather influence traffic speed, congestion, or mobility patterns?**

---

## 🌍 Data Sources  

### **1. Weather API (Open‑Meteo)**  
- Hourly temperature, precipitation, wind speed  
- No API key required  
- Stored as raw JSON in Azure Blob Storage  

### **2. Batch Mobility Data**  
- Historical mobility or traffic datasets (CSV/Parquet)  
- Loaded periodically into cloud storage  
- Used for long‑term trend analysis  

### **3. Streaming Traffic Events (Kafka)**  
- Simulated real‑time vehicle events  
- Useful for latency‑sensitive analytics  
- Stored as micro‑batches in cloud storage  

---

## 🏗️ Architecture  

- **Ingestion Layer**  
  - Python scripts for API + batch ingestion  
  - Kafka producer/consumer for streaming  

- **Storage Layer**  
  - Azure Blob Storage (raw → processed)  

- **Orchestration Layer**  
  - Airflow DAG controlling ingestion + transformations  

- **Transformation Layer**  
  - dbt models (staging → core → marts)  

- **Analytics Layer**  
  - Dashboard exploring weather–mobility relationships  

---

## 🧪 Current Status  

✔ Weather API ingestion implemented  
✔ Data saved locally and uploaded to Azure Blob Storage  
⬜ Batch mobility ingestion  
⬜ Kafka streaming pipeline  
⬜ Airflow orchestration  
⬜ dbt transformations  
⬜ Dashboard  

This README will evolve as the project grows.

---

## 📁 Repository Structure (simplified)

```markdown
climate_mobility_pipeline/
  ingestion/
    api_weather/
      fetch_weather.py
  data/
    raw/
      weather/
  README.md
  config.yaml
```

---

## 🎯 Purpose  
This project demonstrates the full lifecycle of a modern data engineering workflow:

- Designing a multi‑source ingestion strategy  
- Working with cloud storage  
- Building modular, production‑style Python components  
- Preparing for orchestration and transformation layers  
- Creating a pipeline that answers a real analytical question  

It is part of a broader portfolio focused on **cloud‑native, scalable data engineering**.
