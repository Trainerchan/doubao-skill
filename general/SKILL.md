---
name: doubao-general
description: Doubao general chat and multimodal — text chat, image/video/document/audio understanding, function calling, web search. Use when the user asks to analyze, extract, recognize, or chat with Doubao.
version: 1.0.0
metadata:
  tags: [doubao, chat, multimodal, vision, document-understanding, function-calling, volcengine]
---

# Doubao General — 通用对话 & 多模态

调用火山方舟豆包通用模型，支持文本对话、图片/视频/文档/音频理解、联网搜索、知识库检索、函数调用等。

## 前置条件

- `ARK_API_KEY` 已配置（`.env` 文件或环境变量）
- （可选）`DOUBAO_CHAT_MODEL` 覆盖默认模型

```python
from dotenv import load_dotenv
load_dotenv()

import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.getenv("ARK_API_KEY"))
```

## API 端点

- **Chat API**：`POST https://ark.cn-beijing.volces.com/api/v3/chat/completions`
- **Responses API**（新版）：`POST https://ark.cn-beijing.volces.com/api/v3/responses`

## 推荐模型

| 模型 ID | 上下文 | 特点 |
|---------|--------|------|
| `doubao-seed-2-0-lite-260428` ⭐默认 | 256K | 性价比最优，深度思考、多模态、工具调用 |
| `doubao-seed-2-0-pro-260215` | 256K | 最强性能，视觉定位、结构化输出 |
| `doubao-seed-2-0-mini-260428` | 256K | 轻量快速，适合简单任务 |

### 选模型建议

- **lite**（默认）：日常对话、图片理解、文档提取、Function Calling——不确定时就用它
- **pro**：复杂推理、数学题、深度思考、结构化输出、视觉定位——任务明显很难时升级
- **mini**：简单任务、高并发、成本敏感场景

## 使用场景

### 1. 纯文本对话

```python
model = os.getenv("DOUBAO_CHAT_MODEL", "doubao-seed-2-0-lite-260428")

response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "你好，请介绍一下你自己"}],
)
print(response.choices[0].message.content)
```

**cURL**：
```bash
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"doubao-seed-2-0-lite-260428","messages":[{"role":"user","content":"你好"}]}'
```

### 2. 图片理解 / 识别

传入图片 URL 或 Base64。

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

**Base64（本地图片）**：
```python
import base64

with open("/path/to/image.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model=model,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "分析这张图片"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
        ]
    }],
)
```

### 3. 文档理解（PDF/DOCX/XLSX/PPTX）

**直接传 URL（小文件）**：
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

**大文件：先用 File API 上传**

对于大文件（建议 > 10MB 的 PDF/PPTX/XLSX），先上传获取 `file_id`，再在消息中引用：

```python
import os, requests

# Step 1: 上传文件
file_path = "/path/to/large_document.pdf"
with open(file_path, "rb") as f:
    resp = requests.post(
        "https://ark.cn-beijing.volces.com/api/v3/files",
        headers={
            "Authorization": f"Bearer {os.getenv('ARK_API_KEY')}",
        },
        files={
            "file": (os.path.basename(file_path), f),
            "purpose": (None, "file-extract"),
        },
    )
file_id = resp.json()["id"]
print(f"文件已上传: {file_id}")

# Step 2: 在对话中引用
response = client.chat.completions.create(
    model=model,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "请总结这份文档"},
            {"type": "file", "file": {"file_id": file_id}}
        ]
    }],
)
print(response.choices[0].message.content)
```

> File API 支持的格式与 Chat API 一致，具体限制参考火山引擎文档 https://www.volcengine.com/docs/82379/1902647

### 4. 视频理解

```python
response = client.chat.completions.create(
    model=model,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "这个视频在讲什么？"},
            {"type": "video_url", "video_url": {
                "url": "https://example.com/video.mp4",
                "fps": 1  # 每秒抽1帧，[0.2, 5]
            }}
        ]
    }],
)
```

### 5. 音频理解

```python
response = client.chat.completions.create(
    model=model,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "转写这段音频"},
            {"type": "input_audio", "input_audio": {
                "data": audio_base64,
                "format": "mp3"
            }}
        ]
    }],
)
```

> 支持格式：mp3, wav, aac, m4a。单文件 ≤ 25 MB，总时长 ≤ 120 分钟。

### 6. 深度思考模式

```python
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "解这道数学题：..."}],
    extra_body={
        "thinking": {"type": "enabled"},   # enabled / disabled / auto
        "reasoning_effort": "high",        # minimal / low / medium / high
    }
)
# 思考过程在 response.choices[0].message.reasoning_content
```

### 7. 联网搜索

让模型实时搜索互联网获取最新信息：

```python
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "2026年最新诺贝尔和平奖得主是谁？"}],
    tools=[{"type": "web_search"}],
)
print(response.choices[0].message.content)
```

### 8. 知识库检索

关联火山引擎知识库进行检索增强生成：

```python
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "根据公司内部文档，今年的销售目标是什么？"}],
    tools=[{
        "type": "knowledge",
        "knowledge": {"resource_id": "kb-xxxxxxxxxx"}
    }],
)
```

> 需要先在火山引擎控制台创建知识库并上传文档，获取 `resource_id`。

### 9. 函数调用 (Function Calling)

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

### 10. 流式输出

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

## 参数速查

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `model` | string | — | 模型 ID（必填） |
| `messages` | array | — | 消息列表（必填），支持 system/user/assistant/tool |
| `max_tokens` | int | 4096 | 最大输出，不含思维链 |
| `max_completion_tokens` | int | — | 总输出（含思维链），[1,65536]，与 max_tokens 互斥 |
| `temperature` | float | 1.0 | [0,2]，260215系列固定为1 |
| `top_p` | float | 0.7 | [0,1]，260215系列固定为0.95 |
| `thinking` | object | enabled | type: enabled/disabled/auto |
| `reasoning_effort` | string | medium | minimal/low/medium/high |
| `stream` | bool | false | SSE 流式 |
| `response_format` | object | text | text/json_object/json_schema |
| `service_tier` | string | auto | fast/auto/default |
| `stop` | str/arr | null | 停止词（不支持深度思考模型） |
| `tools` | array | — | function / web_search / knowledge / mcp / image_process |
| `tool_choice` | string/obj | auto | none/auto/required/指定 tool |

> 不支持：`frequency_penalty`、`presence_penalty`（doubao-seed-1.8/2.0 系列均不支持）

### content 元素格式

```
text        → {"type": "text", "text": "..."}
image_url   → {"type": "image_url", "image_url": {"url": "..."}}
video_url   → {"type": "video_url", "video_url": {"url": "...", "fps": 1}}
input_audio → {"type": "input_audio", "input_audio": {"data": "...", "format": "mp3"}}
file        → {"type": "file", "file": {"file_id": "..."}}
```

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `401 Unauthorized` | API Key 无效或未设置 | 检查 `ARK_API_KEY` |
| `Invalid signature` | 加密思维内容未原样传回 | encrypted_content 必须原样搬回 |
| `frequency_penalty not supported` | 使用了不支持的参数 | 去掉 frequency_penalty 和 presence_penalty |
| 图片过大 | 超过 36M 像素 | 先缩放再传入 |
| 配额耗尽 | 日限额用完 | 检查控制台用量 |

→ 如 API 返回未预期的错误，参考父 skill 的"文档验证"章节获取最新文档。

## 参考链接

- Chat API 完整文档：https://www.volcengine.com/docs/82379/1494384
- Responses API 文档：https://www.volcengine.com/docs/82379/1569618
- 深度思考文档：https://www.volcengine.com/docs/82379/1449737
- File API 文档：https://www.volcengine.com/docs/82379/1902647
