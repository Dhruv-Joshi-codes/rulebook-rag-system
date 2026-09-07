import os
import json
from app.database import engine, SessionLocal, Base
from app.models import CorpusDocument, Clause, PlantedContradiction, UnanswerableQuestion
from app.parsers.markdown_parser import parse_markdown_clauses
from app.parsers.csv_parser import parse_csv_clauses
from app.parsers.pdf_parser import parse_pdf_clauses
from app.config import settings

def seed():
    print("Creating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 1. Ingest Documents and Clauses
        docs_config = [
            ("Academic Regulations and Degree Governance Charter", "academic_regulations.md", "markdown"),
            ("Residential Life Code & Hostel Regulations Handbook", "hostel_and_housing_policy.md", "markdown"),
            ("Institutional Scholarships, Bursaries, and Financial Aid Guidelines", "scholarship_and_aid_policy.md", "markdown"),
            ("Fee Deadlines and Refunds Schedule", "fee_deadlines_and_refunds.csv", "csv"),
            ("Standing Charter of the Proctorial Board and Senate Committees", "disciplinary_charter.pdf", "pdf")
        ]
        
        total_clauses_count = 0
        total_words_count = 0
        
        for title, filename, file_type in docs_config:
            file_path = os.path.join(settings.corpus_dir, filename)
            if not os.path.exists(file_path):
                print(f"Warning: File {file_path} not found!")
                continue
                
            # Parse clauses based on type
            if file_type == "markdown":
                clauses_data = parse_markdown_clauses(file_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    doc_word_count = len(f.read().split())
            elif file_type == "csv":
                clauses_data = parse_csv_clauses(file_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    doc_word_count = len(f.read().split())
            elif file_type == "pdf":
                clauses_data = parse_pdf_clauses(file_path, filename)
                import pypdf
                reader = pypdf.PdfReader(file_path)
                doc_word_count = sum(len(p.extract_text().split()) for p in reader.pages if p.extract_text())
            else:
                clauses_data = []
                doc_word_count = 0
                
            doc = CorpusDocument(
                title=title,
                filename=filename,
                file_type=file_type,
                file_path=file_path,
                word_count=doc_word_count
            )
            db.add(doc)
            db.flush()
            
            for c in clauses_data:
                clause_obj = Clause(
                    document_id=doc.id,
                    section_id=c.get("section_id", ""),
                    clause_id=c.get("clause_id", ""),
                    title=c.get("title", ""),
                    content=c.get("content", ""),
                    word_count=c.get("word_count", 0),
                    metadata_json=json.dumps({"document_title": doc.title, "filename": filename})
                )
                db.add(clause_obj)
                total_clauses_count += 1
                
            total_words_count += doc_word_count
            print(f"Ingested {filename}: {len(clauses_data)} clauses, {doc_word_count} words")
            
        # 2. Seed Planted Contradictions
        contradictions_file = os.path.join(settings.testset_dir, "planted_contradictions.json")
        if os.path.exists(contradictions_file):
            with open(contradictions_file, "r", encoding="utf-8") as f:
                contradictions_data = json.load(f)
                for item in contradictions_data:
                    c_obj = PlantedContradiction(
                        cid=item["id"],
                        title=item["title"],
                        topic=item["topic"],
                        description=item["description"],
                        point_of_tension=item["point_of_tension"],
                        administrative_ambiguity=item["administrative_ambiguity"],
                        clauses_json=json.dumps(item["conflicting_clauses"])
                    )
                    db.add(c_obj)
            print(f"Seeded {len(contradictions_data)} planted ground-truth contradictions")
            
        # 3. Seed 25 Unanswerable Benchmark Questions
        unanswerable_file = os.path.join(settings.testset_dir, "unanswerable_25.json")
        if os.path.exists(unanswerable_file):
            with open(unanswerable_file, "r", encoding="utf-8") as f:
                unans_data = json.load(f)
                for item in unans_data:
                    u_obj = UnanswerableQuestion(
                        uid=item["id"],
                        category=item["category"],
                        question=item["question"],
                        why_unanswerable=item["why_unanswerable"],
                        adjacent_clauses_json=json.dumps(item.get("adjacent_clauses", []))
                    )
                    db.add(u_obj)
            print(f"Seeded {len(unans_data)} hard unanswerable benchmark questions")
            
        db.commit()
        print(f"\nSUCCESS! Database seeded with {total_clauses_count} clauses across {total_words_count} words.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed()
