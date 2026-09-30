import json
import urllib.request

from evidence_validator import validate_extraction


OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen2.5:1.5b"

MAX_EXTRACTION_ATTEMPTS = 2


def ask_qwen(
    context,
    missing_statements=None
):

    missing_statements = (
        missing_statements
        or []
    )

    missing_guidance = ""

    if missing_statements:

        missing_guidance = """

IMPORTANT:

A previous extraction attempt missed
the following source statements.

You MUST explicitly preserve them
in this extraction:

"""

        for statement in missing_statements:

            missing_guidance += (
                f"- {statement}\n"
            )

    prompt = f"""
You are an evidence extraction component
for a Quality Engineering system.

Extract EVERY atomic factual statement
from the supplied document chunk.

STRICT RULES:

1. Use ONLY information explicitly stated
   in the supplied text.

2. Do not invent information.

3. Do not infer information.

4. Do not make a deployment decision.

5. Do not recommend anything yourself.

6. Do not classify statements as risk,
   impact, resolution, or recommendation.

7. Each item must represent one
   independent factual statement.

8. Preserve the meaning of the supplied text.

9. Do not combine unrelated statements.

10. Do not omit factual statements.

11. Preserve statements involving:
    - vulnerabilities
    - security
    - recommendations
    - approvals
    - testing
    - deployment
    - incidents
    - customer impact
    - resolutions

12. Return valid JSON only.

{missing_guidance}

Return exactly:

{{
    "items": [
        {{
            "statement": "factual statement"
        }}
    ]
}}

SUPPLIED TEXT:

{context}

JSON:
"""

    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(
        request
    ) as response:

        result = json.loads(
            response.read().decode(
                "utf-8"
            )
        )

    return json.loads(
        result["response"]
    )


def extract_evidence(context):

    missing_statements = []

    for attempt in range(
        1,
        MAX_EXTRACTION_ATTEMPTS + 1
    ):

        print(
            f"\nEvidence extraction attempt "
            f"{attempt}/{MAX_EXTRACTION_ATTEMPTS}"
        )

        result = ask_qwen(
            context,
            missing_statements
        )

        evidence = result.get(
            "items",
            []
        )

        validation = validate_extraction(
            context,
            evidence
        )

        print(
            f"Validation status: "
            f"{validation['status']}"
        )

        if validation["status"] == "PASS":

            print(
                "Evidence extraction "
                "validated successfully."
            )

            return evidence

        missing_statements = (
            validation[
                "missing_statements"
            ]
        )

        print(
            "Missing statements detected:"
        )

        for statement in missing_statements:

            print(
                f"• {statement}"
            )

    print(
        "\nWARNING: Evidence extraction "
        "remains incomplete after retry."
    )

    return evidence


if __name__ == "__main__":

    from pathlib import Path

    project_root = (
        Path(__file__).resolve().parent.parent
    )

    file_path = (
        project_root
        / "data"
        / "release_530.txt"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        context = file.read()

    print(
        "\n========== FULL DOCUMENT =========="
    )

    print(context)

    print(
        "\n===================================="
    )

    evidence = extract_evidence(
        context
    )

    print(
        "\n========== FINAL EVIDENCE =========="
    )

    for index, item in enumerate(
        evidence,
        start=1
    ):

        print(
            f"E{index:03d}: "
            f"{item['statement']}"
        )

    print(
        "\nTotal extracted statements:",
        len(evidence)
    )

    print(
        "\n===================================="
    )