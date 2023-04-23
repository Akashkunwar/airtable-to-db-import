# Import necessary libraries
import pymysql
import pandas as pd
from airtable import Airtable
import numpy as np
import warnings

# Ignore any warning messages
warnings.filterwarnings("ignore")

# Insert details
api_key = 'Your_Airtable_API_Key'
base_id = 'Your_Airtable_Base_ID'
AT_table_name = 'Your_Airtable_Table_Name'
view_name = 'View Name Normally = Grid view'
table_name = 'Your_Airtable_Table_Name'

# Connect to Airtable
airtable = Airtable(base_id, AT_table_name, api_key)

# Retrieve records from the specified Airtable view
records = airtable.get_all(view=view_name)

# Convert records to a pandas dataframe
df = pd.DataFrame([record['fields'] for record in records])

# Clean column names (remove white space)
df.columns = df.columns.str.strip()

# Replace white space with underscores in column names
new_columns = {col: col.replace(' ', '_') for col in df.columns}
df = df.rename(columns=new_columns)

# Convert all values in the dataframe to strings
df = df.astype(str)

# Get list of column names
col = list(df.columns)

# Generate SQL schema for the table with the appropriate data types
syn = ''
for x in col:
  syn = syn +"`"+ x +"`"+ ' TEXT NULL,'
schema = 'CREATE TABLE '+ table_name + ' ( '+syn[:-1]+");"

# Connect to MySQL database
conn = pymysql.connect(user='Your_username',
                       password='GXXXXXXXXXXXXXXXXG',
                       database='Your_DataBase_Name',
                       connect_timeout=6000,
                       host='mysql_host_name',
                       ssl={'ca': 'your_mysql_cert_path'})

# Try to create the table in the MySQL database using the generated schema
try:
  with conn.cursor() as cursor:
      cursor.execute(schema)
except:
  pass

# Fill any missing values with 'None'
df = df.fillna('None')

# Insert data into MySQL database in batches of 500
try:
  batch_size = 500
  rows = []
  cnt = len(df[col[0]])
  now = 0
  cursor = conn.cursor()
  for index, row in df.iterrows():
      rows.append(tuple(row))
      if len(rows) == batch_size:
          sql = "INSERT INTO {} VALUES ({})".format(table_name, ','.join(['%s']*len(df.columns)))
          cursor.executemany(sql, rows)
          now = now+500
          print("From ", cnt,'Total : ', now, 'is inserted.')
          conn.commit()
          rows = []
  if rows:
      cursor.executemany(sql, rows)
      now = now+500
      print("From ", cnt,'Total : ', now, 'is inserted.')
      conn.commit()

# If batch insert fails, insert data one row at a time
except:
  cnt = len(df[col[0]])
  now = 0
  cursor = conn.cursor()
  for index, row in df.iterrows():
      sql = "INSERT INTO {} VALUES ({})".format(table_name, ','.join(['%s']*len(df.columns)))
      cursor.execute(sql, tuple(row))
      now = now+1
      print("From ", cnt,'Total : ', now, 'is inserted.')
      conn.commit()
