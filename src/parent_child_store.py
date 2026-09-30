import json
from pathlib import Path

import chromadb


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIRECTORY = PROJECT_ROOT / "data"

CHROMA_DIRECTORY = (
    DATA_DIRECTORY / "chroma_db"
)

COLLECTION_NAME = "release_evidence"


def load_chunks():
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIRECTORY)
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    results = collection.get(
        include=[
            "documents",
            "metadatas"
        ]
    )

    chunks = []

    for document, metadata in zip(
        results["documents"],
        results["metadatas"]
    ):
        chunks.append(
            {
                "document": document,
                "metadata": metadata
            }
        )

    return chunks


def build_parent_child_mapping(chunks):
    parents = {}

    for chunk in chunks:

        metadata = chunk["metadata"]

        release_id = str(
            metadata["release_id"]
        )

        parent_id = (
            f"release_{release_id}_parent"
        )

        if parent_id not in parents:
            parents[parent_id] = {
                "parent_id": parent_id,
                "release_id": release_id,
                "children": []
            }

        parents[parent_id]["children"].append(
            {
                "chunk_id": metadata["chunk_id"],
                "document": chunk["document"]
            }
        )

    return list(parents.values())


def main():

    chunks = load_chunks()

    parents = build_parent_child_mapping(
        chunks
    )

    print("\n" + "=" * 70)
    print("PARENT-CHILD MAPPING")
    print("=" * 70)

    print(
        f"\nTotal chunks: {len(chunks)}"
    )

    print(
        f"Total parents: {len(parents)}"
    )

    for parent in parents:

        print(
            f"\nParent: "
            f"{parent['parent_id']}"
        )

        print(
            f"Release: "
            f"{parent['release_id']}"
        )

        print(
            f"Children: "
            f"{len(parent['children'])}"
        )

        for child in parent["children"]:

            print(
                f"  └── {child['chunk_id']}"
            )


if __name__ == "__main__":
    main()