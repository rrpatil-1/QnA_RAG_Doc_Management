

class BaseLLMService(ABC):
    """
    Abstract base class for LLM services that defines the common interface
    for different LLM implementations (like OpenAI, Ollama, Anthropic, etc.)
    """
    
    @abstractmethod
    def initialize_model(self) -> None:
        """Initialize the LLM model and any necessary configurations"""
        pass

    @abstractmethod
    async def generate_response(
        self, 
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stop_sequences: Optional[List[str]] = None
    ) -> str:
        """
        Generate a response from the LLM
        
        Args:
            prompt: The input text prompt
            temperature: Controls randomness in the output (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            stop_sequences: List of sequences where generation should stop
            
        Returns:
            Generated text response
        """
        pass

 

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a chat completion response
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness in the output
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Response dictionary containing generated message
        """
        pass
