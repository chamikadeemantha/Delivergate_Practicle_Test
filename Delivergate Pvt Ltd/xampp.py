import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, DateTime
import pymysql

# MySQL Database Connection Parameters
MYSQL_USER = 'root'  
MYSQL_PASSWORD = ''  # Empty password as per XAMPP config
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'delivergatedb'

# Create a connection string
db_connection_str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
engine = create_engine(db_connection_str)

# File paths for the CSVs
customers_file_path = r'C:\Users\User\Desktop\Delivergate Pvt Ltd\customers.csv'
orders_file_path = r'C:\Users\User\Desktop\Delivergate Pvt Ltd\order.csv'

# Load CSV files into DataFrames
customers_df = pd.read_csv(customers_file_path, usecols=['customer_id', 'name'])  # Only keep relevant columns
orders_df = pd.read_csv(orders_file_path, usecols=['id', 'customer_id', 'total_amount', 'created_at'])  # Only keep relevant columns

# Rename columns to match the database schema
customers_df = customers_df.rename(columns={'name': 'customer_name'})
orders_df = orders_df.rename(columns={'id': 'order_id', 'created_at': 'order_date'})

# Prepare the metadata for creating tables
metadata = MetaData()

# Define the Customers table
customers_table = Table(
    'customers', metadata,
    Column('customer_id', Integer, primary_key=True),
    Column('customer_name', String(255))
)

# Define the Orders table
orders_table = Table(
    'orders', metadata,
    Column('order_id', Integer, primary_key=True),
    Column('customer_id', Integer),
    Column('total_amount', Float),
    Column('order_date', DateTime)
)

# Create tables in the MySQL database
metadata.create_all(engine)

# Insert data into customers table
customers_df.to_sql('customers', con=engine, if_exists='append', index=False)

# Insert data into orders table
orders_df.to_sql('orders', con=engine, if_exists='append', index=False)

print("Data has been imported into the MySQL database successfully!")
