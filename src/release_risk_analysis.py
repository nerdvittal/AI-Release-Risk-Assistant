import json
from pathlib import Path

from chroma_search import (
    search_chroma,
    detect_release_id
)

from parent_child_retrieval import (
    build_parent_documents
)

from reranker import (
    SemanticReranker
)

from evidence_extractor import (
    extract_evidence
)

from evidence_classifier import (
    classify_evidence
)

from release_readiness import (
    assess_release_readiness
)

from final_report import (
    generate_final_report
)

from question_intent import (
    detect_question_intent
)

from evidence_selector import (
    select_evidence
)

from answer_formatter import (
    format_answer
)


PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

DATA_DIRECTORY = (
    PROJECT_ROOT / "data"
)

TOP_K_CHILDREN = 5
TOP_K_PARENTS = 3


# ============================================================
# RELEASE DETECTION
# ============================================================

def detect_requested_release(question):
    """
    Detect an explicitly mentioned release number.

    Examples:
        Release 530
        release_530
        rel 530
        rel-530
    """

    return detect_release_id(question)


# ============================================================
# BUILD PARENT CANDIDATES
# ============================================================

def build_parent_candidates(
    question,
    release_id=None
):
    """
    Retrieve child chunks first and then expand them
    into parent release context.
    """

    if release_id:

        child_results = search_chroma(
            question,
            top_k=TOP_K_CHILDREN,
            release_id=release_id
        )

    else:

        child_results = search_chroma(
            question,
            top_k=TOP_K_CHILDREN
        )

    parent_documents = (
        build_parent_documents()
    )

    candidates = []

    seen_parents = set()

    documents = child_results.get(
        "documents",
        [[]]
    )[0]

    metadatas = child_results.get(
        "metadatas",
        [[]]
    )[0]

    distances = child_results.get(
        "distances",
        [[]]
    )[0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        metadata = metadata or {}

        current_release_id = str(
            metadata.get(
                "release_id",
                ""
            )
        )

        parent_id = (
            f"release_"
            f"{current_release_id}"
            f"_parent"
        )

        if parent_id in seen_parents:
            continue

        parent = parent_documents.get(
            parent_id
        )

        if parent is None:
            continue

        seen_parents.add(
            parent_id
        )

        candidates.append(
            {
                "document":
                    parent["document"],

                "metadata": {
                    "release_id":
                        current_release_id,

                    "parent_id":
                        parent_id,

                    "matched_child":
                        metadata.get(
                            "chunk_id"
                        )
                },

                "child_distance":
                    distance
            }
        )

    return candidates


# ============================================================
# RERANK PARENT CONTEXT
# ============================================================

def retrieve_parent_context(
    question,
    release_id=None
):
    """
    Retrieve parent release documents and rerank them
    using the ready-made Cross-Encoder.
    """

    candidates = build_parent_candidates(
        question,
        release_id
    )

    if not candidates:
        return []

    reranker = SemanticReranker()

    ranked_candidates = (
        reranker.rerank(
            question,
            candidates
        )
    )

    return ranked_candidates[
        :TOP_K_PARENTS
    ]


# ============================================================
# SOURCE NAME
# ============================================================

def build_source_name(
    release_id
):
    return (
        f"Release {release_id} "
        f"Production Report"
    )


# ============================================================
# DOCUMENT STATUS
# ============================================================

def get_release_document_status(
    release_id
):
    """
    Check whether the requested release document
    exists and contains usable content.
    """

    input_file = (
        DATA_DIRECTORY
        / f"release_{release_id}.txt"
    )

    if not input_file.exists():
        return "NOT_FOUND"

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()

    if not content.strip():
        return "EMPTY"

    return "VALID"


# ============================================================
# EMPTY / NOT FOUND ASSESSMENT
# ============================================================

def build_empty_assessment(
    document_status
):
    if document_status == "EMPTY":

        return {
            "status":
                "INSUFFICIENT_EVIDENCE",

            "risk_status":
                "UNKNOWN",

            "governance_status":
                "NOT_ASSESSABLE",

            "reasons": [],

            "risks": [],

            "impacts": [],

            "resolutions": [],

            "recommendations": [],

            "approvals": [],

            "evidence_gaps": [
                "The requested release document is empty."
            ]
        }

    return {
        "status":
            "INSUFFICIENT_EVIDENCE",

        "risk_status":
            "UNKNOWN",

        "governance_status":
            "NOT_ASSESSABLE",

        "reasons": [],

        "risks": [],

        "impacts": [],

        "resolutions": [],

        "recommendations": [],

        "approvals": [],

        "evidence_gaps": [
            "The requested release document "
            "could not be found."
        ]
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n=================================================="
    )

    print(
        "        AI RELEASE RISK ASSISTANT"
    )

    print(
        "=================================================="
    )

    # ========================================================
    # USER QUESTION
    # ========================================================

    question = input(
        "\nEnter your question: "
    ).strip()

    if not question:

        print(
            "\nQuestion cannot be empty."
        )

        return

    # ========================================================
    # QUESTION INTENT
    # ========================================================

    question_intent = (
        detect_question_intent(
            question
        )
    )

    print(
        "\n========== QUESTION INTENT =========="
    )

    print(
        f"Question: {question}"
    )

    print(
        f"Intent: {question_intent}"
    )

    print(
        "====================================="
    )

    # ========================================================
    # RELEASE DETECTION
    # ========================================================

    requested_release = (
        detect_requested_release(
            question
        )
    )

    if requested_release:

        print(
            "\n========== RELEASE SCOPE =========="
        )

        print(
            f"Requested release: "
            f"{requested_release}"
        )

        print(
            "Retrieval scope: "
            f"Release {requested_release}"
        )

        print(
            "==================================="
        )

    else:

        print(
            "\n========== RELEASE SCOPE =========="
        )

        print(
            "No specific release detected."
        )

        print(
            "Retrieval scope: "
            "All indexed releases"
        )

        print(
            "==================================="
        )

    # ========================================================
    # EXPLICIT RELEASE DOCUMENT VALIDATION
    # ========================================================

    if requested_release:

        document_status = (
            get_release_document_status(
                requested_release
            )
        )

        if document_status == "EMPTY":

            print(
                "\n========== DOCUMENT STATUS =========="
            )

            print(
                "The requested release document "
                "is empty."
            )

            print(
                "Status: EMPTY"
            )

            print(
                "===================================="
            )

            assessment = (
                build_empty_assessment(
                    document_status
                )
            )

            answer = format_answer(
                question,
                question_intent,
                [],
                assessment
            )

            print(
                "\n========== ANSWER =========="
            )

            print(answer)

            print(
                "============================"
            )

            generate_final_report(
                assessment,
                [],
                question,
                document_status=document_status
            )

            return

        if document_status == "NOT_FOUND":

            print(
                "\n========== DOCUMENT STATUS =========="
            )

            print(
                "The requested release document "
                "was not found locally."
            )

            print(
                "Status: NOT_FOUND"
            )

            print(
                "===================================="
            )

            assessment = (
                build_empty_assessment(
                    document_status
                )
            )

            answer = format_answer(
                question,
                question_intent,
                [],
                assessment
            )

            print(
                "\n========== ANSWER =========="
            )

            print(answer)

            print(
                "============================"
            )

            generate_final_report(
                assessment,
                [],
                question,
                document_status=document_status
            )

            return

    # ========================================================
    # RETRIEVAL
    # ========================================================

    print(
        "\n========== RETRIEVAL =========="
    )

    if requested_release:

        print(
            f"Searching Release "
            f"{requested_release}..."
        )

    else:

        print(
            "Searching across all releases..."
        )

    ranked_parents = (
        retrieve_parent_context(
            question,
            requested_release
        )
    )

    if not ranked_parents:

        print(
            "No matching release evidence "
            "was retrieved."
        )

        print(
            "================================"
        )

        assessment = (
            build_empty_assessment(
                "NOT_FOUND"
            )
        )

        answer = format_answer(
            question,
            question_intent,
            [],
            assessment
        )

        print(
            "\n========== ANSWER =========="
        )

        print(answer)

        print(
            "============================"
        )

        generate_final_report(
            assessment,
            [],
            question,
            document_status="INSUFFICIENT_EVIDENCE"
        )

        return

    for index, candidate in enumerate(
        ranked_parents,
        start=1
    ):

        metadata = candidate.get(
            "metadata",
            {}
        )

        print(
            f"Rank {index} | "
            f"Release "
            f"{metadata.get('release_id')} | "
            f"Matched child: "
            f"{metadata.get('matched_child')} | "
            f"Cross-Encoder score: "
            f"{candidate.get('rerank_score', 0):.4f}"
        )

    print(
        "================================"
    )

    # ========================================================
    # EVIDENCE EXTRACTION
    # ========================================================

    print(
        "\n========== EVIDENCE EXTRACTION =========="
    )

    classified_evidence = []

    evidence_counter = 1

    for candidate in ranked_parents:

        metadata = candidate.get(
            "metadata",
            {}
        )

        release_id = str(
            metadata.get(
                "release_id"
            )
        )

        source_name = (
            build_source_name(
                release_id
            )
        )

        context = candidate.get(
            "document",
            ""
        )

        if not context.strip():
            continue

        print(
            f"\nProcessing Release "
            f"{release_id}..."
        )

        atomic_evidence = (
            extract_evidence(
                context
            )
        )

        for item in atomic_evidence:

            statement = item.get(
                "statement"
            )

            if not statement:
                continue

            evidence = classify_evidence(
                statement,
                release_id,
                source_name
            )

            evidence["evidence_id"] = (
                f"E{evidence_counter:03d}"
            )

            classified_evidence.append(
                evidence
            )

            evidence_counter += 1

    print(
        "\n=========================================="
    )

    # ========================================================
    # QUESTION-SPECIFIC EVIDENCE
    # ========================================================

    selected_evidence = (
        select_evidence(
            classified_evidence,
            question_intent
        )
    )

    print(
        "\n========== SELECTED EVIDENCE =========="
    )

    if selected_evidence:

        for item in selected_evidence:

            print(
                f"[{item['evidence_id']}] "
                f"[{item['evidence_type']}] "
                f"{item['statement']}"
            )

    else:

        print(
            "No question-specific evidence found."
        )

    print(
        "========================================"
    )

    # ========================================================
    # RELEASE READINESS
    # ========================================================

    if classified_evidence:

        assessment = (
            assess_release_readiness(
                classified_evidence,
                document_status="VALID"
            )
        )

    else:

        assessment = (
            build_empty_assessment(
                "VALID"
            )
        )

    # ========================================================
    # ANSWER
    # ========================================================

    answer = format_answer(
        question,
        question_intent,
        selected_evidence,
        assessment
    )

    print(
        "\n========== ANSWER =========="
    )

    print(answer)

    print(
        "============================"
    )

    # ========================================================
    # STRUCTURED EVIDENCE
    # ========================================================

    print(
        "\n========== STRUCTURED EVIDENCE =========="
    )

    print(
        json.dumps(
            classified_evidence,
            indent=2
        )
    )

    print(
        "=========================================="
    )

    # ========================================================
    # RELEASE READINESS
    # ========================================================

    print(
        "\n========== RELEASE READINESS =========="
    )

    print(
        json.dumps(
            assessment,
            indent=2
        )
    )

    print(
        "========================================"
    )

    # ========================================================
    # FINAL AUDIT REPORT
    # ========================================================

    generate_final_report(
        assessment,
        selected_evidence,
        question,
        document_status="VALID"
    )


if __name__ == "__main__":
    main()