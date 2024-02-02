# db_backup.py
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

import os
import shutil
import time
from logger import log  # Import the log function from the logger module
import config_loader

config = config_loader.load_config()

# Directory where backup files will be stored
BACKUP_DIR = '/config/backup/'

if config:
    BACKUP_DIR = (config['Backup']['backup_dir'])
    DATABASE_DB = (config['Backup']['database_db'])
    BACKUP_RETENTION = int(config['Backup']['backup_retention'])
else:
    log('Configuration not loaded.')
    sys.exit()

# Ensure the backup directory exists
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Function to create a backup of the database
def create_backup():
    try:
        # Generate a unique backup file name using a timestamp
        backup_file = f'{BACKUP_DIR}backup_{int(time.time())}.db'
        
        # Copy the current database file to the backup location
        shutil.copy(DATABASE_DB, backup_file)
        
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
        if len(backups) >= BACKUP_RETENTION:
            # Delete the oldest backup if there are more than the config.
            os.remove(backups[0])
            log(f'Oldest backup deleted: {backups[0]}')
        
        # Create a new backup
        create_backup()
    except Exception as e:
        log(f'Error managing backups: {e}')

if __name__ == "__main__":
    create_backup()  # Create a backup at the start of the script's run
    manage_backups()  # Manage backups to retain up to five
