"""Prompt templates for the entrepreneurship chatbot.

This module owns *every* string that the LLM sees:
    1. Tunable constants (truncation caps, confidence thresholds).
    2. The 5-section answer protocol — the heading and instruction for each
       section live in a single ``_ANSWER_SECTIONS`` table that drives both
       Chinese and English output, so the two languages cannot drift.
    3. A standalone ``format_evidence_blocks`` helper that owns the
       per-evidence serialisation (label language, score header, truncation),
       so service.py no longer has to assemble those blocks itself.
    4. Two public builders, ``build_answer_prompt`` and
       ``build_next_question_prompt``, that accept ``evidences`` directly and
       gracefully degrade the topic line on low classifier confidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .types import RetrievedChunk

# ---------------------------------------------------------------------------
# Tunables — every magic number that used to be sprinkled around lives here.
# ---------------------------------------------------------------------------

# Hard cap on evidence chunks the LLM ever sees in a single prompt. The UI's
# top-k slider (3-8) feeds straight through up to this ceiling, instead of
# silently being truncated to 4 like it used to be.
MAX_EVIDENCE_IN_PROMPT = 6

# Per-chunk character truncation when injecting raw text into the prompt body.
MAX_CHUNK_CHARS_IN_PROMPT = 900

# How many evidence titles the next-question prompt sees.
MAX_EVIDENCE_TITLES_FOR_NEXT_Q = 4

# Below this classifier confidence we tell the LLM the topic is uncertain
# rather than feed it a label it might over-fit to.
LOW_CONFIDENCE_THRESHOLD = 0.45


# ---------------------------------------------------------------------------
# Topic vocab keyed by the Chinese topic label that the classifier returns.
# ---------------------------------------------------------------------------

TOPIC_DOMAIN_CONTEXT: dict[str, str] = {
    "财务与成本管理": "成本核算、财务软件、库存管理、盈亏分析、现金流预测",
    "营销与用户增长": "营销渠道、邮件营销、社交媒体策略、获客成本、品牌建设、内容运营",
    "团队与组织管理": "招聘策略、员工管理、企业文化、团队搭建、人力资源合规",
    "数据与合规风险": "数据安全、商业保险、薪资合规、隐私法规、风险评估",
    "融资与现金流": "小微贷款、信用额度、投资人对接、现金流管理、融资节奏",
    "工具与CRM系统": "CRM 软件、销售工具、客户数据管理、自动化工具选型",
    "岗位与能力建设": "核心岗位设计、技能培养、招聘市场趋势、创始人能力模型",
    "税务与申报": "税务申报、薪资税、所得税抵扣、小微企业税务策略",
}

TOPIC_DOMAIN_CONTEXT_EN: dict[str, str] = {
    "财务与成本管理": "cost accounting, finance software, inventory management, P&L analysis, cash-flow forecasting",
    "营销与用户增长": "marketing channels, email marketing, social media strategy, CAC, brand building, content operations",
    "团队与组织管理": "hiring strategy, people management, company culture, team building, HR compliance",
    "数据与合规风险": "data security, business insurance, payroll compliance, privacy regulations, risk assessment",
    "融资与现金流": "SMB loans, credit lines, investor relations, cash-flow management, fundraising cadence",
    "工具与CRM系统": "CRM software, sales tooling, customer data management, automation tool selection",
    "岗位与能力建设": "core role design, skill development, hiring market trends, founder capability model",
    "税务与申报": "tax filing, payroll tax, income tax deductions, SMB tax strategy",
}

TOPIC_LABELS_EN: dict[str, str] = {
    "财务与成本管理": "Finance & Cost Management",
    "营销与用户增长": "Marketing & Growth",
    "团队与组织管理": "Team & Org Management",
    "数据与合规风险": "Data & Compliance",
    "融资与现金流": "Funding & Cashflow",
    "工具与CRM系统": "Tools & CRM",
    "岗位与能力建设": "Roles & Skills",
    "税务与申报": "Tax & Filing",
}


# ---------------------------------------------------------------------------
# 5-section answer protocol — single source of truth driving both languages.
# Edit a heading or its instruction here and both languages stay aligned.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AnswerSection:
    heading: str
    body: str


_ANSWER_SECTIONS: dict[str, tuple[AnswerSection, ...]] = {
    "zh": (
        AnswerSection(
            heading="1. 相关性评估",
            body=(
                "用 1-2 句话诚实评估检索证据与用户问题的匹配程度。"
                "如果存在差距(例如用户问特定行业，但证据只涵盖通用方法论)，"
                "需明确指出数据缺口在哪里，并说明现有证据在哪个维度上仍有参考价值。"
            ),
        ),
        AnswerSection(
            heading="2. 核心洞察",
            body=(
                "从证据中提炼对初创者最有价值的底层商业逻辑或关键原则。"
                "重点围绕**识别目标市场、验证产品市场匹配度(PMF)、制定可行商业计划**展开。"
            ),
        ),
        AnswerSection(
            heading="3. 落地步骤",
            body=(
                "给出具体的、带编号的可执行步骤。每一步要明确到一周内可启动的动作。"
                "优先推荐适合早期创业者的低成本验证方法。"
            ),
        ),
        AnswerSection(
            heading="4. 知识缺口与后续调研",
            body="列出 2-3 个证据不足的具体方向，建议用户下一步应该收集什么数据或开展什么调研。",
        ),
        AnswerSection(
            heading="5. 一句话总结",
            body="用一句话提炼本轮对话的核心商业价值。",
        ),
    ),
    "en": (
        AnswerSection(
            heading="1. Relevance Assessment",
            body=(
                "In 1-2 sentences, honestly assess how well the retrieved evidence matches "
                "the user's question. If there is a gap (for example the user asks about a "
                "specific industry while the evidence only covers generic methodology), call "
                "out the data gap explicitly and explain in which dimensions the evidence is "
                "still useful."
            ),
        ),
        AnswerSection(
            heading="2. Core Insight",
            body=(
                "Distil the most valuable underlying business logic or principle from the "
                "evidence. Focus on **identifying the target market, validating product-market "
                "fit (PMF), and building an executable business plan**."
            ),
        ),
        AnswerSection(
            heading="3. Action Steps",
            body=(
                "Provide concrete, numbered, executable steps. Each step must be something the "
                "founder can start within a week. Prefer low-cost validation methods that suit "
                "early-stage founders."
            ),
        ),
        AnswerSection(
            heading="4. Knowledge Gaps & Follow-up Research",
            body=(
                "List 2-3 specific directions where the evidence is thin, and suggest what data "
                "or research the user should gather next."
            ),
        ),
        AnswerSection(
            heading="5. One-line Summary",
            body="Capture the core business value of this turn in a single sentence.",
        ),
    ),
}


# ---------------------------------------------------------------------------
# Per-language static blocks (everything except the 5 protocol sections).
# Kept as a flat dict — one row to grep when product wording changes.
# ---------------------------------------------------------------------------

_LOC: dict[str, dict[str, str]] = {
    "zh": {
        # ---- answer prompt ----
        "role_block": (
            "## 角色\n"
            "你是一位**创业教育顾问**，服务于一个面向商业领域的在线创业教育聊天机器人。\n"
            "你的使命是帮助初次创业者和小微企业主做出明智的商业决策——通过综合知识库中的检索证据，"
            "输出清晰、可执行的指导建议。"
        ),
        "background_block": (
            "## 背景\n"
            "知识库由创业类网站(BusinessNewsDaily)的内容经数据挖掘与文本分析后构建。"
            "每条证据通过 TF-IDF 文本分析模型检索并按相关性排序——编号越小相关度越高（已附 score）。"
            "主题分类模型已将本次提问归类到下方所示的主题。"
        ),
        "context_header": "## 当前查询上下文",
        "topic_label": "分类主题",
        "topic_uncertain": "不确定（请按通用商业问题处理，不要强行套用某个主题）",
        "domain_label": "领域关键词",
        "user_query_label": "用户提问",
        "protocol_header": "## 回答协议(严格遵守)",
        "citation_block": (
            "## 引用规范\n"
            "- 将证据编号作为**括号脚注**放在相关段落末尾\n"
            "- 格式严格为 `(基于证据N)` 或 `(基于证据N,M)`，N、M 为阿拉伯数字\n"
            "- 括号内只写「基于证据」加数字，不要添加任何其他描述文字\n"
            "- 正确示例: '......自动化邮件序列可有效降低获客成本(基于证据1)'\n"
            "- 错误示例: '......(基于证据2中的用户反馈机制)' ← 禁止在括号内追加描述\n"
            "- 严禁反复出现「根据证据X所述......」的表述\n"
            "- 每个事实性论断都必须追溯到至少一条证据\n"
            "- 优先引用相关度更高（编号更小）的证据，仅在补充论据时引用更靠后的证据"
        ),
        "format_block": (
            "## 格式要求\n"
            "- 全文使用**中文**\n"
            "- 五个章节标题必须使用 `## N.` 格式，例如 `## 1. 相关性评估`，不要省略 `##`\n"
            "- 章节内部: 关键术语加粗，步骤用编号列表\n"
            "- 总长度控制在 300-600 字，简洁有力"
        ),
        "evidence_header": "## 检索证据(知识库内容)",
        "answer_marker": "## 你的回答:",
        # ---- evidence formatting ----
        "ev_tag": "证据",
        "ev_score_label": "相关度",
        "ev_title_label": "标题",
        "ev_url_label": "链接",
        "ev_content_label": "内容",
        # ---- next-question prompt ----
        "nq_role_block": (
            "## 角色\n"
            "你是创业教育聊天机器人内部的**下一问预测引擎**。"
            "你的任务是基于当前对话，预测用户最可能想进一步探索的 3 个方向。"
        ),
        "nq_design_block": (
            "## 设计理念\n"
            "好的追问能引导用户深化学习，逐步覆盖创业的各个关键面向。"
            "每个问题应把用户引向一个不同的创业维度，避免重复。"
        ),
        "nq_context_header": "## 对话上下文",
        "nq_topic_label": "当前主题",
        "nq_topic_uncertain": "不确定（请按通用商业问题处理）",
        "nq_query_label": "用户刚才问的",
        "nq_titles_label": "引用的证据标题",
        "nq_titles_empty": "(无)",
        "nq_answer_label": "顾问回答（完整）",
        "nq_rules_block": (
            "## 生成规则(严格执行)\n"
            "1. **三个不同角度** -- 每个问题必须覆盖不同维度:\n"
            "   - **角度 A(财务可行性)**: 成本结构、收入模型、融资渠道、盈亏平衡\n"
            "   - **角度 B(市场与客户)**: 目标市场识别、客户验证、竞争格局、社交媒体分析\n"
            "   - **角度 C(执行与运营)**: 商业计划步骤、团队搭建、工具选型、合规要求、上市策略\n"
            "\n"
            "2. **具体性** -- 每个问题必须引用顾问回答中提到的某个具体术语、工具、指标或概念。"
            "禁止笼统的问题，如「下一步该做什么?」\n"
            "\n"
            "3. **自然表达** -- 像一个正在学习中的创业者自然地发问。使用直接的口语化表达。"
            "禁止模板化开头: 「围绕……」、「基于……」、「关于……」\n"
            "\n"
            "4. **语言** -- 全部使用**中文**"
        ),
        "nq_examples_block": (
            "## 正反示例\n"
            "- 差: '围绕营销策略，下一步最值得验证的假设是什么?'\n"
            "- 好: '如果邮件营销的打开率低于15%，有哪些低成本的替代获客方式?'\n"
            "- 好: '在还没有客户数据的阶段，怎么用社交媒体快速测试产品概念?'\n"
            "- 好: '第一年的现金流预算里，哪些隐性成本最容易被新手忽略?'"
        ),
        "nq_output_block": (
            "## 输出格式\n"
            "仅输出一个 JSON 数组，包含恰好 3 个中文字符串。不要任何解释或 Markdown。\n"
            '示例: ["问题1", "问题2", "问题3"]'
        ),
    },
    "en": {
        # ---- answer prompt ----
        "role_block": (
            "## Role\n"
            "You are an **entrepreneurship education advisor** working inside an online "
            "chatbot for founders. Your mission is to help first-time founders and SMB "
            "owners make sound business decisions by synthesising the retrieved evidence "
            "into clear, actionable guidance."
        ),
        "background_block": (
            "## Background\n"
            "The knowledge base is built from BusinessNewsDaily articles after data mining "
            "and NLP processing. Each evidence chunk was retrieved by a TF-IDF model and "
            "sorted by relevance — the lower the index the more relevant (a score is shown "
            "at the top of each block). A topic classifier has already mapped this query to "
            "the topic shown below."
        ),
        "context_header": "## Current query context",
        "topic_label": "Classified topic",
        "topic_uncertain": "uncertain (treat as a general business question; do not over-fit to any topic)",
        "domain_label": "Domain keywords",
        "user_query_label": "User question",
        "protocol_header": "## Answer protocol (must follow)",
        "citation_block": (
            "## Citation rules\n"
            "- Place the evidence number(s) as a **parenthetical footnote** at the end of "
            "the relevant sentence/paragraph.\n"
            "- The format must be exactly `(based on evidence N)` or "
            "`(based on evidence N,M)`, where N and M are Arabic numerals.\n"
            "- Inside the parentheses, write only `based on evidence` followed by the "
            "digits — no other description.\n"
            "- Correct: \"...automated email sequences cut acquisition cost meaningfully "
            "(based on evidence 1)\"\n"
            "- Wrong: \"...(based on evidence 2 about the feedback mechanism)\" — never "
            "add description inside the parentheses.\n"
            "- Do not repeat phrases like \"according to evidence X...\" over and over.\n"
            "- Every factual claim must trace back to at least one piece of evidence.\n"
            "- Prefer citing the higher-ranked evidence (lower index); reach for later "
            "evidence only as supporting material."
        ),
        "format_block": (
            "## Format requirements\n"
            "- Write the entire answer in **English**.\n"
            "- The five section headings must use the `## N.` format exactly — e.g. "
            "`## 1. Relevance Assessment`. Do not omit the `##`.\n"
            "- Inside each section: bold key terms; use numbered lists for steps.\n"
            "- Keep the total length to roughly 200-400 words — concise and punchy."
        ),
        "evidence_header": "## Retrieved evidence (knowledge base)",
        "answer_marker": "## Your answer:",
        # ---- evidence formatting ----
        "ev_tag": "Evidence",
        "ev_score_label": "Relevance",
        "ev_title_label": "Title",
        "ev_url_label": "URL",
        "ev_content_label": "Content",
        # ---- next-question prompt ----
        "nq_role_block": (
            "## Role\n"
            "You are the **next-question prediction engine** inside an entrepreneurship "
            "education chatbot. Your task is to predict the 3 directions a user is most "
            "likely to want to explore next, based on the current conversation."
        ),
        "nq_design_block": (
            "## Design philosophy\n"
            "Great follow-ups guide the user to deepen their learning and gradually cover "
            "every key facet of entrepreneurship. Each question should pull the user toward "
            "a distinct dimension — never duplicate angles."
        ),
        "nq_context_header": "## Conversation context",
        "nq_topic_label": "Current topic",
        "nq_topic_uncertain": "uncertain (treat as a general business question)",
        "nq_query_label": "User just asked",
        "nq_titles_label": "Cited evidence titles",
        "nq_titles_empty": "(none)",
        "nq_answer_label": "Advisor answer (full)",
        "nq_rules_block": (
            "## Generation rules (strict)\n"
            "1. **Three distinct angles** — every question must cover a different dimension:\n"
            "   - **Angle A (financial viability)**: cost structure, revenue model, "
            "fundraising channels, break-even\n"
            "   - **Angle B (market & customers)**: target-market identification, customer "
            "validation, competitive landscape, social-media analysis\n"
            "   - **Angle C (execution & ops)**: business-plan steps, team building, tool "
            "selection, compliance, go-to-market\n"
            "\n"
            "2. **Specificity** — each question must reference a concrete term, tool, "
            "metric or concept that appears in the advisor's answer. No generic questions "
            "like \"what should I do next?\".\n"
            "\n"
            "3. **Natural voice** — phrase the questions like a curious founder learning "
            "aloud. Use direct, conversational English. Avoid templated openings such as "
            "\"Around...\", \"Based on...\", \"Regarding...\".\n"
            "\n"
            "4. **Language** — write everything in **English**."
        ),
        "nq_examples_block": (
            "## Examples\n"
            "- Bad: \"Around marketing strategy, what is the next assumption to validate?\"\n"
            "- Good: \"If my email open rate stays below 15%, what low-cost acquisition "
            "channels could I try instead?\"\n"
            "- Good: \"With no customer data yet, how can I use social media to quickly "
            "test a product concept?\"\n"
            "- Good: \"In a year-one cash-flow budget, which hidden costs do first-time "
            "founders most often miss?\""
        ),
        "nq_output_block": (
            "## Output format\n"
            "Output a single JSON array containing exactly 3 English strings. No "
            "explanation, no Markdown.\n"
            'Example: ["question 1", "question 2", "question 3"]'
        ),
    },
}


def _resolve_lang(lang: str) -> str:
    return lang if lang in _LOC else "zh"


# ---------------------------------------------------------------------------
# Evidence block formatter (used by both prompt builders)
# ---------------------------------------------------------------------------

def format_evidence_blocks(
    evidences: Sequence[RetrievedChunk] | Sequence[dict],
    lang: str = "zh",
) -> str:
    """Render the evidence list into the prompt-ready section.

    Owns truncation, score header and label localisation so the rest of the
    pipeline never has to assemble these strings by hand.
    """
    lang = _resolve_lang(lang)
    loc = _LOC[lang]

    blocks: list[str] = []
    for i, ev in enumerate(list(evidences)[:MAX_EVIDENCE_IN_PROMPT], 1):
        title = str(ev.get("title", "") or "—")
        url = str(ev.get("url", "") or "—")
        body = str(ev.get("chunk_text", "") or ev.get("snippet", ""))
        if len(body) > MAX_CHUNK_CHARS_IN_PROMPT:
            body = body[:MAX_CHUNK_CHARS_IN_PROMPT].rstrip() + "…"
        try:
            score = float(ev.get("score", 0.0))
        except (TypeError, ValueError):
            score = 0.0

        blocks.append(
            f"[{loc['ev_tag']}{i} | {loc['ev_score_label']}={score:.3f}]\n"
            f"{loc['ev_title_label']}: {title}\n"
            f"{loc['ev_url_label']}: {url}\n"
            f"{loc['ev_content_label']}: {body}"
        )

    return "\n\n".join(blocks)


# ---------------------------------------------------------------------------
# Topic line — gracefully degrades on low classifier confidence
# ---------------------------------------------------------------------------

def _topic_block(topic: str, confidence: float, lang: str) -> str:
    loc = _LOC[lang]
    if confidence < LOW_CONFIDENCE_THRESHOLD:
        return f"- **{loc['topic_label']}**: {loc['topic_uncertain']}\n"

    if lang == "en":
        topic_label = TOPIC_LABELS_EN.get(topic, topic)
        domain_hint = TOPIC_DOMAIN_CONTEXT_EN.get(topic, "")
    else:
        topic_label = topic
        domain_hint = TOPIC_DOMAIN_CONTEXT.get(topic, "")

    line = f"- **{loc['topic_label']}**: {topic_label}\n"
    if domain_hint:
        line += f"- **{loc['domain_label']}**: {domain_hint}\n"
    return line


def _render_protocol(lang: str) -> str:
    sections = _ANSWER_SECTIONS[lang]
    parts: list[str] = [_LOC[lang]["protocol_header"], ""]
    for section in sections:
        parts.append(f"### {section.heading}")
        parts.append(section.body)
        parts.append("")
    return "\n".join(parts).rstrip()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_answer_prompt(
    query: str,
    topic: str,
    evidences: Sequence[RetrievedChunk] | Sequence[dict],
    confidence: float = 1.0,
    lang: str = "zh",
) -> str:
    """Compose the full structured-answer prompt.

    ``evidences`` is a list of retriever-shaped dicts (must carry
    ``title``, ``url``, ``chunk_text`` or ``snippet`` and ``score``). It
    will be capped to ``MAX_EVIDENCE_IN_PROMPT`` and each chunk to
    ``MAX_CHUNK_CHARS_IN_PROMPT``. Pass the classifier's ``confidence`` so
    the topic line degrades gracefully when the classifier is unsure.
    """
    lang = _resolve_lang(lang)
    loc = _LOC[lang]
    return "\n\n".join(
        [
            loc["role_block"],
            loc["background_block"],
            (
                f"{loc['context_header']}\n"
                f"{_topic_block(topic, confidence, lang)}"
                f"- **{loc['user_query_label']}**: {query}"
            ),
            _render_protocol(lang),
            loc["citation_block"],
            loc["format_block"],
            f"{loc['evidence_header']}\n{format_evidence_blocks(evidences, lang)}",
            loc["answer_marker"],
        ]
    ) + "\n"


def build_next_question_prompt(
    query: str,
    topic: str,
    answer: str,
    evidences: Sequence[RetrievedChunk] | Sequence[dict],
    confidence: float = 1.0,
    lang: str = "zh",
) -> str:
    """Compose the follow-up-question prompt.

    Crucially, the *full* answer is forwarded to the LLM (not the first 500
    chars), so the predictor actually sees the one-line summary at the end.
    """
    lang = _resolve_lang(lang)
    loc = _LOC[lang]

    titles = [
        str(ev.get("title", "")).strip()
        for ev in list(evidences)[:MAX_EVIDENCE_TITLES_FOR_NEXT_Q]
        if str(ev.get("title", "")).strip()
    ]
    titles_str = (
        ", ".join(f'"{title}"' for title in titles) if titles
        else loc["nq_titles_empty"]
    )

    if confidence < LOW_CONFIDENCE_THRESHOLD:
        topic_label = loc["nq_topic_uncertain"]
    elif lang == "en":
        topic_label = TOPIC_LABELS_EN.get(topic, topic)
    else:
        topic_label = topic

    full_answer = (answer or "").strip()

    return "\n\n".join(
        [
            loc["nq_role_block"],
            loc["nq_design_block"],
            (
                f"{loc['nq_context_header']}\n"
                f"- **{loc['nq_topic_label']}**: {topic_label}\n"
                f"- **{loc['nq_query_label']}**: {query}\n"
                f"- **{loc['nq_titles_label']}**: {titles_str}\n"
                f"- **{loc['nq_answer_label']}**:\n{full_answer}"
            ),
            loc["nq_rules_block"],
            loc["nq_examples_block"],
            loc["nq_output_block"],
        ]
    )
