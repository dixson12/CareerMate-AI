from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings

# --- Setup (runs once on import) ---
embedding_model = SentenceTransformer(settings.embedding_model)

chroma_client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
collection = chroma_client.get_or_create_collection(name="documents")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)


def chunk_text(text: str) -> list[str]:
    return splitter.split_text(text)


def add_document_to_store(filename: str, text: str):
    chunks = chunk_text(text)
    if not chunks:
        return 0

    embeddings = embedding_model.encode(chunks).tolist()
    ids = [f"{filename}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
    return len(chunks)


def query_documents(query: str, top_k: int = 4) -> list[dict]:
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )

    retrieved = []
    for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
        retrieved.append({"text": doc, "source": metadata["source"]})

    return retrieved