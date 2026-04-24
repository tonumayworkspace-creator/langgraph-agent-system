from langchain_ollama import OllamaEmbeddings

def get_embeddings():
    return OllamaEmbeddings(
        model="llama3:8b",
        base_url="http://host.docker.internal:11434"
    )