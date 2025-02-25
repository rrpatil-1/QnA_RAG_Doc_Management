# from backend.db_service.database_manager import DatabaseManager
from langchain_postgres.vectorstores import PGVector
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from sqlalchemy import create_engine, text
import os
import urllib.parse
from dotenv import load_dotenv

from backend.db_service.vectordb.base import VectorDbServicesAbstract
from backend.utils.logger import CustomLogger
load_dotenv()

logger = CustomLogger()
RETRIVE_DOC_LIMIT = int(os.getenv("DOC_LIMIT"))

class EmbeddingService(VectorDbServicesAbstract):
    def __init__(self):

        """
        Initialize the EmbeddingService class
        """
        self.PASSWORD_POSTGRES = os.getenv("PASSWORD_POSTGRES")
        self.USERNAME_POSTGRES = os.getenv("USERNAME_POSTGRES")
        self.DATABASE_POSTGRES = os.getenv("DATABASE_POSTGRES")
        self.HOST_POSTGRES = os.getenv("HOST_POSTGRES")
        self.PORT_POSTGRES = os.getenv("PORT_POSTGRES")
        self.escape_password = urllib.parse.quote(self.PASSWORD_POSTGRES)
        self.collection_name = os.getenv("collection_name")
        self.model_name = os.getenv("ollama_model")

        self.embeding = os.getenv("embedding_size")
        connection_string = f"postgresql+psycopg://{self.USERNAME_POSTGRES}:{self.escape_password}@{self.HOST_POSTGRES}:{self.PORT_POSTGRES}/{self.DATABASE_POSTGRES}"
        
        self.embeding= OllamaEmbeddings(model=self.model_name)

        self.vectore_store = PGVector(connection=connection_string, embeddings=self.embeding, collection_name=self.collection_name ,use_jsonb=True,embedding_length=self.embeding)
        self.vectore_store.create_tables_if_not_exists()
        self.engine = create_engine(connection_string)


    def create_embedding(self, text):
        """
        Create an embedding for the input text
        Args:
            text (str): The text to create embeddings for
        
        Returns:
            list: The embedding for the input text

        
        """
        return self.embeding.embed_query(text)

    def insert_embedding(self, Document_list):
        
        """
        Insert the embedding for the input text into the database
        
        Args:
            Document_list (list): The list of documents to insert
        Returns:
                 None
        """
        try:
            
            resp =  self.vectore_store.add_documents(Document_list)
            return resp
        except Exception as e:
           return f"Error inserting embedding: {e}"
        

    def search_similar_doc(self, query,limit=RETRIVE_DOC_LIMIT,filter=None):
        """
        Search for similar documents in the database
        querying with the input text   
        default limit is 5
        returns the top k similar documents
        Args:
            query (str): The input text to search
            limit (int): The maximum number of similar documents to return
            filter (dict): The filter to apply to the search
        Returns:
            list: A list of similar documents
        
        """
        try:
            retriver = self.vectore_store.as_retriever(search_type="similarity_score_threshold",search_kwargs={"k": limit, "filter": filter,"score_threshold":0.8})
            response = retriver.invoke(query)
            return response
        except Exception as e:
            logger.log(f"error searching for similar doc: {e}", level="error")
            return f"error searching for similar doc: {e}"

    def delete_embedding(self, id, namespace):
        pass

    def list_documents(self):
        """
        List all the documents in the database
        Returns:
            list: A list of all the documents in the database

        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(f"SELECT DISTINCT(langchain_pg_embedding.cmetadata->>'source') FROM langchain_pg_embedding"))
                documents = result.fetchall()
                return documents
    
        except Exception as e:
            logger.log(f"Error listing documents: {e}", level="error")
            return f"Error listing documents: {e}"