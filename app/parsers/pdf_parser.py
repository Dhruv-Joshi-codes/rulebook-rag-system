import re
from typing import List, Dict, Any
import pypdf

def parse_pdf_clauses(file_path: str, filename: str) -> List[Dict[str, Any]]:
    """
    Parses a PDF regulations document into semantic sections and clauses.
    Preserves clause numbers, section headings, and full text.
    """
    reader = pypdf.PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            full_text += txt + "\n"

    lines = full_text.split("\n")
    clauses = []
    
    doc_title = "Standing Charter of the Proctorial Board and Senate Committees"
    current_section = "General Standing Orders"
    current_clause_id = None
    current_clause_title = None
    current_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        if stripped.startswith("Section "):
            current_section = stripped
            continue
            
        if stripped.startswith("Clause "):
            if current_clause_id and current_lines:
                content = "\n".join(current_lines).strip()
                clauses.append({
                    "document_title": doc_title,
                    "filename": filename,
                    "section_id": current_section,
                    "clause_id": current_clause_id,
                    "title": current_clause_title,
                    "content": content,
                    "word_count": len(content.split())
                })
                current_lines = []
                
            match = re.match(r"Clause\s+([^:]+):\s*(.*)", stripped)
            if match:
                current_clause_id = f"Clause {match.group(1).strip()}"
                current_clause_title = match.group(2).strip()
            else:
                current_clause_id = stripped
                current_clause_title = stripped
            continue
            
        if current_clause_id:
            current_lines.append(line)

    if current_clause_id and current_lines:
        content = "\n".join(current_lines).strip()
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
