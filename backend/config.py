# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # ── HuggingFace API ──────────────────────────
    HF_API_TOKEN = os.getenv("HF_API_TOKEN")

    # CORRECT API URLs
    HF_ABSTRACTIVE_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
    HF_EXTRACTIVE_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2"

    # ── Summary Length Settings ──────────────────
    ABSTRACTIVE_MAX_LENGTH = 150
    ABSTRACTIVE_MIN_LENGTH = 40
    EXTRACTIVE_NUM_SENTENCES = 5

    # ── Input Text Limits ────────────────────────
    MIN_INPUT_WORDS = 50
    MAX_INPUT_WORDS = 1000

    # ── API Settings ─────────────────────────────
    PORT = 8000
    API_TITLE = "AI Text Summarizer"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = """
    AI powered text summarization tool.
    Supports both extractive and abstractive summarization.
    Built with BERT and BART transformer models.
    """