def format_answer(
    question,
    question_intent,
    selected_evidence,
    assessment
):

    # ==================================================
    # NO EVIDENCE
    # ==================================================

    if not selected_evidence:

        return (
            "The supplied evidence does not contain "
            "information sufficient to answer the question."
        )

    # ==================================================
    # ROOT CAUSE
    # ==================================================

    if question_intent == "ROOT_CAUSE":

        statements = [
            item["statement"]
            for item in selected_evidence
        ]

        return " ".join(statements)

    # ==================================================
    # SECURITY RISK
    # ==================================================

    if question_intent == "SECURITY_RISK":

        statements = [
            item["statement"]
            for item in selected_evidence
        ]

        return " ".join(statements)

    # ==================================================
    # PRODUCTION IMPACT
    # ==================================================

    if question_intent == "PRODUCTION_IMPACT":

        statements = [
            item["statement"]
            for item in selected_evidence
        ]

        return " ".join(statements)

    # ==================================================
    # RESOLUTION
    # ==================================================

    if question_intent == "RESOLUTION":

        statements = [
            item["statement"]
            for item in selected_evidence
        ]

        return " ".join(statements)

    # ==================================================
    # RECOMMENDATION
    # ==================================================

    if question_intent == "RECOMMENDATION":

        statements = [
            item["statement"]
            for item in selected_evidence
        ]

        return " ".join(statements)

    # ==================================================
    # APPROVAL
    # ==================================================

    if question_intent == "APPROVAL":

        statements = [
            item["statement"]
            for item in selected_evidence
        ]

        return " ".join(statements)

    # ==================================================
    # RELEASE READINESS
    # ==================================================

    if question_intent == "RELEASE_READINESS":

        return (
            f"Authoritative status: "
            f"{assessment['status']}. "
            f"Risk status: "
            f"{assessment['risk_status']}. "
            f"Governance status: "
            f"{assessment['governance_status']}."
        )

    # ==================================================
    # UNKNOWN / GENERAL QUESTION
    # ==================================================

    statements = [
        item["statement"]
        for item in selected_evidence
    ]

    return (
        "The supplied evidence contains the following "
        "documented information: "
        + " ".join(statements)
    )


if __name__ == "__main__":

    test_evidence = [

        {
            "evidence_id": "E001",
            "statement":
                "The Release Manager approved deployment.",
            "evidence_type": "APPROVAL"
        }
    ]

    test_assessment = {

        "status":
            "CONFLICTING_EVIDENCE",

        "risk_status":
            "BLOCKED",

        "governance_status":
            "CONFLICTING_EVIDENCE"
    }

    answer = format_answer(
        "Who approved the deployment?",
        "APPROVAL",
        test_evidence,
        test_assessment
    )

    print(
        "\n========== TEST ANSWER =========="
    )

    print(answer)

    print(
        "================================="
    )