# 📁 `raw/mobility/txt/`
### *Extracted TXT mobility log from the CRAWDAD roma/taxi dataset*

This directory contains the **raw TXT mobility log** extracted from the original `taxi_february.tar.gz` archive of the [CRAWDAD roma/taxi dataset](https://ieee-dataport.org/open-access/crawdad-romataxi). This file represents the **first fully expanded form** of the mobility data after decompression. It is used as the direct input for the parsing and cleaning stage of the batch ingestion pipeline.

To keep the repository lightweight and GitHub-friendly, the raw TXT mobility log is stored in **Azure Blob Storage**.

---

## 🗂️ File Contents

The log follows a consistent semicolon‑separated structure:
```markdown
DRIVER_ID;TIMESTAMP;POSITION
```
where:
- `DRIVER_ID`: anonymized integer identifier  
- `TIMESTAMP`: precise event timestamp with timezone  
- `POSITION`: geographic point in WKT format, e.g., `POINT(41.900275 12.462746)`  

### **Example of extracted TXT records**
```markdown
156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)
187;2014-02-01 00:00:01.148457+01;POINT(41.9285433333333 12.4690366666667)
297;2014-02-01 00:00:01.220066+01;POINT(41.8910686119733 12.4927045625339)
```
These lines are read directly by the parsing module, which converts them into structured rows before writing the Parquet file in the `processed/mobility/` directory.

---

## 🔄 Upstream & Downstream Flow

### **Upstream sources**
- `taxi_february.tar.gz` archive from the CRAWDAD roma/taxi dataset stored in `raw/mobility/external/`

### **Downstream consumers**
- parsing and cleaning scripts
- structured Parquet mobility data (`processed/mobility/`)
- dbt staging models
- weather‑mobility joined datasets
- curated marts and dashboards
