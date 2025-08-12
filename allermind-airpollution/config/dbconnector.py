import psycopg2
from psycopg2 import sql

# Database connection details
DB_HOST = "localhost"  # Replace with your PostgreSQL host
DB_PORT = "5432"       # Default PostgreSQL port
DB_NAME = "ALLERMIND"  # Replace with your database name
DB_USER = "postgres"       # Replace with your username
DB_PASSWORD = "123456"   # Replace with your password
SCHEMA_NAME = "AIRPOLLUTION"

# Global connection and cursor
connection = None
cursor = None

# Function to establish and return a database connection
def initialize_db_connection():
    global connection, cursor
    try:
        if connection is None or cursor is None:
            connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            connection.autocommit = True
            cursor = connection.cursor()

            # Set schema
            cursor.execute(sql.SQL("SET search_path TO {};" ).format(sql.Identifier(SCHEMA_NAME)))
            print(f"Connected to schema: {SCHEMA_NAME}")

    except Exception as e:
        print(f"Error connecting to the database: {e}")

# Function to close the database connection
def close_db_connection():
    global connection, cursor
    if connection:
        connection.close()
        connection = None
        cursor = None
        print("Database connection closed.")

# Ensure connection is initialized
initialize_db_connection()