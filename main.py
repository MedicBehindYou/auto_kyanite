# kyanite_db.py
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
import subprocess
import threading
import time
import sys
import os
import config_loader
from datetime import datetime
from logger import log
from importer import bulk_import_tags, single_import
from db_setup import setup_database
from db_backup import create_backup, manage_backups
from organize import reorder_table
from uncensor import uncensor
from db_migration import has_version_table, current_version, migrate
from no_ai import no_ai

config = config_loader.load_config()
row_lock = threading.Lock()

if config:
    MAX_INACTIVITY_TIME = float(config['Main']['max_inactivity_time'])  # Convert to float
    DATABASE_DB = (config['Import']['database_db'])
    LOG_TXT = (config['Main']['log_txt'])    
else:
    log('Configuration not loaded.')
    sys.exit()

if not os.path.exists(DATABASE_DB):
    setup_database()


if not has_version_table(DATABASE_DB):
    migrate()
if current_version() != "1.0.0":
    migrateYN = input('DB is currently out of date. Run migration (y/n): ')
    if migrateYN == 'y' or migrateYN == 'Y':
        migrate()
    elif migrateYN == 'n' or migrateYN == 'N':
        print('Migration canceled, closing.')
        sys.exit()
    else:
        print('Invalid option.')
        sys.exit()  

if len(sys.argv) > 1 and sys.argv[1] == "--setup":
    setup_database()
    sys.exit()

if len(sys.argv) > 1 and sys.argv[1] == "--bulk":
    if len(sys.argv) > 2:
        create_backup()
        bulk_import_tags(sys.argv[2]) 
        manage_backups()
    else:
        bulk_import_tags('/config/entries.txt') 
    sys.exit()    

if len(sys.argv) > 1 and sys.argv[1] == "--single":
    if len(sys.argv) > 2:
        create_backup()
        single_import(sys.argv[2]) 
        manage_backups()
    else:
        print("Usage: --single <tag_name>")
    sys.exit()

if len(sys.argv) > 1 and sys.argv[1] == "--organize":
    create_backup()
    reorder_table(DATABASE_DB)
    manage_backups()
    sys.exit()

if len(sys.argv) > 1 and sys.argv[1] == "--uncensor":
    create_backup()
    uncensor(DATABASE_DB)
    manage_backups()
    sys.exit()

if len(sys.argv) > 1 and sys.argv[1] == "--no_ai":
    create_backup()
    no_ai(DATABASE_DB)
    manage_backups()
    sys.exit()

reverse_mode = False
if "-rev" in sys.argv or "--reverse" in sys.argv:
    reverse_mode = True

try:
    create_backup()

    connection = sqlite3.connect(DATABASE_DB)

    cursor = connection.cursor()

    log_file = open(LOG_TXT, 'a')

    def inactivity_checker(process, tag):
        while process.poll() is None:
            current_time = time.time()
            if current_time - subprocess_start_time > MAX_INACTIVITY_TIME:
                log(f'Subprocess for tag "{tag}" closed due to inactivity.')
                process.kill()
                break
            time.sleep(1)

    while True:
        with row_lock:
            if reverse_mode:
                cursor.execute('SELECT name FROM tags WHERE complete = 0 AND running <> 1 ORDER BY ROWID DESC LIMIT 1')
            else:
                cursor.execute('SELECT name FROM tags WHERE complete = 0 AND running <> 1 LIMIT 1')
            
            row = cursor.fetchone()

        if row:
            tag = row[0]
            log(f'Starting processing tag: {tag}')
            cursor.execute("UPDATE tags SET running = '1' WHERE name = ?", row)
            connection.commit()
        else:
            update_query = "UPDATE tags SET complete = 0 WHERE running != 1;"
            cursor.execute(update_query)
            connection.commit()
            log('All tags processed. Resetting for a new run.')
            break

        command = ["/app/kyanite", "-t", tag]

        log(f'Starting subprocess for tag: {tag}')

        process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        subprocess_start_time = time.time()

        inactivity_thread = threading.Thread(target=inactivity_checker, args=(process, tag))
        inactivity_thread.start()

        for line in process.stdout:
            print(line, end='')
            subprocess_start_time = time.time()

        process.wait()
        inactivity_thread.join()

        log(f'Subprocess for tag "{tag}" finished with return code: {process.returncode}')

        if process.returncode == 0:
            try:
                current_timestamp = datetime.now()
                cursor.execute("UPDATE tags SET complete = 1, date = ? WHERE name = ?", (current_timestamp, tag))
                cursor.execute("UPDATE tags SET running = '0' WHERE name = ?", row)
                connection.commit()
                log(f'Tag "{tag}" processed successfully.')
            except Exception as e:
                cursor.execute("ROLLBACK")
                error_message = f'Error processing tag "{tag}": {e}'
                log(error_message)
            else:
                connection.commit()
        elif process.returncode == -9:
            with row_lock:
                cursor.execute("UPDATE tags SET running = '0' WHERE name = ?", row)
                connection.commit()
        elif process.returncode is not None:
            log(f'Subprocess for tag "{tag}" was terminated with return code: {process.returncode}')    
        else:
            cursor.execute("UPDATE tags SET running = '0' WHERE name = ?", row)
            connection.commit()

finally:
    if row is not None:
        cursor.execute("UPDATE tags SET running = '0' WHERE name = ?", row)
        connection.commit()
    manage_backups()

    connection.close()
    log_file.close()
