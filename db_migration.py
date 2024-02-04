# db_migration.py
#    auto_kyanite
#    Copyright (C) 2023  MedicBehindYou
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sqlite3
import os
from logger import log
import config_loader
import sys
from db_backup import create_backup, manage_backups

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

def current_version():
    conn = sqlite3.connect(DATABASE_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT version FROM version WHERE id = 1")
    version = cursor.fetchone()[0]
    return version

def migrate():
    try:
        if not has_version_table(DATABASE_DB):
            create_backup()
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
        log('DB Version Detection Error: ', e)
        conn.close()
        sys.exit()

    try:
        conn = sqlite3.connect(DATABASE_DB)
        cursor = conn.cursor()
        # Execute a query to select the version from the version table
        cursor.execute("SELECT version FROM version WHERE id = 1")

        version = cursor.fetchone()[0]

        if version == "0.0.0":
            create_backup()
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

if __name__ == "__main__":
    migrate()