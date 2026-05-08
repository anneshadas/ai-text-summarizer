# backend/config.py
# ================================================
# CONFIGURATION FILE
# All settings for the entire project in one place
# ================================================

class Config:

    # ── Model Settings ──────────────────────────
    ABSTRACTIVE_MODEL = "sshleifer/distilbart-cnn-12-6"
    EXTRACTIVE_MODEL = "bert-base-uncased"

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