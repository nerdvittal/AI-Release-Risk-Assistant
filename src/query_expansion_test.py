import json
import urllib.request
from pathlib import Path

import chromadb


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "chroma_db"
)

COLLECTION_NAME = "release_evidence"

OLLAMA_URL = (
    "http://localhost:11434/api/embeddings"
)

EMBEDDING_MODEL = "nomic-embed-text"

TOP_K = 3


def generate_embedding(text):
    payload = {
        "model": EMBEDDING_MODEL,
        "prompt": text
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(
            payload
        ).encode("utf-8"),
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


def search_chroma(question):
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIRECTORY)
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    embedding = generate_embedding(
        question
    )

    return collection.query(
        query_embeddings=[embedding],
        n_results=TOP_K
    )


def collect_candidates(queries):
    candidates = {}

    for query in queries:

        print("\n" + "-" * 70)
        print(f"QUERY: {query}")
        print("-" * 70)

        results = search_chroma(query)

        ids = results.get(
            "ids",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        for index, chunk_id in enumerate(ids):

            distance = distances[index]

            metadata = metadatas[index]

            print(
                f"Rank {index + 1}: "
                f"{chunk_id} "
                f"(distance={distance:.4f})"
            )

            if chunk_id not in candidates:

                candidates[chunk_id] = {
                    "chunk_id": chunk_id,
                    "distance": distance,
                    "metadata": metadata,
                    "source_query": query
                }

    return candidates


def main():

    question = (
        "Who approved the deployment "
        "in Release 530?"
    )

    expanded_queries = [
        question,

        "Release 530 deployment approval",

        "Release Manager approved deployment",

        "Who authorized Release 530 deployment?"
    ]

    print("=" * 70)
    print("QUERY EXPANSION EXPERIMENT")
    print("=" * 70)

    print("\nOriginal question:")
    print(question)

    print("\nExpanded queries:")

    for index, query in enumerate(
        expanded_queries,
        start=1
    ):
        print(
            f"{index}. {query}"
        )

    candidates = collect_candidates(
        expanded_queries
    )

    print("\n" + "=" * 70)
    print("COMBINED CANDIDATE POOL")
    print("=" * 70)

    print(
        f"\nUnique candidates found: "
        f"{len(candidates)}"
    )

    for index, candidate in enumerate(
        candidates.values(),
        start=1
    ):

        print(
            f"\nCandidate {index}"
        )

        print(
            f"Chunk: "
            f"{candidate['chunk_id']}"
        )

        print(
            f"Distance: "
            f"{candidate['distance']:.4f}"
        )

        print(
            f"Release: "
            f"{candidate['metadata'].get('release_id')}"
        )

        print(
            f"Topic: "
            f"{candidate['metadata'].get('topic')}"
        )

        print(
            f"Found by: "
            f"{candidate['source_query']}"
        )

    print("\n" + "=" * 70)
    print("QUERY EXPANSION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()