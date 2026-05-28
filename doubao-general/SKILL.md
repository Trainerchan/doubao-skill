---
name: doubao-general
description: Use when the user asks to analyze images, extract text from PDF/DOCX/XLSX/PPTX documents, transcribe audio, understand video content, perform web search assisted Q&A, implement function calling with 豆包, or chat with 豆包/火山方舟/字节跳动大模型.
version: 1.0.0
metadata:
  tags: [doubao, chat, multimodal, vision, document-understanding, function-calling, volcengine, 文档理解, 图片理解, 视频理解, 音频转写, streaming, tool-call, 联网搜索]
---

# Doubao General — 通用对话 & 多模态

调用火山方舟豆包通用模型，支持文本对话、图片/视频/文档/音频理解、联网搜索、函数调用。

## Overview

封装 `volcenginesdkarkruntime.Ark` 客户端调用 `/v3/chat/completions` 端点。支持 `doubao-seed-2-0-lite/pro/mini` 系列模型，256K 上下文。核心原则：所有输入通过 `messages` 数组传递，多模态内容使用 `content` 列表混合 `text` + `image_url` / `file` 类型。

## When to Use

- 用户要求用豆包对话、分析文件、提取信息
- 需要理解图片内容（URL 或本地 base64 编码）
- 需要解析 PDF/DOCX/XLSX/PPTX 文档
- 需要视频/音频理解或转写
- 需要实现 function calling（工具调用）
- 需要流式输出（streaming）

## When NOT to Use

- 生成图片 → 路由到 `doubao-generate-image`
- 生成视频 → 路由到 `doubao-generate-video`
- 用户使用其他厂商模型 → 退出此技能

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
import json

# 定义工具
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

# 第一次调用：模型返回 tool call
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "北京今天天气怎么样？"}],
    tools=tools,
)
msg = response.choices[0].message

# 检查是否有 tool call，执行并回传结果
if msg.tool_calls:
    tool_call = msg.tool_calls[0]
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)

    # 执行实际的函数（示例：返回模拟数据）
    result = {"city": func_args["city"], "weather": "晴", "temperature": 25}

    # 将 tool call 和结果一起回传，获取最终回复
    final_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "北京今天天气怎么样？"},
            {"role": "assistant", "tool_calls": [tool_call]},
            {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result, ensure_ascii=False)},
        ],
    )
    print(final_response.choices[0].message.content)
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

## Common Mistakes

| 错误 | 后果 | 正确做法 |
|------|------|----------|
| 使用 `frequency_penalty` 或 `presence_penalty` | API 返回参数不支持错误 | 豆包不支持这两个参数，不要传入 |
| function calling 只调一次不处理 tool_calls | 拿不到最终回复 | 检查 `msg.tool_calls`，执行函数后回传结果再调一次 |
| 大文件（> 10MB）用 `image_url` 直接传 | 请求失败 | 先通过 File API 上传获取 `file_id`，再用 `{"type": "file"}` 引用 |
| 本地图片直接传路径 | 模型无法访问 | 编码为 `data:image/<format>;base64,...` 格式传入 |
| 流式输出忘记检查 `chunk.choices` | `NoneType` 错误 | 每个 chunk 先判断 `if chunk.choices` |
