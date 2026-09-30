import json
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


# ==================================================
# RELEASE EMBEDDING FILES
# ==================================================

EMBEDDING_FILES = [
    DATA_DIRECTORY / "embedded_chunks_527.json",
    DATA_DIRECTORY / "embedded_chunks_528.json",
    DATA_DIRECTORY / "embedded_chunks_530.json"
]


# ==================================================
# CREATE CHROMA CLIENT
# ==================================================

client = chromadb.PersistentClient(
    path=str(CHROMA_DIRECTORY)
)


# ==================================================
# CREATE / GET COLLECTION
# ==================================================

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


# ==================================================
# LOAD EMBEDDING FILE
# ==================================================

def load_embedding_file(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==================================================
# STORE RELEASE CHUNKS
# ==================================================

def store_release_chunks(file_path):

    chunks = load_embedding_file(
        file_path
    )

    print(
        f"\nLoading: {file_path.name}"
    )

    for chunk in chunks:

        chunk_id = (
            f"release_{chunk['release_id']}_"
            f"{chunk['chunk_id']}"
        )

        collection.upsert(
            ids=[chunk_id],

            embeddings=[
                chunk["embedding"]
            ],

            documents=[
                chunk["content"]
            ],

            metadatas=[
                {
                    "release_id":
                        chunk["release_id"],

                    "chunk_id":
                        chunk["chunk_id"],

                    "document_type":
                        chunk["document_type"],

                    "topic":
                        chunk["topic"],

                    "source_file":
                        file_path.name
                }
            ]
        )

        print(
            f"Stored: {chunk_id}"
        )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    print(
        "\n=========================================="
    )

    print(
        "     CHROMADB RELEASE EVIDENCE STORE"
    )

    print(
        "=========================================="
    )

    print(
        "\nDatabase location:"
    )

    print(
        CHROMA_DIRECTORY
    )

    print(
        "\nCollection:"
    )

    print(
        COLLECTION_NAME
    )

    # ----------------------------------------------
    # LOAD ALL RELEASES
    # ----------------------------------------------

    for embedding_file in EMBEDDING_FILES:

        if not embedding_file.exists():

            print(
                f"\nWARNING: File not found:"
            )

            print(
                embedding_file
            )

            continue

        store_release_chunks(
            embedding_file
        )

    # ----------------------------------------------
    # FINAL COUNT
    # ----------------------------------------------

    print(
        "\n=========================================="
    )

    print(
        "CHROMADB STORE COMPLETE"
    )

    print(
        "Total records:",
        collection.count()
    )

    print(
        "=========================================="
    )