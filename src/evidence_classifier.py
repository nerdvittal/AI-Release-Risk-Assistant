def classify_evidence(
    statement,
    release_id,
    source
):
    text = statement.lower()

    base = {
        "evidence_id": None,
        "statement": statement,
        "release_id": release_id,
        "source": source,
        "evidence_type": "FACT",
        "severity": None,
        "recommendation": None
    }

    # ==================================================
    # RECOMMENDATION
    # ==================================================

    if "recommended blocking deployment" in text:

        base["evidence_type"] = "RECOMMENDATION"

        base["recommendation"] = (
            "Block deployment"
        )

        return base

    # ==================================================
    # APPROVAL
    # ==================================================

    if (
        "approved deployment" in text
        or "approved the deployment" in text
        or "deployment was approved" in text
        or "release manager approved" in text
        or "release manager has approved" in text
    ):

        base["evidence_type"] = "APPROVAL"

        return base

    # ==================================================
    # SECURITY / RISK
    # ==================================================

    if "vulnerability" in text:

        base["evidence_type"] = "RISK"

        if "critical" in text:

            base["severity"] = "critical"

        elif "high" in text:

            base["severity"] = "high"

        elif "medium" in text:

            base["severity"] = "medium"

        return base

    # ==================================================
    # CUSTOMER / PRODUCTION IMPACT
    # ==================================================

    if "customers experienced" in text:

        base["evidence_type"] = "IMPACT"

        return base

    # ==================================================
    # RESOLUTION
    # ==================================================

    if "resolved" in text:

        base["evidence_type"] = "RESOLUTION"

        return base

    # ==================================================
    # DEFAULT
    # ==================================================

    return base


if __name__ == "__main__":

    test_statements = [

        (
            "The release contained a critical "
            "authentication vulnerability."
        ),

        (
            "Security recommended blocking deployment."
        ),

        (
            "The Release Manager approved deployment."
        ),

        (
            "Two hours after deployment, "
            "2,300 customers experienced payment failures."
        ),

        (
            "The issue was resolved after restarting "
            "the payment service."
        ),

        (
            "All planned tests passed."
        )
    ]

    print(
        "\n========== EVIDENCE CLASSIFICATION TEST =========="
    )

    for index, statement in enumerate(
        test_statements,
        start=1
    ):

        result = classify_evidence(
            statement,
            "530",
            "release_530.txt"
        )

        print(
            f"\nE{index:03d}"
        )

        print(
            f"Statement: {result['statement']}"
        )

        print(
            f"Type: {result['evidence_type']}"
        )

        print(
            f"Severity: {result['severity']}"
        )

        print(
            f"Recommendation: "
            f"{result['recommendation']}"
        )

    print(
        "\n=================================================="
    )