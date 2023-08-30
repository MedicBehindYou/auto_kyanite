# TODO: Implement multi threading?

import sqlite3
import subprocess
import threading
import time
from datetime import datetime

# This creates a connection to a new or existing database file
connection = sqlite3.connect('database.db')

# A cursor is used to execute SQL commands and fetch results.
cursor = connection.cursor()

# Define the maximum inactivity time (in seconds) before considering the subprocess inactive
MAX_INACTIVITY_TIME = 600  # Adjust this value as needed

# Initialize log file
log_file = open('log.txt', 'a')

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'[{timestamp}] {message}\n'
    print(log_message, end='')
    log_file.write(log_message)
    log_file.flush()

def inactivity_checker(process, tag):
    while process.poll() is None:
        current_time = time.time()
        if current_time - subprocess_start_time > MAX_INACTIVITY_TIME:
            log(f'Subprocess for tag "{tag}" closed due to inactivity.')
            process.kill()
            break
        time.sleep(1)

while True:
    # Get the first tag with a status of "0"
    cursor.execute('SELECT name FROM tags WHERE complete = 0 LIMIT 1')
    row = cursor.fetchone()

    if row:
        tag = row[0]  # Assuming the "name" column is the first column in the query result
        log(f'Starting processing tag: {tag}')
    else:
        update_query = "UPDATE tags SET complete = 0;"
        cursor.execute(update_query)
        connection.commit()
        log('All tags processed. Resetting for a new run.')
        break

    # Bash command to execute
    command = ["/app/kyanite", "-t", tag]

    log(f'Starting subprocess for tag: {tag}')

    # Execute the Bash command and capture the output
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    subprocess_start_time = time.time()

    # Start the inactivity checker thread
    inactivity_thread = threading.Thread(target=inactivity_checker, args=(process, tag))
    inactivity_thread.start()

    for line in process.stdout:
        print(line, end='')
        subprocess_start_time = time.time()

    # Wait for the subprocess to finish and join the inactivity checker thread
    process.wait()
    inactivity_thread.join()

    log(f'Subprocess for tag "{tag}" finished with return code: {process.returncode}')

    # Only update database if subprocess completed without being killed by inactivity checker
    if process.returncode == 0:
        try:
            current_timestamp = datetime.now()  # Get the current timestamp
            cursor.execute("BEGIN")
            cursor.execute("UPDATE tags SET complete = 1, date = ? WHERE name = ?", (current_timestamp, tag))
            cursor.execute("COMMIT")
            log(f'Tag "{tag}" processed successfully.')
        except Exception as e:
            cursor.execute("ROLLBACK")
            error_message = f'Error processing tag "{tag}": {e}'
            log(error_message)

        connection.commit()
    elif process.returncode is not None:
        log(f'Subprocess for tag "{tag}" was terminated with return code: {process.returncode}')    

connection.close()
log_file.close()
