import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CorpusDocument(Base):
    __tablename__ = "corpus_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False, unique=True)
    file_type = Column(String(50), nullable=False)  # markdown, csv, pdf
    file_path = Column(String(512), nullable=False)
    word_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    clauses = relationship("Clause", back_populates="document", cascade="all, delete-orphan")

class Clause(Base):
    __tablename__ = "clauses"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("corpus_documents.id"), nullable=False)
    section_id = Column(String(100), index=True)
    clause_id = Column(String(100), index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)
    metadata_json = Column(Text, default="{}")

    document = relationship("CorpusDocument", back_populates="clauses")

class PlantedContradiction(Base):
    __tablename__ = "planted_contradictions"

    id = Column(Integer, primary_key=True, index=True)
    cid = Column(String(50), unique=True, index=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    point_of_tension = Column(Text, nullable=False)
    administrative_ambiguity = Column(Text, nullable=False)
    clauses_json = Column(Text, nullable=False)

class UnanswerableQuestion(Base):
    __tablename__ = "unanswerable_questions"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(50), unique=True, index=True)
    category = Column(String(100), nullable=False)
    question = Column(Text, nullable=False)
    why_unanswerable = Column(Text, nullable=False)
    adjacent_clauses_json = Column(Text, default="[]")

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(Text, nullable=False)
    model_used = Column(String(100), default="gemma3:1b")
    status = Column(String(50), nullable=False)  # ANSWERED, UNANSWERABLE, CONTRADICTION
    answer_text = Column(Text, nullable=False)
    citations_json = Column(Text, default="[]")
    contradiction_details_json = Column(Text, default="{}")
    latency_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class BenchmarkRun(Base):
    __tablename__ = "benchmark_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_name = Column(String(255), nullable=False)
    model_used = Column(String(100), nullable=False)
    total_tests = Column(Integer, default=0)
    unanswerable_total = Column(Integer, default=0)
    unanswerable_correct = Column(Integer, default=0)
    contradiction_total = Column(Integer, default=0)
    contradiction_detected = Column(Integer, default=0)
    answerable_total = Column(Integer, default=0)
    answerable_correct = Column(Integer, default=0)
    precision_score = Column(Float, default=0.0)
    recall_score = Column(Float, default=0.0)
    accuracy_score = Column(Float, default=0.0)
    details_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
