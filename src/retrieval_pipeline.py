import json
import urllib.request
from pathlib import Path

import chromadb

from bm25_search import search_bm25
from reranker import SemanticReranker


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "chroma_db"
)

COLLECTION_NAME = "release_evidence"

OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"

TOP_K_CHROMA = 5
TOP_K_BM25 = 5
TOP_K_FINAL = 5


def generate_embedding(text):
    payload = {
        "model": EMBEDDING_MODEL,
        "prompt": text
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    return result["embedding"]


def search_chroma(
    question,
    top_k=TOP_K_CHROMA
):
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIRECTORY)
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    question_embedding = generate_embedding(
        question
    )

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    candidates = []

    for index in range(
        len(results["documents"][0])
    ):
        candidates.append(
            {
                "document": results["documents"][0][index],
                "metadata": results["metadatas"][0][index],
                "chroma_distance": results["distances"][0][index]
            }
        )

    return candidates


def get_candidate_key(candidate):
    metadata = candidate["metadata"]

    return (
        str(metadata.get("release_id")),
        str(metadata.get("chunk_id"))
    )


def build_hybrid_candidates(question):
    chroma_candidates = search_chroma(
        question
    )

    bm25_candidates = search_bm25(
        question,
        top_k=TOP_K_BM25
    )

    candidates = {}

    for candidate in chroma_candidates:
        candidates[
            get_candidate_key(candidate)
        ] = candidate

    for candidate in bm25_candidates:
        key = get_candidate_key(candidate)

        if key in candidates:
            candidates[key][
                "bm25_score"
            ] = candidate["bm25_score"]

        else:
            candidates[key] = candidate

    return list(candidates.values())


def main():

    question = input(
        "Enter your question: "
    ).strip()

    if not question:
        print("Question cannot be empty.")
        return

    print(
        "\nGenerating hybrid candidate pool..."
    )

    candidates = build_hybrid_candidates(
        question
    )

    print(
        f"\nHybrid candidate pool size: "
        f"{len(candidates)}"
    )

    print("\n" + "=" * 70)
    print("HYBRID CANDIDATES")
    print("=" * 70)

    for rank, candidate in enumerate(
        candidates,
        start=1
    ):
        metadata = candidate["metadata"]

        print(
            f"\nCandidate {rank}"
        )

        print(
            f"Release: "
            f"{metadata.get('release_id')}"
        )

        print(
            f"Chunk: "
            f"{metadata.get('chunk_id')}"
        )

        if "bm25_score" in candidate:
            print(
                f"BM25 score: "
                f"{candidate['bm25_score']:.4f}"
            )

        if "chroma_distance" in candidate:
            print(
                f"Chroma distance: "
                f"{candidate['chroma_distance']:.4f}"
            )

        print("\nContent:")
        print(candidate["document"])

    print("\n" + "=" * 70)
    print("CROSS-ENCODER RERANKING")
    print("=" * 70)

    reranker = SemanticReranker()

    ranked_candidates = reranker.rerank(
        question,
        candidates
    )

    for rank, candidate in enumerate(
        ranked_candidates[:TOP_K_FINAL],
        start=1
    ):
        metadata = candidate["metadata"]

        print(
            f"\nRank {rank}"
        )

        print(
            f"Rerank score: "
            f"{candidate['rerank_score']:.4f}"
        )

        print(
            f"Release: "
            f"{metadata.get('release_id')}"
        )

        print(
            f"Chunk: "
            f"{metadata.get('chunk_id')}"
        )

        print("\nContent:")
        print(candidate["document"])


if __name__ == "__main__":
    main()