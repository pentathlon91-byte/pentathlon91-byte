import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient

# ---------------------------------------------------------
# Azure Configuration
# ---------------------------------------------------------
# Connection string must be provided via environment variable.
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")


# ---------------------------------------------------------
# Download Function
# ---------------------------------------------------------
def download_archive_from_azure(container_name: str, blob_path: str, local_path: Path) -> Path:
    """
    Download a file from Azure Blob Storage and save it locally.

    Parameters
    ----------
    container_name : str
        Name of the Azure container (e.g. "data").
    blob_path : str
        Path of the blob inside the container
        (e.g. "external/rome_taxi/taxi_february.tar.gz").
    local_path : Path
        Local filesystem path where the file will be saved.

    Returns
    -------
    Path
        The local path of the downloaded file.
    """
    if AZURE_CONNECTION_STRING is None:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set in the environment.")

    # Connect to Azure Blob Storage
    blob_service = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container = blob_service.get_container_client(container_name)

    # Ensure local directory exists
    local_path.parent.mkdir(parents=True, exist_ok=True)

    # Download blob content
    with open(local_path, "wb") as f:
        blob_data = container.download_blob(blob_path)
        f.write(blob_data.readall())

    return local_path
