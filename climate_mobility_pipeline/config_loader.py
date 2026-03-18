import os
import yaml

def load_config(project_root: str):
    """
    Load the pipeline configuration from config.yaml.

    Parameters
    ----------
    project_root : str
        Absolute path to the project root directory.
        The config file is expected to live at:
        <project_root>/config.yaml

    Returns
    -------
    dict
        Parsed configuration dictionary containing:
        - weather settings
        - paths for raw data
        - Azure storage settings
        - any other pipeline parameters

    Notes
    -----
    This function is intentionally small and focused:
    it handles ONLY reading and parsing the YAML config.
    All logic that depends on the config should live elsewhere.
    """
    
    # Build the full path to config.yaml
    config_path = os.path.join(project_root, "config.yaml")

    # Read and parse the YAML configuration file
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
