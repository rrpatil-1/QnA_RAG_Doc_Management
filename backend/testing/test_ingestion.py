import os
import pytest
from unittest.mock import patch, MagicMock
from backend.driver_services.ingestion_service import IngestionService
from langchain_core.documents import Document
@pytest.fixture
def ingestion_service():
    return IngestionService()


def test_process_and_insert_success(ingestion_service):

    # Call the method
    result = ingestion_service.process_and_insert(os.path.join(os.getcwd(),"sample_doc\\Attension_Is_All_You_Need.pdf"))
    
    # Assertions
    assert result == "success"

def test_process_and_insert_failure(ingestion_service):

    # Call the method
    result = ingestion_service.process_and_insert(os.path.join(os.getcwd(),"sample_doc\\Attension_Is_All_You_Need1.pdf"))

    
    # Assertions
    assert result.startswith("error")
