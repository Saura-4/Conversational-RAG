def recursive_chunk(text, chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", ".", " ", ""]):
    # Base case: text fits in one chunk
    if len(text) <= chunk_size:
        return [text]
    
    # Pick the first separator that exists in text
    separator = ""
    for sep in separators:
        if sep in text:
            separator = sep
            break
    
    # Split by chosen separator
    splits = text.split(separator) if separator else list(text)
    
    chunks = []
    current_chunk = ""
    
    for split in splits:
        piece = split + separator  # re-attach separator
        
        if len(current_chunk) + len(piece) <= chunk_size:
            current_chunk += piece
        else:
            # Current chunk is full
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # If single split is too large, recurse with next separators
            if len(piece) > chunk_size:
                remaining_seps = separators[separators.index(separator) + 1:]
                chunks.extend(recursive_chunk(piece, chunk_size, chunk_overlap, remaining_seps))
                current_chunk = ""
            else:
                # Start new chunk with overlap from previous
                current_chunk = current_chunk[-chunk_overlap:] + piece
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


# # Test it
# text = """your multi paragraph text here"""

# chunks = recursive_chunk(text, chunk_size=200, chunk_overlap=20)
# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i}: {chunk}\n---")