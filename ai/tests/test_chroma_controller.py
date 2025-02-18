"""Script to test the ChromaDB."""

from ..vector_db.chroma_controller import load_csv_to_chroma, query_chromadb
from ..vector_db.chroma_controller import collection

print("\n📌 Datos almacenados en ChromaDB:")
print(collection.peek())  # Muestra algunos datos en la base de datos

csv_path = "./ai/data/raw/BD_Test.xlsx"

print("\n🔹 Loading data in ChromaDB...")
response = load_csv_to_chroma(csv_path)
print(response)

query_text = "Cuantas personas mayores de 60 años hay?"
top_k = 3

print("\n🔹 Making a ChromaDB query...")
query_response = query_chromadb(query_text, top_k)
print(query_response)
