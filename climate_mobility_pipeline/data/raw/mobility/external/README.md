# 📁 `data/raw/mobility/external/`
### *Raw GPS mobility traces from the CRAWDAD roma/taxi dataset*

This directory contains the **original**, **unprocessed mobility traces** from the [CRAWDAD roma/taxi dataset](https://ieee-dataport.org/open-access/crawdad-romataxi), a month‑long collection of GPS positions from approximately 320 taxi cabs operating in Rome. This file represents the **source‑of‑truth raw mobility data** used in the batch ingestion pipeline and is stored exactly as provided by the dataset authors.

The dataset is distributed as a compressed archive (e.g., `taxi_february.tar.gz`) containing timestamp‑ordered TXT logs. To keep the repository lightweight and GitHub-friendly, `taxi_february.tar.gz` is stored in **Azure Blob Storage** and accessed automatically during execution.

**Related publication**: [Bonola, M., Bracciale, L., Loreti, P., Amici, R., Rabuffi, A., & Bianchi, G. (2016). Opportunistic communication in smart city: Experimental insight with small-scale taxi fleets as data carriers. *Ad Hoc Networks*, *43*, 43-55](https://www.sciencedirect.com/science/article/abs/pii/S1570870516300257).

---

## 🗂️ File Contents

Each line follows the schema:
```markdown
DRIVER_ID;TIMESTAMP;POSITION
```
where:
- `DRIVER_ID` — anonymized integer identifier for each taxi  
- `TIMESTAMP` — date and time of the GPS ping  
- `POSITION` — geographic point formatted as `POINT(latitude, longitude)`  

The traces are **sorted by timestamp** and represent positions collected roughly **every 7 seconds**, filtered to exclude low‑accuracy GPS readings.

### **Dataset characteristics**
- **Time span**: 2014-02-01 → 2014-03-02 (30 days)  
- **Fleet size**: ~320 taxis operating in central Rome  
- **Sampling frequency**: ~7 seconds per GPS ping
- **Filtering**: Removed positions with accuracy worse than 20m

### **Example of raw TXT records**
```markdown
156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)
187;2014-02-01 00:00:01.148457+01;POINT(41.9285433333333 12.4690366666667)
297;2014-02-01 00:00:01.220066+01;POINT(41.8910686119733 12.4927045625339)
```
This raw format is later parsed, cleaned, and converted into a structured Parquet file in the `data/processed/mobility/` directory.

---

## 🔄 Upstream & Downstream Flow

### **Upstream sources**
- CRAWDAD / IEEE DataPort dataset: *roma/taxi* (taxicabs traceset)

### **Downstream consumers**
- TXT extraction and parsing pipeline
- structured Parquet mobility data in `data/processed/mobility/`
- dbt staging models
- weather‑mobility joined datasets
- curated marts
- exploratory dashboards
