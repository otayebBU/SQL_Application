#Step 4:  Simulate AI using input (the input to be schemas)
#AI_Sim.py

#Use a loop with input() to simulate chatbot-like interaction. Allow users to load CSV files, run SQL queries, or exit.
#Provide table listing functionality using sqlite_master. Key Concepts: Control flow, CLI design, user experience

import sqlite3
import conflicts

def run_cli():
    conn = sqlite3.connect('database.db')
    while True:
        user_input = input("Enter command (load/query/list/exit): ").strip().lower()

        if user_input == 'load':
            csv_file = input("Enter CSV file name: ")
            table_name = input("Enter table name: ")
            conflicts.create_table_with_conflict_handling(csv_file, table_name, conn)

        elif user_input == 'query':
            sql_query = input("Enter your SQL query: ")
            try:
                cursor = conn.execute(sql_query)
                for row in cursor.fetchall():
                    print(row)
            except Exception as e:
                print(f"Query failed: {e}")

        elif user_input == 'list':
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in cursor.fetchall()]
            print("Tables:", tables)

        elif user_input == 'exit':
            print("Goodbye!")
            break
        else:
            print("Unknown command!")

    conn.close()


run_cli()
