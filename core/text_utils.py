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


_STOPWORDS_ZH = {
    "我们", "你们", "这个", "那个", "可以", "如何", "什么", "以及", "然后",
    "一个", "进行", "需要", "建议", "问题", "创业", "公司",
}

_STOPWORDS_EN = {
    "the", "and", "for", "with", "you", "your", "are", "this", "that", "from",
    "into", "have", "has", "had", "but", "not", "can", "will", "would", "could",
    "should", "what", "how", "why", "when", "who", "any", "all", "our",
    "their", "they", "them", "its", "it's", "about", "more", "than",
    "most", "some", "such", "also", "much", "many", "very", "been", "being",
    "just", "like", "make", "made", "use", "used", "using", "one", "two",
    "first", "next", "step", "steps", "thing", "things", "company", "startup",
    "business", "founder", "founders", "team",
    "to", "of", "in", "on", "at", "by", "is", "be", "as", "or", "if", "an",
    "we", "my", "me", "us", "do", "does", "did", "so", "no", "yes", "ok",
    "answer", "question", "questions", "way", "ways", "good", "best", "new",
    "short", "long", "small", "large",
}


def dynamic_next_question_fallback(
    query: str, answer: str, lang: str = "zh"
) -> List[str]:
    stopwords = _STOPWORDS_EN if lang == "en" else _STOPWORDS_ZH

    tokens = [
        t for t in tokenize(f"{query} {answer}")
        if len(t) >= 2 and t not in stopwords
    ]
    top_terms = [w for w, _ in Counter(tokens).most_common(3)]

    if not top_terms:
        if lang == "en":
            return [
                "Given what we have, what is the smallest verifiable next action?",
                "To lower the cost of being wrong, which three datasets should we collect first?",
                "If we must show results in two weeks, how should the priorities be ranked?",
            ]
        return [
            "基于当前信息，下一步最小可验证动作应该是什么？",
            "要降低试错成本，优先补齐哪三类关键数据？",
            "如果两周内必须出结果，执行优先级该如何排序？",
        ]

    templates = _QUESTION_TEMPLATES_EN if lang == "en" else _QUESTION_TEMPLATES_ZH
    return [
        templates[i % len(templates)].format(term=term)
        for i, term in enumerate(top_terms[:3])
    ]


# Rotated through by index so the three fallback questions never share an
# opening clause. Templates are deliberately phrased to avoid the openings
# the LLM prompt forbids: "围绕…", "基于…", "关于…", "Around…", "Based on…",
# "Regarding…".
_QUESTION_TEMPLATES_ZH: tuple[str, ...] = (
    "如果下一步把重心押在「{term}」，最便宜的验证方式会是什么？",
    "「{term}」这件事，30 天内能跑出哪种可量化的里程碑？",
    "在没有更多数据的情况下，怎么判断「{term}」的判断本身是不是错的？",
    "「{term}」会跟现金流、团队和客户里的哪一项最先发生冲突？",
    "如果只剩一周时间，「{term}」相关的实验该砍到只做哪一个？",
)

_QUESTION_TEMPLATES_EN: tuple[str, ...] = (
    "If we lean on {term} in the next move, what's the cheapest way to test it works?",
    "What's a realistic 30-day milestone that would prove {term} matters here?",
    "Without gathering more data, how would we even tell that the {term} call is wrong?",
    "Where does {term} hit cashflow, team, or customers first?",
    "If we only had a week, which single experiment around {term} would we keep?",
)
