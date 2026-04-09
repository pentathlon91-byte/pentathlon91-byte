# 📄 Traffic Event Schema

*A reference for the synthetic traffic events used in the streaming ingestion pipeline.*

### **Overview**

This directory contains the **canonical JSON schema** for the synthetic traffic events generated during the **historical streaming replay** (2014‑02‑01 → 2014‑03‑02). The schema defines the structure, fields, and semantics of each event published to Kafka by the streaming producer.

These events simulate real-world traffic telemetry and are used to populate the `raw/traffic_stream` directory in **Azure Blob Storage**.

---

## Event Structure

Each traffic event is a JSON object with the following fields:
- `event_id` [`string`]: unique identifier assigned by the producer  
- `timestamp` [`string`]: ISO‑8601 timestamp representing the historical event time  
- `vehicle_id` [`string`]: stable synthetic vehicle identifier (e.g., `vehicle_42`)
- `road_segment` [`string`]: road segment where the event occurred (e.g., `GRA-07`)
- `speed` [`float`]: vehicle speed in km/h at the given timestamp  
- `event_type` [`string`]: one of `speed_update`, `congestion`, `anomaly`   

### **Example**
```json
{
  "event_id": "c1f2e4b8-9a3d-4c1e-9f0a-1b2c3d4e5f6a",
  "timestamp": "2014-02-01T08:12:00",
  "vehicle_id": "vehicle_042",
  "road_segment": "GRA-07",
  "speed": 18.4,
  "event_type": "congestion"
}
```
