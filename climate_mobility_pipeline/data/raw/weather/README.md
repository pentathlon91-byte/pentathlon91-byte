# 📁 `raw/weather/`
### *Daily‑partitioned historical weather data ingested from the Open‑Meteo Archive API*

This directory contains the **unprocessed JSON weather files** retrieved from the **Open-Meteo Archive API**, representing the historical climate data used in the pipeline. Each file corresponds to a **single day** of weather observations for the Rome area, aligned with the 2014 mobility dataset.

The data is stored exactly as returned by the API to preserve full reproducibility, auditability, and traceability. To keep the repository lightweight and GitHub-friendly, only a few sample files are included locally; the full dataset is stored in **Azure Blob Storage** under the same partitioned structure.

---

## 🗂️ File Contents

Weather data is organized using a date‑based partitioning scheme:
```markdown
raw/weather/YYYY/MM/DD/weather_YYYY-MM-DD.json
```
Each JSON file contains the hourly historical weather observations for a specific date, including:
- `time`: hourly timestamp in ISO format  
- `temperature_2m`: hourly temperature  
- `precipitation`: hourly precipitation  
- `windspeed_10m`: hourly wind speed
- metadata such as latitude, longitude, timezone, and elevation

### **Example structure of a raw weather file**
Below is a simplified excerpt illustrating the structure of the JSON files stored in this directory:
```json
{
  "latitude": 41.875,
  "longitude": 12.5,
  "generationtime_ms": 0.08797645568847656,
  "utc_offset_seconds": 3600,
  "timezone": "Europe/Rome",
  "timezone_abbreviation": "GMT+1",
  "elevation": 58.0,
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "\u00b0C",
    "precipitation": "mm",
    "windspeed_10m": "km/h"
  },
  "hourly": {
    "time": [
      "2026-03-19T00:00",
      "2026-03-19T01:00",
      "2026-03-19T02:00"
    ],
    "temperature_2m": [8.3, 7.9, 7.3],
    "precipitation": [0.0, 0.0, 0.0],
    "windspeed_10m": [1.9, 1.8, 1.9]
  }
}
```

---

## 🔄 Upstream & Downstream Flow

### **Upstream sources**
- Open‑Meteo API (no API key required)

### **Downstream consumers**
- dbt staging models
- weather‑mobility joined datasets
- curated marts and dashboards
