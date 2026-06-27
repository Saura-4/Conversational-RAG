from rag_pipeline import (
    collection,
    process_and_add_documents,
    conversation_rag_query,
    create_session,
    semantic_search,
    print_search_results
)

DOCUMENT_FOLDER="test_documents"

print("=" * 70)
print("Building Vector Database...")
print("=" * 70)

process_and_add_documents(collection,DOCUMENT_FOLDER)

print("\nIndexing Complete\n")

session=create_session()

test_queries = [
    # Artificial Intelligence
    "What is Artificial Intelligence?",
    "What is Machine Learning?",
    "What are Large Language Models?",

    # Climate Change
    "What causes climate change?",
    "How can climate change be reduced?",
    "What are greenhouse gases?",

    # Solar System
    "Which planet is the largest?",
    "Which planet is known as the Red Planet?",
    "How many planets are there in the Solar System?",

    # Cross-document
    "Compare Artificial Intelligence and climate change.",

    # Negative test
    "Who won the FIFA World Cup in 2022?"
]

for i,query in enumerate(test_queries,start=1):
    print("\n"+"="*70)
    print(f"Test {i}")
    print("="*70)

    print(f"\nQuestion:\n{query}\n")

    
    results = semantic_search(collection, query, 3)
    print_search_results(results)
    response,sources=conversation_rag_query(
        collection=collection,
        query=query,
        session_id=session,
        n_chunks=3
    )
    print("\nSources Retrieved:")
    for source in sources:
        print(f"  • {source}")

    print("\nResponse:")
    try:
        print(response)
    except UnicodeEncodeError:
        print(response.encode("ascii", "replace").decode("ascii"))