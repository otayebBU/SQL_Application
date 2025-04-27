#Step 3:  Handle Schema Conflicts
#conflicts.py

#Use PRAGMA table_info() to detect existing table schema. Prompt user on schema conflict: overwrite, rename, or skip.
#Implement error logging to a file (error_log.txt). Key Concepts: Defensive coding, logging, user input control

import os
import sqlite3
import tables

def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name=?;
    """, (table_name,))
    return cursor.fetchone() is not None

def create_table_with_conflict_handling(csv_file, table_name, conn):
    if table_exists(conn, table_name):
        action = input(f"Table '{table_name}' exists. Overwrite (o), Rename (r), or Skip (s)? ").lower()
        if action == 'o':
            conn.execute(f"DROP TABLE IF EXISTS {table_name};")
        elif action == 'r':
            table_name += "_new"
        elif action == 's':
            print("Skipping table creation.")
            return
        else:
            with open('error_log.txt', 'a') as f:
                f.write(f"Invalid action for table {table_name}\n")
            print("Invalid action logged.")
            return
    
    tables.create_table_from_csv(csv_file, table_name, conn)

conn = sqlite3.connect('database.db')
create_table_with_conflict_handling('your_file.csv', 'auto_table', conn)
conn.close()
