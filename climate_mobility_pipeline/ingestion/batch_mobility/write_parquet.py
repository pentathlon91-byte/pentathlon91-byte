import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)

def write_parquet(df: pd.DataFrame, output_dir: Path, filename: str) -> Path:
    """
    Write a mobility DataFrame to a Parquet file inside a target directory.

    Parameters
    ----------
    df : pandas.DataFrame
        The structured mobility dataset produced by the parser.
    output_dir : Path
        Directory where the Parquet file will be written.
    filename : str
        Name of the Parquet file to create.

    Returns
    -------
    Path
        Full path to the written Parquet file.
    """

    logger.info("Writing DataFrame to Parquet: %s", output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    try:
        df.to_parquet(output_path, index=False, compression="snappy")
        logger.info("Parquet file written successfully: %s", output_path)
        return output_path

    except Exception:
        logger.exception("Failed to write Parquet file: %s", output_path)
        raise
