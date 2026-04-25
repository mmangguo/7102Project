from __future__ import annotations

from typing import Iterator, Optional

from loguru import logger

from .config import AssistantConfig

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


class LLMClient:
    def __init__(self, config: AssistantConfig):
        self._client = None
        self.model_name: Optional[str] = None
        self.provider_name: Optional[str] = None

        if OpenAI is None:
            logger.warning("OpenAI SDK not installed; LLM features are disabled")
            return

        provider = config.llm_provider
        logger.info(
            "Initializing LLM client | provider={} | model={} | has_bailian_key={} | has_openai_key={}",
            provider,
            config.llm_model,
            bool(config.bailian_api_key),
            bool(config.openai_api_key),
        )
        if provider in ("auto", "bailian") and config.bailian_api_key:
            self._client = OpenAI(
                api_key=config.bailian_api_key,
                base_url=config.bailian_base_url,
            )
            self.model_name = config.llm_model
            self.provider_name = "bailian"
            logger.success("LLM provider selected: {}", self.provider_name)
            return

        if provider in ("auto", "openai") and config.openai_api_key:
            kwargs = {"api_key": config.openai_api_key}
            if config.openai_base_url:
                kwargs["base_url"] = config.openai_base_url
            self._client = OpenAI(**kwargs)
            self.model_name = config.llm_model
            self.provider_name = "openai"
            logger.success("LLM provider selected: {}", self.provider_name)
            return

        logger.warning("No valid API credential found; fallback mode enabled")

    @property
    def available(self) -> bool:
        return self._client is not None and self.model_name is not None

    def generate_text(self, prompt: str, temperature: float = 0.2) -> str:
        if not self.available:
            logger.warning("Skipping LLM call because client is unavailable")
            return ""

        try:
            logger.info(
                "LLM request start | provider={} | model={} | temperature={} | prompt_chars={}",
                self.provider_name,
                self.model_name,
                temperature,
                len(prompt),
            )
            resp = self._client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            text = (resp.choices[0].message.content or "").strip()
            logger.info("LLM request done | output_chars={}", len(text))
            return text
        except Exception as exc:
            logger.exception("LLM request failed: {}", exc)
            return ""

    def stream_text(self, prompt: str, temperature: float = 0.2) -> Iterator[str]:
        if not self.available:
            logger.warning("Skipping LLM stream because client is unavailable")
            return

        try:
            logger.info(
                "LLM stream start | provider={} | model={} | temperature={} | prompt_chars={}",
                self.provider_name,
                self.model_name,
                temperature,
                len(prompt),
            )
            stream = self._client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                stream=True,
            )

            chunk_count = 0
            for event in stream:
                try:
                    delta = event.choices[0].delta.content or ""
                except Exception:
                    delta = ""
                if delta:
                    chunk_count += 1
                    yield delta

            logger.info("LLM stream done | chunks={}", chunk_count)
        except Exception as exc:
            logger.exception("LLM stream failed: {}", exc)
