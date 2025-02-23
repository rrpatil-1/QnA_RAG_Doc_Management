from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from backend.llm_service.base import BaseLLMService
from dotenv import load_dotenv
load_dotenv()
base_url = os.getenv("OLLAMA_API_BASE_URL")

class OllamaService(BaseLLMService):
    def __init__(self, model_name: str, api_base: str = "http://localhost:11434"):
        self.model_name = model_name
        self.api_base = api_base
        self.client = None
        self.initialize_model()

    def initialize_model(self) -> None:
        """Initialize Ollama client"""
        from langchain.llms import Ollama
        self.client = Ollama(
            model=self.model_name,
            base_url=self.api_base
        )

    async def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stop_sequences: Optional[List[str]] = None
    ) -> str:
        try:
            response = await self.client.agenerate(
                prompts=[prompt],
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop_sequences
            )
            return response.generations[0].text
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        try:
            from langchain.chat_models import ChatOllama
            chat_model = ChatOllama(
                model=self.model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
            response = await chat_model.agenerate([messages])
            return {
                "message": response.generations[0][0].text,
                "finish_reason": "stop"
            }
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")


# Example usage:
async def main():
    # Initialize the LLM service
    llm_service = OllamaService(model_name="llama2")
    
    # Generate a response
    response = await llm_service.generate_response(
        prompt="What is machine learning?",
        temperature=0.7
    )
    print(f"Generated response: {response}")
    
    # Generate embeddings
    embeddings = await llm_service.generate_embeddings(
        texts=["Hello world", "How are you?"]
    )
    print(f"Generated embeddings: {embeddings}")
    
    # Chat completion
    chat_response = await llm_service.chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    print(f"Chat response: {chat_response}")
