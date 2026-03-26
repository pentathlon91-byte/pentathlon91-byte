from pathlib import Path
from datetime import datetime, timezone
import logging
import os

from climate_mobility_pipeline.config_loader import load_config

# Worker modules
from climate_mobility_pipeline.ingestion.batch_mobility.acquisition import download_archive_from_azure
from climate_mobility_pipeline.ingestion.batch_mobility.extraction import extract_archive
from climate_mobility_pipeline.ingestion.batch_mobility.parse_mobility import parse_mobility_file
from climate_mobility_pipeline.ingestion.batch_mobility.write_parquet import write_parquet
from climate_mobility_pipeline.ingestion.batch_mobility.azure_upload import upload_to_azure_blob

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Path Setup
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[1]

def main():
    # Load configuration
    config = load_config(str(PROJECT_ROOT))

    azure_cfg = config["azure"]
    mobility_cfg = config["mobility"]
    paths_cfg = config["paths"]

    # Local paths
    local_external_dir = PROJECT_ROOT / mobility_cfg["local"]["external_dir"]
    local_archive_path = local_external_dir / mobility_cfg["local"]["archive_name"]
    local_extract_dir = local_external_dir / mobility_cfg["local"]["extracted_subdir"]

    local_processed_dir = (
        PROJECT_ROOT
        / paths_cfg["local_processed"]
        / "mobility"
    )

    # Azure configuration
    azure_conn = os.getenv(azure_cfg["connection_string_env"])
    container_name = azure_cfg["container"]

    # Base path for raw and processed mobility data in Azure
    azure_raw_txt = paths_cfg["raw"]["mobility_txt"]
    azure_processed = paths_cfg["processed"]["mobility"]

    # Build date-partitioned paths
    now = datetime.now(timezone.utc)
    date_path = now.strftime("%Y/%m/%d")

    # Azure blob paths
    blob_raw_txt = f"{azure_raw_txt}{date_path}/"
    blob_processed = f"{azure_processed}{date_path}/{mobility_cfg['month_processed']}.parquet"

    # Download archive from Azure
    logger.info("Downloading mobility archive from Azure...")
    downloaded = download_archive_from_azure(
        connection_string=azure_conn,
        container_name=container_name,
        blob_path=mobility_cfg["azure"]["blob_path"],
        local_path=local_archive_path
    )

    # Extract archive locally
    extracted_dir = extract_archive(downloaded, local_extract_dir)

    # Find TXT file in extracted directory
    txt_files = list(extracted_dir.glob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(f"No TXT files found in {extracted_dir}")

    txt_path = txt_files[0]

    # Upload raw TXT to Azure
    upload_to_azure_blob(
        local_path=txt_path,
        connection_string=azure_conn,
        container_name=container_name,
        blob_path=f"{blob_raw_txt}{txt_path.name}",
        content_type="text/plain"
    )

    # Parse TXT → DataFrame
    df = parse_mobility_file(txt_path)

    # Write processed parquet locally
    parquet_path = write_parquet(df, local_processed_dir, filename=f"{mobility_cfg['month_processed']}.parquet")

    # Upload processed parquet to Azure
    upload_to_azure_blob(
        local_path=parquet_path,
        connection_string=azure_conn,
        container_name=container_name,
        blob_path=blob_processed,
        content_type="application/octet-stream"
    )

    logger.info("Batch mobility ingestion completed successfully.")

if __name__ == "__main__":
    main()
