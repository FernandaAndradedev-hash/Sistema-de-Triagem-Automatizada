import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")


def _require(key: str) -> str:
    value = os.getenv(key, "").strip()
    if not value:
        print(f"\nERRO: Variável '{key}' não encontrada no .env\n", file=sys.stderr)
        sys.exit(1)
    return value


ANTHROPIC_API_KEY: str = _require("ANTHROPIC_API_KEY")
LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-haiku-4-5")
MAX_EMAIL_LENGTH: int = int(os.getenv("MAX_EMAIL_LENGTH", "5000"))
BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "5"))

# Categorias válidas
VALID_CATEGORIES = {
    "proposta", "reuniao", "financeiro", "reclamacao",
    "feedback", "informacao", "interno", "spam"
}

# Urgências válidas
VALID_URGENCIES = {"alta", "media", "baixa"}