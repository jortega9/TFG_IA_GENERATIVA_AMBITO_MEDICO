"""Embeddings for the vectorial data base."""

import numpy as np
from langchain.embeddings.openai import OpenAIEmbeddings
from ai.config import Config

# Embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=Config.OPENAI_API_KEY)

def get_embedding(text: str) -> list:
    """Generate an embedding for the slected text."""
    return embedding_model.embed_query(text)



