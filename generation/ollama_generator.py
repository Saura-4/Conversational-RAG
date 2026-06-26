import ollama

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
