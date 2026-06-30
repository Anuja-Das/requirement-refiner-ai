"""
rag_loader.py — RAG (Retrieval-Augmented Generation) Knowledge Base Loader

This module handles loading domain knowledge from text files into a ChromaDB
vector database, and retrieving relevant context for a given user query.

Workflow:
1. Text files (.txt) in the "kb/" folder serve as the knowledge base.
2. build_chroma_index() reads those files, generates vector embeddings using
   the Nomic embedding model, and stores them in a persistent ChromaDB collection.
3. retrieve_context() takes a natural-language query, embeds it, and performs a
   similarity search against the stored knowledge base to return the most
   relevant text snippets.

This enables the LLM to ground its responses in project-specific domain knowledge.
"""

import os

import chromadb
from nomic import embed

from app.config.llm_config import embedding_model

# --- Path configuration ---
# BASE_DIR: directory where this script lives (app/rag/)
# KB_DIR: folder containing knowledge base text files
# CHROMA_DB_DIR: folder where ChromaDB persists the vector index
BASE_DIR = os.path.dirname(__file__)
KB_DIR = os.path.join(BASE_DIR, "kb")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")

# Initialize a persistent ChromaDB client so the index survives across restarts,
# and get (or create) the collection that holds our KB embeddings.
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_or_create_collection(name="requirements_kb")


def build_chroma_index():
    """
    Reads all .txt files from the knowledge base folder, generates vector
    embeddings for each document, and upserts them into the ChromaDB collection.

    Skips gracefully if the KB folder is missing or contains no text files.
    """

    if not os.path.exists(KB_DIR):
        print(f"KB folder not found at: {KB_DIR}")
        return

    docs = []
    ids = []

    # Scan the KB directory for .txt files and load their contents
    for f in os.listdir(KB_DIR):
        if f.endswith(".txt"):
            path = os.path.join(KB_DIR, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                docs.append(content)
                ids.append(f)  # Use filename as unique document ID

    print(f"Loaded {len(docs)} KB documents.")

    if not docs:
        print("No KB text files found. Skipping index build.")
        return

    # Generate vector embeddings for each document using the configured model.
    # task_type="search_document" tells the model these are documents to be searched.
    embeddings = embed.text(
        texts=docs,
        model=embedding_model,
        task_type="search_document"
    )["embeddings"]

    # Store documents and their embeddings in ChromaDB for later retrieval
    collection.add(documents=docs, embeddings=embeddings, ids=ids)
    print("Chroma index built successfully.")


def retrieve_context(query: str, top_k: int = 2):
    """
    Performs a semantic similarity search against the knowledge base.

    Args:
        query: The user's natural-language question or requirement text.
        top_k: Number of most-relevant KB snippets to return (default: 2).

    Returns:
        A string containing the top matching KB documents joined by double newlines.
    """

    # If the vector DB is empty (first run), build the index before querying
    if not os.listdir(CHROMA_DB_DIR):
        print("Chroma DB empty — building index first...")
        build_chroma_index()

    # Embed the query using task_type="search_query" (optimized for retrieval queries)
    query_emb = embed.text(
        texts=[query],
        model=embedding_model,
        task_type="search_query"
    )["embeddings"]

    # Perform similarity search in ChromaDB to find the closest KB documents
    results = collection.query(
        query_embeddings=query_emb,
        n_results=top_k
    )

    # Extract the matched document texts from the query results
    docs = results.get("documents", [[]])[0]

    return "\n\n".join(docs)


# When run directly, build/rebuild the vector index from the KB folder
if __name__ == "__main__":
    build_chroma_index()
