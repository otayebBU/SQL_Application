#Step 1:  Load CSV Files into SQLLite.
#Objective: Understand the structure of CSV and how it maps to SQL tables.


#Write a function to inspect column names and data types. Generate and execute a CREATE TABLE statement dynamically.
#Use pandas and Python string formatting to build SQL. Key Concepts: Data type mapping (TEXT, INTEGER, REAL)

#load_to_SQL.py

import pandas as pd
import sqlite3
import os

# Load CSV
csv_file = 'data.csv'  
if not os.path.exists(csv_file):
    print(f"File {csv_file} does not exist!")
    exit()

df = pd.read_csv(csv_file)


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

 
cursor.execute('''
CREATE TABLE IF NOT EXISTS my_table (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    city TEXT
);
''')

# data
try:
    df.to_sql('my_table', conn, if_exists='append', index=False)
except Exception as e:
    print(f"Error inserting data: {e}")

# Query
try:
    for row in cursor.execute('SELECT * FROM my_table LIMIT 5'):
        print(row)
except Exception as e:
    print(f"Error querying data: {e}")

conn.close()

