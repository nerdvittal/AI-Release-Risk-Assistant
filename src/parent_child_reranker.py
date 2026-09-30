import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIRECTORY = PROJECT_ROOT / "src"

if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from parent_child_retrieval import (
    retrieve_parent_context
)

from reranker import SemanticReranker


TOP_K_PARENTS = 3


def rerank_parent_context(
    question
):
    parent_candidates = (
        retrieve_parent_context(question)
    )

    if not parent_candidates:
        return []

    reranker = SemanticReranker()

    rerank_candidates = []

    for candidate in parent_candidates:

        rerank_candidates.append(
            {
                "document": candidate["document"],
                "metadata": {
                    "release_id": candidate[
                        "release_id"
                    ],
                    "parent_id": candidate[
                        "parent_id"
                    ],
                    "matched_child": candidate[
                        "matched_child"
                    ]
                },
                "child_distance": candidate[
                    "child_distance"
                ]
            }
        )

    ranked = reranker.rerank(
        question,
        rerank_candidates
    )

    return ranked


def main():

    question = input(
        "Enter your question: "
    ).strip()

    if not question:
        print("Question cannot be empty.")
        return

    results = rerank_parent_context(
        question
    )

    print("\n" + "=" * 70)
    print("PARENT + CROSS-ENCODER")
    print("=" * 70)

    for rank, result in enumerate(
        results[:TOP_K_PARENTS],
        start=1
    ):

        metadata = result["metadata"]

        print(
            f"\nRank {rank}"
        )

        print(
            f"Release: "
            f"{metadata['release_id']}"
        )

        print(
            f"Matched child: "
            f"{metadata['matched_child']}"
        )

        print(
            f"Rerank score: "
            f"{result['rerank_score']:.4f}"
        )

        print("\nParent context:")
        print(result["document"])


if __name__ == "__main__":
    main()