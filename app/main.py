# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.apis import generator, extractor
from app.front_end.gradio_ui import build_ui

import gradio as gr
import uvicorn

app = FastAPI(title="AI Novelist RAG")

# 允许 CORS（可选）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 后端 API
app.include_router(generator.router)
app.include_router(extractor.router)

# 前端（Gradio UI）
demo = build_ui()
app = gr.mount_gradio_app(app, demo, path="/ui")  # 访问 /ui 查看 Gradio 页面

@app.get("/")
def root():
    return RedirectResponse(url="/ui")  # 访问根页面自动跳转到 Gradio UI

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
