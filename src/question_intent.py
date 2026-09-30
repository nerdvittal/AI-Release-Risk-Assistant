import re


def detect_question_intent(question):

    text = question.lower().strip()

    # ==================================================
    # ROOT CAUSE
    # ==================================================

    root_cause_patterns = [
        r"\bwhat caused\b",
        r"\broot cause\b",
        r"\bwhy did\b",
        r"\bwhy was\b",
        r"\bwhy were\b",
        r"\bcause of\b"
    ]

    for pattern in root_cause_patterns:

        if re.search(pattern, text):

            return "ROOT_CAUSE"

    # ==================================================
    # SECURITY RISK
    # ==================================================

    security_patterns = [
        r"\bsecurity risk",
        r"\bsecurity risks",
        r"\bvulnerabil",
        r"\bsecurity issue",
        r"\bsecurity concern"
    ]

    for pattern in security_patterns:

        if re.search(pattern, text):

            return "SECURITY_RISK"

    # ==================================================
    # RELEASE READINESS
    # ==================================================

    readiness_patterns = [

        r"\brelease .*ready",
        r"\brelease readiness",
        r"\bready for production",
        r"\bready to deploy",

        r"\bis .*release .*safe",
        r"\bis .*safe .*deploy",
        r"\bis .*safe .*production",
        r"\bsafe to deploy",
        r"\bsafe to release",

        r"\bhow safe is .*release",
        r"\bhow safe is .*deployment",
        r"\bhow safe is .*production deployment",
        r"\bhow safe is .*production release",

        r"\bhow ready is .*release",
        r"\bhow ready is .*deployment",
        r"\bhow ready is .*production deployment",
        r"\bhow ready is .*production release",

        r"\bcan .*release .*proceed",
        r"\bshould .*release .*proceed",

        r"\bcan .*deploy",
        r"\bcan .*deployment .*proceed",
        r"\bshould .*deploy",
        r"\bshould .*deployment .*proceed",
        r"\bgo to production",

        r"\bcan we deploy\b",
        r"\bshould we deploy\b",
        r"\bcan we release\b",
        r"\bshould we release\b"
    ]

    for pattern in readiness_patterns:

        if re.search(pattern, text):

            return "RELEASE_READINESS"

    # ==================================================
    # DIRECT READINESS QUESTIONS
    # ==================================================

    direct_readiness_patterns = [

        r"^can the release proceed\b",
        r"^should the release proceed\b",

        r"^is the release ready\b",
        r"^is the release safe\b",
        r"^is the release safe for production\b",

        r"^is it safe to deploy\b",
        r"^is it safe to deploy the release\b",
        r"^is it safe to deploy this release\b",

        r"^can we deploy the release\b",
        r"^can we deploy this release\b",

        r"^should we deploy the release\b",
        r"^should we deploy this release\b",

        r"^can this release go to production\b",

        r"^is this release ready for deployment\b",

        r"^can the deployment proceed\b",

        r"^how safe is the release\b",
        r"^how safe is this release\b",
        r"^how safe is the deployment\b",
        r"^how safe is the production deployment\b",
        r"^how safe is the production release\b",

        r"^how ready is the release\b",
        r"^how ready is this release\b",
        r"^how ready is the deployment\b",
        r"^how ready is the production deployment\b",
        r"^how ready is the production release\b"
    ]

    for pattern in direct_readiness_patterns:

        if re.search(pattern, text):

            return "RELEASE_READINESS"

    # ==================================================
    # PRODUCTION IMPACT
    # ==================================================

    impact_patterns = [
        r"\bwhat impact",
        r"\bcustomer impact",
        r"\bproduction impact",
        r"\bhow many customers",
        r"\bhow many users",
        r"\bimpact of"
    ]

    for pattern in impact_patterns:

        if re.search(pattern, text):

            return "PRODUCTION_IMPACT"

    # ==================================================
    # RESOLUTION
    # ==================================================

    resolution_patterns = [
        r"\bhow was .* resolved",
        r"\bhow was .* fixed",
        r"\bhow did .* get resolved",
        r"\bwhat fixed",
        r"\bwhat resolved",
        r"\bresolution"
    ]

    for pattern in resolution_patterns:

        if re.search(pattern, text):

            return "RESOLUTION"

    # ==================================================
    # RECOMMENDATION
    # ==================================================

    recommendation_patterns = [
        r"\bwhat did .* recommend",
        r"\bwhat was .* recommendation",
        r"\brecommendation",
        r"\bwhat should we do"
    ]

    for pattern in recommendation_patterns:

        if re.search(pattern, text):

            return "RECOMMENDATION"

    # ==================================================
    # APPROVAL
    # ==================================================

    approval_patterns = [
        r"\bwho approved\b",
        r"\bwho has approved\b",
        r"\bwho gave approval\b",
        r"\bwho authorized\b",
        r"\bwho authorized the deployment\b",
        r"\bwho approved the deployment\b",
        r"\bwho approved the release\b",
        r"\bwho gave the approval\b",
        r"\bwho signed off\b",
        r"\bwho signed off on the deployment\b",
        r"\bwho signed off on the release\b",
        r"\bdeployment approval\b",
        r"\brelease approval\b"
    ]

    for pattern in approval_patterns:

        if re.search(pattern, text):

            return "APPROVAL"

    return "UNKNOWN"


if __name__ == "__main__":

    test_questions = [

        "What caused the payment failures?",
        "What security risks are present?",

        "Can the release proceed?",
        "Should the release proceed?",
        "Is the release ready?",
        "Is the release safe?",
        "Is the release safe for production?",
        "Is it safe to deploy?",
        "Is it safe to deploy the release?",
        "Is it safe to deploy this release?",
        "Can we deploy the release?",
        "Can we deploy this release?",
        "Should we deploy the release?",
        "Can this release go to production?",
        "Is this release ready for deployment?",
        "Can the deployment proceed?",
        "How safe is the release?",
        "How safe is this release?",
        "How safe is the deployment?",
        "How safe is the production deployment?",
        "How safe is the production release?",

        "What was the customer impact?",
        "How was the issue resolved?",
        "What did Security recommend?",

        "Who approved the deployment?",
        "Who approved the release?",
        "Who authorized the deployment?",
        "Who signed off on the release?",

        "Tell me about the release."
    ]

    print(
        "\n========== QUESTION INTENT TEST =========="
    )

    for question in test_questions:

        intent = detect_question_intent(
            question
        )

        print(
            f"{question}"
        )

        print(
            f"→ {intent}"
        )

        print(
            "------------------------------------------"
        )

    print(
        "=========================================="
    )