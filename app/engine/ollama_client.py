import httpx
import re
from typing import List, Dict, Any, Optional
from app.config import settings

class OllamaEngineClient:
    """
    Client for Ollama models (gemma3:1b, deepseek-r1:1.5b) with
    intelligent local deterministic fallback for instant benchmarking and offline execution.
    """
    def __init__(self, base_url: str = settings.ollama_base_url, default_model: str = settings.default_model):
        self.base_url = base_url
        self.default_model = default_model

    async def generate_response(
        self,
        query: str,
        retrieved_clauses: List[Dict[str, Any]],
        contradiction_detail: Optional[Dict[str, Any]] = None,
        unanswerable_detail: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        chosen_model = model or self.default_model

        # 1. If Unanswerable Detected by Refusal Gate:
        if unanswerable_detail and unanswerable_detail.get("is_unanswerable"):
            adj_clauses = unanswerable_detail.get("adjacent_clauses", [])
            adj_text = "\n".join([f"- {a}" for a in adj_clauses]) if adj_clauses else "None found."
            answer = (
                f"**STATUS: NOT COVERED IN RULEBOOK**\n\n"
                f"The university regulations do not contain provisions or governing rules regarding this specific inquiry.\n\n"
                f"**Reason for Silence:**\n{unanswerable_detail['why_unanswerable']}\n\n"
                f"**Adjacent Provisions Consulted:**\n{adj_text}\n\n"
                f"*Note: Rather than hallucinating or speculating, the system confirms that this policy is unaddressed in the official corpus.*"
            )
            citations = []
            for a in adj_clauses:
                doc_name = a.split("§")[0].strip() if "§" in a else "University Regulations"
                c_id = "§" + a.split("§")[1].strip() if "§" in a else a
                citations.append({
                    "document": doc_name,
                    "clause_ref": c_id,
                    "clause_title": "Adjacent Policy (Non-Answering)",
                    "snippet": "Contains adjacent provisions but does not authorize or resolve this specific inquiry."
                })
            return {
                "status": "UNANSWERABLE",
                "status_label": "NOT COVERED IN RULEBOOK",
                "answer": answer,
                "citations": citations,
                "model_used": chosen_model
            }

        # 2. If Contradiction Detected:
        if contradiction_detail and contradiction_detail.get("detected"):
            conf_clauses = contradiction_detail.get("conflicting_clauses", [])
            clauses_md = ""
            citations = []
            for idx, c in enumerate(conf_clauses, 1):
                clauses_md += f"**Clause {idx}: [{c['document']} - {c['clause_ref']}: {c['clause_title']}]**\n> \"{c['snippet']}\"\n\n"
                citations.append({
                    "document": c["document"],
                    "clause_ref": c["clause_ref"],
                    "clause_title": c["clause_title"],
                    "snippet": c["snippet"]
                })

            answer = (
                f"**STATUS: REGULATORY CONTRADICTION DETECTED**\n\n"
                f"**Topic:** {contradiction_detail['topic']}\n\n"
                f"The official university regulations contain direct, mutually conflicting provisions across different sections:\n\n"
                f"{clauses_md}"
                f"**Point of Tension:**\n{contradiction_detail['point_of_tension']}\n\n"
                f"**Administrative & Legal Dilemma for Students:**\n{contradiction_detail['administrative_ambiguity']}\n\n"
                f"*Conclusion: A definitive single answer cannot be provided because the rulebook simultaneously asserts contradictory standards.*"
            )
            return {
                "status": "CONTRADICTION",
                "status_label": "CONTRADICTION DETECTED",
                "answer": answer,
                "citations": citations,
                "model_used": chosen_model
            }

        # 3. If standard answerable query:
        # Check if fast heuristic requested or if we should call Ollama
        if chosen_model == "heuristic-fast" or not retrieved_clauses:
            return self._heuristic_answer(query, retrieved_clauses)

        # Attempt Ollama LLM call (gemma3:1b or deepseek-r1:1.5b)
        try:
            return await self._call_ollama(query, retrieved_clauses, chosen_model)
        except Exception as e:
            print(f"Ollama call failed ({type(e).__name__}: {e}), falling back to deterministic synthesis engine...")
            res = self._heuristic_answer(query, retrieved_clauses)
            res["model_used"] = f"{chosen_model} (fallback)"
            return res

    async def _call_ollama(self, query: str, retrieved_clauses: List[Dict[str, Any]], model: str) -> Dict[str, Any]:
        context_str = ""
        citations = []
        for c in retrieved_clauses:
            context_str += f"\n--- DOCUMENT: {c['document_title']} | CLAUSE: {c['clause_id']} ({c['title']}) ---\n{c['content']}\n"
            citations.append({
                "document": c["document_title"],
                "clause_ref": c["clause_id"],
                "clause_title": c["title"],
                "snippet": c["content"][:200] + "..." if len(c["content"]) > 200 else c["content"]
            })

        system_prompt = (
            "You are the official University Regulatory Advisor. Answer the student's question strictly using "
            "the provided excerpts from the regulations. You MUST explicitly cite the document name and clause identifier "
            "for every fact stated (e.g. [Academic Regulations, Clause 2.1]). If the excerpt does not answer the question, "
            "admit that the regulations do not specify."
        )

        user_prompt = f"REGULATORY EXCERPTS:\n{context_str}\n\nSTUDENT QUESTION: {query}\n\nProvide an authoritative, cited answer:"

        async with httpx.AsyncClient(timeout=90.0) as client:
            resp = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 300
                    }
                }
            )
            if resp.status_code == 200:
                data = resp.json()
                raw_response = data.get("response", "").strip()
                # Clean any DeepSeek think tags
                clean_response = re.sub(r"<think>.*?</think>", "", raw_response, flags=re.DOTALL).strip()
                return {
                    "status": "ANSWERED",
                    "status_label": "ANSWERED WITH CITATIONS",
                    "answer": clean_response,
                    "citations": citations[:2],
                    "model_used": model
                }
            else:
                raise RuntimeError(f"Ollama returned status {resp.status_code}: {resp.text}")

    def _heuristic_answer(self, query: str, retrieved_clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Deterministic, cited extractor for answerable queries.
        Extracts exact sentences from top retrieved clause matching the user's question.
        """
        if not retrieved_clauses:
            return {
                "status": "UNANSWERABLE",
                "status_label": "NOT COVERED IN RULEBOOK",
                "answer": "The consulted university regulations do not contain provisions answering this question.",
                "citations": [],
                "model_used": "heuristic-fast"
            }

        top_clause = retrieved_clauses[0]
        content = top_clause["content"]
        
        citations = [{
            "document": top_clause["document_title"],
            "clause_ref": top_clause["clause_id"],
            "clause_title": top_clause["title"],
            "snippet": content[:250] + "..." if len(content) > 250 else content
        }]

        answer = (
            f"According to **{top_clause['document_title']} [{top_clause['clause_id']}: {top_clause['title']}]**:\n\n"
            f"{content}\n\n"
            f"*Governing Citation: [{top_clause['document_title']}, {top_clause['clause_id']}]*"
        )

        return {
            "status": "ANSWERED",
            "status_label": "ANSWERED WITH CITATIONS",
            "answer": answer,
            "citations": citations,
            "model_used": "heuristic-fast"
        }
