import os
import logging
from pathlib import Path
from datetime import datetime, timedelta

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

def ingest_single_day(target_date, config, local_raw_weather, azure_conn, container_name, azure_raw_weather_root):
    """Fetch, store, and upload weather data for a single historical day."""

    lat = config["weather"]["latitude"]
    lon = config["weather"]["longitude"]
    variables = config["weather"]["hourly_params"]
    timezone_str = config["weather"]["timezone"]

    date_str = target_date.strftime("%Y-%m-%d")
    logger.info(f"Fetching historical weather for {date_str}")

    # Fetch one day of weather (start_date == end_date)
    data = fetch_weather_data(
        latitude=lat,
        longitude=lon,
        variables=variables,
        start_date=date_str,
        end_date=date_str,
        timezone=timezone_str
    )

    # Save locally into YYYY/MM/DD/weather_YYYY-MM-DD.json
    local_file = save_to_local(
        data=data,
        base_output_dir=local_raw_weather,
        target_date=target_date
    )

    # Upload to Azure with matching partitioning
    if azure_conn:
        date_path = target_date.strftime("%Y/%m/%d")
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

        logger.info(f"Uploaded weather data to Azure at {blob_path}")
    else:
        logger.warning("Azure connection string not found. Skipping upload.")

def main():
    """Historical weather ingestion, partitioned by day."""

    # -----------------------------
    # Load configuration
    # -----------------------------
    config = load_config(str(PROJECT_ROOT))

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

    # Required historical dates
    start_date_str = config["weather"]["start_date"]
    end_date_str = config["weather"]["end_date"]

    if not start_date_str or not end_date_str:
        raise ValueError("Historical ingestion requires start_date and end_date in config.yaml")

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    logger.info(f"Starting historical weather ingestion from {start_date} to {end_date}")

    current = start_date
    while current <= end_date:
        ingest_single_day(
            target_date=current,
            config=config,
            local_raw_weather=local_raw_weather,
            azure_conn=azure_conn,
            container_name=container_name,
            azure_raw_weather_root=azure_raw_weather_root
        )
        current += timedelta(days=1)

    logger.info("Historical weather ingestion completed.")

if __name__ == "__main__":
    main()
