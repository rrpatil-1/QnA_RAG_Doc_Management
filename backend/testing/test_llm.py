import json
import os,sys
from pathlib import Path

# Get the absolute path of the project root directory
ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT))
import pytest
from backend.llm_service.Ollama.llm_processing import OllamaService
import os
@pytest.fixture
def ollama_service():
    return OllamaService()
@pytest.fixture
def Prompt():
    file = os.path.join(os.getcwd(), "prompts","qa_prompt.json")

    with open(file,'r') as f:
        prompt_json  = json.load(f)
        prompt = prompt_json['system']
    return prompt


def test_get_response(ollama_service,Prompt):
    
    response = ollama_service.generate_response(messages="What is the capital of France?",prompt=Prompt,context="paris is beautiful city in eruope, it is also a capital of france")
    assert "paris" in response.content.lower()

def test_generate_response_error(ollama_service,Prompt):

    response = ollama_service.generate_response(messages="who is rahul",prompt=Prompt,context="")
    resp = (response.content).lower()
    print(resp)
    assert "i don't have the information" in resp

