import docx
import PyPDF2
import os
import chromadb
from chromadb.utils import embedding_functions
import uuid
from datetime import datetime
import json
import ollama

def read_text_file(file_path:str):
    """ Read content form a text file"""
    with open(file_path,'r',encoding='utf-8') as file:
        return file.read()
    
def read_pdf_file(file_path:str):
    """Read content from a PDF File"""
    text=""
    with open(file_path, 'rb')as file:
        pdf_reader=PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text+=page.extract_text()+"\n"
        return text
    
def read_docx_file(file_path:str):
    """Read content from a Word document"""
    doc=docx.Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def read_document(file_path: str):
    """ Read document content based on file extension"""
    _,file_extension=os.path.splitext(file_path)
    file_extension=file_extension.lower()

    if file_extension=='.txt':
        return read_text_file(file_path)
    elif file_extension=='.pdf':
        return read_pdf_file(file_path)
    elif file_extension=='.docx':
        return read_docx_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
    

def split_text(text: str,chunk_size:int=500):
    """Split text into chunks while preserving sentence boundaries"""
    sentences=text.replace('\n',' ').split('. ')
    chunks=[]
    current_chunk=[]
    current_size=0

    for sentence in sentences:
        sentence=sentence.strip()
        if not sentence:
            continue

        if not sentence.endswith('.'):
            sentence+='.'

        sentence_size=len(sentence)


        if current_size+sentence_size>chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk=[sentence]
            current_size=sentence_size
        else:
            current_chunk.append(sentence)
            current_size+=sentence_size
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


client=chromadb.PersistentClient(path="chroma_db")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection=client.get_or_create_collection(
    name="documents_collection",
    embedding_function=sentence_transformer_ef
)

def process_document(file_path:str):
    """Process a single document and prepare it for ChromaDB"""

    try:
        content=read_document(file_path)
        chunks=split_text(content)

        file_name=os.path.basename(file_path)
        metadatas=[{"source": file_name,"chunk":i} for i in range(len(chunks))]
        ids=[f"{file_name}_chunk_{i}" for i in range(len(chunks))]

        return ids,chunks,metadatas

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return [],[],[]
    
def add_to_collection(collection,ids,texts,metadatas):
    """Add documents to collection in batches"""
    if not texts:
        return
    batch_size=100
    for i in range(0,len(texts),batch_size):
        end_idx=min(i+batch_size,len(texts))
        collection.add(
            documents=texts[i:end_idx],
            metadatas=metadatas[i:end_idx],
            ids=ids[i:end_idx]
        )  

def process_and_add_documents(collection,folder_path:str):
    """Process all documents in a folder and add to collection"""
    files=[os.path.join(folder_path,file)
            for file in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path,file))]

    for file_path in files:
        print(f"Processing {os.path.basename(file_path)}....")
        ids,texts,metadatas=process_document(file_path)
        add_to_collection(collection,ids,texts,metadatas)
        print(f"Added {len(texts)} chunks to collection")

def semantic_search(collection,query:str,n_results:int=2):
    """perform semantic search on the collection """
    results=collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results


def get_context_with_sources(results):
    """extract context and source information form the result"""

    context="\n\n".join(results['documents'][0])

    sources=[
        f"{meta['source']} (chunk {meta['chunk']})" for meta in results['metadatas'][0]
    ]

    return context,sources

def print_search_results(results):
    """print formatted search results"""
    print("\nSearch Results:\n"+"-"*50)

    for i in range(len(results['documents'][0])):
        doc=results['documents'][0][i]
        meta=results['metadatas'][0][i]
        distance=results['distances'][0][i]

        print(f"\nResult {i+1}")
        print(f"Source: {meta['source']},chunk{meta['chunk']}")
        print(f"Distance: {distance}")
        print(f"Content {doc}\n")

def rag_query(collection,query:str,n_chunks:int=2):
    """PErform RAG Query: retrieve relevant chunks and generate answer"""

    results=semantic_search(collection,query,n_chunks)
    context,source=get_context_with_sources(results)

    response=generate_response(query,context)

    return response,source

conversations={}

def create_session():
    """Create a new conversation session"""
    session_id=str(uuid.uuid4())
    conversations[session_id]=[]
    return session_id

def add_message(session_id:str,role:str,content:str):

    """Add a message to the conversation history"""

    if session_id not in conversations:
        conversations[session_id]=[]

    conversations[session_id].append({
        "role":role,
        "content":content,
        "timestamp":datetime.now().isoformat()
    })

def get_conversation_history(session_id:str, max_messages:int=None):
    """Get conversation history for a session"""

    if session_id not in conversations:
        return []
    
    history=conversations[session_id]

    if max_messages:
        history=history[-max_messages:]

    return history

def format_history_for_prompt(session_id:str,max_messages:int=5):
    """Format conversation history for inclusion in prompts"""

    history=get_conversation_history(session_id,max_messages)
    formated_history=""

    for msg in history:
        role="Human" if msg["role"]=="user" else "Assistant"
        formated_history+=f"{role}: {msg['content']}\n\n"

    return formated_history.strip()

def contextualize_query(query:str, conversation_history:str):
    """Convert follow-up questions into standalone queries"""
    contextualize_prompt = """
    You are a query rewriting assistant.

    Given the conversation history and the user's latest question, rewrite the latest question into a clear, standalone question if it depends on previous conversation.

    Rules:
    - Do NOT answer the question.
    - Do NOT explain anything.
    - Do NOT add new information.
    - Preserve the user's original intent.
    - If the question is already complete and understandable, return it exactly as it is.
    - Output ONLY the rewritten question.
    """
    try: 
        completion = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "system", "content": contextualize_prompt},
                {"role": "user", "content": f"Chat history:\n{conversation_history}\n\nQuestion:\n{query}"}
            ]
        )
        return completion['message']['content']
    
    except Exception as e:
        print(f"Error contextualizing query: {str(e)}")
        return query
    

def get_prompt(context, conversation_history, query):
    prompt = f"""
    You are a helpful assistant that answers questions using the provided document context.

    Rules:
    - Answer using ONLY the information in the document context.
    - If the context does not contain enough information, say:
    "I cannot answer this based on the provided information."
    - Do NOT use outside knowledge.
    - Keep the answer clear and concise.
    - Use the conversation history only to understand references like "it", "they", or "that". Do not use it as a source of factual information if the documents do not support the answer.

    Document Context:
    {context}

    Conversation History:
    {conversation_history}

    User Question:
    {query}

    Answer:
    """
    return prompt

def generate_response(query:str,context:str,conversation_history:str=""):
    prompt=get_prompt(context,conversation_history,query)

    try:
        response=ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature":0,
                "num_predict":500
            }
                
        )
        return response['message']['content']

    except Exception as e:
        return f"Error generating response: {str(e)}"

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

    context,source=get_context_with_sources(semantic_search(collection,query,n_chunks)
    )
    print("Context:",context)
    print("Source:",source)

    response=generate_response(query,context,conversation_history)

    add_message(session_id,"user",query)
    add_message(session_id,"assistant", response)

    return response,source