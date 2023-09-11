# logger.py

import datetime
import config_loader

config = config_loader.load_config()

if config:
    LOG_TXT = (config['Logger']['log_txt'])
else:
    log('Configuration not loaded. Cannot perform backup and backup management.')
    sys.exit()

def log(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'[{timestamp}] {message}\n'
    print(log_message, end='')
    with open('/config/log.txt', 'a') as log_file:
        log_file.write(log_message)
