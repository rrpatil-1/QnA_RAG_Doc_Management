import os,sys
from pathlib import Path

# Get the absolute path of the project root directory
ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT))
from backend.document_process.process_pdfdoc import PDFProcessor
import pytest

@pytest.fixture
def pdf_processor():
    return PDFProcessor()

def test_process_pdf_success(pdf_processor):
    file =os.path.join(os.getcwd(), "sample_doc\\Attension_Is_All_You_Need-2.pdf")
    chunk = pdf_processor.process_pdf(file)
    assert len(chunk) > 0

def test_process_pdf_failure(pdf_processor):
    file = os.path.join(os.getcwd(), "sample_doc\\Attension_Is_All_You_Need-1.pdf")
    chunk = pdf_processor.process_pdf(file)
    assert chunk.startswith("error")


