import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen2.5:1.5b"


def check_relevance(question, chunk):

    prompt = f"""
You are a relevance checker for a Quality Engineering AI system.

Your job is to decide whether the supplied document chunk contains
information that can directly help answer the user's question.

Rules:
1. Use only the supplied chunk.
2. Return YES if the chunk contains information that is directly relevant to the question.
3. Return YES if the chunk contains important evidence, risks, warnings, constraints, recommendations, or facts that could materially affect the answer.
4. Return NO only if the chunk has no meaningful connection to the question.
5. Do not require the chunk to directly answer the question.
6. For release, deployment, safety, or decision-related questions, preserve evidence that could affect the decision.
7. Do not answer the user's question.
8. Return only YES or NO.

User question:
{question}

Document chunk:
{chunk}

Relevance:
"""

    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    answer = result["response"].strip().upper()

    if "YES" in answer:
        return "YES"

    return "NO"


if __name__ == "__main__":

    question = input("Enter your question: ").strip()

    chunk = input(
        "\nEnter the document chunk to evaluate:\n"
    ).strip()

    result = check_relevance(
        question,
        chunk
    )

    print("\n========== RELEVANCE DECISION ==========")
    print("Question:", question)
    print("Decision:", result)
    print("========================================")