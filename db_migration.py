import sqlite3
import os
from logger import log
import config_loader
import sys

config = config_loader.load_config()

if config:
    DATABASE_DB = (config['Migrate']['database_db'])
else:
    log('Configuration not loaded.')
    sys.exit()

def has_version_table(DATABASE_DB):
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE_DB)
    cursor = conn.cursor()

    # Check if the "version" table exists in the database schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='version'")
    version_table_exists = cursor.fetchone() is not None

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    return version_table_exists

try:
    if not has_version_table(DATABASE_DB):
        log(f'Creating new versions table: {DATABASE_DB}')
        conn = sqlite3.connect(DATABASE_DB)
        cursor = conn.cursor()

        # Create the version table
        cursor.execute('''
            CREATE TABLE version (
                id INTEGER PRIMARY KEY,
                version TEXT
            )
        ''')

        # Insert initial version data
        cursor.execute("INSERT INTO version (version) VALUES ('0.0.0')")

        # Commit changes and close connection
        conn.commit()
        conn.close()

except Exception as e:
    log('DB Version Detection Error: {str(e)}')
    conn.close()
    sys.exit()

try:
    conn = sqlite3.connect(DATABASE_DB)
    cursor = conn.cursor()
    # Execute a query to select the version from the version table
    cursor.execute("SELECT version FROM version WHERE id = 1")

    version = cursor.fetchone()[0]

    if version == "0.0.0":
        cursor.execute('''ALTER TABLE tags ADD COLUMN running INTEGER DEFAULT 0''')
        cursor.execute("UPDATE version SET version = ('1.0.0') WHERE id = 1")

        conn.commit()
        conn.close()
        
        log('DB upgraded from 0.0.0 to 1.0.0')
    else:
        log('No available migrations.')

except sqlite3.Error as e:
    log("Error reading data from SQLite table:", e)

finally:
    conn.close()