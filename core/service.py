from __future__ import annotations

from pathlib import Path
from typing import Iterator, List

from loguru import logger

from .classifier import TopicClassifier
from .config import AssistantConfig
from .llm import LLMClient
from .logging import configure_logging
from .prompts import build_answer_prompt, build_next_question_prompt
from .retriever import TfidfRetriever
from .text_utils import dynamic_next_question_fallback, normalize_question_list
from .types import AnswerResult, EvidenceItem, RetrievedChunk


class EntrepreneurshipAssistant:
    def __init__(self, base_dir: str | Path):
        configure_logging()
        self.config = AssistantConfig.from_env(base_dir)
        self.retriever = TfidfRetriever(str(self.config.chunks_path))
        self.classifier = TopicClassifier(str(self.config.topic_keywords_path))
        self.llm = LLMClient(self.config)
        logger.info(
            "Assistant initialized | base_dir={} | llm_available={}",
            self.config.base_dir,
            self.llm.available,
        )

    @staticmethod
    def _fallback_answer(evidences: List[RetrievedChunk]) -> str:
        if not evidences:
            return (
                "未检索到可用依据。\n\n"
                "**建议**：尝试补充更多背景信息（行业、目标客户、预算、时间范围），"
                "以便检索到更相关的资料。"
            )

        lines = [
            "**⚠️ 当前为离线模式（未配置 API Key），以下为基于检索证据的摘要：**\n",
        ]
        for i, ev in enumerate(evidences, 1):
            title = ev.get("title", "(无标题)")
            snippet = ev.get("snippet", "")
            if len(snippet) > 180:
                snippet = snippet[:180].rstrip() + "…"
            lines.append(f"**{i}. {title}**\n\n> {snippet}\n")

        lines.append(
            "---\n\n"
            "💡 **下一步建议**：先明确一个可验证目标，再用小规模实验获取反馈。"
            "配置 API Key 后可获得 LLM 生成的结构化深度回答。"
        )
        return "\n".join(lines)

    def _generate_answer(
        self, query: str, topic: str, evidences: List[RetrievedChunk]
    ) -> str:
        if not self.llm.available:
            logger.warning("Answer fallback: llm unavailable")
            return self._fallback_answer(evidences)

        context_blocks = [
            f"[证据{i}] 标题: {ev['title']}\nURL: {ev['url']}\n内容: {ev['chunk_text'][:900]}"
            for i, ev in enumerate(evidences[:4], 1)
        ]
        prompt = build_answer_prompt(
            query=query, topic=topic, context_blocks=context_blocks
        )
        text = self.llm.generate_text(prompt, temperature=0.2)
        if text:
            logger.info("Answer generated via LLM")
        else:
            logger.warning("Answer fallback: empty LLM output")
        return text if text else self._fallback_answer(evidences)

    def _build_cleaned_evidence(
        self, evidences: List[RetrievedChunk], max_display: int = 0
    ) -> List[dict]:
        limit = max_display if max_display > 0 else len(evidences)
        return [
            EvidenceItem(
                chunk_id=str(ev["chunk_id"]),
                title=str(ev["title"]),
                url=str(ev["url"]),
                score=round(float(ev["score"]), 4),
                snippet=str(ev["snippet"]),
            ).__dict__
            for ev in evidences[:limit]
        ]

    def _build_answer_prompt(
        self, query: str, topic: str, evidences: List[RetrievedChunk]
    ) -> str:
        context_blocks = [
            f"[证据{i}] 标题: {ev['title']}\nURL: {ev['url']}\n内容: {ev['chunk_text'][:900]}"
            for i, ev in enumerate(evidences[:4], 1)
        ]
        return build_answer_prompt(
            query=query, topic=topic, context_blocks=context_blocks
        )

    def _predict_next_questions(
        self,
        query: str,
        topic: str,
        answer: str,
        evidences: List[RetrievedChunk],
    ) -> List[str]:
        if not self.llm.available:
            logger.warning("Next-question fallback: llm unavailable")
            return dynamic_next_question_fallback(query, answer)

        evidence_titles = [ev.get("title", "") for ev in evidences[:3]]
        prompt = build_next_question_prompt(
            query=query,
            topic=topic,
            answer=answer,
            evidence_titles=evidence_titles,
        )
        text = self.llm.generate_text(prompt, temperature=0.4)
        candidates = normalize_question_list(text)
        candidates = [q for q in candidates if q and q != query]
        logger.info("Next-question candidates parsed | count={}", len(candidates))

        unique = []
        seen = set()
        for q in candidates:
            if q not in seen:
                seen.add(q)
                unique.append(q)
        return (
            unique[:3]
            if len(unique) >= 3
            else dynamic_next_question_fallback(query, answer)
        )

    def answer_query(self, query: str, top_k: int = 5) -> AnswerResult:
        logger.info("Pipeline start | query={} | top_k={}", query[:80], top_k)
        evidences = self.retriever.retrieve(query, k=top_k)
        logger.info(
            "Retrieval done | count={} | best_score={}",
            len(evidences),
            round(evidences[0]["score"], 4) if evidences else None,
        )
        cls = self.classifier.classify(query, evidences)
        logger.info(
            "Classification done | topic={} | confidence={}",
            cls["topic"],
            cls["confidence"],
        )
        answer = self._generate_answer(query, cls["topic"], evidences)
        next_questions = self._predict_next_questions(
            query, cls["topic"], answer, evidences
        )
        logger.info("Pipeline complete | next_questions={}", len(next_questions))

        return {
            "topic": cls["topic"],
            "confidence": cls["confidence"],
            "answer": answer,
            "evidence": self._build_cleaned_evidence(evidences),
            "next_questions": next_questions,
        }

    def prepare_turn(self, query: str, top_k: int = 5) -> dict:
        logger.info("Prepare turn start | query={} | top_k={}", query[:80], top_k)
        evidences = self.retriever.retrieve(query, k=top_k)
        cls = self.classifier.classify(query, evidences)
        logger.info(
            "Prepare turn complete | topic={} | confidence={} | evidence_count={}",
            cls["topic"],
            cls["confidence"],
            len(evidences),
        )
        return {
            "query": query,
            "topic": cls["topic"],
            "confidence": cls["confidence"],
            "evidences": evidences,
            "answer_prompt": self._build_answer_prompt(query, cls["topic"], evidences),
            "evidence": self._build_cleaned_evidence(evidences),
        }

    def stream_answer(self, turn: dict) -> Iterator[str]:
        evidences = turn["evidences"]
        if not self.llm.available:
            logger.warning("Streaming fallback: llm unavailable")
            yield self._fallback_answer(evidences)
            return

        logger.info("Streaming answer from LLM")
        yield from self.llm.stream_text(turn["answer_prompt"], temperature=0.2)

    def finalize_turn(self, turn: dict, answer_text: str) -> AnswerResult:
        answer = answer_text.strip() if answer_text else ""
        if not answer:
            logger.warning("Finalize turn fallback: empty streamed answer")
            answer = self._fallback_answer(turn["evidences"])

        next_questions = self._predict_next_questions(
            turn["query"],
            turn["topic"],
            answer,
            turn["evidences"],
        )

        return {
            "topic": turn["topic"],
            "confidence": turn["confidence"],
            "answer": answer,
            "evidence": turn["evidence"],
            "next_questions": next_questions,
        }
