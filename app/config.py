import os
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_DIR = os.path.join(BASE_DIR, "corpus")
TESTSET_DIR = os.path.join(BASE_DIR, "testset")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

class Settings(BaseModel):
    app_name: str = "University Regulation QA & Contradiction Detection RAG"
    version: str = "1.0.0"
    database_url: str = f"sqlite:///{os.path.join(DATA_DIR, 'regulations.db')}"
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    default_model: str = os.getenv("DEFAULT_MODEL", "gemma3:1b")
    available_models: list[str] = ["gemma3:1b", "deepseek-r1:1.5b", "heuristic-fast"]
    base_dir: str = BASE_DIR
    corpus_dir: str = CORPUS_DIR
    testset_dir: str = TESTSET_DIR

settings = Settings()
