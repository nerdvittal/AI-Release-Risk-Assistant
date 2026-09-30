from pathlib import Path


# ==================================================
# PROJECT PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIRECTORY = PROJECT_ROOT / "data"


# ==================================================
# INPUT DOCUMENT
# ==================================================

# Change ONLY this value when you want to analyse
# another release document.
#
# Example:
# release_527.txt
# release_528.txt
# release_529.txt

INPUT_DOCUMENT = "release_528.txt"


# ==================================================
# MODEL CONFIGURATION
# ==================================================

LLM_MODEL = "qwen2.5:1.5b"

EMBEDDING_MODEL = "nomic-embed-text"

OLLAMA_BASE_URL = "http://localhost:11434"


# ==================================================
# RETRIEVAL CONFIGURATION
# ==================================================

TOP_K = 3


# ==================================================
# DERIVED PATHS
# ==================================================

INPUT_FILE = DATA_DIRECTORY / INPUT_DOCUMENT


# Example:
# release_527.txt
#       ↓
# embedded_chunks_527.json
#
# release_528.txt
#       ↓
# embedded_chunks_528.json

release_stem = Path(INPUT_DOCUMENT).stem

RELEASE_ID = release_stem.replace(
    "release_",
    ""
)

EMBEDDING_FILE = (
    DATA_DIRECTORY
    / f"embedded_chunks_{RELEASE_ID}.json"
)


# ==================================================
# DOCUMENT METADATA
# ==================================================

SOURCE_NAME = (
    f"Release {RELEASE_ID} Production Report"
)