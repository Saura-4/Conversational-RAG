from unstructured.partition.pdf import partition_pdf

from unstructured.chunking.title import chunk_by_title

def semantic_page_chunk(
        pdf_path:str,
        max_characters:int =512,
        combine_text_under_n_chars: int=100
)->list[dict]:
    
    elements=partition_pdf(
        filename=pdf_path,
        strategy="fast"
    )

    semantic_chunks=chunk_by_title(
        elements,
        multipage_sections=False,
        max_characters=max_characters,
        combine_text_under_n_chars=combine_text_under_n_chars
    )

    chunks=[]
    page_chunk_counter={}

    for chunk in semantic_chunks:
        page=chunk.metadata.page_number

        if page is None:
            page=-1
        
        if page not in page_chunk_counter:
            page_chunk_counter[page]=0

        chunks.append({
            "text": str(chunk).strip(),
            "page":page,
            "chunk": page_chunk_counter[page],
        })

        page_chunk_counter[page]+=1

    return chunks