import os
import json
import time
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, Base, engine
from app.models import CorpusDocument, Clause, PlantedContradiction, UnanswerableQuestion, QueryLog, BenchmarkRun
from app.schemas import (
    QueryRequest, QueryResponse, CorpusSummary, CorpusDocInfo, 
    ContradictionInfo, UnanswerableInfo, BenchmarkRequest, BenchmarkSummary
)
from app.engine.rag_service import RAGService

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="University Regulation QA & Contradiction Detection RAG System"
)

# Mount static folder
static_dir = os.path.join(settings.base_dir, "app", "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Rulebook RAG System API is running. UI index.html not yet placed in app/static."}

@app.get("/api/models")
def get_available_models():
    return {
        "default": settings.default_model,
        "available": settings.available_models
    }

@app.post("/api/query", response_model=QueryResponse)
async def query_regulations(req: QueryRequest, db: Session = Depends(get_db)):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty")
    service = RAGService(db)
    return await service.answer_query(req.query, model=req.model)

@app.get("/api/corpus", response_model=CorpusSummary)
def get_corpus_summary(db: Session = Depends(get_db)):
    docs = db.query(CorpusDocument).all()
    doc_infos = []
    total_words = 0
    total_clauses = 0

    for d in docs:
        c_count = db.query(Clause).filter(Clause.document_id == d.id).count()
        total_clauses += c_count
        total_words += d.word_count
        doc_infos.append(CorpusDocInfo(
            id=d.id,
            title=d.title,
            filename=d.filename,
            file_type=d.file_type,
            word_count=d.word_count,
            clause_count=c_count
        ))

    return CorpusSummary(
        total_documents=len(docs),
        total_words=total_words,
        total_clauses=total_clauses,
        documents=doc_infos
    )

@app.get("/api/corpus/document/{doc_id}")
def get_document_clauses(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(CorpusDocument).filter(CorpusDocument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    clauses = db.query(Clause).filter(Clause.document_id == doc_id).all()
    return {
        "document": {
            "id": doc.id,
            "title": doc.title,
            "filename": doc.filename,
            "word_count": doc.word_count
        },
        "clauses": [
            {
                "id": c.id,
                "section_id": c.section_id,
                "clause_id": c.clause_id,
                "title": c.title,
                "content": c.content,
                "word_count": c.word_count
            } for c in clauses
        ]
    }

@app.get("/api/contradictions", response_model=List[ContradictionInfo])
def get_planted_contradictions(db: Session = Depends(get_db)):
    contradictions = db.query(PlantedContradiction).all()
    testset_file = os.path.join(settings.testset_dir, "planted_contradictions.json")
    tq_map = {}
    if os.path.exists(testset_file):
        with open(testset_file, "r", encoding="utf-8") as f:
            for item in json.load(f):
                tq_map[item["id"]] = item.get("test_queries", [])

    results = []
    for c in contradictions:
        results.append(ContradictionInfo(
            cid=c.cid,
            title=c.title,
            topic=c.topic,
            description=c.description,
            point_of_tension=c.point_of_tension,
            administrative_ambiguity=c.administrative_ambiguity,
            clauses=json.loads(c.clauses_json),
            test_queries=tq_map.get(c.cid, [])
        ))
    return results

@app.get("/api/unanswerable-testset", response_model=List[UnanswerableInfo])
def get_unanswerable_testset(db: Session = Depends(get_db)):
    unans = db.query(UnanswerableQuestion).all()
    results = []
    for u in unans:
        adj = json.loads(u.adjacent_clauses_json) if u.adjacent_clauses_json else []
        results.append(UnanswerableInfo(
            uid=u.uid,
            category=u.category,
            question=u.question,
            why_unanswerable=u.why_unanswerable,
            adjacent_clauses=adj
        ))
    return results

@app.get("/api/history")
def get_query_history(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(QueryLog).order_by(QueryLog.created_at.desc()).limit(limit).all()
    return [
        {
            "id": l.id,
            "query": l.query_text,
            "model_used": l.model_used,
            "status": l.status,
            "answer": l.answer_text,
            "citations": json.loads(l.citations_json) if l.citations_json else [],
            "latency_ms": l.latency_ms,
            "created_at": l.created_at.isoformat()
        } for l in logs
    ]

@app.post("/api/benchmark/run", response_model=BenchmarkSummary)
async def run_benchmark_suite(req: BenchmarkRequest, db: Session = Depends(get_db)):
    service = RAGService(db)
    model = req.model or "heuristic-fast"

    # 1. Load test sets
    unans_file = os.path.join(settings.testset_dir, "unanswerable_25.json")
    with open(unans_file, "r", encoding="utf-8") as f:
        unanswerables = json.load(f)

    contra_file = os.path.join(settings.testset_dir, "planted_contradictions.json")
    with open(contra_file, "r", encoding="utf-8") as f:
        contradictions = json.load(f)

    ans_file = os.path.join(settings.testset_dir, "answerable_queries.json")
    with open(ans_file, "r", encoding="utf-8") as f:
        answerables = json.load(f)

    details = []
    
    # Run Unanswerable benchmark
    unans_correct = 0
    for u in unanswerables:
        res = await service.answer_query(u["question"], model=model)
        passed = (res.status == "UNANSWERABLE")
        if passed:
            unans_correct += 1
        details.append({
            "test_type": "UNANSWERABLE",
            "id": u["id"],
            "query": u["question"],
            "expected_status": "UNANSWERABLE",
            "actual_status": res.status,
            "passed": passed,
            "latency_ms": res.latency_ms
        })

    # Run Contradiction benchmark
    contra_correct = 0
    for c in contradictions:
        q = c["test_queries"][0]
        res = await service.answer_query(q, model=model)
        passed = (res.status == "CONTRADICTION" and res.contradiction and res.contradiction.contradiction_id == c["id"])
        if passed:
            contra_correct += 1
        details.append({
            "test_type": "CONTRADICTION",
            "id": c["id"],
            "query": q,
            "expected_status": "CONTRADICTION",
            "actual_status": res.status,
            "passed": passed,
            "latency_ms": res.latency_ms
        })

    # Run Answerable benchmark
    ans_correct = 0
    for a in answerables:
        res = await service.answer_query(a["question"], model=model)
        passed = (res.status == "ANSWERED" and len(res.citations) > 0)
        if passed:
            ans_correct += 1
        details.append({
            "test_type": "ANSWERABLE",
            "id": a["id"],
            "query": a["question"],
            "expected_status": "ANSWERED",
            "actual_status": res.status,
            "passed": passed,
            "latency_ms": res.latency_ms
        })

    total_tests = len(unanswerables) + len(contradictions) + len(answerables)
    total_passed = unans_correct + contra_correct + ans_correct
    overall_acc = round((total_passed / total_tests) * 100, 2)
    unans_acc = round((unans_correct / len(unanswerables)) * 100, 2)
    contra_acc = round((contra_correct / len(contradictions)) * 100, 2)
    ans_acc = round((ans_correct / len(answerables)) * 100, 2)

    # Save to BenchmarkRun table
    run_rec = BenchmarkRun(
        run_name=f"Evaluation Suite ({model})",
        model_used=model,
        total_tests=total_tests,
        unanswerable_total=len(unanswerables),
        unanswerable_correct=unans_correct,
        contradiction_total=len(contradictions),
        contradiction_detected=contra_correct,
        answerable_total=len(answerables),
        answerable_correct=ans_correct,
        accuracy_score=overall_acc,
        details_json=json.dumps(details)
    )
    db.add(run_rec)
    db.commit()

    return BenchmarkSummary(
        run_name=run_rec.run_name,
        model_used=model,
        total_tests=total_tests,
        unanswerable_tested=len(unanswerables),
        unanswerable_correct=unans_correct,
        unanswerable_accuracy=unans_acc,
        contradictions_tested=len(contradictions),
        contradictions_detected=contra_correct,
        contradiction_accuracy=contra_acc,
        answerable_tested=len(answerables),
        answerable_correct=ans_correct,
        answerable_accuracy=ans_acc,
        overall_accuracy=overall_acc,
        details=details
    )
