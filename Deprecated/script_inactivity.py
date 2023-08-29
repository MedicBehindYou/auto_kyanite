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

while True:
    # Get the first tag with a status of "0"
    cursor.execute('SELECT name FROM tags WHERE complete = 0 LIMIT 1')
    row = cursor.fetchone()

    print(row)

    if row:
        tag = row[0]  # Assuming the "name" column is the first column in the query result
    else:
        update_query = "UPDATE tags SET complete = 0;"
        cursor.execute(update_query)
        connection.commit()
        break

    # Bash command to execute
    command = ["/app/kyanite", "-t", tag]

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
        print("Subprocess closed due to inactivity.")
    else:
        try:
            current_timestamp = datetime.now()  # Get the current timestamp
            cursor.execute("BEGIN")
            cursor.execute("UPDATE tags SET complete = 1, date = ? WHERE name = ?", (current_timestamp, tag))
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print("Error:", e)

    connection.commit()

connection.close()
