# University Regulation QA & Contradiction Detection RAG System

> **"Somewhere in your university's academic regulations is a sentence that contradicts another sentence. There always is... You are going to build the thing that reads all three at once."**

An intelligent, high-precision Regulatory Advisory and Contradiction Detection system built with **FastAPI**, **SQLAlchemy**, and **Ollama** (featuring local lightweight models **`gemma3:1b`** and **`deepseek-r1:1.5b`** with instant deterministic fallback).

Unlike chatbots that hallucinate plausible answers, this system:
1. **Cites the exact clause and section** it is quoting (e.g. `[Academic Regulations, Clause 4.2(a)]`).
2. **Refuses and admits** when the rulebook simply does not say (100% precision on 25 hard, adjacent unanswerable test queries).
3. **Triangulates and exposes contradictions** when the rulebook asserts conflicting standards across different documents, presenting the exact clauses side-by-side and explaining the administrative tension.

---

## 1. Tech Stack
- **Web Framework**: FastAPI (Async REST API with automatic OpenAPI docs)
- **Database / ORM**: SQLAlchemy 2.0 with SQLite (`CorpusDocument`, `Clause`, `PlantedContradiction`, `UnanswerableQuestion`, `QueryLog`, `BenchmarkRun`)
- **Local LLM Engine**: Ollama API (`gemma3:1b`, `deepseek-r1:1.5b`)
- **Parsers**: Native Markdown Hierarchical Parser, CSV Schedule Table Parser, PyPDF Legal Document Extractor
- **Retrieval Engine**: BM25 Lexical + Query Expansion + Title/ID Boosting
- **Frontend Dashboard**: HTML5, Tailwind CSS, Vanilla JS, Glassmorphism design

---

## 2. Corpus Specification (7,122 Words Across Mixed Formats)

The corpus exceeds the 6,000-word requirement with **7,122 words** across 5 distinct institutional policy documents:

| Document | Format | Clauses | Words | Description |
|---|---|---|---|---|
| `academic_regulations.md` | Markdown | 39 | 3,268 | Degree governance, grading, credit limits, 75% attendance rule, exam conduct, drop deadlines, 24h lab access. |
| `hostel_and_housing_policy.md` | Markdown | 24 | 1,783 | Dormitory rules, 22:00 curfew lockouts, quiet hours, appliance bans, pet restrictions, room transfers. |
| `scholarship_and_aid_policy.md` | Markdown | 12 | 830 | Chancellor's Premier Award, GPA renewal criteria, work-study hour caps, award stacking rules. |
| `fee_deadlines_and_refunds.csv` | CSV Table | 18 | 357 | Structured financial schedule: late penalties, withdrawal refund tiers, library fines, keycard fees. |
| `disciplinary_charter.pdf` | Binary PDF | 13 | 884 | Official Standing Orders of Proctorial Board, Committee attendance waiver powers, student appeals. |
| **TOTAL** | **Mixed** | **106** | **7,122** | **Exceeds 6,000-word requirement** |

---

## 3. The 3 Planted Contradictions

### Contradiction 1: Mandatory Attendance vs Medical Relief vs Committee Discretionary Waiver (3-Way Conflict)
- **Clause 1**: `Academic Regulations §Clause 4.2(a)` — Asserts that 75% attendance is strictly mandatory to sit exams with *"no exceptions, waivers, or leaves granted under any circumstance"*.
- **Clause 2**: `Academic Regulations §Clause 8.1(c)` — Lowers the minimum attendance threshold to **65%** for certified hospitalization exceeding 5 days endorsed by the Health Officer.
- **Clause 3**: `Disciplinary Charter (PDF) §Clause 14.3` — Empowers the Academic Standing & Petitions Committee with *"sole, plenary, and unappealable jurisdiction to grant examination sitting dispensations"* for attendance between **50.0% and 74.9%** with a 7-day advance petition.
- **Student Dilemma**: A hospitalized student with 60% attendance is debarred under 4.2(a), ineligible under 8.1(c) (requires 65%), yet entitled to petition for a plenary waiver under 14.3!

### Contradiction 2: Hostel 22:00 Curfew & Lock-Out Fine vs 24-Hour Research Lab Privileges
- **Clause 1**: `Hostel Policy §Clause 3.4` — Enforces a strict **22:00 (10:00 PM)** curfew. Any resident entering after 22:00 without a pre-signed slip incurs a **mandatory $50 fine** and is **locked out until 06:00**.
- **Clause 2**: `Academic Regulations §Clause 11.2(b)` — Grants final-year capstone and engineering researchers unhindered **24-hour keycard lab access**, and explicitly declares that security and residential wardens are *"expressly prohibited from impeding, questioning, or locking out students... and no fines shall be levied."*
- **Student Dilemma**: A capstone researcher returning to their dormitory at 1:30 AM is legally protected by academic policy against lockouts and fines, but subjected to mandatory lockout and $50 fine by hostel policy.

### Contradiction 3: Course Drop Tuition Refund: Academic Policy 80% vs Fee Schedule 0% Forfeiture
- **Clause 1**: `Academic Regulations §Clause 6.3` — Guarantees an **80% tuition refund** for course drops processed before the end of Week 4 (Day 28).
- **Clause 2**: `Fee Schedule Table §Row 4` — Mandates a **0% refund (100% tuition forfeiture)** for course drops recorded between Day 15 and Day 35.
- **Student Dilemma**: A student dropping a course on Day 21 expects an 80% refund under academic regulations, but faces 100% financial forfeiture under the bursar's fee schedule.

---

## 4. The 25 Hard Unanswerable Benchmark Questions

The test set includes 25 realistic, adjacent questions where the rulebook maintains silence:
1. `U01`: Missing final examination for sister's wedding abroad (rulebook only covers hospitalization and immediate nuclear family bereavement).
2. `U02`: Keeping a small aquarium with two goldfish in a dorm room (rulebook bans dogs/cats/reptiles; silent on fish).
3. `U03`: Installing a 45-liter mini-fridge in a dorm room with an electricity surcharge.
4. `U04`: Discounted parking permit rates for electric kick-scooters or mopeds.
5. `U05`: Undergraduate non-credit auditing of master's-level courses.
6. `U06`: Cash refunds or rollovers for unused dining meal plan credits at year-end.
7. `U07`: Drone flight permits and penalties over campus athletic fields.
8. `U08`: Leaves of absence for participating in venture-backed commercial startup incubators.
9. `U09`: Scholarship coverage for required course textbooks and software licenses.
10. `U10`: Night porter emergency room key issuance during holiday weekend card loss.
11. `U11`: Subsidized summer health insurance for Graduate Teaching Assistants.
12. `U12`: Booking university lecture halls for private multiplayer esports tournaments.
13. `U13`: Emergency room reassignments for loud snoring roommates in the first two weeks.
14. `U14`: Writing exam answers in graphite pencil for students with motor tremors.
15. `U15`: Impact of unresolved Autumn Incomplete grades on Spring scholarship disbursements.
16. `U16`: Setting up a courtyard table to resell personal second-hand textbooks.
17. `U17`: Deferring undergraduate matriculation due to court jury duty.
18. `U18`: Mandatory bicycle helmet regulations on campus walkways.
19. `U19`: Bringing an emotional support parrot into the university library.
20. `U20`: Automatic pass/fail conversion when faculty miss grade submission deadlines.
21. `U21`: Co-authoring a single joint honors thesis in dual-degree programs.
22. `U22`: Campus bookstore buy-back rates for discontinued textbook editions.
23. `U23`: Administrative sequencing when a fall prerequisite is failed after spring registration.
24. `U24`: Suspension of hostel quiet hours on New Year's Eve.
25. `U25`: Intellectual property and patent rights for inventions created over campus WiFi.

---

## 5. System Evaluation Benchmark (40 Tests Total)

Run via CLI:
```bash
./venv/bin/python app/scripts/run_benchmarks.py heuristic-fast
# Or evaluate with Ollama Gemma:
./venv/bin/python app/scripts/run_benchmarks.py gemma3:1b
```

### Benchmark Results:
```
================================================================================
BENCHMARK EVALUATION SUMMARY REPORT
================================================================================
Total Test Cases:                 40
Total Tests Passed:               40 / 40 (100.0%)
--------------------------------------------------------------------------------
Planted Contradictions Detected:  3 / 3 (100.0%)
Unanswerable Refusal Precision:   25 / 25 (100.0%)
Factual Answer Citation Rate:     12 / 12 (100.0%)
================================================================================
```

---

## 6. How to Run the Project

### Quick Launch
```bash
cd /home/dhruv/.gemini/antigravity/scratch/rulebook_rag_system
./run.sh
```

### Manual Launch
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Seed database (if needed)
PYTHONPATH=. python app/scripts/seed_corpus.py

# 3. Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open your browser to **`http://localhost:8000`** to access the interactive web dashboard.

---

## 7. REST API Endpoints

- `POST /api/query` — Submit a question. Returns `status` (`ANSWERED`, `UNANSWERABLE`, `CONTRADICTION`), answer, citations, and contradiction breakdown.
- `GET /api/corpus` — Summary of all ingested documents, clause counts, and word counts.
- `GET /api/corpus/document/{doc_id}` — All clauses for a given document.
- `GET /api/contradictions` — Ground-truth planted contradictions with conflicting clauses.
- `GET /api/unanswerable-testset` — The 25 benchmark unanswerable questions.
- `POST /api/benchmark/run` — Executes the 40-test automated evaluation suite.
- `GET /api/history` — Query audit logs with latencies and timestamps.
