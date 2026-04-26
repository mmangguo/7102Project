# 创业知识库聊天助手 · 产品文档
# Entrepreneurship Knowledge Base Chat Assistant · Product Document

> 中/English 双语产品文档。左栏为中文（产品方 / 业务视角），右栏为英文（engineering‑friendly description）。
> Bilingual product document. Chinese on the left (product / business view); English on the right (engineering-friendly description).

---

## 1. 产品概览 / Product Overview

**中文**

创业知识库聊天助手是一个面向早期创业者的 **检索增强问答（RAG）MVP**。它以 BusinessNewsDaily 的小微企业相关文章作为知识源，基于 TF-IDF 检索、轻量主题分类、LLM 流式回答与动态下一问预测，帮助用户把零散的商业经验转化为“可落地的下一步动作”。

产品形态：基于 Streamlit 的单页聊天应用，支持证据折叠展示、行内引用角标、一键追问。

**English**

The Entrepreneurship Knowledge Base Chat Assistant is a **Retrieval-Augmented Generation (RAG) MVP** for early-stage founders. It uses cleaned articles from BusinessNewsDaily as its knowledge source and combines TF‑IDF retrieval, lightweight topic classification, streaming LLM answers, and dynamic next-question prediction to turn fragmented business advice into concrete next actions.

Form factor: a single-page Streamlit chat app with collapsible evidence, inline citation badges, and one-click follow-up questions.

---

## 2. 目标用户与使用场景 / Target Users & Use Cases

| 维度 / Dimension | 中文 | English |
| --- | --- | --- |
| 核心用户 / Core users | 0–1 阶段创业者、独立开发者、小微企业主 | Pre-seed founders, indie hackers, SMB owners |
| 典型场景 / Typical scenarios | 市场验证、冷启动获客、现金流/税务初步判断、岗位与组织搭建、CRM/工具选型 | Market validation, cold-start acquisition, basic cashflow/tax triage, hiring & team setup, CRM/tooling selection |
| 不适用场景 / Out of scope | 合规/法律/财税的最终决策；行业深度报告；实时市场数据 | Final compliance/legal/tax decisions; deep industry reports; real-time market data |

---

## 3. 核心功能 / Core Features

### 3.1 检索增强问答 / RAG Q&A

- **中文**：用户提问 → TF-IDF 检索 top-k 证据 → 将编号证据拼入提示词 → LLM 流式生成分结构的专业回答（核心洞察 / 落地建议 / 补充维度 / 总结）。
- **English**: User query → TF‑IDF retrieves top-k evidence → numbered evidence is injected into the prompt → LLM streams a structured answer (Core Insight / Actionable Steps / Missing Dimensions / Summary).

### 3.2 主题分类（后台辅助） / Topic Classification (Background)

- **中文**：基于 LDA 产出的 8 个主题关键词（财务与成本、营销与增长、团队、数据合规、融资、CRM、岗位能力、税务）。结果用于 Prompt 上下文与日志分析，**不在前端展示**。
- **English**: 8 LDA-derived topic labels (finance & cost, marketing & growth, team, data & compliance, funding, CRM, roles & skills, tax). The result is fed into the prompt and logs only; it is **not exposed in the UI**.

### 3.3 下一问预测 / Next-Question Prediction

- **中文**：回答完成后，LLM 以“毒舌投资人”视角产出 3 个互斥视角的追问（生存挑战 / 用户体感 / 反直觉思维）。无 API 时回退到基于高频词的模板追问。
- **English**: After each answer the LLM produces 3 sharp follow-ups from three mutually-exclusive angles (survival risk / user experience / counter-intuitive). Falls back to keyword-template questions when no API is available.

### 3.4 证据展示 / Evidence Surfacing

- **中文**：回答中的“（基于证据 1,2）”形式会被渲染成小角标 `[1,2]`；折叠区展示标题、原文链接与片段。
- **English**: Inline references like “(based on evidence 1,2)” are rendered as compact badges `[1,2]`; a collapsible panel lists source titles, URLs and snippets.

### 3.5 流式输出与思考态 / Streaming & Thinking State

- **中文**：使用 `st.status` + `st.empty` 分阶段展示“理解问题 → 检索资料 → 组织回答 → 生成追问”，回答阶段为 **真实流式**（非前端伪流式）。
- **English**: `st.status` + `st.empty` surface a staged thinking flow (understand → retrieve → compose → follow-ups). The answer phase is **true streaming** from the model, not fake progressive rendering.

### 3.6 容错回退 / Graceful Degradation

- **中文**：未配置可用 API Key 时，自动回退到本地规则摘要与模板追问，**界面不中断**。
- **English**: When no usable API key is configured, the system falls back to a local rule-based summary and template follow-ups; the UI stays fully functional.

---

## 4. 系统架构 / System Architecture

```
+---------------------------------------------------------------+
|                         app.py (entry)                        |
|  set_page_config -> inject_global_styles -> init_state        |
|  render_history  -> get_assistant        -> run_turn          |
+-------------------------------+-------------------------------+
                                |
                +---------------v----------------+
                |        ui/ (presentation)      |
                |  core.assistant (cache)        |
                |  core.session  (state)         |
                |  flows.chat_turn (single turn) |
                |  components.{chat_history,     |
                |    citations, suggestions,     |
                |    styles}                     |
                +---------------+----------------+
                                |
                +---------------v----------------+
                |      pipeline.py (facade)      |
                |   EntrepreneurshipAssistant    |
                +---------------+----------------+
                                |
        +-----------------------+-----------------------+
        |                       |                       |
+-------v--------+    +---------v---------+    +--------v--------+
| core.retriever |    | core.classifier   |    |    core.llm     |
|   (TF-IDF)     |    |   (LDA keyword)   |    | (OpenAI SDK /   |
|                |    |                   |    |  DashScope)     |
+-------+--------+    +---------+---------+    +--------+--------+
        |                       |                       |
        |   core.prompts  core.text_utils  core.config  |
        +-----------------------+-----------------------+
                                |
                    +-----------v-----------+
                    |   data/ (read-only)   |
                    |  rag_chunks + LDA     |
                    +-----------------------+
```

**中文说明**：分层清晰 —— 入口层（`app.py`）只做编排；`ui/` 负责呈现与会话；`core/` 为业务核心；`data/` 是只读的离线产物（来自独立的爬取与 NLP 流水线）。

**English note**: Layers are kept thin — `app.py` only orchestrates; `ui/` handles presentation and session; `core/` contains business logic; `data/` holds read-only offline artifacts produced by a separate crawling & NLP pipeline.

---

## 5. 端到端请求时序 / End-to-End Turn Sequence

```
User ──► chat_input ──► run_turn(query)
               │
               ▼
        prepare_turn()                     (core.service)
               ├── retriever.retrieve(k=5) (TF-IDF → top-k chunks)
               ├── classifier.classify()   (LDA keyword overlap)
               └── build_answer_prompt()   (evidence + role prompt)
               │
               ▼
        stream_answer()                    (LLM chat.completions stream)
               └── UI chunks concatenated & re-rendered with citation badges
               │
               ▼
        finalize_turn(answer_text)
               └── _predict_next_questions() (LLM or fallback)
               │
               ▼
        st.session_state.messages.append(...)
               │
               ▼
        render_next_question_buttons()     (one-click follow-ups)
```

---

## 6. 数据与知识源 / Data & Knowledge Source

### 6.1 数据产物 / Data Artifacts

| 文件 / File | 说明 | Description |
| --- | --- | --- |
| `data/.../rag_chunks/chunks.csv` | RAG 检索切片（~16k 行） | RAG chunks (~16k rows) |
| `data/.../rag_chunks/chunks.jsonl` | 同上的 JSONL 版本 | Same chunks as JSONL |
| `data/.../rag_chunks/article_index.csv` | 文档级索引（~1.4k 文档） | Document-level index (~1.4k docs) |
| `data/.../nlp_analysis/lda_topics_keywords.csv` | 8 主题 × Top 关键词 | 8 topics × top keywords |
| `data/.../nlp_analysis/embeddings.npy` | 预计算句向量（all‑MiniLM‑L6‑v2） | Pre-computed sentence embeddings (all‑MiniLM‑L6‑v2) |
| `data/.../nlp_analysis/*` | NER、关键词共现、主题分布、语义相似度、知识图谱边等中间产物 | Auxiliary NLP outputs (NER, co‑occurrence, topic dist., semantic edges, KG edges …) |

### 6.2 主题体系 / Topic Taxonomy

| ID | 中文标签 | English Label | 示例关键词 / Sample keywords |
| --- | --- | --- | --- |
| 0 | 财务与成本管理 | Finance & Cost Management | accounting, cost, inventory, software |
| 1 | 营销与用户增长 | Marketing & Growth | customers, email, social, brand |
| 2 | 团队与组织管理 | Team & Org Management | employees, workplace, benefits |
| 3 | 数据与合规风险 | Data & Compliance | data, insurance, payroll, security |
| 4 | 融资与现金流 | Funding & Cashflow | credit, loan, bank, owners |
| 5 | 工具与 CRM 系统 | Tools & CRM | crm, features, sales, tools |
| 6 | 岗位与能力建设 | Roles & Skills | job, skills, hiring, career |
| 7 | 税务与申报 | Tax & Filing | tax, payroll, income, file |

### 6.3 离线生成流水线 / Offline Pipeline

**中文**：`businessnewsdaily_crawl_pipeline.ipynb` 负责“URL 清洗 → 并发抓取 → 正文解析 → 清洗结构化 → RAG 切片落盘 → NLP 产物（TF‑IDF/LDA/embedding/NER/知识图谱边）”的端到端离线工作流，与在线服务解耦。

**English**: `businessnewsdaily_crawl_pipeline.ipynb` owns the end-to-end offline workflow — URL cleaning → concurrent crawling → body parsing → structured cleaning → RAG chunking → NLP artifacts (TF‑IDF / LDA / embeddings / NER / KG edges). It is decoupled from the online service.

---

## 7. 技术栈 / Tech Stack

| 分类 / Layer | 选型 / Choice | 原因 / Why |
| --- | --- | --- |
| 前端 / Frontend | Streamlit ≥ 1.35 | MVP 体验、原生流式 + chat primitives / Fast MVP UX, native streaming + chat primitives |
| 检索 / Retrieval | scikit‑learn TfidfVectorizer (1–2 gram, max_features=50k) | 零依赖、可解释、秒级冷启动 / Zero-dep, interpretable, fast cold start |
| 分类 / Classification | 基于 LDA 关键词重叠的轻量分类器 | 无需训练，便于冷启动 / No training, cold-start friendly |
| LLM | OpenAI SDK（兼容百炼 DashScope & OpenAI） | 一套代码双通道，`responses.create` + `chat.completions.stream` |
| 日志 / Logging | loguru | 开箱即用的结构化日志 / Zero-config structured logging |
| 数据处理 / Data | pandas ≥ 2.0, numpy 2.x | 标配 |

---

## 8. 目录结构 / Directory Structure

```
7102Project/
├── app.py                             # Streamlit 入口 / entry
├── pipeline.py                        # 对外门面 / facade re-export
├── requirements.txt
├── README.md                          # 中文快速开始 / CN quickstart
├── docs/
│   └── PRODUCT.md                     # 本文件 / this file
├── businessnewsdaily_crawl_pipeline.ipynb   # 离线数据流水线 / offline pipeline
├── validate_mvp.py                    # 冒烟测试 / smoke test
├── core/
│   ├── service.py     # EntrepreneurshipAssistant 编排 / orchestration
│   ├── retriever.py   # TF-IDF 检索 / retrieval
│   ├── classifier.py  # 主题分类 / classification
│   ├── llm.py         # OpenAI 兼容客户端 / OpenAI-compatible client
│   ├── prompts.py     # 回答 & 追问 Prompt / prompts
│   ├── config.py      # .env 加载 / env loader
│   ├── text_utils.py  # 分词 / JSON 解析 / 回退追问
│   ├── logging.py     # loguru 配置 / logger config
│   └── types.py       # TypedDict / dataclass schemas
├── ui/
│   ├── core/
│   │   ├── assistant.py    # @st.cache_resource 实例 / cached instance
│   │   └── session.py      # session_state 初始化与路由
│   ├── flows/
│   │   └── chat_turn.py    # 单轮问答流程 / single-turn flow
│   └── components/
│       ├── chat_history.py # 历史渲染 / history
│       ├── citations.py    # 引用角标 & 证据折叠区 / citations + evidence
│       ├── suggestions.py  # 下一问按钮 / follow-up buttons
│       └── styles.py       # 全局样式 / global styles
└── data/
    └── dataset_businessnewsdaily/
        ├── clean/rag_chunks/          # chunks.csv / .jsonl / article_index.csv
        └── reports/nlp_analysis/      # lda_*, embeddings.npy, ner_*, ...
```

---

## 9. 快速开始 / Quickstart

### 9.1 安装依赖 / Install

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 9.2 配置环境 / Configure

**中文**：在项目根目录创建 `.env`（可选 —— 未配置时自动回退）。
**English**: Create a `.env` at project root (optional — the app falls back gracefully without it).

```env
LLM_PROVIDER=auto           # auto | bailian | openai
LLM_MODEL=qwen-plus

BAILIAN_API_KEY=your_bailian_api_key
BAILIAN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# Optional OpenAI-compatible endpoint
# OPENAI_API_KEY=sk-...
# OPENAI_BASE_URL=https://api.openai.com/v1
```

### 9.3 启动 / Run

```bash
.venv/bin/streamlit run app.py
```

**中文**：如果默认 8501 端口被占用，可加 `--server.port 8520`。若在 iframe/内嵌浏览器中预览页面空白，追加 `--server.enableCORS=false --server.enableXsrfProtection=false` 以放宽 WebSocket 握手。

**English**: If port 8501 is taken, add `--server.port 8520`. If the page renders blank inside an in-IDE preview (iframe), append `--server.enableCORS=false --server.enableXsrfProtection=false` to relax the WebSocket handshake.

---

## 10. 配置项矩阵 / Configuration Matrix

| 变量 / Variable | 默认 / Default | 作用 / Purpose |
| --- | --- | --- |
| `LLM_PROVIDER` | `auto` | `auto` 优先百炼，其次 OpenAI / `auto` prefers DashScope, then OpenAI |
| `LLM_MODEL` | `qwen-plus`（回退读 `BAILIAN_MODEL` / `OPENAI_MODEL`） | 统一的模型名 / unified model name |
| `BAILIAN_API_KEY` | — | 百炼凭证 / DashScope key |
| `BAILIAN_BASE_URL` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | OpenAI 兼容端点 / OpenAI-compatible endpoint |
| `OPENAI_API_KEY` | — | OpenAI 凭证 / OpenAI key |
| `OPENAI_BASE_URL` | — | 自定义端点 / optional custom endpoint |
| `LOG_LEVEL` | `INFO` | `DEBUG`/`INFO`/`WARNING`/`ERROR` |
| `LOG_FILE` | — | 写入文件（可选） / optional log file |

---

## 11. 可观测性 / Observability

**中文**

- 使用 loguru 输出结构化日志，涵盖：流水线启动、检索耗时与最高分、主题与置信度、LLM 请求与输出字符数、流式 chunk 数、回退触发点。
- 通过 `LOG_LEVEL` 控制粒度；可选 `LOG_FILE` 持久化到磁盘。

**English**

- Structured logs via loguru cover pipeline kickoff, retrieval latency & best score, topic & confidence, LLM request/response sizes, stream chunk count, and every fallback branch.
- `LOG_LEVEL` controls verbosity; `LOG_FILE` optionally persists logs to disk.

---

## 12. 关键设计决策 / Key Design Decisions

| 决策 / Decision | 中文理由 | English rationale |
| --- | --- | --- |
| TF‑IDF 作为默认检索 | 零模型依赖、冷启动 < 3s、可解释；向量检索留作后续升级 | Zero model dep, <3s cold start, interpretable; vector search reserved for a later upgrade |
| 主题分类不上前端 | 避免误导用户；置信度用于后台分析 | Avoid misleading users; confidence is for backend analytics |
| 回答阶段真流式 | 降低首字节时延，提高专注感 | Lower first-token latency, better focus |
| 回退模式必存在 | MVP 演示不能因为 Key 异常中断 | MVP demo must not break on API outages |
| `.env` + env 双读 | 本地开发与容器化部署都可用 | Works both in local dev and containerized deploys |
| `st.cache_resource` 缓存助手 | 避免每轮重建 TF‑IDF 矩阵与模型客户端 | Avoid rebuilding TF‑IDF matrix & client per turn |

---

## 13. 已知限制 / Known Limitations

- **中文**
  - 知识源局限于 BusinessNewsDaily，行业覆盖以英语小微企业为主；中文本地化内容较少。
  - TF‑IDF 无语义泛化，长尾问题可能检索失败；需升级到向量检索。
  - 分类器基于关键词重叠，对复合问题可能偏置；置信度仅供参考。
  - 证据片段为原文切片，长度上限 260 字符，可能在句中截断。
  - 目前没有鉴权、多用户会话、问答存档与反馈闭环。

- **English**
  - Knowledge is limited to BusinessNewsDaily; coverage skews toward English SMB content, with sparse Chinese localization.
  - TF‑IDF lacks semantic generalization; long-tail queries may miss — a vector retriever upgrade is planned.
  - The classifier uses keyword overlap and can be biased on compound queries; confidence is indicative only.
  - Evidence snippets are raw slices capped at 260 chars and may truncate mid-sentence.
  - No auth, multi-user sessions, Q&A archive, or feedback loop yet.

---

## 14. 产品路线图 / Roadmap

| 优先级 / Priority | 能力 / Capability | 中文描述 | English description |
| --- | --- | --- | --- |
| P0 | 向量检索升级 | 接入 `embeddings.npy` + cosine / FAISS，TF‑IDF 作为关键词兜底 | Wire up `embeddings.npy` + cosine / FAISS; keep TF‑IDF as a keyword fallback |
| P0 | 可观测面板 | 会话级指标、回退率、平均响应时延可视化 | Session-level metrics, fallback rate, p50/p95 latency dashboards |
| P1 | 多轮上下文 | 将历史问题用于检索查询改写与 prompt 注入 | Use chat history for query rewriting & prompt injection |
| P1 | 反馈闭环 | 👍/👎 + 评语 → 训练排序器 / 优化 Prompt | Thumbs feedback + comments → train a re-ranker / tune prompts |
| P2 | 本地化知识 | 增加中文创业内容源、双语检索 | Add Chinese founder content sources, bilingual retrieval |
| P2 | 行业过滤器 | 让用户选择行业标签以限定检索空间 | Industry tag filters to constrain the search space |
| P3 | 部署与鉴权 | Docker 镜像、Streamlit Auth / SSO、限流 | Docker image, Streamlit Auth / SSO, rate limiting |

---

## 15. 成功指标 / Success Metrics

| 指标 / Metric | 目标 / Target | 说明 / Notes |
| --- | --- | --- |
| 首答流式首字节延迟 / First-token latency | ≤ 1.5s（P50） | 含检索 + 分类 + 提示词组装 / Includes retrieval + classification + prompt build |
| 证据命中率 / Evidence hit rate | top‑1 score > 0.15 占比 ≥ 70% | 衡量检索相关性 / Proxy for retrieval relevance |
| 追问点击率 / Follow-up CTR | ≥ 25% | 反映下一问质量 / Reflects follow-up quality |
| 回退触发率 / Fallback rate | ≤ 10% | 衡量系统稳定性 / Indicates system health |
| 会话留存轮次 / Turns per session | ≥ 3 | 反映互动深度 / Indicates engagement depth |

---

## 16. 参考入口点 / Reference Entry Points

- 入口 / Entry: `app.py`
- 业务门面 / Facade: `pipeline.py`
- 核心编排 / Core orchestration: `core/service.py :: EntrepreneurshipAssistant`
- 检索 / Retrieval: `core/retriever.py :: TfidfRetriever`
- 分类 / Classification: `core/classifier.py :: TopicClassifier`
- LLM 客户端 / LLM client: `core/llm.py :: LLMClient`
- Prompt 模板 / Prompts: `core/prompts.py`
- 单轮流程 / Single turn flow: `ui/flows/chat_turn.py :: run_turn`
- 冒烟测试 / Smoke test: `validate_mvp.py`
