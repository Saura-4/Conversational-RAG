def get_ingestor(strategy="basic"):
    if strategy == "basic":
        from .basic_ingestion import read_document
        return read_document
    
    elif strategy == "pdf":
        from .pdf_ingestion import read_pdf_pages
        return read_pdf_pages

    else:
        raise ValueError(f"Unknown ingestion strategy: {strategy}")
