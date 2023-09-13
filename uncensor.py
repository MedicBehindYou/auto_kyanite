import sqlite3
import datetime
import sys
import config_loader
from logger import log

config = config_loader.load_config()
if config:
    DATABASE_DB = config['Uncensor']['database_db']
else:
    log('Configuration not loaded.')
    sys.exit()

def uncensor(DATABASE_DB):

    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE_DB)
    cursor = conn.cursor()

    # Fetch all tags from the 'name' column
    cursor.execute("SELECT name FROM tags")
    tags = cursor.fetchall()

    # Create a set to store unique tags without ',uncensored'
    unique_tags = set()
    tags_with_uncensored = set()

    # Iterate through the tags and filter out those that match the criteria
    for row in tags:
        tag = row[0]
        if tag.endswith(',uncensored'):
            normalized_tag = tag[:-11]  # Remove the last 11 characters (',uncensored')
            tags_with_uncensored.add(normalized_tag)
        else:
            unique_tags.add(tag)

    # Exclude tags that have ',uncensored' counterparts
    unique_tags -= tags_with_uncensored

    # Insert new entries with ',uncensored' for unique tags
    for tag in unique_tags:
        new_tag = tag + ',uncensored'
        cursor.execute("INSERT INTO tags (name) VALUES (?)", (new_tag,))

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()

    # Log the process
    log('Unique tags without \',uncensored\' suffix added to the database.')

if __name__ == "__main__":
    # Example usage
    uncensor(DATABASE_DB)