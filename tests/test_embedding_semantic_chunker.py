from ingestion.pdf_ingestion import read_pdf_pages
from chunking.embedding_semantic_chunker import embedding_semantic_chunk

PDF_PATH = r"S:\project\RAG\RAG-from-scratch\Conversational_RAG\test_documents\23bcy10108_Continues_assessment_2.pdf"


def main():

    pages = read_pdf_pages(PDF_PATH)

    text = "\n".join(page["text"] for page in pages)

    chunks = embedding_semantic_chunk(text)

    print(f"Chunks: {len(chunks)}\n")

    for chunk in chunks:

        print("=" * 100)
        print(f"Chunk : {chunk['chunk']}")
        print("-" * 100)
        print(chunk["text"])
        print()


if __name__ == "__main__":
    main()