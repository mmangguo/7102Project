from __future__ import annotations

from typing import List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .types import RetrievedChunk


class TfidfRetriever:
    def __init__(self, chunks_path: str):
        self.df = pd.read_csv(chunks_path).fillna("")
        self.df["chunk_text"] = self.df["chunk_text"].astype(str)
        self.df["title"] = self.df["title"].astype(str)
        self.df["url"] = self.df["url"].astype(str)

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=50000,
            min_df=2,
        )
        self.chunk_matrix = self.vectorizer.fit_transform(self.df["chunk_text"])

    def retrieve(self, query: str, k: int = 5) -> List[RetrievedChunk]:
        query_vec = self.vectorizer.transform([query])
        scores = linear_kernel(query_vec, self.chunk_matrix).flatten()
        top_indices = scores.argsort()[::-1][:k]

        items: List[RetrievedChunk] = []
        for idx in top_indices:
            row = self.df.iloc[idx]
            snippet = str(row["chunk_text"]).replace("\n", " ").strip()
            snippet = snippet[:260] + ("..." if len(snippet) > 260 else "")
            items.append(
                {
                    "chunk_id": row["chunk_id"],
                    "title": row["title"],
                    "url": row["url"],
                    "score": float(scores[idx]),
                    "snippet": snippet,
                    "chunk_text": row["chunk_text"],
                }
            )
        return items
