import re


def normalize_text(text):
    """
    Normalize text for basic comparison.

    This is intentionally conservative.
    It does NOT try to understand meaning.
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def extract_sentences(context):
    """
    Split source context into sentence-like units.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        context.strip()
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def statement_contains_key_terms(
    source_sentence,
    extracted_statement
):
    """
    Check whether important terms from the source
    appear in the extracted statement.

    This is NOT semantic validation.
    It is an initial deterministic safety check.
    """

    source_words = set(
        normalize_text(
            source_sentence
        ).split()
    )

    extracted_words = set(
        normalize_text(
            extracted_statement
        ).split()
    )

    if not source_words:
        return True

    overlap = (
        source_words
        & extracted_words
    )

    overlap_ratio = (
        len(overlap)
        / len(source_words)
    )

    return overlap_ratio >= 0.50


def validate_extraction(
    context,
    extracted_evidence
):
    """
    Compare source statements against extracted evidence.

    Returns a validation report.
    """

    source_sentences = extract_sentences(
        context
    )

    extracted_statements = [
        item.get(
            "statement",
            ""
        )
        for item in extracted_evidence
    ]

    missing_sentences = []

    for sentence in source_sentences:

        matched = False

        for statement in extracted_statements:

            if statement_contains_key_terms(
                sentence,
                statement
            ):
                matched = True
                break

        if not matched:

            missing_sentences.append(
                sentence
            )

    return {
        "status": (
            "PASS"
            if not missing_sentences
            else "INCOMPLETE"
        ),
        "source_statement_count":
            len(source_sentences),
        "extracted_statement_count":
            len(extracted_statements),
        "missing_statements":
            missing_sentences
    }


if __name__ == "__main__":

    context = """
Release 530 Production Report

Release 530 was deployed on September 24.

The deployment completed successfully.

All planned tests passed.

A critical authentication vulnerability was identified.

Security recommended blocking deployment.

The Release Manager approved deployment.
"""

    extracted_evidence = [
        {
            "statement":
                "Release 530 was deployed on September 24."
        },
        {
            "statement":
                "The deployment completed successfully."
        },
        {
            "statement":
                "All planned tests passed."
        },
        {
            "statement":
                "Security recommended blocking deployment."
        }
    ]

    result = validate_extraction(
        context,
        extracted_evidence
    )

    print(
        "\n========== EVIDENCE VALIDATION =========="
    )

    print(
        f"Status: {result['status']}"
    )

    print(
        f"Source statements: "
        f"{result['source_statement_count']}"
    )

    print(
        f"Extracted statements: "
        f"{result['extracted_statement_count']}"
    )

    print(
        "\nMissing statements:"
    )

    if result["missing_statements"]:

        for statement in result[
            "missing_statements"
        ]:

            print(
                f"• {statement}"
            )

    else:

        print(
            "None"
        )

    print(
        "\n=========================================="
    )