from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str


class RAGResponse(BaseModel):
    answer: str
    context_used: Optional[List[str]] = None