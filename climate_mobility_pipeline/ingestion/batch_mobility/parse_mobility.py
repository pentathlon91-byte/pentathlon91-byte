import logging
from pathlib import Path
from datetime import datetime
import pandas as pd

# Module-level logger for consistent, structured logging
logger = logging.getLogger(__name__)

def parse_mobility_file(txt_path: Path) -> pd.DataFrame:
    """
    Parse a Rome taxi mobility TXT file into a structured DataFrame.

    Parameters
    ----------
    txt_path : Path
        Full path to the extracted TXT file containing raw mobility data.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with one row per GPS ping, containing:
        - vehicle_id : int
        - timestamp  : datetime64[ns, tz]
        - latitude   : float
        - longitude  : float

    Notes
    -----
    - This function performs ONLY parsing and type conversion.
    - It assumes each line follows the format:
          vehicle_id ; timestamp ; POINT(lat lon)
    """

    logger.info("Parsing mobility TXT file: %s", txt_path)

    rows = []

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()

                if not line:
                    continue  # skip empty lines

                try:
                    vehicle_id, ts, point = line.split(";")

                    # Clean POINT(lat lon)
                    point = point.replace("POINT(", "").replace(")", "")
                    lat_str, lon_str = point.split()

                    rows.append({
                        "vehicle_id": int(vehicle_id),
                        "timestamp": datetime.fromisoformat(ts),
                        "latitude": float(lat_str),
                        "longitude": float(lon_str),
                    })

                except Exception as e:
                    logger.error(
                        "Failed to parse line %d in %s: %s",
                        line_number, txt_path, e
                    )
                    raise

        df = pd.DataFrame(rows)
        logger.info("Parsed %d rows from %s", len(df), txt_path)
        return df

    except Exception:
        logger.exception("Failed to parse mobility file: %s", txt_path)
        raise
