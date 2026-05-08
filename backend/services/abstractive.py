# backend/services/abstractive.py
import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.preprocessor import TextPreprocessor
from config import Config

class AbstractiveSummarizer:

    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.headers = {
            "Authorization": f"Bearer {Config.HF_API_TOKEN}"
        }

    def summarize(self, text: str,
                  max_length: int = None,
                  min_length: int = None) -> dict:

        if max_length is None:
            max_length = Config.ABSTRACTIVE_MAX_LENGTH
        if min_length is None:
            min_length = Config.ABSTRACTIVE_MIN_LENGTH

        # Step 1: Clean text
        clean_text = self.preprocessor.clean(text)

        # Step 2: Call HuggingFace API
        payload = {
            "inputs": clean_text,
            "parameters": {
                "max_length": max_length,
                "min_length": min_length,
                "do_sample": False
            }
        }

        print("Calling HuggingFace API...")
        response = requests.post(
            Config.HF_ABSTRACTIVE_URL,
            headers=self.headers,
            json=payload,
            timeout=60
        )

        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")

        # Handle empty response
        if not response.text:
            return {
                "summary": "HuggingFace API returned empty response. Please try again.",
                "method": "abstractive",
                "original_words": len(text.split()),
                "summary_words": 0,
                "compression_ratio": 0
            }

        result = response.json()
        print(f"API Response: {result}")

        # Handle model loading
        if isinstance(result, dict) and "error" in result:
            if "loading" in result["error"].lower():
                return {
                    "summary": "Model is loading on HuggingFace, please try again in 20 seconds.",
                    "method": "abstractive",
                    "original_words": len(text.split()),
                    "summary_words": 0,
                    "compression_ratio": 0
                }
            raise Exception(result["error"])

        # Handle list response
        if isinstance(result, list):
            summary = result[0]['summary_text']
        else:
            raise Exception(f"Unexpected response: {result}")

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