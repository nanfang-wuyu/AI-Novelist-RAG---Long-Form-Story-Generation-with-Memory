# AI Novelist RAG - Long-Form Story Generation with Memory

This is a dedicated AI system for generating long-form novels with coherent logic, consistent world-building, and thematic integrity, solving common LLMs issues like incoherence, self-contradiction, and theme drift.

This project combines Langchain, Retrieval-Augmented Generation (RAG), FAISS, FastAPI, and Gradio, along with OpenAI or local quantized models (e.g., LLaMA). It allows the AI to extract key information and context from its own outputs and store them in a vector database to “remember” what it’s written—resulting in more logical and immersive storytelling. 

This system is designed as both a technical practice and a creative tool. 

## Key Features

- High-quality novel generation (via OpenAI APIs or local LLMs)
- Automatic information extraction (currently via BERT-based summary model)
- Long-context memory (via FAISS vector store)
- Context-aware coherent prompt (via RAG-like context enhancement)
- Web-based UI (via Gradio)
- Experimental consistency scoring (planned to use long-context metrics)

## Project Structure

```
ai-novelist-rag/
├── app/
│   ├── main.py                # FastAPI + Gradio mount point
│   ├── apis/                  # API endpoints for generation, editing, benchmarks
│   ├── front_end/             # Gradio-based UI
│   ├── managers/              # Managers and chains for chapter, summary, and vector memory
│   ├── models/                # Model loading and wrapper logic
│   ├── tests/                 # (Not showed here) Jupyter notebooks for quick testing
│   └── utils/                 # General utilities 
│
├── data/                      # (Not showed here) Local store for texts, summaries, vector DB 
├── docker/                    # Dockerfile and config for deployment
├── scripts/
│   ├── setup.sh               # Install dependencies
│   └── launch_local.sh        # Launch the app locally
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Getting Started

1. Install dependencies:

```bash
bash scripts/setup.sh
```

2. Launch the app locally:

```bash
bash scripts/launch_local.sh
```

Default setup:

- Uses gpt-4o-mini (via OpenAI API) for novel generation
- Uses bart-large-cnn for chapter summarization  
- Configurable in config.py (coming soon)

Requires your own OpenAI API key

## Coming Soon

- Chinese-style writing support
- Multiple books/novels within the same workspace
- Streaming generation responses to frontend
- Benchmark consistency improvement with and without memory
- Deployment to Azure

## Contributing

This project is still under active development, Star, Fork, and PRs are welcome!
