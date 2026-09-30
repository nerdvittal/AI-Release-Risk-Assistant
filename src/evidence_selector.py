def select_evidence(
    classified_evidence,
    question_intent
):

    # ==================================================
    # ROOT CAUSE
    # ==================================================

    if question_intent == "ROOT_CAUSE":

        selected = []

        for item in classified_evidence:

            statement = item.get(
                "statement",
                ""
            ).lower()

            evidence_type = item.get(
                "evidence_type"
            )

            if (
                evidence_type == "FACT"
                and (
                    "root cause" in statement
                    or "caused" in statement
                )
            ):

                selected.append(item)

        return selected

    # ==================================================
    # SECURITY RISK
    # ==================================================

    if question_intent == "SECURITY_RISK":

        return [
            item
            for item in classified_evidence
            if item.get("evidence_type") == "RISK"
        ]

    # ==================================================
    # PRODUCTION IMPACT
    # ==================================================

    if question_intent == "PRODUCTION_IMPACT":

        return [
            item
            for item in classified_evidence
            if item.get("evidence_type") == "IMPACT"
        ]

    # ==================================================
    # RESOLUTION
    # ==================================================

    if question_intent == "RESOLUTION":

        return [
            item
            for item in classified_evidence
            if item.get("evidence_type") == "RESOLUTION"
        ]

    # ==================================================
    # RECOMMENDATION
    # ==================================================

    if question_intent == "RECOMMENDATION":

        return [
            item
            for item in classified_evidence
            if item.get("evidence_type") == "RECOMMENDATION"
        ]

    if question_intent == "APPROVAL":

        return [
            item
            for item in classified_evidence
            if item.get("evidence_type") == "APPROVAL"
    ]
    # ==================================================
    # RELEASE READINESS
    # ==================================================
    #
    # Readiness questions require the complete
    # assessment rather than a subset of evidence.
    #
    # Therefore return all evidence.
    #

    if question_intent == "RELEASE_READINESS":

        return classified_evidence

    # ==================================================
    # UNKNOWN
    # ==================================================
    #
    # Preserve all evidence when the system does not
    # understand the question.
    #

    return classified_evidence


# ======================================================
# TEST
# ======================================================

if __name__ == "__main__":

    test_evidence = [

        {
            "evidence_id": "E001",
            "statement":
                "Two hours after deployment, 2,300 customers experienced payment failures.",
            "evidence_type":
                "IMPACT"
        },

        {
            "evidence_id": "E002",
            "statement":
                "The root cause was connection pool exhaustion.",
            "evidence_type":
                "FACT"
        },

        {
            "evidence_id": "E003",
            "statement":
                "A temporary workaround was available.",
            "evidence_type":
                "FACT"
        },

        {
            "evidence_id": "E004",
            "statement":
                "The issue was resolved after restarting the payment service.",
            "evidence_type":
                "RESOLUTION"
        },

        {
            "evidence_id": "E005",
            "statement":
                "The release contained a critical authentication vulnerability.",
            "evidence_type":
                "RISK"
        },

        {
            "evidence_id": "E006",
            "statement":
                "Security recommended blocking deployment.",
            "evidence_type":
                "RECOMMENDATION"
        }
    ]

    test_intents = [

        "ROOT_CAUSE",

        "SECURITY_RISK",

        "PRODUCTION_IMPACT",

        "RESOLUTION",

        "RECOMMENDATION",

        "RELEASE_READINESS",

        "UNKNOWN"
    ]

    print(
        "\n========== EVIDENCE SELECTION TEST =========="
    )

    for intent in test_intents:

        selected = select_evidence(
            test_evidence,
            intent
        )

        print(
            f"\nINTENT: {intent}"
        )

        if selected:

            for item in selected:

                print(
                    f"[{item['evidence_id']}] "
                    f"{item['statement']}"
                )

        else:

            print(
                "No matching evidence."
            )

        print(
            "------------------------------------------"
        )

    print(
        "\n============================================"
    )