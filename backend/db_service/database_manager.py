import psycopg2
from dotenv import load_dotenv
import os
import urllib

from backend.utils.logger import CustomLogger

# Load environment variables from.env file
load_dotenv()

logger = CustomLogger(logger_name=__name__)

# Define database connection parameters 
PASSWORD_POSTGRES = os.getenv("PASSWORD_POSTGRES")
USERNAME_POSTGRES = os.getenv("USERNAME_POSTGRES")
DATABASE_POSTGRES = os.getenv("DATABASE_POSTGRES")
HOST_POSTGRES = os.getenv("HOST_POSTGRES")
PORT_POSTGRES = os.getenv("PORT_POSTGRES")
password_postgres = os.getenv("PASSWORD_POSTGRES")

encoded_password = password_postgres.encode('utf-8')
escape_password = urllib.parse.quote(encoded_password)



class PostgresConnection:
    def __init__(self):
        self.host = HOST_POSTGRES
        self.database = DATABASE_POSTGRES
        self.user = USERNAME_POSTGRES
        self.password = escape_password
        self.port = PORT_POSTGRES
        self.isolation_level = "READ_COMMITTED"
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
                
            )
        except Exception as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.fetchall()

class DatabaseManager:
    connection = PostgresConnection
    def __init__(self, connection,SCHEME_POSTGRES):
        self.connection = connection.connect()
        self.scheme_name = SCHEME_POSTGRES

    def create_table(self, table_name, schema):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});"
        self.connection.execute_query(query)

    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.connection.execute_query(query, list(data.values()))

    def fetch_data(self, table_name, conditions=None):
        query = f"SELECT * FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        return self.connection.execute_query(query)

# # Usage example
# if __name__ == "__main__":
#     conn = PostgresConnection(host="localhost", database="mydb", user="user", password="password")
#     conn.connect()
#     db_manager = DatabaseManager(conn)
#     db_manager.create_table("example_table", "id SERIAL PRIMARY KEY, name VARCHAR(100)")
#     db_manager.insert_data("example_table", {"name": "John Doe"})
#     data = db_manager.fetch_data("example_table")
#     print(data)
#     conn.close()
