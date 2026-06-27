from ingestion.pdf_ingestion import read_pdf_pages


def page_chunk(
    pages: list[dict],
    chunk_size: int = 512,
    overlap: int = 50
) -> list[dict]:
    """
    Chunk each page independently while preserving page metadata.

    Args:
        pages: [
            {
                "page": 1,
                "text": "..."
            },
            ...
        ]

    Returns:
        [
            {
                "text": "...",
                "page": 1,
                "chunk": 0
            },
            ...
        ]
    """

    if chunk_size <= 0:
        return []

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk_size")

    chunks = []

    for page in pages:

        text = page["text"]

        if not text:
            continue

        start = 0
        chunk_index = 0

        while start < len(text):

            chunk = text[start:start + chunk_size].strip()

            if chunk:
                chunks.append({
                    "text": chunk,
                    "page": page["page"],
                    "chunk": chunk_index
                })

            start += chunk_size - overlap
            chunk_index += 1

    return chunks
