import json
import re
import urllib.request
from pathlib import Path

import chromadb


# ==================================================
# PROJECT PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIRECTORY = PROJECT_ROOT / "data"

CHROMA_DIRECTORY = (
    DATA_DIRECTORY / "chroma_db"
)


# ==================================================
# CHROMA CONFIGURATION
# ==================================================

COLLECTION_NAME = "release_evidence"

OLLAMA_URL = (
    "http://localhost:11434/api/embeddings"
)

EMBEDDING_MODEL = "nomic-embed-text"

TOP_K = 3


# ==================================================
# GENERATE QUERY EMBEDDING
# ==================================================

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
            "Content-Type":
                "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(
        request
    ) as response:

        result = json.loads(
            response.read().decode(
                "utf-8"
            )
        )

    return result["embedding"]


# ==================================================
# DETECT RELEASE ID
# ==================================================

def detect_release_id(question):

    patterns = [
        r"\brelease[\s_-]*(\d+)\b",
        r"\brel[\s_-]*(\d+)\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            question.lower()
        )

        if match:

            return match.group(1)

    return None


# ==================================================
# CHROMADB SEARCH
# ==================================================

def search_chroma(
    question,
    top_k=TOP_K,
    release_id=None
):

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIRECTORY)
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    question_embedding = (
        generate_embedding(question)
    )

    query_parameters = {
        "query_embeddings": [
            question_embedding
        ],
        "n_results": top_k
    }

    # ----------------------------------------------
    # RELEASE FILTER
    # ----------------------------------------------

    if release_id:

        query_parameters["where"] = {
            "release_id": release_id
        }

    results = collection.query(
        **query_parameters
    )

    return results


# ==================================================
# DISPLAY RESULTS
# ==================================================

def display_results(
    question,
    release_id,
    results
):

    print(
        "\n=========================================="
    )

    print(
        "       CHROMADB SEMANTIC SEARCH"
    )

    print(
        "=========================================="
    )

    print(
        "\nQuestion:"
    )

    print(
        question
    )

    print(
        "\nRelease filter:"
    )

    print(
        release_id
        if release_id
        else "ALL RELEASES"
    )

    ids = results.get(
        "ids",
        [[]]
    )[0]

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    print(
        f"\nResults returned: {len(ids)}"
    )

    for index, chunk_id in enumerate(
        ids
    ):

        print(
            "\n------------------------------------------"
        )

        print(
            f"Rank: {index + 1}"
        )

        print(
            f"ID: {chunk_id}"
        )

        if index < len(distances):

            print(
                f"Distance: "
                f"{distances[index]:.4f}"
            )

        if index < len(metadatas):

            metadata = metadatas[index]

            print(
                f"Release ID: "
                f"{metadata.get('release_id')}"
            )

            print(
                f"Chunk ID: "
                f"{metadata.get('chunk_id')}"
            )

            print(
                f"Topic: "
                f"{metadata.get('topic')}"
            )

            print(
                f"Source: "
                f"{metadata.get('source_file')}"
            )

        if index < len(documents):

            print(
                "\nContent:"
            )

            print(
                documents[index]
            )

    print(
        "\n=========================================="
    )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    question = input(
        "Enter your question: "
    ).strip()

    if not question:

        print(
            "Question cannot be empty."
        )

        raise SystemExit

    release_id = detect_release_id(
        question
    )

    results = search_chroma(
        question,
        release_id=release_id
    )

    display_results(
        question,
        release_id,
        results
    )