import configparser
from logger import log
def load_config(config_file='config.ini'):
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        return config
    except Exception as e:
        error_message = f'Error loading config: {e}'
        log(error_message)
        return None
