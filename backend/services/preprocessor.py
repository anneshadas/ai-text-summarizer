# backend/services/preprocessor.py
import re
import nltk

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

class TextPreprocessor:

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def clean(self, text: str) -> str:
        text = re.sub(r'http\S+|www\S+', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
        text = text.strip()
        return text

    def validate(self, text: str) -> dict:
        word_count = len(text.split())
        if word_count < 50:
            return {
                "valid": False,
                "message": f"Text too short ({word_count} words). Need at least 50 words.",
                "word_count": word_count
            }
        if word_count > 1000:
            return {
                "valid": False,
                "message": f"Text too long ({word_count} words). Maximum 1000 words.",
                "word_count": word_count
            }
        return {
            "valid": True,
            "message": "Text is valid",
            "word_count": word_count
        }

    def split_sentences(self, text: str) -> list:
        sentences = sent_tokenize(text)
        sentences = [s.strip() for s in sentences
                     if len(s.strip()) > 10]
        return sentences

    def remove_stopwords(self, text: str) -> str:
        tokens = word_tokenize(text.lower())
        filtered = [word for word in tokens
                    if word not in self.stop_words
                    and word.isalpha()]
        return ' '.join(filtered)