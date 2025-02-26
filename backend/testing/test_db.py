
from langchain_core.documents import Document
from backend.db_service.database_manager import DatabaseManager
from backend.db_service.vectordb.embedding_service.service import EmbeddingService


def main():
    try:
        emb = EmbeddingService()
        vector = emb.create_embedding("hello world")
        print(len(vector))

        res = emb.insert_embedding([Document(page_content="there are cat in ponds and dogs in home", metadata={"source": "test3"})])
        print(res)

        doc = emb.search_similar_doc("what is capital of india?")
        print(doc)
        print(len(doc))
        
    except Exception as e:
        print(e)