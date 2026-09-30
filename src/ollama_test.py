import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen2.5:1.5b",
    "prompt": "Explain software testing in one simple sentence.",
    "stream": False
}

request = urllib.request.Request(
    OLLAMA_URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json"
    },
    method="POST"
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))

print("Model:", result["model"])
print("Response:", result["response"])
print("Completed:", result["done"])