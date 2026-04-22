from dataclasses import dataclass
from typing import List, TypedDict


@dataclass
class EvidenceItem:
    chunk_id: str
    title: str
    url: str
    score: float
    snippet: str


class RetrievedChunk(TypedDict):
    chunk_id: str
    title: str
    url: str
    score: float
    snippet: str
    chunk_text: str


class AnswerResult(TypedDict):
    topic: str
    confidence: float
    answer: str
    evidence: List[dict]
    next_questions: List[str]
