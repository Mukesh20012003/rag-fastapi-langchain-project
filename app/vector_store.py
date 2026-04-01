import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.document_loader import load_documents, split_documents

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vectorstore")
VECTOR_STORE_PATH = os.path.join(VECTOR_STORE_DIR, "faiss_index")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def create_vector_store():
    documents = load_documents()
    chunks = split_documents(documents)

    if not chunks:
        return None

    embeddings = get_embedding_model()
    vector_store = FAISS.from_documents(chunks, embeddings)

    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    vector_store.save_local(VECTOR_STORE_PATH)

    return {
        "documents_loaded": len(documents),
        "chunks_created": len(chunks),
        "vector_store_path": VECTOR_STORE_PATH
    }


def load_vector_store():
    embeddings = get_embedding_model()

    if not os.path.exists(VECTOR_STORE_PATH):
        return None

    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store