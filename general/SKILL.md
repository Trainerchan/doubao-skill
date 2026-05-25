---
name: doubao-general
description: Doubao (豆包) general chat and multimodal understanding — analyze images, extract PDF/DOCX/XLSX content, transcribe audio, understand video, web search, function calling. Use when the user asks to analyze a file, extract text from documents, recognize image content, transcribe audio, or chat with 豆包/火山方舟.
version: 1.0.0
metadata:
  tags: [doubao, chat, multimodal, vision, document-understanding, function-calling, volcengine]
---

# Doubao General — 通用对话 & 多模态

调用火山方舟豆包通用模型，支持文本对话、图片/视频/文档/音频理解、联网搜索、函数调用。

## 前置条件

```python
from dotenv import load_dotenv
load_dotenv()

import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.getenv("ARK_API_KEY"))
model = os.getenv("DOUBAO_CHAT_MODEL", "doubao-seed-2-0-lite-260428")
```

默认模型 `doubao-seed-2-0-lite-260428`（256K 上下文，性价比最优）。复杂推理升级为 `doubao-seed-2-0-pro-260215`，简单任务降级为 `doubao-seed-2-0-mini-260428`。详见 [REFERENCE.md](REFERENCE.md)。

## 使用场景

### 1. 纯文本对话

```python
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "你好，请介绍一下你自己"}],
)
print(response.choices[0].message.content)
```

### 2. 图片理解

**图片 URL**：
```python
response = client.chat.completions.create(
    model=model,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "这张图片里有什么？"},
            {"type": "image_url", "image_url": {"url": "https://example.com/photo.jpg"}}
        ]
    }],
)
```

**Base64（本地图片）**：将图片编码为 `data:image/...;base64,...` 格式传入 `image_url`，详见 [REFERENCE.md](REFERENCE.md)。

### 3. 文档理解（PDF/DOCX/XLSX/PPTX）

**小文件 — 直接传 URL**：
```python
response = client.chat.completions.create(
    model=model,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "请总结这份文档"},
            {"type": "image_url", "image_url": {"url": "https://example.com/document.pdf"}}
        ]
    }],
)
```

**大文件（> 10MB）**：先通过 File API 上传获取 `file_id`，再以 `{"type": "file", "file": {"file_id": "..."}}` 引用，详见 [REFERENCE.md](REFERENCE.md)。

### 4. 函数调用 (Function Calling)

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "北京今天天气怎么样？"}],
    tools=tools,
)
```

### 5. 流式输出

```python
stream = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "讲个故事"}],
    stream=True,
    stream_options={"include_usage": True},
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## 更多功能

视频理解、音频转写、深度思考、联网搜索、知识库检索等参见 [REFERENCE.md](REFERENCE.md)。
