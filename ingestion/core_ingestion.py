def get_ingestor(strategy="basic"):
    if strategy == "basic":
        from .basic_ingestion import read_document
        return read_document
    else:
        raise ValueError(f"Unknown ingestion strategy: {strategy}")
