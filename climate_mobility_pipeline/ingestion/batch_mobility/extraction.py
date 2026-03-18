import tarfile
from pathlib import Path

# ---------------------------------------------------------
# Extraction Function
# ---------------------------------------------------------
def extract_archive(archive_path: Path, extract_to: Path) -> Path:
    """
    Extract a .tar.gz archive into a target directory.

    Parameters
    ----------
    archive_path : Path
        Full path to the .tar.gz archive. This path is constructed
        by the orchestrator using values from config.yaml.
    extract_to : Path
        Directory where the archive contents will be extracted.
        Also constructed by the orchestrator based on config.yaml.

    Returns
    -------
    Path
        The directory containing the extracted files.

    Notes
    -----
    - This function does NOT read configuration directly.
    - It performs only the extraction step.
    - All path logic and config handling should occur in the orchestrator.
    """
    
    # Ensure the extraction directory exists
    extract_to.mkdir(parents=True, exist_ok=True)

    # Extract the archive contents
    with tarfile.open(archive_path, "r:gz") as tar:
        tar.extractall(path=extract_to)

    return extract_to
