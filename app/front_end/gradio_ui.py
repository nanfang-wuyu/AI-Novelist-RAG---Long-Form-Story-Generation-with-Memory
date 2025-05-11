import gradio as gr
import requests

API_BASE = "http://localhost:8000"

def get_texts(lang):
    if lang == "中文":
        return {
            "title": "小说生成系统",
            "generate_tab": "生成章节",
            "change_tab": "修改章节",
            "get_all_tab": "查看所有章节",
            "get_one_tab": "查阅单章",
            "input_text": "请写下你想要写的新章节包含什么样的故事情节？",
            "change_text": "请输入修改后的内容",
            "chapter_num": "章节编号",
            "generate_button": "生成",
            "change_button": "修改",
            "get_all_button": "查看全部",
            "get_one_button": "查阅",
            "output": "输出结果",
            "lang_label": "选择界面语言",
            "view_one_dropdown": "章节编号",
            "view_one_output": "章节内容",
            "view_one_submit": "提交修改",
            "view_one_edit": "编辑",
            "view_one_status": "修改状态",
        }
    else:
        return {
            "title": "AI Novel Generator",
            "generate_tab": "Generate Chapter",
            "change_tab": "Edit Chapter",
            "get_all_tab": "View All",
            "get_one_tab": "View One",
            "input_text": "Please write down what kind of storyline you would like the new chapter you are writing to contain?",
            "change_text": "Enter new content to replace",
            "chapter_num": "Chapter Number",
            "generate_button": "Generate",
            "change_button": "Update",
            "get_all_button": "Get All",
            "get_one_button": "Get One",
            "output": "Output",
            "lang_label": "Select UI language",
            "view_one_dropdown": "Chapter Number",
            "view_one_output": "Chapter Content",
            "view_one_submit": "Submit Change",
            "view_one_edit": "Edit chapter",
            "view_one_status": "Change Status",
        }



# ==== API call functions ====

def generate(text):
    response = requests.post(f"{API_BASE}/generate", json={"query": text})
    return response.json().get("chapter", "")

def change(chapter_num, new_content):
    response = requests.post(f"{API_BASE}/change", json={
        "chapter": new_content,
        "chapter_num": chapter_num       
    })
    return response.json().get("message", "Success")

def get_all():
    response = requests.post(f"{API_BASE}/get_all")
    all_chapters = response.json().get("all_chapters", [])
    chapter_count = len(all_chapters)
    options = [f"{i+1}" for i in range(chapter_count)]
    return options, all_chapters

def get_one(chapter_num):
    response = requests.post(f"{API_BASE}/get_one", json={"chapter_num": chapter_num})
    return response.json().get("content",  response.json().get("error", "Chapter not found."))

def get_one_cached(chapter_num, cached_chapters):
    try:
        print("load_from_cache")
        return cached_chapters[int(chapter_num) - 1]["content"]
    except (IndexError, ValueError, TypeError):
        print("load_from_backend")
        return get_one(chapter_num)

def on_generate(prompt):
    chapter = generate(prompt)
    options, chapters = get_all()
    return chapter, gr.update(choices=options, value=options[-1]), chapters

def on_load():
    options, chapters = get_all()
    return gr.update(choices=options, value=options[-1]), chapters

def on_select_chapter(chapter_num, cached):
    chapter = get_one_cached(chapter_num, cached)
    return chapter, gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

def on_edit():
    return gr.update(interactive=True), gr.update(visible=True), gr.update(visible=False)

def on_submit_edit(chapter_num, new_content):
    msg = change(chapter_num, new_content)
    return gr.update(interactive=False), gr.update(visible=False), gr.update(visible=True), msg

# ==== Gradio UI ====
def build_ui():
    with gr.Blocks() as demo:
        
        def update_labels(lang):
            txt = get_texts(lang)
            return (
                gr.update(value=txt["title"]),
                gr.update(label=txt["input_text"]), gr.update(label=txt["output"]), 
                gr.update(value=txt["generate_button"]),
                gr.update(label=txt["lang_label"]),
                gr.update(label=txt["generate_tab"]),
                gr.update(label=txt["view_one_dropdown"]),
                gr.update(label=txt["view_one_output"]),
                gr.update(value=txt["view_one_submit"]),
                gr.update(value=txt["view_one_edit"]),
                gr.update(label=txt["view_one_status"]),
                gr.update(label=txt["get_one_tab"]), 

            )

        txt = get_texts("English")

        title = gr.Markdown(f"# {txt['title']}")
        lang_dropdown = gr.Dropdown(choices=["English", "中文"], value="English", label=txt["lang_label"])

        cached_chapters = gr.State([])

        with gr.Tab(txt["generate_tab"]) as generate_tab:
            input_box = gr.Textbox(label=txt["input_text"])
            output_box = gr.Textbox(label=txt["output"])
            generate_btn = gr.Button(txt["generate_button"])
            # generate_btn.click(fn=generate, inputs=input_box, outputs=output_box)
            

        # with gr.Tab(txt["change_tab"]) as change_tab:
        #     chapter_num = gr.Number(label=txt["chapter_num"])
        #     new_content = gr.Textbox(label=txt["change_text"])
        #     result = gr.Textbox(label=txt["output"])
        #     change_btn = gr.Button(txt["change_button"])
        #     change_btn.click(fn=change, inputs=[chapter_num, new_content], outputs=result)

        # with gr.Tab(txt["get_all_tab"]) as get_all_tab:
        #     result_all = gr.Textbox(label=txt["output"], lines=20)
        #     all_btn = gr.Button(txt["get_all_button"])
        #     all_btn.click(fn=get_all, outputs=result_all)

        # with gr.Tab(txt["get_one_tab"]) as get_one_tab:
        #     one_chapter_num = gr.Number(label=txt["chapter_num"])
        #     one_result = gr.Textbox(label=txt["output"], lines=10)
        #     one_btn = gr.Button(txt["get_one_button"])
        #     one_btn.click(fn=get_one, inputs=one_chapter_num, outputs=one_result)

        with gr.Tab("View One") as view_one_tab:
            view_one_dropdown = gr.Dropdown(label=txt["view_one_dropdown"], choices=[], visible=True)
            view_one_output = gr.Textbox(label=txt["view_one_output"], lines=10, interactive=False)
            view_one_submit = gr.Button(txt["view_one_submit"], visible=False)
            view_one_edit = gr.Button(txt["view_one_edit"], visible=True)
            view_one_status = gr.Textbox(label=txt["view_one_status"], visible=False)

            view_one_dropdown.change(on_select_chapter, inputs=[view_one_dropdown, cached_chapters], outputs=[view_one_output, view_one_submit, view_one_edit, view_one_status])
            view_one_edit.click(on_edit, outputs=[view_one_output, view_one_submit, view_one_edit])
            view_one_submit.click(on_submit_edit, inputs=[view_one_dropdown, view_one_output], outputs=[view_one_output, view_one_submit, view_one_edit, view_one_status])

        generate_btn.click(fn=on_generate, inputs=input_box,
                        outputs=[output_box, view_one_dropdown, cached_chapters])
        
        demo.load(lambda: on_load(), outputs=[view_one_dropdown, cached_chapters])

        lang_dropdown.change(
            fn=update_labels,
            inputs=lang_dropdown,
            outputs=[
                title,
                input_box, output_box, generate_btn,
                lang_dropdown,
                generate_tab,
                view_one_dropdown,
                view_one_output,
                view_one_submit,
                view_one_edit,
                view_one_status,
                view_one_tab,
            ]
        )

    # demo.launch()
    return demo

if __name__ == "__main__":
    ui = build_ui()
    ui.launch()