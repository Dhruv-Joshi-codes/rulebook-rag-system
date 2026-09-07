from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    query: str = Field(..., description="Student inquiry regarding university rules")
    model: Optional[str] = Field(None, description="Model to use (gemma3:1b, deepseek-r1:1.5b, heuristic-fast)")
    strict_citation: bool = Field(True, description="Enforce strict citation requirement")

class Citation(BaseModel):
    document: str
    clause_ref: str
    clause_title: str
    snippet: str

class ContradictionDetail(BaseModel):
    detected: bool
    contradiction_id: Optional[str] = None
    title: Optional[str] = None
    topic: Optional[str] = None
    point_of_tension: Optional[str] = None
    administrative_ambiguity: Optional[str] = None
    conflicting_clauses: List[Citation] = []

class QueryResponse(BaseModel):
    query: str
    status: str  # ANSWERED, UNANSWERABLE, CONTRADICTION
    status_label: str
    answer: str
    citations: List[Citation] = []
    contradiction: Optional[ContradictionDetail] = None
    model_used: str
    latency_ms: float

class CorpusDocInfo(BaseModel):
    id: int
    title: str
    filename: str
    file_type: str
    word_count: int
    clause_count: int

class CorpusSummary(BaseModel):
    total_documents: int
    total_words: int
    total_clauses: int
    documents: List[CorpusDocInfo]

class ContradictionInfo(BaseModel):
    cid: str
    title: str
    topic: str
    description: str
    point_of_tension: str
    administrative_ambiguity: str
    clauses: List[Dict[str, Any]]
    test_queries: List[str]

class UnanswerableInfo(BaseModel):
    uid: str
    category: str
    question: str
    why_unanswerable: str
    adjacent_clauses: List[str]

class BenchmarkRequest(BaseModel):
    model: Optional[str] = "heuristic-fast"

class BenchmarkSummary(BaseModel):
    run_name: str
    model_used: str
    total_tests: int
    unanswerable_tested: int
    unanswerable_correct: int
    unanswerable_accuracy: float
    contradictions_tested: int
    contradictions_detected: int
    contradiction_accuracy: float
    answerable_tested: int
    answerable_correct: int
    answerable_accuracy: float
    overall_accuracy: float
    details: List[Dict[str, Any]] = []
