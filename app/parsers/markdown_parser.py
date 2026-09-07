import re
from typing import List, Dict, Any

def parse_markdown_clauses(file_path: str, filename: str) -> List[Dict[str, Any]]:
    """
    Parses a markdown regulations file into semantic clause chunks.
    Extracts document title, section headings, and clause identifiers.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc_title = "University Regulation Document"
    current_section = "General Provisions"
    clauses = []
    
    current_clause_id = None
    current_clause_title = None
    current_clause_lines = []

    for line in lines:
        stripped = line.strip()
        
        # Document title (# ...)
        if stripped.startswith("# ") and not stripped.startswith("## "):
            doc_title = stripped[2:].strip()
            continue
            
        # Section (### Section X: ...)
        if stripped.startswith("### Section "):
            current_section = stripped[4:].strip()
            continue
            
        # Clause (#### Clause X.Y: ...)
        if stripped.startswith("#### Clause "):
            # Flush previous clause if exists
            if current_clause_id and current_clause_lines:
                content = "\n".join(current_clause_lines).strip()
                clauses.append({
                    "document_title": doc_title,
                    "filename": filename,
                    "section_id": current_section,
                    "clause_id": current_clause_id,
                    "title": current_clause_title,
                    "content": content,
                    "word_count": len(content.split())
                })
                current_clause_lines = []
                
            match = re.match(r"#### Clause\s+([^:]+):\s*(.*)", stripped)
            if match:
                current_clause_id = f"Clause {match.group(1).strip()}"
                current_clause_title = match.group(2).strip()
            else:
                current_clause_id = stripped[5:].strip()
                current_clause_title = current_clause_id
            continue
            
        if current_clause_id:
            current_clause_lines.append(line)

    # Flush final clause
    if current_clause_id and current_clause_lines:
        content = "\n".join(current_clause_lines).strip()
        clauses.append({
            "document_title": doc_title,
            "filename": filename,
            "section_id": current_section,
            "clause_id": current_clause_id,
            "title": current_clause_title,
            "content": content,
            "word_count": len(content.split())
        })

    return clauses
