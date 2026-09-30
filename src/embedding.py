import json
import urllib.request
from pathlib import Path

from chunk_document import create_chunks


OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text):
    payload = {
        "model": EMBEDDING_MODEL,
        "prompt": text
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    return result["embedding"]


def create_embeddings(file_path, output_path):
    chunks = create_chunks(file_path)

    embedded_chunks = []

    print("========== EMBEDDING PROCESS ==========")
    print("Embedding model:", EMBEDDING_MODEL)
    print("Input document:", file_path)
    print("Total chunks:", len(chunks))

    for chunk in chunks:
        embedding = generate_embedding(chunk["content"])

        embedded_chunk = {
            "chunk_id": chunk["chunk_id"],
            "content": chunk["content"],
            "release_id": chunk["release_id"],
            "document_type": chunk["document_type"],
            "topic": chunk["topic"],
            "embedding": embedding
        }

        embedded_chunks.append(embedded_chunk)

        print(
            f"{chunk['chunk_id']} → "
            f"{len(embedding)} dimensions"
        )

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            embedded_chunks,
            file,
            indent=4
        )

    print("\nSaved embedded chunks to:")
    print(output_path)
    print("======================================")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "data" / "release_528.txt"
    output_file = project_root / "data" / "embedded_chunks_528.json"

    create_embeddings(
        input_file,
        output_file
    )