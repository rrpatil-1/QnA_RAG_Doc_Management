# from backend.db_service.database_manager import DatabaseManager
from langchain_postgres.vectorstores import PGVector
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
import numpy as np
from sqlalchemy import create_engine, text
import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.db_service.vectordb.base import VectorDbServicesAbstract
from backend.utils.logger import CustomLogger
load_dotenv()

logger = CustomLogger()


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
        self.RETRIVE_DOC_LIMIT = int(os.getenv("DOC_LIMIT"))
        self.ollama_url = os.getenv("ollama_url")
        self.embeding_size = int(os.getenv("embedding_size"))
        connection_string = f"postgresql+psycopg://{self.USERNAME_POSTGRES}:{self.escape_password}@{self.HOST_POSTGRES}:{self.PORT_POSTGRES}/{self.DATABASE_POSTGRES}"
        

        self.engine = create_async_engine(connection_string,
            pool_size=20,  # Maximum number of connections in pool
            max_overflow=10,  # Allow 10 connections beyond pool_size
            pool_timeout=30,  # Seconds to wait for available connection
            pool_pre_ping=True,  # Verify connection before using
            pool_recycle=3600,  # Recycle connections after 1 hour
        )
        # Create async session factory
        self.async_session = sessionmaker(
            self.engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
        self.embeding= OllamaEmbeddings(model=self.model_name,base_url=self.ollama_url)
        # self.vectore_store = PGVector(connection=connection_string, embeddings=self.embeding, collection_name=self.collection_name ,use_jsonb=True,embedding_length=self.embeding_size)
        # Configure vector store with connection pool
        self.vectore_store = PGVector(
            connection=connection_string,
            embeddings=self.embeding,
            collection_name=self.collection_name,
            use_jsonb=True,
            embedding_length=self.embeding_size
        )

        self.vectore_store.create_tables_if_not_exists()


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
           logger.log(f"inserting embedding: {e}", level="error")
           raise f"error inserting embedding: {e}"
        

    async def search_similar_doc(self, query,limit=None,filter=None):
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
            if limit is None:
                limit = self.RETRIVE_DOC_LIMIT
            logger.log(f"limit: {limit}", level="info")
            # retriver = self.vectore_store.as_retriever(search_type="similarity_score_threshold",search_kwargs={"k": limit, "filter": filter,"score_threshold":0.5})
            retriver = self.vectore_store.as_retriever(search_type="mmr",search_kwargs={"k": limit, "filter": filter})
            
            response = retriver.invoke(query)
            return response
        except Exception as e:
            logger.log(f"error searching for similar doc: {e}", level="error")
            return f"error searching for similar doc: {e}"
        # try:
        #     docs = self.vectore_store.similarity_search_with_score(
        #         query=query,
        #         k=limit,  # Fetch more initially to allow for filtering
        #         filter=filter
        #     )
        #     logger.log(f"docs: {docs}", level="info")
        #     # Filter and sort results
        #     filtered_docs = []
        #     for doc, score in docs:
        #         # Convert cosine distance to similarity score (1 - distance)
        #         similarity = 1 - score
        #         print(similarity)
        #         if similarity >= 0.4:  # Adjust threshold as needed
        #             filtered_docs.append((doc, similarity))
            
        #     logger.log(f"filtered_docs: {filtered_docs}", level="info")
        #     # Sort by similarity score (highest first)
        #     filtered_docs.sort(key=lambda x: x[1], reverse=True)

        #     if filtered_docs:
        #         # Return only the top k results
        #         return [doc for doc, score in filtered_docs[:limit]]
        #     else:
        #         return []
            
        # except Exception as e:
        #     logger.log(f"error searching for similar doc: {e}", level="error")
        #     return f"error searching for similar doc: {e}"
        
    def delete_embedding(self, id, namespace):
        pass

    # def list_documents(self,query):
    #     """
    #     List all the documents in the database
    #     Returns:
    #         list: A list of all the documents in the database

    #     """
    #     try:
    #         with self.engine.connect() as connection:
    #             result = connection.execute(text(query))
    #             documents = result.fetchall()
    #             return documents
    
    #     except Exception as e:
    #         logger.log(f"Error listing documents: {e}", level="error")
    #         return f"error listing documents: {e}"
        
    async def list_documents(self, query):
        """
        List all the documents in the database asynchronously
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            list: A list of all the documents in the database
        """
        try:
            async with self.async_session() as session:
                # Execute query asynchronously
                result = await session.execute(text(query))
                # Fetch all results asynchronously
                documents = result.fetchall()
                return documents

        except Exception as e:
            logger.log(f"Error listing documents: {e}", level="error")
            raise Exception(f"Error listing documents: {e}")
        
    async def cleanup(self):
        """
        Cleanup database connections and resources
        """
        try:
            if hasattr(self, 'engine'):
                # Dispose of the SQLAlchemy engine
                await self.engine.dispose()
                
            # Clear any other resources
            self.vectore_store = None
            self.embeding = None
            
            logger.log("EmbeddingService cleanup completed successfully", level="info")
            
        except Exception as e:
            logger.log(f"Error during EmbeddingService cleanup: {e}", level="error")
            raise
        