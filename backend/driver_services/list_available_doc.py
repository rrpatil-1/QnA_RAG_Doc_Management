import os

from jinja2 import Template

from backend.db_service.vectordb.embedding_service.service import EmbeddingService
from backend.utils.logger import CustomLogger
logger = CustomLogger()

file = os.path.join(os.getcwd(), "backend", "db_service", "sql", "get_doc_list.sql")


class ListDocuments:
    def __init__(self):
        self.file = file
        
        self.embeding = EmbeddingService()
    async def get_doc_list(self):
        """
        Fetch all documents from the database and return them as a list.
        """
        try:
            logger.log(f"Reading sql file {self.file}", level="info")
            template = Template(open(self.file).read())
            sql=template.render()
            result =  await self.embeding.list_documents(sql)
            return result
        except Exception as e:
            strerror =  f"error while fetching documents: {e}"
            raise strerror
    async def cleanup(self):
        await self.embeding.cleanup()