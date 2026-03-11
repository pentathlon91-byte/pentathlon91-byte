import os
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any
import requests
from azure.storage.blob import BlobServiceClient, ContentSettings
import yaml

# ---------------------------------------------------------
# Setting up paths
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))                 # ingestion/api_weather/
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))   # climate_mobility_pipeline/

# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Configuration Loader
# ---------------------------------------------------------
def load_config():
    config_path = os.path.abspath(os.path.join(PROJECT_ROOT, "config.yaml"))
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------
# API Client
# ---------------------------------------------------------
def fetch_weather_data(
    latitude: float,
    longitude: float,
    variables: List[str]
) -> Dict[str, Any]:
    """
    Fetch hourly weather data from the Open-Meteo API.
    """
    base_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join(variables),
        "timezone": "auto"
    }

    try:
        logger.info("Requesting weather data from Open-Meteo API...")
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        logger.info("Weather data fetched successfully.")
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise

# ---------------------------------------------------------
# Local Storage
# ---------------------------------------------------------
def save_to_local(data: Dict[str, Any], output_dir: str) -> str:
    """
    Save weather data to a timestamped JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"weather_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Saved weather data locally at {filepath}")
    return filepath

# ---------------------------------------------------------
# Azure Blob Upload
# ---------------------------------------------------------
def upload_to_azure_blob(
    local_path: str,
    connection_string: str,
    container_name: str,
    blob_path: str
):
    """
    Upload a local file to Azure Blob Storage.
    """
    try:
        logger.info("Connecting to Azure Blob Storage...")
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        # Ensure container exists
        try:
            container_client.create_container()
            logger.info(f"Created container '{container_name}'.")
        except Exception:
            pass  # Container already exists

        blob_client = container_client.get_blob_client(blob_path)

        with open(local_path, "rb") as data:
            blob_client.upload_blob(
                data,
                overwrite=True,
                content_settings=ContentSettings(content_type="application/json")
            )

        logger.info(f"Uploaded file to Azure Blob: {container_name}/{blob_path}")

    except Exception as e:
        logger.error(f"Azure Blob upload failed: {e}")
        raise

# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------
def main():
    config = load_config()

    # Weather configuration
    LATITUDE = config["weather"]["latitude"]
    LONGITUDE = config["weather"]["longitude"]
    VARIABLES = config["weather"]["variables"]

    # Paths
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, config["paths"]["raw_data_weather"])

    # Azure configuration (use environment variables for safety)
    AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    CONTAINER_NAME = config["azure"]["container_name"]
    BLOB_PREFIX = config["azure"]["blob_prefix"]

    # Fetch data
    weather_data = fetch_weather_data(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        variables=VARIABLES
    )

    # Save locally
    local_file = save_to_local(weather_data, OUTPUT_DIR)

    # Upload to Azure
    if AZURE_CONNECTION_STRING:
        blob_name = f"{BLOB_PREFIX}/{os.path.basename(local_file)}"
        upload_to_azure_blob(
            local_path=local_file,
            connection_string=AZURE_CONNECTION_STRING,
            container_name=CONTAINER_NAME,
            blob_path=blob_name
        )
    else:
        logger.warning("Azure connection string not found. Skipping upload.")

if __name__ == "__main__":
    main()