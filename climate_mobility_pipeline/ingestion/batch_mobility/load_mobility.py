import os
from pathlib import Path
from climate_mobility_pipeline.config_loader import load_config

# Local modules (each with a single responsibility)
from climate_mobility_pipeline.ingestion.batch_mobility.acquisition import download_archive_from_azure
from climate_mobility_pipeline.ingestion.batch_mobility.extraction import extract_archive

# ---------------------------------------------------------
# Path Setup
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent          # ingestion/batch_mobility/
PROJECT_ROOT = BASE_DIR.parents[1]                  # climate_mobility_pipeline/

def main():
    # -----------------------------
    # Load configuration
    # -----------------------------
    config = load_config(str(PROJECT_ROOT))

    mobility_cfg = config["mobility"]

    # Azure parameters
    container_name = mobility_cfg["azure"]["container_name"]
    blob_path = mobility_cfg["azure"]["blob_path"]

    # Local paths
    external_dir = PROJECT_ROOT / mobility_cfg["local"]["external_dir"]
    archive_path = external_dir / mobility_cfg["local"]["archive_name"]
    extract_to = external_dir / mobility_cfg["local"]["extracted_subdir"]

    # -----------------------------
    # Download archive from Azure
    # -----------------------------
    downloaded = download_archive_from_azure(
        container_name=container_name,
        blob_path=blob_path,
        local_path=archive_path
    )
    print("Archive downloaded:", downloaded)

    # -----------------------------
    # Extract archive locally
    # -----------------------------
    extracted_dir = extract_archive(downloaded, extract_to)
    print("Extraction complete:", extracted_dir)

if __name__ == "__main__":
    main()
