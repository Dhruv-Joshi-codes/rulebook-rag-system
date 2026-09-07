import csv
from typing import List, Dict, Any

def parse_csv_clauses(file_path: str, filename: str) -> List[Dict[str, Any]]:
    """
    Parses a fee and deadline CSV schedule into structured clause chunks.
    Each row becomes a distinct rule entry with exact row identifier.
    """
    clauses = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        
        row_idx = 1
        for row in reader:
            if not row or len(row) < 4:
                continue
            category, window, penalty, terms = row[0], row[1], row[2], row[3]
            clause_id = f"Row {row_idx}"
            title = f"{category} ({window})"
            content = f"Transaction Category: {category}\nDeadline/Window: {window}\nFinancial Penalty or Refund Tier: {penalty}\nGoverning Policy Terms: {terms}"
            
            clauses.append({
                "document_title": "Fee Deadlines and Refunds Schedule",
                "filename": filename,
                "section_id": f"Schedule: {category}",
                "clause_id": clause_id,
                "title": title,
                "content": content,
                "word_count": len(content.split())
            })
            row_idx += 1

    return clauses
