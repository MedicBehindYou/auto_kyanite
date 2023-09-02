# db_setup.py

import sqlite3
import sys
from logger import log  # Import the log function from the logger module

def setup_database():
    try:
        # Create or connect to the 'database.db' SQLite database file
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Create the 'tags' table with the specified columns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                complete INTEGER DEFAULT 0,
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Commit the changes and close the database connection
        connection.commit()
        connection.close()

        log('Database setup completed.')
    except Exception as e:
        log(f'Error setting up the database: {e}')
        sys.exit(1)  # Exit with an error code if there was an error

if __name__ == "__main__":
    setup_database()

