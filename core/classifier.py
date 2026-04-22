from __future__ import annotations

from typing import Dict, List

import pandas as pd

from .text_utils import tokenize
from .types import RetrievedChunk


class TopicClassifier:
    TOPIC_LABELS = {
        0: "财务与成本管理",
        1: "营销与用户增长",
        2: "团队与组织管理",
        3: "数据与合规风险",
        4: "融资与现金流",
        5: "工具与CRM系统",
        6: "岗位与能力建设",
        7: "税务与申报",
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
        query_tokens = set(tokenize(query))
        best_topic = 0
        best_score = 0.0

        for topic_id, keywords in self.topic_keywords.items():
            overlap = sum(1 for kw in keywords if kw in query_tokens)
            score = overlap / max(len(keywords), 1)
            if score > best_score:
                best_topic = topic_id
                best_score = score

        if best_score == 0.0 and retrieved:
            title_text = " ".join(item["title"] for item in retrieved)
            title_tokens = set(tokenize(title_text))
            for topic_id, keywords in self.topic_keywords.items():
                overlap = sum(1 for kw in keywords if kw in title_tokens)
                score = overlap / max(len(keywords), 1)
                if score > best_score:
                    best_topic = topic_id
                    best_score = score

        confidence = min(0.95, max(0.35, best_score * 3 + 0.35))
        return {
            "topic_id": best_topic,
            "topic": self.TOPIC_LABELS.get(best_topic, f"主题{best_topic}"),
            "confidence": round(confidence, 3),
        }
