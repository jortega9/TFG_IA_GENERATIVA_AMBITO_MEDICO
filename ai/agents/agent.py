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
        prompt: str,
        response_format=None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.3,
    ):
        """Calls the OpenAI API.

        Args:
            prompt (str): The given prompt.
            response_format (FormatSchema): format schema for the response.
            model (str, optional): Set the model from the OpenAI models availables. Defaults to "gpt-4o-mini".
            temperature (float, optional): Set the temperature model. Defaults to 0.3.

        Returns:
            Schema: Returns the format schema with the new scores and explanations.
            or
            str: Returns a response from OpenAI API if there is not a response_format
        """

        messages = [{"role": "system", "content": prompt}]

        if response_format:
            response = self.client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                response_format=response_format,
            )
        else:
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