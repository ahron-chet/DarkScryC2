import psycopg2
import json
import os

# Database connection parameters
DB_NAME = "darkscryc2managment"
USER = "postgres"
PASSWORD = "DarkScry2025!"
HOST = "localhost"  # or use '127.0.0.1'
PORT = "5432"  # Default PostgreSQL port

# Path to save the JSON files
OUTPUT_DIR = "/home/dbexport"

# Make sure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

    cursor = connection.cursor()

    # Get list of all tables in the public schema
    cursor.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public';
    """)
    tables = cursor.fetchall()

    # Loop through each table and export to JSON
    for table in tables:
        table_name = table[0]
        print(f"Exporting table {table_name} to JSON...")

        # Fetch all rows from the current table
        cursor.execute(f"SELECT row_to_json({table_name}) FROM {table_name};")
        rows = cursor.fetchall()

        # Write the rows as JSON to a file
        with open(os.path.join(OUTPUT_DIR, f"{table_name}.json"), "w") as json_file:
            json.dump([row[0] for row in rows], json_file, indent=4)

    print("Export complete!")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
