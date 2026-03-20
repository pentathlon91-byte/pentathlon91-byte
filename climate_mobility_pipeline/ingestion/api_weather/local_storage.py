import json
import logging
from pathlib import Path
from datetime import datetime, timezone

# Module-level logger for consistent, structured logging
logger = logging.getLogger(__name__)

def save_to_local(data: dict, output_dir: Path) -> Path:
    """
    Save weather data to a timestamped JSON file in the local raw-data directory.

    Parameters
    ----------
    data : dict
        Weather data returned by the API client.
    output_dir : Path
        Directory where the JSON file will be written.

    Returns
    -------
    Path
        Full path to the saved JSON file.

    Notes
    -----
    - This function is responsible ONLY for local persistence.
    - It does not handle API calls, Azure uploads, or configuration.
    - Filenames include a UTC timestamp to ensure uniqueness.
    """

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Timestamped filename for traceability
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"weather_{timestamp}.json"
    filepath = output_dir / filename

    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        logger.info("Saved weather data locally at %s", filepath)
        return filepath

    except Exception:
        logger.exception("Failed to save weather data locally at %s", filepath)
        raise
