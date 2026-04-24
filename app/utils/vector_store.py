import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.utils.embeddings import get_embeddings

VECTOR_PATH = "faiss_index"


def load_vector_store():
    embeddings = get_embeddings()

    if os.path.exists(VECTOR_PATH):
        return FAISS.load_local(
            VECTOR_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    # 🔥 FIX: initialize with dummy document
    dummy_doc = Document(page_content="init")
    db = FAISS.from_documents([dummy_doc], embeddings)
    db.save_local(VECTOR_PATH)
    return db


def save_to_vector_store(text, metadata=None):
    db = load_vector_store()

    doc = Document(page_content=text, metadata=metadata or {})
    db.add_documents([doc])

    db.save_local(VECTOR_PATH)


def search_similar(query, k=2):
    db = load_vector_store()

    results = db.similarity_search(query, k=k)

    # 🔥 Filter out dummy init doc
    filtered = [doc.page_content for doc in results if doc.page_content != "init"]

    return filtered