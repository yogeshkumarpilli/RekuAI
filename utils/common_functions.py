import os
import yaml
import pandas as pd
from src.logger import logging
from src.custom_exception import CustomException


logger = logging.getLogger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist in the given path")
        with open(file_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logging.info(f"Successfully read the yaml file from {file_path}")
            return config
    except Exception as e:
        logger.error(f"Error while reading the yaml file {file_path}: {e}")
        raise CustomException("Error while reading the yaml file", e)
