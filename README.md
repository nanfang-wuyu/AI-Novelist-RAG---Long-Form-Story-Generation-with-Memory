# 🧠 AI Novelist RAG

A dedicated AI system for long-form novel generation, designed to tackle common issues like **incoherent logic**, **self-contradiction**, and **theme drift** in LLM-generated narratives.

This project integrates **Langchain + RAG + FastAPI + Local Quantized Models (e.g., Qwen)** to enable the AI to **extract key narrative elements** from its own outputs and store them in a memory-enhancing vector database (FAISS), effectively boosting logic retention and narrative consistency.

---

## 🧩 Core Idea

> **Let the AI "remember" what it writes, to keep stories logically consistent.**

- ✅ High-quality novel generation via Qwen
- ✅ Automatic extraction of key narrative settings (characters, themes, backgrounds)
- ✅ Vector memory with FAISS for context recall
- ✅ Retrieval-augmented writing with self-referencing history
- ✅ Optional consistency scoring using CoT-style benchmarks

---

## 📂 Project Structure

```
ai-novelist-rag/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── apis/
│   │   ├── generator.py
│   │   ├── extractor.py
│   │   ├── memory.py
│   │   └── benchmark.py
│   ├── models/
│   │   ├── model.py
│   │   └── faiss_index.py
│   ├── chains/
│   │   ├── rag_chain.py
│   │   └── memory_insert_chain.py
│   └── utils/
│       ├── logger.py
│       ├── text_processing.py
│       └── utils.py
├── data/
│   ├── memory_store.faiss
│   └── samples/
│       ├── raws/
│       └── processed/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/
│   └── launch_local.sh
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Quick Start

```bash
bash scripts/launch_local.sh
```

Default: Local quantized Qwen model (configurable via `config.py`).

---

## 📌 Tech Stack

- 🤖 Qwen quantized (INT4 / bfloat16)
- 🧱 Langchain pipeline management
- 🔍 FAISS for vector search
- 🔁 Retrieval-Augmented Generation (RAG)
- 🛠️ FastAPI for backend serving
- 🐳 Docker/docker-compose (optional deployment)

---

## 📌 TODO

- [ ] Interactive multi-turn topic-driven generation
- [ ] CoT-style logic scoring feedback loop
- [ ] Azure / Hugging Face Spaces deployment
- [ ] Unit test integration

---

## 🧠 Suitable For

- AI + Literature applications
- Multimodal + long-context logic reasoning
- Langchain + RAG stack practice
- Technical portfolio for interviews

---

# 🧠 AI Novelist RAG（中文）

一个专为“小说生成”设计的 AI 系统，致力于解决大语言模型在长文本生成中常见的 **逻辑性弱**、**前后矛盾**、**主题偏移** 等问题。

本项目结合 **Langchain + RAG + FastAPI + 本地量化模型（如 Qwen）**，实现 AI 在小说生成过程中自动抽取关键设定，并写入向量记忆库，从而增强模型的“逻辑一致性”和“记忆保持”。

## 🧩 核心思想

> **AI 自动记忆自己写过的内容，保持小说逻辑统一。**

## 📂 项目结构

（同上，略）

## 🚀 快速启动

```bash
bash scripts/launch_local.sh
```

默认使用本地 Qwen 模型（量化版本），配置可在 `config.py` 中修改。

## 📌 依赖技术栈

- 🤖 Qwen 本地量化模型（INT4 / bfloat16）
- 🧱 Langchain 流程构建
- 🔍 FAISS 向量数据库
- 🔁 Retrieval-Augmented Generation（RAG）
- 🛠️ FastAPI 后端接口
- 🐳 Docker / docker-compose 部署（可选）

## 📌 TODO（下一阶段）

- [ ] 添加多轮生成支持
- [ ] 实现逻辑评分反馈机制
- [ ] 云端部署版本（Azure / Hugging Face Spaces）
- [ ] 单元测试支持

## 🧠 项目适用于

- AI + 文学创作方向
- 多模态 + 长上下文推理实验
- Langchain + RAG 训练项目
- 技术型面试展示

---

欢迎 Star & Fork，开发中 🚧