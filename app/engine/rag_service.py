import time
import json
from typing import Optional
from sqlalchemy.orm import Session
from app.engine.retriever import HybridRetriever
from app.engine.contradiction import ContradictionDetector
from app.engine.refusal_gate import RefusalGatekeeper
from app.engine.ollama_client import OllamaEngineClient
from app.schemas import QueryResponse, ContradictionDetail, Citation
from app.models import QueryLog

class RAGService:
    def __init__(self, db: Session):
        self.db = db
        self.retriever = HybridRetriever(db)
        self.contradiction_detector = ContradictionDetector(db)
        self.refusal_gate = RefusalGatekeeper(db)
        self.engine_client = OllamaEngineClient()

    async def answer_query(self, query: str, model: Optional[str] = None) -> QueryResponse:
        start_time = time.time()

        # Step 1: Hybrid Retrieval
        retrieved_clauses = self.retriever.retrieve(query, top_k=5)

        # Step 2: Contradiction Detection
        contradiction_detail = self.contradiction_detector.detect(query, retrieved_clauses)

        # Step 3: Refusal Gatekeeper (only if not a contradiction)
        unanswerable_detail = None
        if not contradiction_detail:
            unanswerable_detail = self.refusal_gate.evaluate(query, retrieved_clauses)

        # Step 4: Generation via Ollama or Fallback Engine
        gen_result = await self.engine_client.generate_response(
            query=query,
            retrieved_clauses=retrieved_clauses,
            contradiction_detail=contradiction_detail,
            unanswerable_detail=unanswerable_detail,
            model=model
        )

        latency_ms = round((time.time() - start_time) * 1000, 2)

        # Build ContradictionDetail schema if detected
        c_detail_obj = None
        if contradiction_detail and contradiction_detail.get("detected"):
            c_detail_obj = ContradictionDetail(
                detected=True,
                contradiction_id=contradiction_detail.get("contradiction_id"),
                title=contradiction_detail.get("title"),
                topic=contradiction_detail.get("topic"),
                point_of_tension=contradiction_detail.get("point_of_tension"),
                administrative_ambiguity=contradiction_detail.get("administrative_ambiguity"),
                conflicting_clauses=[Citation(**c) for c in contradiction_detail.get("conflicting_clauses", [])]
            )

        citations_list = [Citation(**c) for c in gen_result.get("citations", [])]

        # Log query to SQLAlchemy database
        try:
            log_entry = QueryLog(
                query_text=query,
                model_used=gen_result["model_used"],
                status=gen_result["status"],
                answer_text=gen_result["answer"],
                citations_json=json.dumps([c.model_dump() for c in citations_list]),
                contradiction_details_json=json.dumps(contradiction_detail) if contradiction_detail else "{}",
                latency_ms=latency_ms
            )
            self.db.add(log_entry)
            self.db.commit()
        except Exception as e:
            print(f"Failed to log query: {e}")
            self.db.rollback()

        return QueryResponse(
            query=query,
            status=gen_result["status"],
            status_label=gen_result["status_label"],
            answer=gen_result["answer"],
            citations=citations_list,
            contradiction=c_detail_obj,
            model_used=gen_result["model_used"],
            latency_ms=latency_ms
        )
