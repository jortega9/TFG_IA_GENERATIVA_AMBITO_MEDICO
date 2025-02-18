import os
from dotenv import load_dotenv
from openai import OpenAI

class Agent:
    """Agent for handling LLM tasks"""

    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def call_llm(
        self, prompt, response_format=None, model="gpt-4o-mini", temperature=0
    ):
        """Internal method to call the LLM with a given prompt."""
        messages = [{"role": "system", "content": prompt}]

        if response_format:
            # Pydantic
            response = self.client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                response_format=response_format,
            )
        else:
            # No Pydantic
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )

        return (
            response.choices[0].message.parsed
            if response_format
            else response.choices[0].message.content
        )

    def get_text_embedding(self, text, model="text-embedding-3-small", dim=768):
        """Get embeddings for a given text"""
        if not text:
            return None
        response = self.client.embeddings.create(
            input=text, model=model, dimensions=dim
        )

        return response.data[0].embedding