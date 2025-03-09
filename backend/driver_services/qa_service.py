import asyncio
import os
from backend.llm_service.Ollama.llm_processing import OllamaService
from backend.db_service.vectordb.embedding_service.service import EmbeddingService
from dotenv import load_dotenv
import json
from nltk.tokenize import word_tokenize
from backend.utils.logger import CustomLogger
from backend.utils.ranking import BM25Retriever

logger = CustomLogger()

load_dotenv()

file = os.path.join(os.getcwd(), "prompts","qa_prompt.json")
logger.log(f"loading prompt from {file}", level="info")
class QAService:
    def __init__(self):
        self.llm_service = OllamaService()
        self.embedding_service = EmbeddingService()
        self.file = file
    async def get_context(self, query: str,docs:None|dict):
        try:
            logger.log(f"searching for context for: {query}", level="info")
            
            similar_docs = await self.embedding_service.search_similar_doc(query,filter=docs)
            if type(similar_docs) is str:
                raise Exception(similar_docs)
            
            logger.log(f"retrive {len(similar_docs)}  docs from db", level="info")
            
            if len(similar_docs) == 0:
                return []
            # Extract the content of each similar document for context.
            
            context = [doc.page_content for doc in similar_docs]
            
            # retrive most relivant doc
            result  = BM25Retriever().retrieve_with_threshold(query,corpus=context)
            logger.log(f"found {len(result)} relevant record", level="info")
            if result:
                result = [doc for doc, _ in result]
            
            return "\n".join(result)
        
        except Exception as e:
            logger.log(f"error getting context: {e}", level="error")
            return f"error: {e}"
        
    async def get_answer(self, question:str,filter=None):
        try:
            with open(self.file,'r',encoding='utf-8') as f:
                prompt_json  = json.load(f)
                prompt = prompt_json['system']            
            context = await self.get_context(question,filter)
            if type(context) is str and context.startswith("error"):
                raise Exception(context)

            logger.log(f"calling llm for user query", level="info")
            
            response = await self.llm_service.a_generate_response(
            messages=question,
            prompt=prompt,
            context=context
        )
            return response.content
        except Exception as e:
            logger.log(f"Error getting answer: {e}", level="error")
            return f"error: {e}"
        
    async def cleanup(self):
        await self.embedding_service.cleanup()
        
