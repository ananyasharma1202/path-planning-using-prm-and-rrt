import yaml
import logging

def load_config(config_file: str) -> dict:
    """
    Load configuration settings from a YAML file.

    :param config_file: Path to the YAML configuration file.
    :return: A dictionary containing the configuration settings.
    """
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except Exception as e:
        logging.error(f"Failed to load configuration file: {e}")
        raise

def setup_logging(log_level=logging.INFO):
    """
    Set up logging configuration.

    :param log_level: Logging level (e.g., logging.INFO, logging.DEBUG).
    """
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
