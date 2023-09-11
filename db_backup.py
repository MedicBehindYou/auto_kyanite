# db_backup.py

import os
import shutil
import time
from logger import log  # Import the log function from the logger module

# Directory where backup files will be stored
BACKUP_DIR = '/config/backup/'

# Ensure the backup directory exists
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Function to create a backup of the database
def create_backup():
    try:
        # Generate a unique backup file name using a timestamp
        backup_file = f'{BACKUP_DIR}backup_{int(time.time())}.db'
        
        # Copy the current database file to the backup location
        shutil.copy('/config/database.db', backup_file)
        
        log(f'Database backed up to {backup_file}')
    except Exception as e:
        log(f'Error creating database backup: {e}')

# Function to manage backups and retain up to five backups
def manage_backups():
    try:
        # Get a list of backup files in the backup directory
        backups = [os.path.join(BACKUP_DIR, file) for file in os.listdir(BACKUP_DIR) if file.startswith('backup_')]
        
        # Sort the list by modification time (oldest first)
        backups.sort(key=lambda x: os.path.getmtime(x))
        
        # Check the number of backups
        if len(backups) >= 5:
            # Delete the oldest backup if there are more than five
            os.remove(backups[0])
            log(f'Oldest backup deleted: {backups[0]}')
        
        # Create a new backup
        create_backup()
    except Exception as e:
        log(f'Error managing backups: {e}')

if __name__ == "__main__":
    create_backup()  # Create a backup at the start of the script's run
    manage_backups()  # Manage backups to retain up to five
