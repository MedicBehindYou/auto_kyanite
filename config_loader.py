# config_loader.py

import configparser
def load_config(config_file='/config/config.ini'):
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        return config
    except Exception as e:
        error_message = f'Error loading config: {e}'
        print(error_message)
        return None
