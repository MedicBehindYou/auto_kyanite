# organize.py
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
import logging
from logger import log
import config_loader

config = config_loader.load_config()

if config:
    DATABASE_DB = (config['Organize']['database_db'])
else:
    log('Configuration not loaded.')
    sys.exit()


def reorder_table(db_file):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create a new table with the desired schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "tags_new" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "name" TEXT,
                "complete" INTEGER DEFAULT 0,
                "date" INTEGER,
                "running" INTEGER DEFAULT 0
            )
        ''')

        # Insert data from the original table into the new table, ordering by "name"
        cursor.execute('''
            INSERT INTO "tags_new" ("name", "complete", "date", "running")
            SELECT "name", "complete", "date", "running" FROM "tags"
            ORDER BY "name" ASC
        ''')

        # Drop the original table
        cursor.execute('DROP TABLE IF EXISTS "tags"')

        # Rename the new table to the original table name
        cursor.execute('ALTER TABLE "tags_new" RENAME TO "tags"')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Log success using the log function from logger.py
        log('Table "tags" reordered successfully.')

    except sqlite3.Error as e:
        # Log the error using the log function from logger.py
        log(f'Error reordering the table: {str(e)}')

if __name__ == "__main__":
    db_file = DATABASE_DB 
    reorder_table(db_file)
