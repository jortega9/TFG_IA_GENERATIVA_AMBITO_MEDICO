"""Controller for the ChromaDB."""
import chromadb
import pandas as pd
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from ai.utils.embeddings import get_embedding

# ChromaDB configuration
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="csv_data")

def load_csv_to_chroma(file_path: str):
    """Load a CSV file, generate the embeddings and save that embeddings
    in a ChromaDB.

    Args:
        file_path (str): _description_
    """
    df = pd.read_excel(file_path, engine="openpyxl")

    # Convert rows to structured text.
    structured_texts = df.astype(str).apply(lambda row : " | ".join(row), axis=1).tolist()

    # Once we have the structured text, embed all the rows.
    for i, row in enumerate(structured_texts):
        embedding = get_embedding(row)
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            metadatas=[{"text": row}]
        )
    
    return {"message" : f"{len(df)} rows stored in ChromaDB."}

def query_chromadb(query: str, top_k: int = 5):
    """Make a query in the ChromaDB

    Args:
        query (str): Text that contains the query.
        top_k_ (int, optional): Number of results. Defaults to 5.
    """
    
    query_embedding = get_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    return {"query": query, "results": results}


