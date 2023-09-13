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
                "date" INTEGER
            )
        ''')

        # Insert data from the original table into the new table, ordering by "name"
        cursor.execute('''
            INSERT INTO "tags_new" ("name", "complete", "date")
            SELECT "name", "complete", "date" FROM "tags"
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
    db_file = DATABASE_DB  # Replace with your database file path
    reorder_table(db_file)
