from ingestion.pdf_ingestion import read_pdf_pages
from chunking.page_chunker import page_chunk

PDF_PATH = r"S:\project\RAG\RAG-from-scratch\Conversational_RAG\test_documents\23bcy10108_Continues_assessment_2.pdf"


def main():

    pages = read_pdf_pages(PDF_PATH)

    chunks = page_chunk(
        pages,
        chunk_size=512,
        overlap=50
    )

    print(f"Pages : {len(pages)}")
    print(f"Chunks: {len(chunks)}\n")

    for chunk in chunks:
        print("=" * 100)
        print(f"Page  : {chunk['page']}")
        print(f"Chunk : {chunk['chunk']}")
        print("-" * 100)
        print(chunk["text"])
        print()


if __name__ == "__main__":
    main()