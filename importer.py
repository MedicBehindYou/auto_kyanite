# tag_import.py

import sqlite3
from datetime import datetime
from logger import log  # Import the log function from the logger module
import config_loader

config = config_loader.load_config()

if config:
    DATABASE_DB = (config['Import']['database_db'])
    ENTRIES_TXT = (config['Import']['entries_txt'])
else:
    log('Configuration not loaded. Cannot perform backup and backup management.')
    sys.exit()

def bulk_import_tags(filename):
    try:
        # Create or connect to the 'database.db' SQLite database file
        connection = sqlite3.connect(DATABASE_DB)
        cursor = connection.cursor()

        # Read the entries from the text file and insert them into the 'tags' table
        with open(filename, 'r') as file:
            for line in file:
                entry = line.strip().replace('"', '')  # Remove quotes and strip whitespace
                cursor.execute("INSERT INTO tags (name, date) VALUES (?, ?)", (entry, 'N/A'))

        # Commit the changes and close the database connection
        connection.commit()
        connection.close()

        log(f'Entries from "{filename}" imported successfully.')
    except Exception as e:
        log(f'Error bulk importing entries from "{filename}": {e}')

def single_import(name):
    try:
        # Create or connect to the 'database.db' SQLite database file
        connection = sqlite3.connect(DATABASE_DB)
        cursor = connection.cursor()

        # Insert a single entry into the 'tags' table
        sanitized_name = name.strip().replace('"', '')  # Remove quotes and strip whitespace
        cursor.execute("INSERT INTO tags (name, date) VALUES (?, ?)", (sanitized_name, 'N/A'))

        # Commit the changes and close the database connection
        connection.commit()
        connection.close()

        log(f'Single entry "{sanitized_name}" imported successfully.')
    except Exception as e:
        log(f'Error importing single entry "{name}": {e}')

if __name__ == "__main__":
    import_tags(ENTRIES_TXT)
