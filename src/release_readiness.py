import json


def assess_release_readiness(
    evidence,
    document_status="VALID"
):

    # ==================================================
    # EMPTY DOCUMENT
    # ==================================================

    if document_status == "EMPTY":

        return {
            "status": "INSUFFICIENT_EVIDENCE",
            "risk_status": "UNKNOWN",
            "governance_status": "NOT_ASSESSABLE",
            "document_status": "EMPTY",
            "reasons": [],
            "risks": [],
            "impacts": [],
            "resolutions": [],
            "recommendations": [],
            "approvals": [],
            "evidence_gaps": [
                "The supplied release document is empty.",
                "Release risk cannot be assessed without release evidence.",
                "No final deployment approval decision is documented."
            ]
        }

    # ==================================================
    # STATE FLAGS
    # ==================================================

    has_blocking_recommendation = False
    has_material_risk = False
    approval_documented = False

    # ==================================================
    # EVIDENCE COLLECTION
    # ==================================================

    reasons = []
    risks = []
    impacts = []
    resolutions = []
    recommendations = []
    approvals = []
    evidence_gaps = []

    for item in evidence:

        evidence_type = item.get(
            "evidence_type"
        )

        statement = item.get(
            "statement"
        )

        severity = item.get(
            "severity"
        )

        recommendation = item.get(
            "recommendation"
        )

        # ----------------------------------------------
        # APPROVAL
        # ----------------------------------------------

        if evidence_type == "APPROVAL":

            approval_documented = True

            approvals.append(
                statement
            )

        # ----------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------

        elif evidence_type == "RECOMMENDATION":

            recommendations.append(
                statement
            )

            if recommendation:

                recommendation_text = (
                    recommendation.lower()
                )

                if "block" in recommendation_text:

                    has_blocking_recommendation = True

                    reasons.append(
                        statement
                    )

        # ----------------------------------------------
        # RISK
        # ----------------------------------------------

        elif evidence_type == "RISK":

            risks.append(
                statement
            )

            if severity:

                severity_level = (
                    severity.lower()
                )

                if severity_level in [
                    "critical",
                    "high",
                    "medium"
                ]:

                    has_material_risk = True

                    reasons.append(
                        statement
                    )

        # ----------------------------------------------
        # IMPACT
        # ----------------------------------------------

        elif evidence_type == "IMPACT":

            impacts.append(
                statement
            )

        # ----------------------------------------------
        # RESOLUTION
        # ----------------------------------------------

        elif evidence_type == "RESOLUTION":

            resolutions.append(
                statement
            )

        # ----------------------------------------------
        # EVIDENCE GAP
        # ----------------------------------------------

        elif evidence_type == "EVIDENCE_GAP":

            evidence_gaps.append(
                statement
            )

    # ==================================================
    # GOVERNANCE STATUS
    # ==================================================

    if approval_documented:

        governance_status = (
            "APPROVAL_DOCUMENTED"
        )

    else:

        governance_status = (
            "APPROVAL_NOT_DOCUMENTED"
        )

        if not any(
            "approval" in gap.lower()
            for gap in evidence_gaps
        ):

            evidence_gaps.append(
                "No final deployment approval decision is documented."
            )

    # ==================================================
    # GOVERNANCE CONFLICT
    # ==================================================

    governance_conflict = (
        approval_documented
        and has_blocking_recommendation
    )

    if governance_conflict:

        governance_status = (
            "CONFLICTING_EVIDENCE"
        )

        reasons.append(
            "A deployment approval is documented "
            "while Security recommended blocking deployment."
        )

    # ==================================================
    # RISK STATUS
    # ==================================================

    if has_blocking_recommendation:

        risk_status = "BLOCKED"

    elif has_material_risk:

        risk_status = "RISK_IDENTIFIED"

    elif risks:

        risk_status = "RISK_IDENTIFIED"

    else:

        risk_status = "NO_RISK_IDENTIFIED"

    # ==================================================
    # OVERALL STATUS
    # ==================================================

    if governance_conflict:

        overall_status = (
            "CONFLICTING_EVIDENCE"
        )

    elif has_blocking_recommendation:

        overall_status = "BLOCKED"

    elif has_material_risk:

        overall_status = "RISK_IDENTIFIED"

    elif evidence_gaps:

        overall_status = "INSUFFICIENT_EVIDENCE"

    else:

        overall_status = "NO_BLOCKER_FOUND"

    # ==================================================
    # FINAL RESULT
    # ==================================================

    return {
        "status": overall_status,
        "risk_status": risk_status,
        "governance_status": governance_status,
        "document_status": document_status,
        "reasons": reasons,
        "risks": risks,
        "impacts": impacts,
        "resolutions": resolutions,
        "recommendations": recommendations,
        "approvals": approvals,
        "evidence_gaps": evidence_gaps
    }


if __name__ == "__main__":

    scenarios = {

        "SCENARIO A - BLOCKING RECOMMENDATION": [

            {
                "evidence_type": "RISK",
                "statement":
                    "The release contained a critical authentication vulnerability.",
                "severity": "critical",
                "recommendation": None
            },

            {
                "evidence_type": "RECOMMENDATION",
                "statement":
                    "Security recommended blocking deployment.",
                "severity": None,
                "recommendation":
                    "Block deployment."
            }
        ],

        "SCENARIO B - RISK WITHOUT BLOCKER": [

            {
                "evidence_type": "RISK",
                "statement":
                    "The release has a high performance risk.",
                "severity": "high",
                "recommendation": None
            }
        ],

        "SCENARIO C - INSUFFICIENT EVIDENCE": [

            {
                "evidence_type": "FACT",
                "statement":
                    "Release 600 was created.",
                "severity": None,
                "recommendation": None
            },

            {
                "evidence_type": "EVIDENCE_GAP",
                "statement":
                    "No release approval decision is documented.",
                "severity": None,
                "recommendation": None
            }
        ],

        "SCENARIO D - NO DOCUMENTED RISKS": [

            {
                "evidence_type": "FACT",
                "statement":
                    "No security risks were identified.",
                "severity": None,
                "recommendation": None
            },

            {
                "evidence_type": "FACT",
                "statement":
                    "No vulnerabilities were identified.",
                "severity": None,
                "recommendation": None
            }
        ],

        "SCENARIO E - EMPTY DOCUMENT": [],

        "SCENARIO F - GOVERNANCE CONFLICT": [

            {
                "evidence_type": "RISK",
                "statement":
                    "A critical authentication vulnerability was identified.",
                "severity": "critical",
                "recommendation": None
            },

            {
                "evidence_type": "RECOMMENDATION",
                "statement":
                    "Security recommended blocking deployment.",
                "severity": None,
                "recommendation":
                    "Block deployment."
            },

            {
                "evidence_type": "APPROVAL",
                "statement":
                    "The Release Manager approved deployment.",
                "severity": None,
                "recommendation": None
            }
        ]
    }

    print(
        "\n========== ASSESSMENT TESTS =========="
    )

    for scenario_name, evidence in scenarios.items():

        if scenario_name == "SCENARIO E - EMPTY DOCUMENT":

            result = assess_release_readiness(
                evidence,
                document_status="EMPTY"
            )

        else:

            result = assess_release_readiness(
                evidence
            )

        print(
            f"\n{scenario_name}"
        )

        print(
            "---------------------------------------"
        )

        print(
            json.dumps(
                result,
                indent=2
            )
        )

    print(
        "\n======================================="
    )