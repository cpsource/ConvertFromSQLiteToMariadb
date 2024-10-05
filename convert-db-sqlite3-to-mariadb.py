import os
import sys
from dotenv import load_dotenv
import sqlite3
import re
import mysql.connector

# Load dotenv
try:
    # Attempt to load dotenv file using the environment variable
    dotenv_config = load_dotenv(f"{os.getenv('HOME')}/.env")
    print("dotenv file loaded successfully.")
except Exception as e:
    # Handle any exceptions that may occur
    print(f"An error occurred while loading dotenv: {e}")

# Step 1: Dump SQLite3 table
def dump_sqlite_table(db_name, table_name, dump_file):
    conn = sqlite3.connect(db_name)
    with open(dump_file, 'w') as f:
        for line in conn.iterdump():
            if table_name in line:
                f.write(f'{line}\n')
    conn.close()

# Step 2: Convert SQLite dump to MariaDB-compatible SQL
def convert_sqlite_to_mariadb(dump_file, converted_file):
    with open(dump_file, 'r') as f, open(converted_file, 'w') as out:
        for line in f:
            # Convert AUTOINCREMENT to AUTO_INCREMENT
            line = re.sub(r'AUTOINCREMENT', 'AUTO_INCREMENT', line)

            # Convert INTEGER PRIMARY KEY to INT AUTO_INCREMENT PRIMARY KEY
            line = re.sub(r'INTEGER PRIMARY KEY', 'INT AUTO_INCREMENT PRIMARY KEY', line)

            # Replace double quotes with backticks for table and column names
            line = re.sub(r'"(.*?)"', r'`\1`', line)

            # Remove SQLite-specific commands (like PRAGMAs)
            if 'PRAGMA' in line or 'sqlite_sequence' in line or 'BEGIN TRANSACTION' in line or 'COMMIT' in line:
                continue

            # Write the modified SQL
            out.write(line)

# Step 3: Import into MariaDB
def import_to_mariadb(converted_file):
    conn = mysql.connector.connect(
        user=os.getenv('MARIADB_USER_NAME'),
        password=os.getenv('MARIADB_USER_PASSWORD'),
        host=os.getenv('MARIADB_USER_HOST'),
        port=os.getenv('MARIADB_USER_PORT'),
        database=os.getenv('MARIADB_USER_DATABASE')
    )

    cursor = conn.cursor()

    with open(converted_file, 'r') as f:
        sql_commands = f.read().split(';')  # Split SQL file into commands
        for command in sql_commands:
            if command.strip():  # Skip empty commands
                try:
                    cursor.execute(command)
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    print(f"Command failed: {command}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"SQL imported successfully into MariaDB database '{os.getenv('MARIADB_USER_DATABASE')}'")

# Main function to execute the process
def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <sqlite_db_path> <sqlite_table_name>")
        sys.exit(1)

    # Get database and table name from command-line arguments
    sqlite_db = sys.argv[1]  # First argument: SQLite DB file
    sqlite_table = sys.argv[2]  # Second argument: SQLite table name

    # Output files for SQL dumps
    sqlite_dump_file = 'sqlite_dump.sql'
    mariadb_converted_file = 'mariadb_dump.sql'

    # Step 1: Dump SQLite3 table
    dump_sqlite_table(sqlite_db, sqlite_table, sqlite_dump_file)

    # Step 2: Convert to MariaDB-compatible SQL
    convert_sqlite_to_mariadb(sqlite_dump_file, mariadb_converted_file)

    # Step 3: Import into MariaDB
    import_to_mariadb(mariadb_converted_file)

if __name__ == '__main__':
    main()

