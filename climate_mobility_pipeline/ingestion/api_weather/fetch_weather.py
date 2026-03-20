import os
import logging
from pathlib import Path
from datetime import datetime, timezone

from climate_mobility_pipeline.config_loader import load_config

# Worker modules
from climate_mobility_pipeline.ingestion.api_weather.api_client import fetch_weather_data
from climate_mobility_pipeline.ingestion.api_weather.local_storage import save_to_local
from climate_mobility_pipeline.ingestion.api_weather.azure_upload import upload_to_azure_blob

# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Path Setup
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[1]   # climate_mobility_pipeline/

def main():
    """
    Orchestrates the full weather ingestion workflow:
    1. Load configuration
    2. Fetch weather data from the API
    3. Save the data locally
    4. Upload the file to Azure Blob Storage
    """

    # -----------------------------
    # Load configuration
    # -----------------------------
    config = load_config(str(PROJECT_ROOT))

    lat = config["weather"]["latitude"]
    lon = config["weather"]["longitude"]
    variables = config["weather"]["hourly_params"]

    # Local raw weather directory
    local_raw_weather = (
        Path(PROJECT_ROOT)
        / config["paths"]["local_raw"]
        / "weather"
    )

    # Azure configuration
    azure_conn = os.getenv(config["azure"]["connection_string_env"])
    container_name = config["azure"]["container"]

    # Base path for raw weather in Azure
    azure_raw_weather_root = config["paths"]["raw"]["weather"]

    # -----------------------------
    # Fetch data from the API
    # -----------------------------
    data = fetch_weather_data(lat, lon, variables)

    # -----------------------------
    # Save locally
    # -----------------------------
    local_file = save_to_local(data, local_raw_weather)

    # -----------------------------
    # Upload to Azure
    # -----------------------------
    if azure_conn:
        # Build date-partitioned blob path
        now = datetime.now(timezone.utc)
        date_path = now.strftime("%Y/%m/%d")

        blob_path = (
            f"{azure_raw_weather_root}"
            f"{date_path}/"
            f"{Path(local_file).name}"
        )

        upload_to_azure_blob(
            local_path=local_file,
            connection_string=azure_conn,
            container_name=container_name,
            blob_path=blob_path,
            content_type="application/json"
        )

        logger.info("Uploaded weather data to Azure at %s", blob_path)

    else:
        logger.warning("Azure connection string not found. Skipping upload.")

if __name__ == "__main__":
    main()
