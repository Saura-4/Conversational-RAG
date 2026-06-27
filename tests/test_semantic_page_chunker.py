from chunking.semantic_page_chunker import semantic_page_chunk

PDF_PATH = r"S:\project\RAG\RAG-from-scratch\Conversational_RAG\test_documents\23bcy10108_Continues_assessment_2.pdf"


def main():

    chunks = semantic_page_chunk(
        PDF_PATH,
        max_characters=512,
        combine_text_under_n_chars=100,
    )

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