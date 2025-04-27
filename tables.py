#Step 2:  Create Tables Dynamically from CSV
#tabel.py

#Use PRAGMA table_info() to detect existing table schema. Prompt user on schema conflict: overwrite, rename, or skip.
#Implement error logging to a file (error_log.txt). Key Concepts: Defensive coding, logging, user input control

import pandas as pd
import sqlite3
import re

def infer_sql_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "REAL"
    elif pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATE"
    else:
        return "TEXT"

def create_table_from_csv(csv_file, table_name, conn):
    if not re.match("^[A-Za-z0-9_]+$", table_name):
        print("Invalid table name! Use only letters, numbers, and underscores.")
        return
    
    df = pd.read_csv(csv_file)
    columns = df.dtypes

    fields = []
    for col_name, dtype in columns.items():
        sql_type = infer_sql_type(dtype)
        fields.append(f'"{col_name}" {sql_type}')

    create_stmt = f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(fields)});'
    try:
        conn.execute(create_stmt)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Table '{table_name}' created and data inserted!")
    except Exception as e:
        print(f"Error creating table: {e}")


conn = sqlite3.connect('database.db')
create_table_from_csv('your_file.csv', 'auto_table', conn)
conn.close()


