import uuid
from datetime import datetime
import ollama

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
