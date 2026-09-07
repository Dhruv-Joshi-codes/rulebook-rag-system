import os
import sys
import json
import asyncio

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.database import SessionLocal
from app.engine.rag_service import RAGService
from app.config import settings

async def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "heuristic-fast"
    print("=" * 80)
    print(f"UNIVERSITY REGULATION QA & CONTRADICTION RADAR - BENCHMARK RUNNER")
    print(f"Active Engine / Model: {model}")
    print("=" * 80)

    db = SessionLocal()
    service = RAGService(db)

    # 1. Test Contradictions
    contra_file = os.path.join(settings.testset_dir, "planted_contradictions.json")
    with open(contra_file, "r", encoding="utf-8") as f:
        contradictions = json.load(f)

    print(f"\n[1/3] EVALUATING PLANTED CONTRADICTIONS ({len(contradictions)} tests)...")
    contra_passed = 0
    for idx, c in enumerate(contradictions, 1):
        q = c["test_queries"][0]
        res = await service.answer_query(q, model=model)
        detected = (res.status == "CONTRADICTION" and res.contradiction and res.contradiction.contradiction_id == c["id"])
        if detected:
            contra_passed += 1
            print(f"  ✓ [{c['id']}] PASS: {c['title'][:55]}... ({res.latency_ms}ms)")
        else:
            print(f"  ✗ [{c['id']}] FAIL: Expected CONTRADICTION, got {res.status}")

    # 2. Test 25 Unanswerable Questions
    unans_file = os.path.join(settings.testset_dir, "unanswerable_25.json")
    with open(unans_file, "r", encoding="utf-8") as f:
        unanswerables = json.load(f)

    print(f"\n[2/3] EVALUATING 25 UNANSWERABLE BENCHMARK QUESTIONS...")
    unans_passed = 0
    for idx, u in enumerate(unanswerables, 1):
        res = await service.answer_query(u["question"], model=model)
        refused = (res.status == "UNANSWERABLE")
        if refused:
            unans_passed += 1
            print(f"  ✓ [{u['id']}] REFUSED (Correct): {u['question'][:55]}... ({res.latency_ms}ms)")
        else:
            print(f"  ✗ [{u['id']}] HALLUCINATED/FAILED: Expected UNANSWERABLE, got {res.status}")

    # 3. Test 12 Answerable Questions
    ans_file = os.path.join(settings.testset_dir, "answerable_queries.json")
    with open(ans_file, "r", encoding="utf-8") as f:
        answerables = json.load(f)

    print(f"\n[3/3] EVALUATING 12 ANSWERABLE FACTUAL QUERIES...")
    ans_passed = 0
    for idx, a in enumerate(answerables, 1):
        res = await service.answer_query(a["question"], model=model)
        has_citations = len(res.citations) > 0
        answered = (res.status == "ANSWERED" and has_citations)
        if answered:
            ans_passed += 1
            print(f"  ✓ [{a['id']}] ANSWERED WITH CITATIONS: {a['question'][:55]}... ({res.latency_ms}ms)")
        else:
            print(f"  ✗ [{a['id']}] FAIL: Expected ANSWERED, got {res.status}")

    total_tests = len(contradictions) + len(unanswerables) + len(answerables)
    total_passed = contra_passed + unans_passed + ans_passed
    overall_acc = (total_passed / total_tests) * 100
    contra_acc = (contra_passed / len(contradictions)) * 100
    unans_acc = (unans_passed / len(unanswerables)) * 100
    ans_acc = (ans_passed / len(answerables)) * 100

    print("\n" + "=" * 80)
    print("BENCHMARK EVALUATION SUMMARY REPORT")
    print("=" * 80)
    print(f"Total Test Cases:                 {total_tests}")
    print(f"Total Tests Passed:               {total_passed} / {total_tests} ({overall_acc:.1f}%)")
    print("-" * 80)
    print(f"Planted Contradictions Detected:  {contra_passed} / {len(contradictions)} ({contra_acc:.1f}%)")
    print(f"Unanswerable Refusal Precision:   {unans_passed} / {len(unanswerables)} ({unans_acc:.1f}%)")
    print(f"Factual Answer Citation Rate:     {ans_passed} / {len(answerables)} ({ans_acc:.1f}%)")
    print("=" * 80)

    db.close()

if __name__ == "__main__":
    asyncio.run(main())
