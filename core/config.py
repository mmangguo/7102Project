from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


def _load_env_file(env_path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not env_path.exists():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key:
            values[key] = val
    return values


def _env(key: str, env_file: Dict[str, str], default: str | None = None) -> str | None:
    if key in os.environ and os.environ[key] != "":
        return os.environ[key]
    if key in env_file and env_file[key] != "":
        return env_file[key]
    return default


@dataclass
class AssistantConfig:
    base_dir: Path
    chunks_path: Path
    topic_keywords_path: Path
    llm_provider: str
    llm_model: str
    bailian_api_key: str | None
    bailian_base_url: str
    openai_api_key: str | None
    openai_base_url: str | None

    @classmethod
    def from_env(cls, base_dir: str | Path) -> "AssistantConfig":
        root = Path(base_dir)
        env_file = _load_env_file(root / ".env")

        llm_model = (
            _env("LLM_MODEL", env_file)
            or _env("BAILIAN_MODEL", env_file)
            or _env("OPENAI_MODEL", env_file)
            or "qwen-plus"
        )

        return cls(
            base_dir=root,
            chunks_path=root
            / "data"
            / "dataset_businessnewsdaily"
            / "clean"
            / "rag_chunks"
            / "chunks.csv",
            topic_keywords_path=root
            / "data"
            / "dataset_businessnewsdaily"
            / "reports"
            / "nlp_analysis"
            / "lda_topics_keywords.csv",
            llm_provider=(_env("LLM_PROVIDER", env_file, "auto") or "auto")
            .strip()
            .lower(),
            llm_model=llm_model.strip(),
            bailian_api_key=_env("BAILIAN_API_KEY", env_file),
            bailian_base_url=(
                _env(
                    "BAILIAN_BASE_URL",
                    env_file,
                    "https://dashscope.aliyuncs.com/compatible-mode/v1",
                )
                or "https://dashscope.aliyuncs.com/compatible-mode/v1"
            ).strip(),
            openai_api_key=_env("OPENAI_API_KEY", env_file),
            openai_base_url=_env("OPENAI_BASE_URL", env_file),
        )
