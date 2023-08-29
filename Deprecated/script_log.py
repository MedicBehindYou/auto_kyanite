# Inactivity checker does not function on this version.

import sqlite3
import subprocess
import time
from datetime import datetime

# This creates a connection to a new or existing database file
connection = sqlite3.connect('database.db')

# A cursor is used to execute SQL commands and fetch results.
cursor = connection.cursor()

# Define the maximum inactivity time (in seconds) before considering the subprocess inactive
MAX_INACTIVITY_TIME = 300  # Adjust this value as needed

# Initialize log file
log_file = open('log.txt', 'a')

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'[{timestamp}] {message}\n'
    print(log_message, end='')
    log_file.write(log_message)
    log_file.flush()

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
    
    # Get the start time of the subprocess
    subprocess_start_time = time.time()

    for line in process.stdout:
        print(line, end='')

        # Update the subprocess start time to the current time as there's activity
        subprocess_start_time = time.time()

    # Wait for the subprocess to finish
    process.wait()

    # Calculate the time the subprocess was inactive
    inactivity_time = time.time() - subprocess_start_time

    # Check if the subprocess was inactive for too long
    if inactivity_time > MAX_INACTIVITY_TIME:
        log("Subprocess closed due to inactivity.")
    else:
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

connection.close()
log_file.close()
