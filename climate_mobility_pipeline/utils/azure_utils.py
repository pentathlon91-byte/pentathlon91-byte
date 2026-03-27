import logging
from pathlib import Path
from azure.storage.blob import BlobServiceClient, ContentSettings

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
        Path of the blob inside the container.
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

    try:
        blob_service = BlobServiceClient.from_connection_string(connection_string)
        container = blob_service.get_container_client(container_name)
    except Exception:
        logger.exception("Failed to connect to Azure Blob Storage.")
        raise

    local_path.parent.mkdir(parents=True, exist_ok=True)

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

def upload_to_azure_blob(
    local_path: Path,
    connection_string: str,
    container_name: str,
    blob_path: str,
    content_type: str = None,
):
    """
    Upload a local file to Azure Blob Storage.

    Parameters
    ----------
    local_path : Path
        Path to the local file that will be uploaded.
    connection_string : str
        Azure Storage connection string.
    container_name : str
        Name of the Azure Blob container.
    blob_path : str
        Path inside the container.
    content_type : str, optional
        MIME type for the uploaded file. If None, inferred from extension.
    """

    try:
        logger.info("Connecting to Azure Blob Storage...")

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        try:
            container_client.create_container()
        except Exception:
            pass

        if content_type is None:
            suffix = local_path.suffix.lower()
            if suffix == ".json":
                content_type = "application/json"
            elif suffix == ".parquet":
                content_type = "application/octet-stream"
            elif suffix in [".txt", ".csv"]:
                content_type = "text/plain"
            elif suffix in [".gz", ".tar", ".tgz"]:
                content_type = "application/gzip"
            else:
                content_type = "application/octet-stream"

        blob_client = container_client.get_blob_client(blob_path)

        logger.info("Uploading %s to Azure Blob: %s/%s", local_path, container_name, blob_path)

        with open(local_path, "rb") as data:
            blob_client.upload_blob(
                data,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type),
            )

        logger.info("Upload complete: %s", blob_path)

    except Exception:
        logger.exception("Azure Blob upload failed for file: %s", local_path)
        raise
