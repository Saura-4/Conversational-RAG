from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings

def embedding_semantic_chunk(
        data,
        model:str="nomic-embed-text",
        breakpoint_threshold_type:str="percentile",
        breakpoint_threshold_amount:int=95,
)->list[dict]:
    
    embeddings=OllamaEmbeddings(
        model=model
    )

    semantic_splitter=SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type=breakpoint_threshold_type,
        breakpoint_threshold_amount=breakpoint_threshold_amount,
    )

    if isinstance(data, str):
        pages = [{"text": data}]
    else:
        pages = data

    chunks=[]
    global_chunk_idx = 0
    
    for page in pages:
        text = page.get("text", "")
        if not text.strip():
            continue
            
        semantic_chunks=semantic_splitter.split_text(text)
        
        for chunk in semantic_chunks:
            meta = page.copy()
            meta["text"] = chunk
            meta["chunk"] = global_chunk_idx
            chunks.append(meta)
            global_chunk_idx += 1
            
    return chunks