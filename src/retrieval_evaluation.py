import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIRECTORY = PROJECT_ROOT / "src"
DATA_DIRECTORY = PROJECT_ROOT / "data"

if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from retrieval_pipeline import (
    search_chroma,
    build_hybrid_candidates
)
from reranker import SemanticReranker


TOP_K = 3
GOLDEN_DATASET_FILE = (
    DATA_DIRECTORY / "golden_dataset.json"
)


def load_golden_dataset():
    with open(
        GOLDEN_DATASET_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        dataset = json.load(file)

    return dataset["cases"]


def candidate_key(candidate):
    metadata = candidate["metadata"]

    return (
        str(metadata.get("release_id")),
        str(metadata.get("chunk_id"))
    )


def calculate_precision_at_k(
    candidates,
    expected_chunks,
    k=TOP_K
):
    top_candidates = candidates[:k]

    if not top_candidates:
        return 0.0

    relevant_count = sum(
        1
        for candidate in top_candidates
        if candidate_key(candidate) in expected_chunks
    )

    return relevant_count / k


def calculate_recall_at_k(
    candidates,
    expected_chunks,
    k=TOP_K
):
    top_candidates = candidates[:k]

    if not expected_chunks:
        return 0.0

    retrieved_relevant = sum(
        1
        for candidate in top_candidates
        if candidate_key(candidate) in expected_chunks
    )

    return retrieved_relevant / len(expected_chunks)


def calculate_mrr(
    candidates,
    expected_chunks
):
    for rank, candidate in enumerate(
        candidates[:TOP_K],
        start=1
    ):
        if candidate_key(candidate) in expected_chunks:
            return 1.0 / rank

    return 0.0


def evaluate_mode(
    mode_name,
    dataset,
    retrieval_function,
    reranker=None
):
    print("\n" + "=" * 80)
    print(mode_name)
    print("=" * 80)

    precision_scores = []
    recall_scores = []
    mrr_scores = []

    for item in dataset:

        question = item["question"]

        expected_chunks = {
            tuple(chunk)
            for chunk in item["expected_chunks"]
        }

        candidates = retrieval_function(
            question
        )

        if reranker is not None:
            candidates = reranker.rerank(
                question,
                candidates
            )

        precision = calculate_precision_at_k(
            candidates,
            expected_chunks
        )

        recall = calculate_recall_at_k(
            candidates,
            expected_chunks
        )

        mrr = calculate_mrr(
            candidates,
            expected_chunks
        )

        precision_scores.append(precision)
        recall_scores.append(recall)
        mrr_scores.append(mrr)

        print(
            f"\nQuestion: {question}"
        )

        print("Retrieved:")

        for rank, candidate in enumerate(
            candidates[:TOP_K],
            start=1
        ):
            print(
                f"  {rank}. "
                f"{candidate_key(candidate)}"
            )

        print(
            f"Precision@3: {precision:.2f} | "
            f"Recall@3: {recall:.2f} | "
            f"MRR: {mrr:.2f}"
        )

    average_precision = (
        sum(precision_scores)
        / len(precision_scores)
    )

    average_recall = (
        sum(recall_scores)
        / len(recall_scores)
    )

    average_mrr = (
        sum(mrr_scores)
        / len(mrr_scores)
    )

    print("\n" + "-" * 80)

    print(
        f"Average Precision@3: "
        f"{average_precision:.2f}"
    )

    print(
        f"Average Recall@3: "
        f"{average_recall:.2f}"
    )

    print(
        f"Average MRR: "
        f"{average_mrr:.2f}"
    )

    return {
        "precision": average_precision,
        "recall": average_recall,
        "mrr": average_mrr
    }


def main():

    dataset = load_golden_dataset()

    print("\nRETRIEVAL EVALUATION")
    print(
        "\nGolden dataset size:",
        len(dataset)
    )

    chroma_results = evaluate_mode(
        "1. CHROMA BASELINE",
        dataset,
        lambda question: search_chroma(
            question,
            top_k=5
        )
    )

    hybrid_results = evaluate_mode(
        "2. HYBRID: CHROMA + BM25",
        dataset,
        build_hybrid_candidates
    )

    print("\nLoading Cross-Encoder once...")

    reranker = SemanticReranker()

    hybrid_reranked_results = evaluate_mode(
        "3. HYBRID + CROSS-ENCODER",
        dataset,
        build_hybrid_candidates,
        reranker
    )

    print("\n" + "=" * 80)
    print("FINAL COMPARISON")
    print("=" * 80)

    print(
        "\nMode                         "
        "Precision@3   Recall@3   MRR"
    )

    print(
        f"Chroma baseline             "
        f"{chroma_results['precision']:.2f}"
        f"           "
        f"{chroma_results['recall']:.2f}"
        f"        "
        f"{chroma_results['mrr']:.2f}"
    )

    print(
        f"Hybrid                      "
        f"{hybrid_results['precision']:.2f}"
        f"           "
        f"{hybrid_results['recall']:.2f}"
        f"        "
        f"{hybrid_results['mrr']:.2f}"
    )

    print(
        f"Hybrid + Cross-Encoder     "
        f"{hybrid_reranked_results['precision']:.2f}"
        f"           "
        f"{hybrid_reranked_results['recall']:.2f}"
        f"        "
        f"{hybrid_reranked_results['mrr']:.2f}"
    )


if __name__ == "__main__":
    main()