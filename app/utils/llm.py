from langchain_ollama import ChatOllama

def get_llm():
    return ChatOllama(
        model="llama3:8b",
        temperature=0,
        base_url="http://host.docker.internal:11434"
    )