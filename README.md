# 创业知识库聊天助手 MVP / Founder Assistant MVP

> **English TL;DR** — A bilingual (English / 中文) Streamlit chatbot for first-time
> founders, backed by a TF-IDF retriever over BusinessNewsDaily articles, a topic
> classifier, and an LLM (DashScope Bailian or OpenAI-compatible) that returns a
> structured 5-section answer with inline citations and 3 follow-up questions.
> Default UI language is English; switch in the top-right corner. No API key →
> the app degrades gracefully to an offline rule-based summary.

本项目是一个可演示的创业问答 MVP，基于 BusinessNewsDaily 已清洗数据，提供完整链路：
- RAG 检索（TF-IDF）
- 主题分类（用于流程和日志，不在前端单独展示）
- 大模型回答生成（支持真实流式输出）
- 下一问预测（LLM 生成 + 回退策略）
- Streamlit 聊天界面（证据折叠展示）
- **中英文双语切换**：右上角 `中文 / EN` 一键切换，UI 文案与 LLM 回答语言同步

## 当前架构

### 入口层
- `app.py`：页面初始化、语言切换器挂载与主流程编排（薄入口）

### 业务核心层
- `pipeline.py`：对外兼容导出 `EntrepreneurshipAssistant`
- `core/service.py`：问答流程编排（持有语言与置信度，转发给 prompts）
- `core/retriever.py`：检索模块（TF-IDF）
- `core/classifier.py`：主题分类
- `core/llm.py`：LLM 客户端（统一走 `chat.completions`，同步与流式同源）
- `core/prompts.py`：提示词定义（结构化 5 章节 + 证据块渲染器 + 置信度感知）
- `core/config.py`：配置加载（支持读取 `.env`）
- `core/text_utils.py`：文本工具与下一问回退策略（中英双模板，禁开禁开头）

### 前端模块层
- `ui/core/i18n.py`：翻译字典与语言状态（`init_language` / `get_lang` / `set_lang` / `t`）
- `ui/core/assistant.py`：助手实例缓存
- `ui/core/session.py`：会话状态管理（含语言初始化）
- `ui/components/header.py`：顶部 hero（按当前语言渲染）
- `ui/components/sidebar.py`：侧边栏（按当前语言渲染）
- `ui/components/welcome.py`：欢迎屏与双语 starter prompts
- `ui/components/chat_history.py`：历史消息渲染
- `ui/components/citations.py`：引用角标、章节渲染（中英双正则）
- `ui/components/suggestions.py`：下一问按钮
- `ui/components/language_switcher.py`：右上角 `中文 / EN` 切换组件
- `ui/components/styles.py`：全局样式（含语言切换胶囊样式）
- `ui/flows/chat_turn.py`：单轮问答流程（思考状态、流式回答、后处理；按语言透传到核心层）

## 快速启动

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 配置环境变量（推荐在项目根目录创建 `.env`）

```env
LLM_PROVIDER=auto
LLM_MODEL=qwen-plus

BAILIAN_API_KEY=your_bailian_api_key_here
BAILIAN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 可选 OpenAI 兼容配置
# OPENAI_API_KEY=your_openai_api_key_here
# OPENAI_BASE_URL=https://api.openai.com/v1
```

说明：
- 若未设置 `LLM_MODEL`，会回退读取 `BAILIAN_MODEL` 或 `OPENAI_MODEL`。
- 当 `LLM_PROVIDER=auto` 时，优先使用百炼凭证，其次 OpenAI 凭证。

3. 启动应用

```bash
streamlit run app.py
```

## 运行行为说明

- 默认语言为 **English**；右上角点击 `中文` 即可切换，状态保存在 `st.session_state.language`，对 UI 与 LLM prompt 同时生效。
- 回答阶段为真实流式输出，不是前端伪流式。
- 前端不展示主题分类，但日志会记录分类结果与置信度；当置信度低于 `LOW_CONFIDENCE_THRESHOLD`（默认 0.45）时，prompt 会把主题降级为「不确定 / uncertain」，避免 LLM 误锚定。
- 证据以「查看引用内容 / View cited evidence」折叠区展示，作为辅助信息。
- 下一问按钮可点击触发自动追问，问题文本与当前界面语言一致。
- 未配置可用 API Key 时，系统会回退到本地规则摘要（也支持中英两语），应用不中断。

## Prompt 模块约定（`core/prompts.py`）

提示词全部集中在 `core/prompts.py`，便于产品调优：

- **可调常量**位于文件顶部：
  - `MAX_EVIDENCE_IN_PROMPT = 6`：发给 LLM 的最大证据条数（UI 滑块 3-8 真实生效，不会被偷偷裁到 4）
  - `MAX_CHUNK_CHARS_IN_PROMPT = 900`：单条证据正文截断
  - `MAX_EVIDENCE_TITLES_FOR_NEXT_Q = 4`：追问 prompt 看到的证据标题数
  - `LOW_CONFIDENCE_THRESHOLD = 0.45`：低于此分类置信度即降级主题行
- **结构化 5 章节**（`AnswerSection`）：相关性评估 / 核心洞察 / 落地步骤 / 知识缺口 / 一句话总结。中英文章节内容由同一张 `_ANSWER_SECTIONS` 表驱动，确保两语言永不漂移。
- **证据块渲染**统一交给 `format_evidence_blocks(evidences, lang)`，自动注入 `相关度 / Relevance` 分数行，service 层无需自己拼字符串。
- **追问 prompt** 直接接收完整 `answer`（不再被截到 500 字），并在低置信度时改写主题行；fallback 模板已避开禁用开头（`围绕…` / `Around…` / `基于…` / `Based on…` / `关于…` / `Regarding…`）。

## 日志

- 默认输出到终端（loguru）。
- 可选环境变量：
  - `LOG_LEVEL=DEBUG|INFO|WARNING|ERROR`
  - `LOG_FILE=logs/app.log`

## 数据路径

- `data/dataset_businessnewsdaily/clean/rag_chunks/chunks.csv`
- `data/dataset_businessnewsdaily/reports/nlp_analysis/lda_topics_keywords.csv`

## 文档约定

- `plan.md`：项目执行计划与实现日志（唯一维护文档）
- `docs/PRODUCT.md`：完整的产品/技术参考手册
