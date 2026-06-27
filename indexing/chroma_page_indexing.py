import os
import chromadb
from chromadb.utils import embedding_functions

from ingestion.core_ingestion import get_ingestor
from chunking.core_chunk import get_chunker

read_document = get_ingestor("pdf")
split_text = get_chunker("page")

client=chromadb.PersistentClient(path="chroma_db")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection=client.get_or_create_collection(
    name="documents_collection",
    embedding_function=sentence_transformer_ef
)

def process_document(file_path:str):
    """Process a single document using dict chunks and prepare it for ChromaDB"""

    try:
        pages = read_document(file_path)
        chunks = split_text(pages)

        file_name=os.path.basename(file_path)
        
        texts = []
        metadatas = []
        ids = []
        
        for i, chunk_dict in enumerate(chunks):
            texts.append(chunk_dict["text"])
            
            # Merge source into metadata
            meta = chunk_dict.copy()
            del meta["text"]
            meta["source"] = file_name
            metadatas.append(meta)
            
            ids.append(f"{file_name}_chunk_{i}")

        return ids, texts, metadatas

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
        if file_path.lower().endswith('.pdf'):
            print(f"Processing {os.path.basename(file_path)}....")
            ids,texts,metadatas=process_document(file_path)
            add_to_collection(collection,ids,texts,metadatas)
            print(f"Added {len(texts)} chunks to collection")
        else:
            print(f"Skipping {os.path.basename(file_path)} (only PDF supported by page chunker)")
