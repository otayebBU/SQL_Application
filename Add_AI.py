#Step 5:  Add AI to generate SQL
# Add_AI.py

#Pass table schema and user request to an LLM. Let AI generate SQL and execute it. Display results and optionally the generated SQL.
# Key Concepts: Prompt engineering, schema context, LLM integration
import openai
import sqlite3
import os


openai.api_key = os.getenv("OPENAI_API_KEY")  # Store your API key securely

def generate_sql_from_prompt(prompt, schema_info):
    """
    Generates SQL query based on user prompt and database schema information.
    """
    full_prompt = f"""
    You are an AI assistant tasked with converting user queries into SQL statements.
    The database uses SQLite and contains the following tables:
    {schema_info}

    User Query: "{prompt}"

    Generate a valid SQLite SQL query.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can use "gpt-3.5-turbo" or "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating SQL queries."},
                {"role": "user", "content": full_prompt}
            ]
        )
        
        sql_query = response["choices"][0]["message"]["content"].strip()
        return sql_query
    except openai.error.OpenAIError as e:
        print(f"Error generating SQL: {e}")
        return None

def run_cli_with_ai():
    """
    Runs a command-line interface (CLI) for interacting with the AI and database.
    """
    conn = sqlite3.connect('database.db')
    while True:
        user_input = input("Ask me a question about the data (or type 'exit' to quit): ").strip()

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        schema_info = get_schema_info(conn)
        sql_query = generate_sql_from_prompt(user_input, schema_info)

        if sql_query:
            print("\nGenerated SQL:")
            print(sql_query)

            try:
                cursor = conn.execute(sql_query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except Exception as e:
                print(f"Error running SQL: {e}")
        else:
            print("Failed to generate SQL. Please try again.")

    conn.close()

def get_schema_info(conn):
    """
    Retrieves schema information for all tables in the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema = ""
    for table_name in tables:
        table = table_name[0]
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        column_info = ", ".join([col[1] for col in columns])
        schema += f"- {table} ({column_info})\n"
    return schema

if __name__ == "__main__":
    run_cli_with_ai()
