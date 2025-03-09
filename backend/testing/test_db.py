
import os,sys
from pathlib import Path

from backend.driver_services.list_available_doc import ListDocuments

# Get the absolute path of the project root directory
ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT))

from jinja2 import Template
from backend.db_service.vectordb.embedding_service.service import EmbeddingService
from langchain_core.documents import Document
import pytest
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def embedding_size():
    return int(os.environ.get('embedding_size'))
# embeding_size = int(os.environ.get('embedding_size'))
@pytest.fixture
def emb():
    return EmbeddingService()

def test_create_embedding(emb,embedding_size):
    vector = emb.create_embedding("hello world")
    assert len(vector) == embedding_size

def test_insert_embedding(emb):
    res = emb.insert_embedding([Document(page_content="there are cat in ponds and dogs in home", metadata={"source": "test3"})])
    assert type(res) == list

def test_search_similar_doc(emb):
    doc = emb.search_similar_doc("what is capital of india?")
    assert len(doc) == 0

def test_search_similar_doc1(emb):
    doc = emb.search_similar_doc("what is attension is all you need")
    assert len(doc) > 0

def test_search_similar_doc_filter(emb):
    doc = emb.search_similar_doc("what is attension is all you need",filter={'sorce':"test"})
    assert len(doc) == 0

def test_search_similar_doc_limit(emb):
    doc = emb.search_similar_doc("what is attension is all you need",limit=4)
    assert len(doc) == 4

def test_list_documents_succes(emb):
    file = os.path.join(os.getcwd(), "backend", "db_service", "sql", "get_doc_list.sql")
    template = Template(open(file).read())
    sql = template.render()
    doc = emb.list_documents(sql)
    assert type(doc) == list

