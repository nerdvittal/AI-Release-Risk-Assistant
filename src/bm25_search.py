import chromadb
from rank_bm25 import BM25Okapi


PROJECT_ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent

CHROMA_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "chroma_db"
)

COLLECTION_NAME = "release_evidence"


def tokenize(text):
    return text.lower().split()


def load_documents():
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

    documents = results["documents"]
    metadatas = results["metadatas"]

    records = []

    for document, metadata in zip(
        documents,
        metadatas
    ):
        records.append(
            {
                "document": document,
                "metadata": metadata
            }
        )

    return records


def search_bm25(
    question,
    top_k=5
):
    records = load_documents()

    if not records:
        return []

    tokenized_documents = [
        tokenize(record["document"])
        for record in records
    ]

    bm25 = BM25Okapi(
        tokenized_documents
    )

    query_tokens = tokenize(question)

    scores = bm25.get_scores(
        query_tokens
    )

    ranked_indexes = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True
    )

    results = []

    for index in ranked_indexes[:top_k]:

        result = {
            "document": records[index]["document"],
            "metadata": records[index]["metadata"],
            "bm25_score": float(scores[index])
        }

        results.append(result)

    return results


if __name__ == "__main__":

    question = input(
        "Enter your question: "
    ).strip()

    results = search_bm25(
        question
    )

    print("\n" + "=" * 70)
    print("BM25 SEARCH RESULTS")
    print("=" * 70)

    for rank, result in enumerate(
        results,
        start=1
    ):
        print(
            f"\nRank {rank}"
        )

        print(
            f"BM25 score: "
            f"{result['bm25_score']:.4f}"
        )

        print(
            f"Release: "
            f"{result['metadata'].get('release_id')}"
        )

        print(
            f"Chunk: "
            f"{result['metadata'].get('chunk_id')}"
        )

        print("\nContent:")
        print(result["document"])