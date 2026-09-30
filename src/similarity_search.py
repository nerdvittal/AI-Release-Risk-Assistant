import json
import math
import urllib.request
from pathlib import Path


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


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def load_embedded_chunks(embedding_file):
    file_path = Path(embedding_file)

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def search_similar_chunks(question, embedding_file, top_k=3):
    question_embedding = generate_embedding(question)
    embedded_chunks = load_embedded_chunks(embedding_file)

    results = []

    for chunk in embedded_chunks:
        score = cosine_similarity(
            question_embedding,
            chunk["embedding"]
        )

        
        results.append({
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "score": score
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":
    question = input("Enter your question: ").strip()

    project_root = Path(__file__).resolve().parent.parent

    embedding_file = (
        project_root
        / "data"
        / "embedded_chunks_528.json"
    )

    results = search_similar_chunks(
        question,
        embedding_file
    )

    print("\n========== TOP MATCHING CHUNKS ==========")

    if not results:
        print("No results found.")
    else:
        print(
            f"Best similarity score: "
            f"{results[0]['score']:.4f}"
        )

        for result in results:
            print(f"\nChunk ID: {result['chunk_id']}")
            print(f"Similarity score: {result['score']:.4f}")
            print("Content:")
            print(result["content"])
            print("--------------------------------------")

    print("========================================")