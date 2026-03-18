import os
import logging
from climate_mobility_pipeline.config_loader import load_config

# Local modules (each with a single responsibility)
from climate_mobility_pipeline.ingestion.api_weather.api_client import fetch_weather_data
from climate_mobility_pipeline.ingestion.api_weather.local_storage import save_to_local
from climate_mobility_pipeline.ingestion.api_weather.azure_upload import upload_to_azure_blob

# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------
# Configure structured logging for the entire module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Path Setup
# ---------------------------------------------------------
# __file__ → ingestion/api_weather/fetch_weather.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PROJECT_ROOT → climate_mobility_pipeline/
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

# ---------------------------------------------------------
# Main Orchestration Logic
# ---------------------------------------------------------
def main():
    """
    Orchestrates the full weather ingestion workflow:
    1. Load configuration
    2. Fetch weather data from the API
    3. Save the data locally
    4. Upload the file to Azure Blob Storage (optional)

    This function coordinates the ingestion pipeline but delegates
    all actual work to modular components.
    """

    # -----------------------------
    # Load configuration
    # -----------------------------
    config = load_config(PROJECT_ROOT)

    LAT = config["weather"]["latitude"]
    LON = config["weather"]["longitude"]
    VARS = config["weather"]["variables"]

    # Local raw-data directory for weather ingestion
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, config["paths"]["raw_data_weather"])

    # Azure configuration (connection string via environment variable)
    AZURE_CONN = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    CONTAINER = config["weather"]["azure"]["container_name"]
    PREFIX = config["weather"]["azure"]["blob_prefix"]

    # -----------------------------
    # Fetch data from the API
    # -----------------------------
    data = fetch_weather_data(LAT, LON, VARS)

    # -----------------------------
    # Save locally as timestamped JSON
    # -----------------------------
    local_file = save_to_local(data, OUTPUT_DIR)

    # -----------------------------
    # Upload to Azure (optional)
    # -----------------------------
    if AZURE_CONN:
        # Blob path inside the container
        blob_name = f"{PREFIX}/{os.path.basename(local_file)}"

        upload_to_azure_blob(
            local_path=local_file,
            connection_string=AZURE_CONN,
            container_name=CONTAINER,
            blob_path=blob_name
        )
    else:
        logger.warning("Azure connection string not found. Skipping upload.")

# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
