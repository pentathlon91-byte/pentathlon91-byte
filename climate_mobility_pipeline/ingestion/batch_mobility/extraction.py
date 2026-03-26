import logging
import tarfile
from pathlib import Path

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
    """

    logger.info("Extracting archive: %s", archive_path)

    extract_to.mkdir(parents=True, exist_ok=True)

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
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
