from __future__ import annotations

import json
import re
from collections import Counter
from typing import List


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z]{2,}|[\u4e00-\u9fff]{1,}", text.lower())


def normalize_question_list(raw: str) -> List[str]:
    raw = raw.strip()
    if not raw:
        return []

    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return [str(x).strip() for x in data if str(x).strip()]
    except Exception:
        pass

    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    cleaned = []
    for line in lines:
        line = re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip()
        if line:
            cleaned.append(line)
    return cleaned


def dynamic_next_question_fallback(query: str, answer: str) -> List[str]:
    stopwords = {
        "我们",
        "你们",
        "这个",
        "那个",
        "可以",
        "如何",
        "什么",
        "以及",
        "然后",
        "一个",
        "进行",
        "需要",
        "建议",
        "问题",
        "创业",
        "公司",
    }
    tokens = [
        t for t in tokenize(f"{query} {answer}") if len(t) >= 2 and t not in stopwords
    ]
    top_terms = [w for w, _ in Counter(tokens).most_common(3)]
    if not top_terms:
        return [
            "基于当前信息，下一步最小可验证动作应该是什么？",
            "要降低试错成本，优先补齐哪三类关键数据？",
            "如果两周内必须出结果，执行优先级该如何排序？",
        ]

    return [
        f"围绕“{term}”，下一步最值得优先验证的假设是什么？" for term in top_terms[:3]
    ]
