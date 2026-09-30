def generate_final_report(
    assessment,
    evidence,
    question,
    document_status="VALID"
):

    print(
        "\n=================================================="
    )

    print(
        "        AI RELEASE RISK ASSISTANT"
    )

    print(
        "=================================================="
    )

    # ==================================================
    # DOCUMENT STATUS
    # ==================================================

    print(
        "\nDOCUMENT STATUS"
    )

    print(
        "---------------"
    )

    print(
        document_status
    )

    # ==================================================
    # QUESTION
    # ==================================================

    print(
        "\nQUESTION"
    )

    print(
        "--------"
    )

    print(
        question
    )

    # ==================================================
    # AUTHORITATIVE STATUS
    # ==================================================

    print(
        "\nAUTHORITATIVE STATUS"
    )

    print(
        "--------------------"
    )

    print(
        assessment["status"]
    )

    # ==================================================
    # RISK STATUS
    # ==================================================

    print(
        "\nRISK STATUS"
    )

    print(
        "-----------"
    )

    print(
        assessment["risk_status"]
    )

    # ==================================================
    # GOVERNANCE STATUS
    # ==================================================

    print(
        "\nGOVERNANCE STATUS"
    )

    print(
        "-----------------"
    )

    print(
        assessment["governance_status"]
    )

    # ==================================================
    # EVIDENCE
    # ==================================================

    print(
        "\nEVIDENCE"
    )

    print(
        "--------"
    )

    if evidence:

        for item in evidence:

            evidence_id = item.get(
                "evidence_id",
                "UNKNOWN"
            )

            statement = item.get(
                "statement",
                ""
            )

            evidence_type = item.get(
                "evidence_type",
                "FACT"
            )

            print(
                f"[{evidence_id}] "
                f"[{evidence_type}] "
                f"{statement}"
            )

    else:

        print(
            "No evidence is available from "
            "the supplied document."
        )

    # ==================================================
    # DECISION REASONS
    # ==================================================

    print(
        "\nDECISION REASONS"
    )

    print(
        "----------------"
    )

    if assessment["reasons"]:

        for item in assessment["reasons"]:

            print(
                f"• {item}"
            )

    else:

        print(
            "• No blocking or material-risk "
            "reason documented."
        )

    # ==================================================
    # RISKS
    # ==================================================

    print(
        "\nRISKS"
    )

    print(
        "-----"
    )

    if assessment["risks"]:

        for item in assessment["risks"]:

            print(
                f"• {item}"
            )

    elif document_status == "EMPTY":

        print(
            "• Risk status cannot be determined "
            "because the document is empty."
        )

    else:

        print(
            "• No documented risks identified."
        )

    # ==================================================
    # IMPACTS
    # ==================================================

    print(
        "\nIMPACTS"
    )

    print(
        "-------"
    )

    if assessment["impacts"]:

        for item in assessment["impacts"]:

            print(
                f"• {item}"
            )

    else:

        print(
            "• No documented impacts identified."
        )

    # ==================================================
    # RESOLUTIONS
    # ==================================================

    print(
        "\nRESOLUTIONS"
    )

    print(
        "-----------"
    )

    if assessment["resolutions"]:

        for item in assessment["resolutions"]:

            print(
                f"• {item}"
            )

    else:

        print(
            "• No documented resolutions identified."
        )

    # ==================================================
    # RECOMMENDATIONS
    # ==================================================

    print(
        "\nRECOMMENDATIONS"
    )

    print(
        "---------------"
    )

    if assessment["recommendations"]:

        for item in assessment["recommendations"]:

            print(
                f"• {item}"
            )

    else:

        print(
            "• No documented recommendations."
        )

    # ==================================================
    # EVIDENCE GAPS
    # ==================================================

    print(
        "\nEVIDENCE GAPS"
    )

    print(
        "-------------"
    )

    if assessment["evidence_gaps"]:

        for item in assessment["evidence_gaps"]:

            print(
                f"• {item}"
            )

    else:

        print(
            "• None documented."
        )

    # ==================================================
    # HUMAN SIGN-OFF
    # ==================================================

    print(
        "\nHUMAN SIGN-OFF"
    )

    print(
        "--------------"
    )

    print(
        "Required"
    )

    print(
        "\n=================================================="
    )


if __name__ == "__main__":

    test_assessment = {

        "status": "BLOCKED",

        "risk_status": "BLOCKED",

        "governance_status":
            "APPROVAL_NOT_DOCUMENTED",

        "reasons": [
            "The release contained a critical authentication vulnerability.",
            "Security recommended blocking deployment."
        ],

        "risks": [
            "The release contained a critical authentication vulnerability."
        ],

        "impacts": [
            "Two hours after deployment, 2,300 customers experienced payment failures."
        ],

        "resolutions": [
            "The issue was resolved after restarting the payment service."
        ],

        "recommendations": [
            "Security recommended blocking deployment."
        ],

        "evidence_gaps": [
            "No final deployment approval decision is documented."
        ]
    }

    test_evidence = [

        {
            "evidence_id": "E001",
            "statement":
                "Two hours after deployment, 2,300 customers experienced payment failures.",
            "evidence_type": "IMPACT"
        },

        {
            "evidence_id": "E002",
            "statement":
                "The root cause was connection pool exhaustion.",
            "evidence_type": "FACT"
        },

        {
            "evidence_id": "E005",
            "statement":
                "The release contained a critical authentication vulnerability.",
            "evidence_type": "RISK"
        },

        {
            "evidence_id": "E006",
            "statement":
                "Security recommended blocking deployment.",
            "evidence_type": "RECOMMENDATION"
        }
    ]

    generate_final_report(
        test_assessment,
        test_evidence,
        "What caused the payment failures?"
    )