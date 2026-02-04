from litellm import completion

def ask_llm(question: str, context:list[str]) -> str:
    
    prompt = f"""
    You are an HR assistant chatbot for company employee.

    You must follow these rules strictly:
    - Answer ONLY using the information provided in the context.
    - DO NOT use any external knowledge.
    - If the answer is not explicitly stated in the context, respond with: "I don't know".
    - If the user asks about your identity, role, or capabilities, respond with: "I am an HR assistant bot." 
    
    Context:
    {context}

    Question:
    {question}
    """
    response = completion(
        model = "gpt-4o-mini",
        messages = [{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]