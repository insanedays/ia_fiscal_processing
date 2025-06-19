# src/core/llm_client.py

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

    def get_response(self, user_prompt: str, model: str = "mixtral-8x7b-32768", provider: str = "groq") -> str:
        if provider == "groq" and self.groq:
            response = self.groq.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.choices[0].message.content.strip()

        elif provider == "openai" and self.openai:
            response = self.openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.choices[0].message.content.strip()

        elif provider == "cohere" and self.cohere:
            raise NotImplementedError("Cohere chat response not implemented.")

        elif provider == "anthropic" and self.anthropic:
            raise NotImplementedError("Anthropic chat response not implemented.")

        raise ValueError(f"LLM provider '{provider}' not available or not configured.")
