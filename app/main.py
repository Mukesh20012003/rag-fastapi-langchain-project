import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schemas import QueryRequest, QueryResponse, RAGResponse
from app.document_loader import load_documents, split_documents
from app.vector_store import create_vector_store
from app.rag_chain import get_rag_response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
FRONTEND_DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")
FRONTEND_ASSETS_DIR = os.path.join(FRONTEND_DIST_DIR, "assets")

app = FastAPI(title="RAG System with FastAPI and LangChain")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
def api_home():
    return {"message": "RAG FastAPI backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/test", response_model=QueryResponse)
def test_response():
    return QueryResponse(answer="FastAPI is working correctly")


@app.get("/load-docs")
def load_docs():
    documents = load_documents()
    chunks = split_documents(documents)

    return {
        "total_documents_loaded": len(documents),
        "total_chunks_created": len(chunks),
        "sample_chunk": chunks[0].page_content if chunks else "No chunks created"
    }


@app.post("/create-vector-store")
def build_vector_store():
    result = create_vector_store()

    if result is None:
        return {"message": "No documents found to create vector store"}

    return {
        "message": "Vector store created successfully",
        "details": result
    }


@app.post("/ask", response_model=RAGResponse)
def ask_question(request: QueryRequest):
    result = get_rag_response(request.question)
    return result


@app.post("/upload-doc")
def upload_document(file: UploadFile = File(...)):
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    allowed_extensions = [".txt", ".pdf"]
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .pdf files are allowed"
        )

    file_path = os.path.join(DOCUMENTS_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = create_vector_store()

    return {
        "message": f"File '{file.filename}' uploaded successfully",
        "vector_store_status": result
    }


if os.path.exists(FRONTEND_ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=FRONTEND_ASSETS_DIR), name="assets")


@app.get("/")
def serve_frontend():
    index_file = os.path.join(FRONTEND_DIST_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend build not found. Please run 'npm run build' inside frontend folder."}