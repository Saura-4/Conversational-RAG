def get_indexer(strategy="chroma"):
    if strategy == "chroma":
        from .chroma_indexing import collection, process_and_add_documents
        return collection, process_and_add_documents
    elif strategy == "chroma_page":
        from .chroma_page_indexing import collection, process_and_add_documents
        return collection, process_and_add_documents
    elif strategy == "chroma_semantic_page":
        from .chroma_semantic_page_indexing import collection, process_and_add_documents
        return collection, process_and_add_documents
    elif strategy == "chroma_embedding":
        from .chroma_embedding_indexing import collection, process_and_add_documents
        return collection, process_and_add_documents
    else:
        raise ValueError(f"Unknown indexing strategy: {strategy}")
