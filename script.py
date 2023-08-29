import sqlite3
import subprocess
import time
from datetime import datetime

# This creates a connection to a new or existing database file
connection = sqlite3.connect('database.db')

# A cursor is used to execute SQL commands and fetch results.
cursor = connection.cursor()

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
    for line in process.stdout:
        print(line, end='')

    # Wait for the subprocess to finish
    process.wait()

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
