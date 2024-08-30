import yaml
import logging
from typing import List, Tuple

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


def path_corrector(paths: List[List[Tuple]]) -> List[List[Tuple]]:
    """
    Corrects the paths by ensuring that consecutive points are not duplicated.
    
    :param paths: List of paths, where each path is a list of line segments or points.
    :return: List of corrected paths.
    """
    def _correct_path(path: List[Tuple]) -> List[Tuple]:
        """
        Helper function to correct a single path.
        
        :param path: List of line segments or points.
        :return: Corrected path.
        """
        corrected_path = []
        last_point = None

        for segment in path:
            if len(segment) == 2:
                start, end = segment
                if last_point is None or last_point != start:
                    corrected_path.append(start)
                corrected_path.append(end)
                last_point = end
            else:
                point = segment
                if last_point is None or last_point != point:
                    corrected_path.append(point)
                last_point = point

        return corrected_path

    corrected_paths = [ _correct_path(path) for path in paths ]
    return corrected_paths

