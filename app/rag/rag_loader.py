import os

import chromadb
from nomic import embed

from app.config.llm_config import embedding_model

BASE_DIR = os.path.dirname(__file__)
KB_DIR = os.path.join(BASE_DIR, "kb")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")

# Create client + collection (same as before)
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_or_create_collection(name="requirements_kb")


def build_chroma_index():
    """
    Builds index ONLY if documents exist.
    Does NOT remove or break existing functionality.
    """

    if not os.path.exists(KB_DIR):
        print(f"KB folder not found at: {KB_DIR}")
        return

    docs = []
    ids = []

    for f in os.listdir(KB_DIR):
        if f.endswith(".txt"):
            path = os.path.join(KB_DIR, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                docs.append(content)
                ids.append(f)

    print(f"Loaded {len(docs)} KB documents.")

    if not docs:
        print("No KB text files found. Skipping index build.")
        return

    # Generate embeddings (same model, same API)
    embeddings = embed.text(
        texts=docs,
        model=embedding_model,
        task_type="search_document"
    )["embeddings"]

    # Add to Chroma (no change)
    collection.add(documents=docs, embeddings=embeddings, ids=ids)
    print("Chroma index built successfully.")


def retrieve_context(query: str, top_k: int = 2):
    """
    Retrieves relevant KB text for the given query.
    Functionality remains EXACTLY the same.
    """

    # Ensure DB is initialized at least once
    if not os.listdir(CHROMA_DB_DIR):
        print("Chroma DB empty — building index first...")
        build_chroma_index()

    # Embed query (same)
    query_emb = embed.text(
        texts=[query],
        model=embedding_model,
        task_type="search_query"
    )["embeddings"]

    # Query Chroma (same)
    results = collection.query(
        query_embeddings=query_emb,
        n_results=top_k
    )

    docs = results.get("documents", [[]])[0]

    # Return same format
    return "\n\n".join(docs)


if __name__ == "__main__":
    build_chroma_index()
