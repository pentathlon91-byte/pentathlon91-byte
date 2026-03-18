import os
import json
import logging
from datetime import datetime, timezone

# Module-level logger for consistent, structured logging
logger = logging.getLogger(__name__)

def save_to_local(data, output_dir):
    """
    Save weather data to a timestamped JSON file in the local raw-data directory.

    Parameters
    ----------
    data : dict
        Weather data returned by the API client.
    output_dir : str
        Directory where the JSON file will be written.

    Returns
    -------
    str
        Full path to the saved JSON file.

    Notes
    -----
    - This function is responsible ONLY for local persistence.
    - It does not handle API calls, Azure uploads, or configuration.
    - Filenames include a UTC timestamp to ensure uniqueness.
    """

    # Ensure the output directory exists (create if missing)
    os.makedirs(output_dir, exist_ok=True)

    # Generate a timestamped filename for traceability and uniqueness
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"weather_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    # Write the JSON file with pretty formatting
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Saved weather data locally at {filepath}")
    return filepath
