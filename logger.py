# logger.py

import datetime

def log(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'[{timestamp}] {message}\n'
    print(log_message, end='')
    with open('/config/log.txt', 'a') as log_file:
        log_file.write(log_message)
