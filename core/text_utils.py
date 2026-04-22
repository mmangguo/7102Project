from __future__ import annotations

import json
import re
from collections import Counter
from typing import List


def tokenize(text: str) -> List[str]:
    """
    Tokenizes text by extracting English words (2+ chars) and
    Chinese characters.
    """
    return re.findall(r"[a-zA-Z]{2,}|[\u4e00-\u9fff]{1,}", text.lower())


def normalize_question_list(raw: str) -> List[str]:
    """
    Parses LLM output into a list of strings, handling both JSON arrays
    and markdown-style lists.
    """
    raw = raw.strip()
    if not raw:
        return []

    # Attempt to parse as JSON first
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return [str(x).strip() for x in data if str(x).strip()]
    except Exception:
        pass

    # Fallback: Parse line by line and strip markdown bullet points/numbers
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    cleaned = []
    for line in lines:
        line = re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip()
        if line:
            cleaned.append(line)
    return cleaned


def dynamic_next_question_fallback(query: str, answer: str) -> List[str]:
    """
    Generates template-based follow-up questions if the LLM fails to
    provide sharp predictions.
    """
    # Professional English stopwords and domain-specific noise
    stopwords = {
        "we",
        "you",
        "this",
        "that",
        "can",
        "how",
        "what",
        "and",
        "then",
        "the",
        "perform",
        "need",
        "suggest",
        "question",
        "startup",
        "company",
        "business",
        "would",
        "should",
    }

    tokens = [
        t for t in tokenize(f"{query} {answer}") if len(t) >= 2 and t not in stopwords
    ]

    # Extract the top 3 most frequent meaningful terms
    top_terms = [w for w, _ in Counter(tokens).most_common(3)]

    if not top_terms:
        return [
            "Based on current info, what should be the next Minimum Viable Action (MVA)?",
            "To minimize trial-and-error costs, which three types of key data should be prioritized?",
            "If results are required within two weeks, how should execution priorities be ranked?",
        ]

    return [
        f"Regarding '{term}', what is the most critical hypothesis to validate next?"
        for term in top_terms[:3]
    ]
