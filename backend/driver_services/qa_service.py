import asyncio
import os
from backend.llm_service.Ollama.llm_processing import OllamaService
from backend.db_service.vectordb.embedding_service.service import EmbeddingService
from dotenv import load_dotenv
import json

from backend.utils.logger import CustomLogger

logger = CustomLogger()

load_dotenv()
file = os.path.join(os.getcwd(), "prompts\\qa_prompt.json")

class QAService:
    def __init__(self):
        self.llm_service = OllamaService()
        self.embedding_service = EmbeddingService()
        self.file = file
    def get_context(self, query: str,docs:None|dict):
        try:
            logger.log(f"searcing for context for: {query}", level="info")
            
            similar_docs = self.embedding_service.search_similar_doc(query,filter=docs)
            if type(similar_docs) is str:
                raise Exception(similar_docs)
            
            logger.log(f"found {len(similar_docs)} similar docs", level="info")
            
            if len(similar_docs) == 0:
                return []
            # Extract the content of each similar document for context.
            context = '\n'.join([similar_docs[i][0].page_content for i in range(len(similar_docs))])

            return context
        except Exception as e:
            logger.log(f"error getting context: {e}", level="error")
            return f"error: {e}"
        
    async def get_answer(self, question:str,docs=None):
        try:
            with open(self.file,'r') as f:
                prompt_json  = json.load(f)
                prompt = prompt_json['system']            
            context = self.get_context(question,docs)
            if type(context) is str and context.startswith("error"):
                raise Exception(context)
            
            response = await self.llm_service.a_generate_response(
            messages=question,
            prompt=prompt,
            context=context
        )
            return response
        except Exception as e:
            logger.log(f"Error getting answer: {e}", level="error")
            return f"error: {e}"
        

# Usage example

# qa_service = QAService()

# answer = asyncio.run(qa_service.get_answer("Who is rahul"))
# print(answer)
