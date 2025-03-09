from dotenv import load_dotenv
import os
import urllib
from sqlalchemy import create_engine, text,MetaData
from sqlalchemy.exc import DBAPIError, OperationalError
from backend.utils.logger import CustomLogger

# Load environment variables from.env file
load_dotenv()

logger = CustomLogger(logger_name=__name__)

# Define database connection parameters 
PASSWORD_POSTGRES = os.environ.get("PASSWORD_POSTGRES")
USERNAME_POSTGRES = os.environ.get("USERNAME_POSTGRES")
DATABASE_POSTGRES = os.environ.get("DATABASE_POSTGRES")
HOST_POSTGRES = os.environ.get("HOST_POSTGRES")
PORT_POSTGRES = os.environ.get("PORT_POSTGRES")
password_postgres = os.environ.get("PASSWORD_POSTGRES")
# SCHEME_POSTGRES = os.environ.get("SCHEME_POSTGRES")

encoded_password = password_postgres.encode('utf-8')
escape_password = urllib.parse.quote(encoded_password)

POSTGRESS_DB_URL = f"postgresql+psycopg://{USERNAME_POSTGRES}:{escape_password}@{HOST_POSTGRES}:{PORT_POSTGRES}/{DATABASE_POSTGRES}"


class PostgresConnection:
    engine = create_engine(POSTGRESS_DB_URL,isolation_level="READ COMMITTED",pool_size=5,max_overflow=20)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    conn = engine.connect()
    conn = conn.execution_options(autocommit=False)

    @classmethod
    def get_engine(cls):
        return PostgresConnection.engine
    
    @classmethod
    def get_connection(cls):
        return PostgresConnection.conn
    
    @classmethod
    def get_metadata(cls):
        return PostgresConnection.metadata
        
    

class DatabaseManager:
    connection  = PostgresConnection
    def __init__(self,connection,SCHEMA_POSTGRES):
    
        """
        Initialize the DatabaseManager class
        """
        self.connection = connection
        self.scheme_name = SCHEMA_POSTGRES

    def commit_transaction(*transaction):
        try:
            for trans in transaction[1]:
                trans.commit()
            logger.log(f"Committed { len(transaction[1])} transactions successfully", level="info")
        except (DBAPIError,OperationalError) as e:
            logger.log(f"Database error in commit_transaction: {e}", level="error")
            raise e
        except Exception as e:
            logger.log(f"Unexpected error in commit_transaction: {e}", level="error")
            raise e
    
    def rollback_transaction(*transaction):
        try:
            for trans in transaction[1]:
                trans.rollback()
        except Exception as e:
            logger.log(f"Error in rollback_transaction: {e}", level="error")
            raise e
    def execute_query(self,query):
        with self.connection.get_engine().connect() as conn:
            schema_qulaified_query = query.replace("<schema_name>", self.scheme_name)
            sql_query = text(schema_qulaified_query)
            result = conn.execute(sql_query)
            return result
        
    def read_data(self,query):
        with self.connection.get_engine().connect() as conn:
            schema_qulaified_query = query.replace("<schema_name>", self.scheme_name)
            sql_query = text(schema_qulaified_query)
            result = conn.execute(sql_query)
            data =  result.fetchall()
            return data
