import json
import logging
from pathlib import Path
from datetime import datetime, timezone

# Module-level logger for consistent, structured logging
logger = logging.getLogger(__name__)

def save_to_local(data: dict, base_output_dir: Path, target_date) -> Path:
    """
    Save weather data to a daily-partitioned JSON file.

    Parameters
    ----------
    data : dict
        Weather data returned by the API client.
    base_output_dir : Path
        Base directory for raw weather data (e.g., data/raw/weather/).
    target_date : datetime.date
        The date for which the weather data was fetched.

    Returns
    -------
    Path
        Full path to the saved JSON file.

    Notes
    -----
    - Creates a directory structure YYYY/MM/DD under base_output_dir.
    - Saves a deterministic filename: weather_YYYY-MM-DD.json.
    """

    # Build partitioned directory: YYYY/MM/DD
    year = target_date.strftime("%Y")
    month = target_date.strftime("%m")
    day = target_date.strftime("%d")

    output_dir = base_output_dir / year / month / day
    output_dir.mkdir(parents=True, exist_ok=True)

    # Deterministic filename for the day
    filename = f"weather_{target_date.strftime('%Y-%m-%d')}.json"
    filepath = output_dir / filename

    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        logger.info("Saved weather data locally at %s", filepath)
        return filepath

    except Exception:
        logger.exception("Failed to save weather data locally at %s", filepath)
        raise
