import os

# support for various LLM clients  
from groq import Groq
from openai import OpenAI
from cohere import Client as CohereClient
from anthropic import Anthropic

# environment variables to load API keys from a .env file
from dotenv import load_dotenv
load_dotenv()

class LLMClients:
    def __init__(self):
        self.groq = self._init_groq()
        self.openai = self._init_openai()
        self.cohere = self._init_cohere()
        self.anthropic = self._init_anthropic()

    def _init_groq(self):
        key = os.getenv("GROQ_API_KEY")
        return Groq(api_key=key) if key else None

    def _init_openai(self):
        key = os.getenv("OPENAI_API_KEY")
        return OpenAI(api_key=key) if key else None

    def _init_cohere(self):
        key = os.getenv("COHERE_API_KEY")
        return CohereClient(api_key=key) if key else None

    def _init_anthropic(self):
        key = os.getenv("ANTHROPIC_API_KEY")
        return Anthropic(api_key=key) if key else None
