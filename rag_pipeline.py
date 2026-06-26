from indexing.core_indexing import get_indexer
from retrieval.core_retrieval import get_retriever
from generation.core_generation import get_generator
from contextualization.core_contextualization import get_contextualizer

# Load strategies via factories
collection, process_and_add_documents = get_indexer("chroma")
semantic_search, get_context_with_sources, print_search_results = get_retriever("semantic")
generate_response = get_generator("ollama")
create_session, add_message, format_history_for_prompt, contextualize_query = get_contextualizer("memory")


def rag_query(collection,query:str,n_chunks:int=2):
    """PErform RAG Query: retrieve relevant chunks and generate answer"""

    results=semantic_search(collection,query,n_chunks)
    context,source=get_context_with_sources(results)

    response=generate_response(query,context)

    return response,source

def conversation_rag_query(
    collection,
    query:str,
    session_id:str,
    n_chunks:int=3
):
    """perform RAG query with conversation history """

    conversation_history=format_history_for_prompt(session_id)

    query=contextualize_query(query,conversation_history)
    print("Contextualized Query:",query)

    context,source=get_context_with_sources(semantic_search(collection,query,n_chunks))
    print("Context:",context)
    print("Source:",source)

    response=generate_response(query,context,conversation_history)

    add_message(session_id,"user",query)
    add_message(session_id,"assistant", response)

    return response,source