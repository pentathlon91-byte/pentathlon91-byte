import logging
import tarfile
from pathlib import Path

# Module-level logger for consistent, structured logging
logger = logging.getLogger(__name__)

def extract_archive(archive_path: Path, extract_to: Path) -> Path:
    """
    Extract a .tar.gz archive into a target directory.

    Parameters
    ----------
    archive_path : Path
        Full path to the .tar.gz archive.
    extract_to : Path
        Directory where the archive contents will be extracted.

    Returns
    -------
    Path
        The directory containing the extracted files.

    Notes
    -----
    - This function performs ONLY the extraction step.
    - All path logic and config handling occur in the orchestrator.
    """

    logger.info("Extracting archive: %s", archive_path)

    # Ensure the extraction directory exists
    extract_to.mkdir(parents=True, exist_ok=True)

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            # Security: prevent path traversal attacks
            for member in tar.getmembers():
                member_path = extract_to / member.name
                if not str(member_path.resolve()).startswith(str(extract_to.resolve())):
                    raise Exception(f"Unsafe path detected in archive: {member.name}")

            tar.extractall(path=extract_to)

        logger.info("Extraction complete: %s", extract_to)
        return extract_to

    except Exception:
        logger.exception("Failed to extract archive: %s", archive_path)
        raise
