import logging
from azure.storage.blob import BlobServiceClient, ContentSettings

# Module-level logger for structured, consistent logging
logger = logging.getLogger(__name__)

def upload_to_azure_blob(local_path, connection_string, container_name, blob_path):
    """
    Upload a local file to Azure Blob Storage.

    Parameters
    ----------
    local_path : str
        Path to the local file that will be uploaded.
    connection_string : str
        Azure Storage connection string (must include account key).
    container_name : str
        Name of the Azure Blob container where the file will be stored.
    blob_path : str
        Path inside the container (e.g. "weather/20240318/weather_1234.json").

    Notes
    -----
    - This function is responsible ONLY for uploading a file.
    - It does not handle downloading, parsing, or local storage.
    - It ensures the container exists before uploading.
    """

    try:
        logger.info("Connecting to Azure Blob Storage...")

        # Create a client for the storage account
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get a reference to the container
        container_client = blob_service_client.get_container_client(container_name)

        # Ensure the container exists (create if missing)
        try:
            container_client.create_container()
        except Exception:
            # If it already exists, we silently continue
            pass

        # Create a client for the specific blob path
        blob_client = container_client.get_blob_client(blob_path)

        # Upload the file
        with open(local_path, "rb") as data:
            blob_client.upload_blob(
                data,
                overwrite=True,  # Allow replacing existing files
                content_settings=ContentSettings(content_type="application/json")
            )

        logger.info(f"Uploaded file to Azure Blob: {container_name}/{blob_path}")

    except Exception as e:
        # Catch any Azure or network-related errors
        logger.error(f"Azure Blob upload failed: {e}")
        raise
