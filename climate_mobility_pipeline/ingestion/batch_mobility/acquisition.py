import logging
from pathlib import Path
from azure.storage.blob import BlobServiceClient

# Module-level logger for consistent, structured logging
logger = logging.getLogger(__name__)

def download_archive_from_azure(
    connection_string: str,
    container_name: str,
    blob_path: str,
    local_path: Path
) -> Path:
    """
    Download a file from Azure Blob Storage and save it locally.

    Parameters
    ----------
    connection_string : str
        Azure Storage connection string.
    container_name : str
        Name of the Azure container.
    blob_path : str
        Path of the blob inside the container
        (e.g. "raw/mobility/external/2026/03/19/archive.tar.gz").
    local_path : Path
        Local filesystem path where the file will be saved.

    Returns
    -------
    Path
        The local path of the downloaded file.
    """

    if not connection_string:
        logger.error("Azure connection string is missing.")
        raise ValueError("Azure connection string is required.")

    logger.info(
        "Starting download from Azure Blob Storage: container=%s, blob=%s",
        container_name,
        blob_path,
    )

    # Connect to Azure Blob Storage
    try:
        blob_service = BlobServiceClient.from_connection_string(connection_string)
        container = blob_service.get_container_client(container_name)
    except Exception:
        logger.exception("Failed to connect to Azure Blob Storage.")
        raise

    # Ensure local directory exists
    local_path.parent.mkdir(parents=True, exist_ok=True)

    # Download blob content
    try:
        logger.info("Downloading blob to local path: %s", local_path)
        with open(local_path, "wb") as f:
            blob_data = container.download_blob(blob_path)
            f.write(blob_data.readall())
        logger.info("Download complete: %s", local_path)
    except Exception:
        logger.exception("Failed during blob download or file write.")
        raise

    return local_path
