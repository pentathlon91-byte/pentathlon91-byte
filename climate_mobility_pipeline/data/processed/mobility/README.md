# 📁 `data/processed/mobility/`
### *Analytics‑ready mobility data (Parquet format)*

This directory contains the **cleaned**, **parsed**, and **structured mobility dataset** produced by the batch ingestion pipeline. It represents the **final stage** of processing for the historical mobility log and is the version used by downstream analytics, dbt models, and weather‑mobility integrations.

To keep the repository lightweight and GitHub-friendly, the Parquet file is stored in **Azure Blob Storage**.

---

## 🗂️ File Contents

The Parquet file contains the structured output of the TXT mobility log extracted from the original `.tar.gz` archive.

### **Core fields**
- `vehicle_id` — unique vehicle identifier  
- `timestamp` — event timestamp  
- `latitude`, `longitude` — cleaned GPS coordinates

### **Schema and head of the processed mobility data**
Below is a preview of the structured mobility records after parsing the raw TXT log and before writing it to Parquet.
```markdown
   vehicle_id                        timestamp   latitude  longitude
0         156 2014-02-01 00:00:00.739166+01:00  41.883672  12.487778
1         187 2014-02-01 00:00:01.148457+01:00  41.928543  12.469037
2         297 2014-02-01 00:00:01.220066+01:00  41.891069  12.492705
3          89 2014-02-01 00:00:01.470854+01:00  41.793177  12.432122
4          79 2014-02-01 00:00:01.631136+01:00  41.900275  12.462746

<class 'pandas.DataFrame'>
RangeIndex: 21817851 entries, 0 to 21817850
Data columns (total 4 columns):
 #   Column      Dtype
---  ------      -----
 0   vehicle_id  int64
 1   timestamp   datetime64[us, UTC+01:00]
 2   latitude    float64
 3   longitude   float64
dtypes: datetime64[us, UTC+01:00](1), float64(2), int64(1)
memory usage: 665.8 MB
```

---

## 🔄 Upstream & Downstream Flow

### **Upstream sources**
- `.tar.gz` archive stored in Azure (`raw/mobility/external/`)
- extracted TXT log (`raw/mobility/external/txt/`)
- parsed rows from the batch ingestion pipeline

### **Downstream consumers**
- dbt staging models
- weather‑mobility joined datasets
- curated marts and dashboards
