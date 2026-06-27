def get_chunker(strategy="sentence"):
    if strategy == "sentence":
        from .sentence_chunker import split_text
        return split_text
    
    elif strategy=="recursive":
        from .recursive_chunker import recursive_chunk
        return recursive_chunk
    
    elif strategy == "page":
        from .page_chunker import page_chunk
        return page_chunk
    
    elif strategy == "semantic_page":
        from .semantic_page_chunker import semantic_page_chunk
        return semantic_page_chunk
    
    elif strategy == "embedding_semantic":
        from .embedding_semantic_chunker import embedding_semantic_chunk
        return embedding_semantic_chunk
    
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")
