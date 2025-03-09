import os
from typing import List, Dict, Any, Optional
from backend.llm_service.base import BaseLLMService
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from dotenv import load_dotenv
load_dotenv()

base_url = os.getenv("ollama_url")

model_name = os.getenv("ollama_model")
max_tokens = int(os.getenv("LLM_MAX_TOKENS"))
temperature = float(os.getenv("LLM_TEMPERATURE"))

class OllamaService(BaseLLMService):
    def __init__(self):
        self.model_name = model_name
        self.api_base = base_url
        self.client = None
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.initialize_model()

    def initialize_model(self) -> None:
        """Initialize Ollama client"""
        
        self.client = ChatOllama(
            model=self.model_name,
            base_url=self.api_base,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

    def generate_response(
        self,
        prompt: str,
        messages: str,
        context: str,
    ) -> str:
        try:
            prompt = PromptTemplate(input_variables=["question","context"],template=prompt)

            chain = prompt | self.client
            response = chain.invoke(
                {
                "question": messages,
                "context":context
                }
            )
            return response
        except Exception as e:
            return f"error in generating response: {e}"

    async def a_generate_response(
        self,
        messages: str,
        prompt: str,
        context:str
    ):
        try:
            # prompt = PromptTemplate(input_variables=["question","context"],template=prompt)

            # chain = prompt | self.client
            # response = chain.invoke({"question": messages,"context":context})
            # return response
            response =  self.generate_response(prompt=prompt,messages=messages,context=context)
            return response
        except Exception as e:
            return f"error in generating response: {e}"



