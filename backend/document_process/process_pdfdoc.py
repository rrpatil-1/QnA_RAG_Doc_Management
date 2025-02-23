from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Optional, Dict
import os
import shutil
from backend.document_process.base import DocProcessorBase
from dotenv import load_dotenv

from backend.utils.logger import CustomLogger
load_dotenv()

logger = CustomLogger()

class PDFProcessor(DocProcessorBase):
    def __init__(self):
        """
        Initialize the PDF processor with specified embedding model
        
        Args:
            embedding_model_name: Name of the HuggingFace embedding model to use
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        

    def process_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Process a PDF file and return its chunks
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of document chunks with metadata
        """
        try:
            # Load PDF
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            
            # Extract filename for metadata
            filename = os.path.basename(pdf_path)
            
            # Add source metadata to each document
            for doc in documents:
                doc.metadata={"source":filename}
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            return chunks
        
        except Exception as e:
            logger.log(f"Error during processing PDF {pdf_path}: {str(e)}", level="error")
            print(f"Error processing PDF {pdf_path}: {str(e)}")
            return []