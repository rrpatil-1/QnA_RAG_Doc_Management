
from dotenv import load_dotenv
import os
import urllib
import psycopg2
from sqlalchemy import create_engine, text,MetaData
from sqlalchemy.exc import DBAPIError, OperationalError
from backend.utils.logger import CustomLogger

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
