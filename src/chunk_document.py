from pathlib import Path

from config import INPUT_FILE


def create_chunks(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # ==================================================
    # DOCUMENT VALIDATION
    # ==================================================

    if not content.strip():
        raise ValueError(
            f"The input document is empty: {file_path.name}"
        )

    segments = [
        segment.strip()
        for segment in content.split("\n\n")
        if segment.strip()
    ]

    if not segments:
        raise ValueError(
            f"No usable content was found in: "
            f"{file_path.name}"
        )

    # ==================================================
    # RELEASE IDENTIFICATION
    # ==================================================

    release_id = file_path.stem.replace(
        "release_",
        ""
    )

    # ==================================================
    # CHUNK CREATION
    # ==================================================

    chunks = []

    chunk_ranges = [
        (0, 3, "deployment"),
        (3, 7, "production_incident"),
        (7, 9, "security")
    ]

    for index, (start, end, topic) in enumerate(
        chunk_ranges,
        start=1
    ):

        chunk_segments = segments[start:end]

        if not chunk_segments:
            continue

        chunks.append(
            {
                "chunk_id": f"chunk_{index}",
                "content": "\n\n".join(
                    chunk_segments
                ),
                "release_id": release_id,
                "document_type": "production_report",
                "topic": topic
            }
        )

    # ==================================================
    # FINAL VALIDATION
    # ==================================================

    if not chunks:
        raise ValueError(
            f"No valid chunks could be created from: "
            f"{file_path.name}"
        )

    return chunks


if __name__ == "__main__":

    print(
        "\n========== CHUNKING TEST =========="
    )

    print(
        f"Input document: {INPUT_FILE}"
    )

    chunks = create_chunks(
        INPUT_FILE
    )

    print(
        f"Total chunks: {len(chunks)}"
    )

    for chunk in chunks:

        print(
            "\n----------------------------------------"
        )

        print(
            f"Chunk ID: {chunk['chunk_id']}"
        )

        print(
            f"Release ID: {chunk['release_id']}"
        )

        print(
            f"Topic: {chunk['topic']}"
        )

        print(
            "Content:"
        )

        print(
            chunk["content"]
        )

    print(
        "\n========================================"
    )