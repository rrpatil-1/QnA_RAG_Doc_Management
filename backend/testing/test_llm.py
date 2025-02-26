import os
import json

from backend.db_service.vectordb.embedding_service.service import EmbeddingService
from backend.llm_service.Ollama.llm_processing import OllamaService


def main():
    try:
        file = os.path.join(os.getcwd(), "prompts\\qa_prompt.json")

        with open(file,'r') as f:
            prompt  = json.load(f)
            prompt = prompt['system']

        question = "what is multihead attension?"
        emb = EmbeddingService()
        llm = OllamaService()
        context = emb.search_similar_doc(question)
        context = '\n'.join([context[i][0].page_content for i in range(len(context))])

        response =  llm.generate_response(messages=question,context=context,prompt=prompt)

        print(response)
    except Exception as e:
        print(e)
