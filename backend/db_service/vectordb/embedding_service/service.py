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
load_dotenv()

RETRIVE_DOC_LIMIT = int(os.getenv("DOC_LIMIT"))

class EmbeddingService(VectorDbServicesAbstract):
    def __init__(self):
        self.PASSWORD_POSTGRES = os.getenv("PASSWORD_POSTGRES")
        self.USERNAME_POSTGRES = os.getenv("USERNAME_POSTGRES")
        self.DATABASE_POSTGRES = os.getenv("DATABASE_POSTGRES")
        self.HOST_POSTGRES = os.getenv("HOST_POSTGRES")
        self.PORT_POSTGRES = os.getenv("PORT_POSTGRES")
        self.escape_password = urllib.parse.quote(self.PASSWORD_POSTGRES)
        self.collection_name = os.getenv("collection_name")
        self.model_name = os.getenv("ollama_model")


        connection_string = f"postgresql+psycopg://{self.USERNAME_POSTGRES}:{self.escape_password}@{self.HOST_POSTGRES}:{self.PORT_POSTGRES}/{self.DATABASE_POSTGRES}"
        
        self.embeding= OllamaEmbeddings(model=self.model_name)

        self.vectore_store = PGVector(connection=connection_string, embeddings=self.embeding, collection_name=self.collection_name ,use_jsonb=True)
        self.engine = create_engine(connection_string)

    def create_embedding(self, text):
        return self.embeding.embed_query(text)

    async def insert_embedding(self, Document_list):
        # vectore_sore.add_documents([Document(page_content="there are cat in ponds", metadata={"source": "test"})])
        return self.vectore_store.add_documents(Document_list)
        

    def search_similar_doc(self, query,limit=RETRIVE_DOC_LIMIT,filter=None):
        similar = self.vectore_store.similarity_search_with_score(query,k=limit,filter=filter)
        return similar

    def delete_embedding(self, id, namespace):
        pass

    def list_documents(self):
        
        with self.engine.connect() as connection:
            result = connection.execute(text(f"SELECT DISTINCT(metadata->>'source') FROM documents"))
            documents = result.fetchall()
            return documents