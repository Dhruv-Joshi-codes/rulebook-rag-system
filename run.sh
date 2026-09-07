#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

# Ensure database is seeded
if [ ! -f "data/regulations.db" ]; then
    echo "Seeding database with university regulations..."
    PYTHONPATH=. ./venv/bin/python app/scripts/seed_corpus.py
fi

echo "================================================================="
echo "Starting University Regulation QA & Contradiction Radar..."
echo "Web UI available at: http://localhost:8000"
echo "API Docs at:         http://localhost:8000/docs"
echo "================================================================="

exec ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
