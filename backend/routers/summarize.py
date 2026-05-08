# backend/routers/summarize.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.preprocessor import TextPreprocessor
from services.abstractive import AbstractiveSummarizer
from services.extractive import ExtractiveSummarizer

router = APIRouter()
preprocessor = TextPreprocessor()
abstractive = AbstractiveSummarizer()
extractive = ExtractiveSummarizer()

class SummarizeRequest(BaseModel):
    text: str
    method: str = "abstractive"  # "abstractive" or "extractive"
    max_length: int = None
    min_length: int = None
    num_sentences: int = None

@router.post("/summarize")
def summarize(request: SummarizeRequest):

    # Step 1: Validate input
    validation = preprocessor.validate(request.text)
    if not validation["valid"]:
        raise HTTPException(status_code=400, detail=validation["message"])

    # Step 2: Route to correct summarizer
    if request.method == "abstractive":
        result = abstractive.summarize(
            request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
    elif request.method == "extractive":
        result = extractive.summarize(
            request.text,
            num_sentences=request.num_sentences
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid method. Use 'abstractive' or 'extractive'"
        )

    return result