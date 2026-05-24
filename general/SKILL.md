# Doubao General — 通用对话 & 多模态

调用火山方舟豆包通用模型，支持文本对话、图片/视频/文档/音频理解等。

## 前置条件

- `ARK_API_KEY` 环境变量已配置
- （可选）`DOUBAO_CHAT_MODEL` 覆盖默认模型

## API 端点

- **Chat API**（推荐，OpenAI 兼容）：`POST https://ark.cn-beijing.volces.com/api/v3/chat/completions`
- **Responses API**（新版）：`POST https://ark.cn-beijing.volces.com/api/v3/responses`

## 推荐模型

| 模型 ID | 上下文 | 特点 |
|---------|--------|------|
| `doubao-seed-2-0-lite-260428` ⭐默认 | 256K | 性价比最优，深度思考、多模态、工具调用 |
| `doubao-seed-2-0-pro-260215` | 256K | 最强性能，视觉定位、结构化输出 |
| `doubao-seed-2-0-mini-260428` | 256K | 轻量快速，适合简单任务 |

## 使用场景

### 1. 纯文本对话

**Python（OpenAI SDK，推荐）**：
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.getenv("ARK_API_KEY"),
)

response = client.chat.completions.create(
    model=os.getenv("DOUBAO_CHAT_MODEL", "doubao-seed-2-0-lite-260428"),
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
    model="doubao-seed-2-0-lite-260428",
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
    model="doubao-seed-2-0-lite-260428",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "分析这张图片"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
        ]
    }],
)
```

**cURL（Base64）**：
```bash
IMG=$(base64 -w0 /path/to/image.jpg)
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"doubao-seed-2-0-lite-260428\",\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"描述图片\"},{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/jpeg;base64,$IMG\"}}]}]}"
```

### 3. 文档理解（PDF/DOCX/XLSX/PPTX）

```python
response = client.chat.completions.create(
    model="doubao-seed-2-0-lite-260428",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "请总结这份文档"},
            {"type": "image_url", "image_url": {"url": "https://example.com/document.pdf"}}
        ]
    }],
)
```

> 大文件建议先用 File API 上传：`POST /v3/files` → 获得 `file_id`，然后在消息中用 `{"type": "file", "file": {"file_id": "xxx"}}` 引用。详见：https://www.volcengine.com/docs/82379/1902647

### 4. 视频理解

```python
response = client.chat.completions.create(
    model="doubao-seed-2-0-lite-260428",
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
    model="doubao-seed-2-0-lite-260428",
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
    model="doubao-seed-2-0-lite-260428",
    messages=[{"role": "user", "content": "解这道数学题：..."}],
    thinking={"type": "enabled"},      # enabled / disabled / auto
    reasoning_effort="high",           # minimal / low / medium / high
)
# 思考过程在 response.choices[0].message.reasoning_content
```

### 7. 函数调用 (Function Calling)

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
    model="doubao-seed-2-0-lite-260428",
    messages=[{"role": "user", "content": "北京今天天气怎么样？"}],
    tools=tools,
)
```

### 8. 流式输出

```python
stream = client.chat.completions.create(
    model="doubao-seed-2-0-lite-260428",
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

> 不支持：`frequency_penalty`、`presence_penalty`（doubao-seed-1.8/2.0 系列均不支持）

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `401 Unauthorized` | API Key 无效或未设置 | 检查 `ARK_API_KEY` |
| `Invalid signature` | 加密思维内容未原样回传 | encrypted_content 必须原样搬回 |
| `frequency_penalty not supported` | 使用了不支持的参数 | 去掉 frequency_penalty 和 presence_penalty |
| 图片过大 | 超过 36M 像素 | 先缩放再传入 |
| 配额耗尽 | 日限额用完 | 检查控制台用量 |

## 参考链接

- Chat API 完整文档：https://www.volcengine.com/docs/82379/1494384
- Responses API 文档：https://www.volcengine.com/docs/82379/1569618
- 深度思考文档：https://www.volcengine.com/docs/82379/1449737
