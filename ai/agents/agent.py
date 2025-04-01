"""TODO:

Returns:
    _type_: _description_
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

class Agent:
    """Agent for handling LLM tasks"""

    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def call_llm(
        self,
        prompt=None,
        messages=None,
        response_format=None,
        model="gpt-4o",
        temperature=0.3,
        tools=None,
        tool_choice="auto"  # puede ser "auto", "none", o dict con una función concreta
    ):
        """Internal method to call the LLM with either a prompt or messages and optional tool calling support."""

        if prompt:
            messages_payload = [{"role": "system", "content": prompt}]
        elif messages:
            messages_payload = messages
        else:
            raise ValueError("Either prompt or messages must be provided.")

        # OpenAI con herramientas y Pydantic
        if response_format:
            response = self.client.beta.chat.completions.parse(
                model=model,
                messages=messages_payload,
                response_format=response_format,
                tools=tools,
                tool_choice=tool_choice,
            )
            return response.choices[0].message.parsed

        # OpenAI con herramientas pero sin parseo
        elif tools:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages_payload,
                temperature=temperature,
                tools=tools,
                tool_choice=tool_choice,
            )
            return response.choices[0].message.function_call  

        # Sin herramientas
        else:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages_payload,
                temperature=temperature,
            )
            return response.choices[0].message.content



    def get_text_embedding(self, text, model="text-embedding-3-small", dim=768):
        """Get embeddings for a given text"""
        if not text:
            return None
        response = self.client.embeddings.create(
            input=text, model=model, dimensions=dim
        )

        return response.data[0].embedding