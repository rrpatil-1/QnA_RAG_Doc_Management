from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from pathlib import Path

class DocProcessorBase(ABC):
    """
    Abstract base class defining the interface for PDF processors
    """

    @abstractmethod
    def process_pdf(self, pdf_path: str | Path) -> List[Dict]:
        """
        Process a single PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of processed document chunks with metadata
        """
        pass