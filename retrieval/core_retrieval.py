def get_retriever(strategy="semantic"):
    if strategy == "semantic":
        from .semantic_search import semantic_search, get_context_with_sources, print_search_results
        return semantic_search, get_context_with_sources, print_search_results
    else:
        raise ValueError(f"Unknown retrieval strategy: {strategy}")
