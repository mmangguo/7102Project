# 创业知识库聊天助手 MVP

本项目是一个可演示的创业问答 MVP，基于 BusinessNewsDaily 已清洗数据，提供完整链路：
- RAG 检索（TF-IDF）
- 主题分类（用于流程和日志，不在前端单独展示）
- 大模型回答生成（支持真实流式输出）
- 下一问预测（LLM 生成 + 回退策略）
- Streamlit 聊天界面（证据折叠展示）

## 当前架构

### 入口层
- app.py：页面初始化与主流程编排（薄入口）

### 业务核心层
- pipeline.py：对外兼容导出 EntrepreneurshipAssistant
- core/service.py：问答流程编排
- core/retriever.py：检索模块（TF-IDF）
- core/classifier.py：主题分类
- core/llm.py：LLM 客户端与流式调用
- core/prompts.py：提示词定义
- core/config.py：配置加载（支持读取 .env）
- core/text_utils.py：文本工具与回退策略

### 前端模块层
- ui/core/assistant.py：助手实例缓存
- ui/core/session.py：会话状态管理
- ui/components/chat_history.py：历史消息渲染
- ui/components/citations.py：引用角标和证据折叠区
- ui/components/suggestions.py：下一问按钮
- ui/components/styles.py：全局样式
- ui/flows/chat_turn.py：单轮问答流程（思考状态、流式回答、后处理）

## 快速启动

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 配置环境变量（推荐在项目根目录创建 .env）

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
- 若未设置 LLM_MODEL，会回退读取 BAILIAN_MODEL 或 OPENAI_MODEL。
- 当 LLM_PROVIDER=auto 时，优先使用百炼凭证，其次 OpenAI 凭证。

3. 启动应用

```bash
streamlit run app.py
```

## 运行行为说明

- 回答阶段为真实流式输出，不是前端伪流式。
- 前端不展示主题分类，但日志会记录分类结果与置信度。
- 证据以“查看引用内容”折叠区展示，作为辅助信息。
- 下一问按钮可点击触发自动追问。
- 未配置可用 API Key 时，系统会回退到本地规则摘要，应用不中断。

## 日志

- 默认输出到终端（loguru）。
- 可选环境变量：
  - LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
  - LOG_FILE=logs/app.log

## 数据路径

- data/dataset_businessnewsdaily/clean/rag_chunks/chunks.csv
- data/dataset_businessnewsdaily/reports/nlp_analysis/lda_topics_keywords.csv

## 文档约定

- plan.md：项目执行计划与实现日志（唯一维护文档）
