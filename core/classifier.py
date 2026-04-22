from __future__ import annotations

from typing import Dict, List

import pandas as pd

from .text_utils import tokenize
from .types import RetrievedChunk


class TopicClassifier:
    # Professionally translated labels for the startup domain
    TOPIC_LABELS = {
        0: "Finance & Cost Management",
        1: "Marketing & User Growth",
        2: "Team & Organizational Management",
        3: "Data & Compliance Risks",
        4: "Fundraising & Cash Flow",
        5: "Tools & CRM Systems",
        6: "Talent & Capability Building",
        7: "Taxation & Regulatory Filing",
    }

    def __init__(self, topic_keywords_path: str):
        self.topic_keywords = self._load_topic_keywords(topic_keywords_path)

    @staticmethod
    def _load_topic_keywords(topic_keywords_path: str) -> Dict[int, List[str]]:
        topic_df = pd.read_csv(topic_keywords_path)
        result: Dict[int, List[str]] = {}
        for _, row in topic_df.iterrows():
            topic_id = int(row["topic_id"])
            keywords_raw = str(row["top_keywords"])
            result[topic_id] = [
                k.strip().lower() for k in keywords_raw.split(",") if k.strip()
            ]
        return result

    def classify(self, query: str, retrieved: List[RetrievedChunk]) -> dict:
        """
        Classifies the user query into a startup-related topic based on keyword overlap.
        Includes a fallback mechanism using retrieved document titles.
        """
        query_tokens = set(tokenize(query))
        best_topic = 0
        best_score = 0.0

        # Primary classification based on the user's query
        for topic_id, keywords in self.topic_keywords.items():
            overlap = sum(1 for kw in keywords if kw in query_tokens)
            score = overlap / max(len(keywords), 1)
            if score > best_score:
                best_topic = topic_id
                best_score = score

        # Secondary classification based on RAG retrieval results if query match is weak
        if best_score == 0.0 and retrieved:
            title_text = " ".join(item["title"] for item in retrieved)
            title_tokens = set(tokenize(title_text))
            for topic_id, keywords in self.topic_keywords.items():
                overlap = sum(1 for kw in keywords if kw in title_tokens)
                score = overlap / max(len(keywords), 1)
                if score > best_score:
                    best_topic = topic_id
                    best_score = score

        # Heuristic confidence calculation
        confidence = min(0.95, max(0.35, best_score * 3 + 0.35))

        return {
            "topic_id": best_topic,
            "topic": self.TOPIC_LABELS.get(best_topic, f"Topic {best_topic}"),
            "confidence": round(confidence, 3),
        }
