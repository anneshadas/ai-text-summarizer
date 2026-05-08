# backend/services/abstractive.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model_loader import ModelLoader
from services.preprocessor import TextPreprocessor
from config import Config

class AbstractiveSummarizer:

    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def summarize(self, text: str,
                  max_length: int = None,
                  min_length: int = None) -> dict:

        if max_length is None:
            max_length = Config.ABSTRACTIVE_MAX_LENGTH
        if min_length is None:
            min_length = Config.ABSTRACTIVE_MIN_LENGTH

        # Step 1: Clean text
        clean_text = self.preprocessor.clean(text)

        # Step 2: Get BART model
        summarizer = ModelLoader.get_abstractive_model()

        # Step 3: Generate summary
        print("Generating abstractive summary...")
        result = summarizer(
            clean_text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            early_stopping=True
        )

        summary = result[0]['summary_text']

        # Step 4: Calculate stats
        original_words = len(text.split())
        summary_words = len(summary.split())
        compression = round(summary_words / original_words * 100, 2)

        return {
            "summary": summary,
            "method": "abstractive",
            "original_words": original_words,
            "summary_words": summary_words,
            "compression_ratio": compression
        }