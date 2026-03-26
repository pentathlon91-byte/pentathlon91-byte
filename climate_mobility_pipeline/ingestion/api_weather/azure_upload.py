import logging
from pathlib import Path
from azure.storage.blob import BlobServiceClient, ContentSettings

logger = logging.getLogger(__name__)

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

    except Exception as e:
        logger.exception("Azure Blob upload failed: %s", e)
        raise
