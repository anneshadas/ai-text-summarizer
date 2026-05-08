# backend/services/extractive.py
import sys
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.preprocessor import TextPreprocessor
from config import Config

class ExtractiveSummarizer:

    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def get_embeddings(self, sentences: list) -> np.ndarray:
        """
        Converts sentences to TF-IDF vectors locally
        Fast, no API needed ✅
        """
        vectorizer = TfidfVectorizer(stop_words='english')
        
        try:
            tfidf_matrix = vectorizer.fit_transform(sentences)
            return tfidf_matrix.toarray()
        except Exception as e:
            raise Exception(f"TF-IDF Error: {str(e)}")

    def score_sentences(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Scores sentences by cosine similarity
        """
        similarity_matrix = cosine_similarity(embeddings)
        scores = similarity_matrix.mean(axis=1)
        return scores

    def summarize(self, text: str,
                  num_sentences: int = None) -> dict:

        if num_sentences is None:
            num_sentences = Config.EXTRACTIVE_NUM_SENTENCES

        # Step 1: Clean text
        clean_text = self.preprocessor.clean(text)

        # Step 2: Split into sentences
        sentences = self.preprocessor.split_sentences(clean_text)

        print(f"Total sentences: {len(sentences)}")

        if len(sentences) <= num_sentences:
            num_sentences = len(sentences)

        # Step 3: Get TF-IDF embeddings
        print("Computing TF-IDF embeddings locally...")
        embeddings = self.get_embeddings(sentences)

        # Step 4: Score sentences
        scores = self.score_sentences(embeddings)

        # Step 5: Get top N indices
        top_indices = np.argsort(scores)[-num_sentences:]

        # Step 6: Sort to maintain original order
        top_indices = sorted(top_indices)

        # Step 7: Join selected sentences
        summary = ' '.join([sentences[i] for i in top_indices])

        original_words = len(text.split())
        summary_words = len(summary.split())
        compression = round(summary_words / original_words * 100, 2)

        return {
            "summary": summary,
            "method": "extractive",
            "original_sentences": len(sentences),
            "summary_sentences": num_sentences,
            "original_words": original_words,
            "summary_words": summary_words,
            "compression_ratio": compression
        }