# backend/models/model_loader.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transformers import pipeline, AutoTokenizer, AutoModel
from config import Config

class ModelLoader:

    _abstractive_model = None
    _extractive_tokenizer = None
    _extractive_model = None

    @classmethod
    def get_abstractive_model(cls):
        if cls._abstractive_model is None:
            print(f"\nLoading abstractive model: {Config.ABSTRACTIVE_MODEL}")
            print("Please wait...")
            cls._abstractive_model = pipeline(
                task="summarization",
                model=Config.ABSTRACTIVE_MODEL,
                device=-1
            )
            print("✅ Abstractive model loaded!")
        return cls._abstractive_model

    @classmethod
    def get_extractive_model(cls):
        if cls._extractive_model is None:
            print(f"\nLoading extractive model: {Config.EXTRACTIVE_MODEL}")
            print("Please wait...")
            cls._extractive_tokenizer = AutoTokenizer.from_pretrained(
                Config.EXTRACTIVE_MODEL
            )
            cls._extractive_model = AutoModel.from_pretrained(
                Config.EXTRACTIVE_MODEL
            )
            print("✅ Extractive model loaded!")
        return cls._extractive_tokenizer, cls._extractive_model