import re
import math
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Clause, CorpusDocument

class HybridRetriever:
    """
    Hybrid Lexical & Semantic Keyword Clause Retriever.
    Uses BM25 token-matching with IDF weighting, field boosts for clause titles/IDs,
    and query term expansion.
    """
    def __init__(self, db: Session):
        self.db = db
        self._load_corpus()

    def _load_corpus(self):
        clauses = self.db.query(Clause).all()
        self.clause_records = []
        self.doc_lengths = []
        self.doc_freq = {}
        
        stop_words = {
            "a", "an", "the", "and", "or", "in", "of", "to", "for", "with", "on", "at", 
            "by", "from", "up", "about", "into", "over", "after", "is", "are", "was", 
            "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", 
            "but", "if", "or", "because", "as", "until", "while", "that", "this", "what",
            "can", "i", "my", "me", "we", "you", "your", "it", "its"
        }
        self.stop_words = stop_words

        for c in clauses:
            doc_meta = self.db.query(CorpusDocument).filter(CorpusDocument.id == c.document_id).first()
            doc_name = doc_meta.filename if doc_meta else "regulations.md"
            doc_title = doc_meta.title if doc_meta else "University Regulations"

            tokens = self._tokenize(f"{c.clause_id} {c.title} {c.section_id} {c.content}")
            unique_tokens = set(tokens)
            
            for t in unique_tokens:
                self.doc_freq[t] = self.doc_freq.get(t, 0) + 1

            self.clause_records.append({
                "id": c.id,
                "document_title": doc_title,
                "filename": doc_name,
                "section_id": c.section_id,
                "clause_id": c.clause_id,
                "title": c.title,
                "content": c.content,
                "tokens": tokens,
                "word_count": c.word_count
            })
            self.doc_lengths.append(len(tokens))

        self.N = len(self.clause_records)
        self.avg_dl = sum(self.doc_lengths) / max(1, self.N)

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r"[A-Za-z0-9%$§\.\-]+", text.lower())
        return [w for w in words if w not in self.stop_words and len(w) > 1]

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # Query Expansion for typical university regulation synonyms
        expansion_map = {
            "attendance": ["attendance", "75%", "65%", "50%", "debarment", "contact", "absence", "hospitalization"],
            "hospitalized": ["hospitalization", "medical", "65%", "health", "doctor"],
            "exam": ["examination", "exams", "hall", "sit", "sitting", "debarment"],
            "curfew": ["curfew", "22:00", "lockout", "lock-out", "gate", "24-hour", "hostel"],
            "lab": ["laboratory", "research", "capstone", "24-hour", "computing", "maker"],
            "refund": ["refund", "80%", "0%", "forfeiture", "withdrawal", "drop", "tuition"],
            "drop": ["drop", "withdrawal", "withdraw", "day", "refund", "forfeiture"],
            "wedding": ["wedding", "marriage", "family", "ceremony", "absence"],
            "fish": ["aquarium", "goldfish", "pet", "animal", "creature"],
            "fridge": ["refrigerator", "fridge", "appliance", "electrical", "kitchen"],
            "scooter": ["scooter", "moped", "vehicle", "parking", "bicycle"],
            "drone": ["drone", "uav", "filming", "airspace", "camera"],
            "snor": ["snore", "snoring", "roommate", "transfer", "sleep"]
        }
        
        expanded_tokens = list(query_tokens)
        for qt in query_tokens:
            for key, exp_list in expansion_map.items():
                if key in qt:
                    expanded_tokens.extend(exp_list)
        expanded_tokens = list(set(expanded_tokens))

        scores = []
        k1 = 1.5
        b = 0.75

        for idx, rec in enumerate(self.clause_records):
            doc_len = self.doc_lengths[idx]
            token_counts = {}
            for t in rec["tokens"]:
                token_counts[t] = token_counts.get(t, 0) + 1

            bm25_score = 0.0
            for qt in expanded_tokens:
                if qt in token_counts:
                    tf = token_counts[qt]
                    df = self.doc_freq.get(qt, 1)
                    idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
                    num = tf * (k1 + 1)
                    denom = tf + k1 * (1 - b + b * (doc_len / self.avg_dl))
                    bm25_score += idf * (num / denom)

            # Boost if query matches clause title or clause identifier
            title_lower = rec["title"].lower()
            id_lower = rec["clause_id"].lower()
            for qt in query_tokens:
                if qt in title_lower:
                    bm25_score += 2.0
                if qt in id_lower:
                    bm25_score += 3.0

            scores.append((bm25_score, rec))

        scores.sort(key=lambda x: x[0], reverse=True)
        top_results = []
        for score, rec in scores[:top_k]:
            if score > 0.1:
                item = dict(rec)
                item["retrieval_score"] = round(score, 3)
                top_results.append(item)

        return top_results
