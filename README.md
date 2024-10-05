
# SQLite to MariaDB Migration Script

This script automates the process of dumping a table from an SQLite3 database, converting it to a MariaDB-compatible format, and importing it into a MariaDB database. The script can be run from the command line with arguments specifying the SQLite database file and the table name.

## Prerequisites

### 1. Environment Variables
The script requires several environment variables for connecting to the MariaDB database. These should be defined in a `.env` file located in the user's home directory (`$HOME/.env`).

The required environment variables are:

- `MARIADB_USER_NAME` – The MariaDB username.
- `MARIADB_USER_PASSWORD` – The MariaDB password.
- `MARIADB_USER_HOST` – The MariaDB host (e.g., `localhost` or IP address).
- `MARIADB_USER_PORT` – The port for connecting to MariaDB (e.g., `3306`).
- `MARIADB_USER_DATABASE` – The target MariaDB database where the table will be imported.

### 2. Dependencies

Ensure that the following Python packages are installed:

- `sqlite3` (part of the standard Python library)
- `mysql-connector-python` (for connecting to MariaDB)
- `python-dotenv` (for loading environment variables from `.env`)

You can install the dependencies with:

```bash
pip install mysql-connector-python python-dotenv
```

## Usage

### Command-Line Arguments

This script accepts two command-line arguments:

1. **SQLite3 Database File Path**: The path to the SQLite3 database file.
2. **Table Name**: The name of the table to be migrated.

### Running the Script

Run the script as follows:

```bash
python script.py <sqlite_db_path> <sqlite_table_name>
```

For example:

```bash
python script.py /path/to/your_sqlite_db.db your_table_name
```

### Example:

```bash
python script.py /var/data/fail3ban_server.db threat_table
```

### What the Script Does:

1. **Step 1**: Dumps the specified table from the SQLite3 database into an SQL file (`sqlite_dump.sql`).
2. **Step 2**: Converts the SQL dump into a MariaDB-compatible format and saves it as `mariadb_dump.sql`.
3. **Step 3**: Imports the converted SQL dump into the MariaDB database specified in the environment variables.

### Output:

- The SQLite dump is saved in `sqlite_dump.sql`.
- The MariaDB-compatible SQL dump is saved in `mariadb_dump.sql`.
- The table is imported into the MariaDB database specified in the `.env` file.

## Error Handling

- If any SQL command fails during the import to MariaDB, the error message and failed command are printed.
- Ensure that the SQLite database and table exist before running the script.
- The `.env` file must be correctly configured with the appropriate MariaDB connection details.

## Logging

The script prints the following to the console:

- Success messages for loading environment variables and completing various steps.
- Error messages if any issues arise during execution (e.g., connection problems, SQL execution errors).

## Troubleshooting

1. **Environment Variables Not Loaded**: 
   If the `.env` file is not loaded correctly, check that the file exists in the home directory (`$HOME/.env`) and contains the required environment variables.

2. **MariaDB Connection Issues**: 
   If the connection to MariaDB fails, verify that the host, port, username, password, and database are correct in the `.env` file.

3. **SQLite Table Not Found**: 
   If the specified SQLite table is not found, ensure the table name is correct and exists in the provided SQLite database.

## License

This script is provided "as-is" without any express or implied warranties.

---

This `README.md` should help a system administrator understand how to use your script effectively. Let me know if you need any modifications! (This script and doc was written by ChatGPT 4.o in about ten minutes with some prompts from @cpsource.)

