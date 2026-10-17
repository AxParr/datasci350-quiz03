"""A minimal RAG pipeline over the course's own notes.

Requires a running Ollama and two models:
    ollama pull embeddinggemma
    ollama pull llama3.2:1b
And two Python packages:
    pip install ollama chromadb

Run from inside this folder: python rag.py
"""

from pathlib import Path

import chromadb
import ollama

client = chromadb.Client()
collection = client.create_collection(
    name="notes",
    configuration={"hnsw": {"space": "cosine"}})

# Step 1: split the notes into paragraphs
paragraphs = []
files = []
for path in Path("corpus").glob("*.md"):
    text = path.read_text(encoding="utf-8")
    for paragraph in text.split("\n\n"):
        if len(paragraph) > 80:
            paragraphs.append(paragraph)
            files.append({"file": path.name})

# Step 2: embed the paragraphs and store them
# Chroma needs an ID for each one: "0", "1", "2"...
ids = []
for n in range(len(paragraphs)):
    ids.append(str(n))

response = ollama.embed(
    model="embeddinggemma", input=paragraphs)
collection.add(ids=ids, embeddings=response["embeddings"],
               documents=paragraphs, metadatas=files)
print("Chunks stored:", collection.count())

# Step 3: find the 3 paragraphs closest to the question
question = input("Your question: ")

response = ollama.embed(model="embeddinggemma", input=question)
results = collection.query(query_embeddings=response["embeddings"], n_results=3)

data = results["documents"][0]
print("Sources:", results["metadatas"][0])
for distance in results["distances"][0]:
    print("Similarity:", round(1 - distance, 2))

# Step 4: generate an answer from those paragraphs
prompt = f"Using only this data: {data}. Answer this question: {question}"

output = ollama.generate(model="llama3.2:1b", prompt=prompt)
print(output["response"])
