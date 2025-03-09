import os
import concurrent.futures
from backend.document_process.process_pdfdoc import PDFProcessor
from backend.db_service.vectordb.embedding_service.service import EmbeddingService
from dotenv import load_dotenv

from backend.utils.logger import CustomLogger

logger = CustomLogger()


load_dotenv()

max_batch_size = int(os.getenv("EMBEDDING_BATCH_SIZE"))

class IngestionService:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.embedding_service = EmbeddingService()
        self.max_batch_size = max_batch_size

    async def process_and_insert(self, file_path):
        """
        Process a PDF file and insert its chunks into the vector database
        Args:
            file_path: Path to the PDF file
        
        Returns:
            str: Success message if successful, error message if not
         """
        try:
            if file_path.endswith('.pdf'):
                chunks = self.pdf_processor.process_pdf(file_path)
                
            if type(chunks)==str:
                raise Exception(chunks)
            
            if len(chunks) == 0:
                raise ValueError(f"No Document found in the PDF: total chunks {len(chunks)}")
            
            logger.log(f"total documents to process:{len(chunks)}",level="info")
            
            self.max_batch_size = len(chunks) if len(chunks)<self.max_batch_size else self.max_batch_size

            # with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            #     task = [executor.submit(self.embedding_service.insert_embedding(chunks[i:i+self.max_batch_size])) for i in range(0,len(chunks),self.max_batch_size)]

            #     for future in concurrent.futures.as_completed(task):
            #         try:
            #             future.result()
            #         except Exception as e:
            #             logger.log(f"Error inserting embedding: {e}", level="error")
            #             raise e
            for i in range(0, len(chunks), self.max_batch_size):
                self.embedding_service.insert_embedding(chunks[i:i+self.max_batch_size])
                logger.log(f"Processed and inserted Batch{i} for {i+self.max_batch_size} documents", level="info")
            logger.log(f"Successfully processed and inserted: {file_path}",level="info")
            return "success"

        except Exception as e:
            # logger.log(f"Error processing {file_path}: {e}",level="error")
            return f"error processing {file_path}: {e}"
        
    async def cleanup(self):
        await self.embedding_service.cleanup()
        