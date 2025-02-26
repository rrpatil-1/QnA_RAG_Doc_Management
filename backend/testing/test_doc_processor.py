
from backend.document_process.process_pdfdoc import PDFProcessor
import os

def main():
    try:
        pdfProcess = PDFProcessor()

        file =os.path.join(os.getcwd(), "sample_doc\\deepseek_research.pdf")

        chunk = pdfProcess.process_pdf(file)

        print(chunk)
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")