def split_text(text: str,chunk_size:int=500):
    """Split text into chunks while preserving sentence boundaries"""
    sentences=text.replace('\n',' ').split('. ')
    chunks=[]
    current_chunk=[]
    current_size=0

    for sentence in sentences:
        sentence=sentence.strip()
        if not sentence:
            continue

        if not sentence.endswith('.'):
            sentence+='.'

        sentence_size=len(sentence)


        if current_size+sentence_size>chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk=[sentence]
            current_size=sentence_size
        else:
            current_chunk.append(sentence)
            current_size+=sentence_size
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks



# Test it
text = """your multi paragraph text here."""

chunks = split_text(text, chunk_size=200)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {chunk}\n---")