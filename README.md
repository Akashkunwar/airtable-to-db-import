# Airtable to MySQL Table Migration

This Python script migrates data from an Airtable table to a MySQL database table. It uses the Pandas library to read data from the Airtable API and clean it up, then generates an appropriate SQL schema for the MySQL table. Finally, it inserts the data into the MySQL table in batches of 500 to optimize performance.

To use this script, you will need to provide your Airtable API key, base ID, and table name, as well as your MySQL database credentials and table name. 

## Dependencies

- `pymysql`: Python library to connect to MySQL database
- `pandas`: Python library to manipulate data
- `airtable-python-wrapper`: Python wrapper for Airtable API

## Usage

1. Install the required libraries: `pip install pymysql pandas airtable-python-wrapper`
2. Modify the script to include your API key, base ID, table name, and MySQL database credentials
3. Run the script using `python airtable_to_mysql.py`

## Notes

- This script assumes that all columns in the Airtable table will be of the `TEXT` data type in the MySQL table.
- If the batch insert fails for any reason, the script will insert data one row at a time.
- This script ignores any warning messages that may occur during the execution of the script.

