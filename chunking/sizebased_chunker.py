def chunk_by_size(text: str, chunk_size: int = 512, overlap: int = 50) -> list[dict]:

    if not text or chunk_size <= 0:
        return []
    
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk_size")
    
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        chunks.append(text[start:start + chunk_size].strip())
        start += chunk_size - overlap


    return chunks