import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIRECTORY = PROJECT_ROOT / "src"

if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from retrieval_pipeline import search_chroma
from parent_child_store import (
    load_chunks,
    build_parent_child_mapping
)


TOP_K_CHILDREN = 3


def build_parent_documents():
    chunks = load_chunks()

    parents = build_parent_child_mapping(
        chunks
    )

    parent_documents = {}

    for parent in parents:

        parent_id = parent["parent_id"]

        child_documents = [
            child["document"]
            for child in parent["children"]
        ]

        parent_documents[parent_id] = {
            "parent_id": parent_id,
            "release_id": parent["release_id"],
            "document": "\n\n".join(
                child_documents
            )
        }

    return parent_documents


def retrieve_parent_context(
    question,
    top_k=TOP_K_CHILDREN
):
    child_results = search_chroma(
        question,
        top_k=top_k
    )

    parent_documents = build_parent_documents()

    results = []
    seen_parents = set()

    for child in child_results:

        metadata = child["metadata"]

        release_id = str(
            metadata["release_id"]
        )

        parent_id = (
            f"release_{release_id}_parent"
        )

        if parent_id in seen_parents:
            continue

        parent = parent_documents.get(
            parent_id
        )

        if parent is None:
            continue

        seen_parents.add(parent_id)

        results.append(
            {
                "parent_id": parent_id,
                "release_id": release_id,
                "matched_child": metadata[
                    "chunk_id"
                ],
                "child_distance": child[
                    "chroma_distance"
                ],
                "document": parent[
                    "document"
                ]
            }
        )

    return results


def main():

    question = input(
        "Enter your question: "
    ).strip()

    if not question:
        print("Question cannot be empty.")
        return

    results = retrieve_parent_context(
        question
    )

    print("\n" + "=" * 70)
    print("PARENT-CONTEXT RETRIEVAL")
    print("=" * 70)

    for rank, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\nRank {rank}"
        )

        print(
            f"Parent: "
            f"{result['parent_id']}"
        )

        print(
            f"Matched child: "
            f"{result['matched_child']}"
        )

        print(
            f"Child distance: "
            f"{result['child_distance']:.4f}"
        )

        print("\nParent context:")
        print(result["document"])


if __name__ == "__main__":
    main()