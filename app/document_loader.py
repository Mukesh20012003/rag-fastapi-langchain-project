import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCUMENTS_PATH = os.path.join(BASE_DIR, "documents")


def load_documents():
    documents = []

    if not os.path.exists(DOCUMENTS_PATH):
        print(f"Folder '{DOCUMENTS_PATH}' not found.")
        return documents

    for file_name in os.listdir(DOCUMENTS_PATH):
        file_path = os.path.join(DOCUMENTS_PATH, file_name)

        try:
            if file_name.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())

            elif file_name.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
                documents.extend(loader.load())

        except Exception as e:
            print(f"Error loading {file_name}: {e}")

    return documents


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return text_splitter.split_documents(documents)