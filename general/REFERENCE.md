# Doubao General — 参考手册

## API 端点

- **Chat API**：`POST https://ark.cn-beijing.volces.com/api/v3/chat/completions`
- **Responses API**（新版）：`POST https://ark.cn-beijing.volces.com/api/v3/responses`

## 模型速查

| 模型 ID | 上下文 | 特点 |
|---------|--------|------|
| `doubao-seed-2-0-lite-260428` ⭐默认 | 256K | 性价比最优，深度思考、多模态、工具调用 |
| `doubao-seed-2-0-pro-260215` | 256K | 最强性能，视觉定位、结构化输出 |
| `doubao-seed-2-0-mini-260428` | 256K | 轻量快速，适合简单任务 |

选模型建议：**lite**（默认）适用日常对话、图片理解、文档提取、Function Calling；**pro** 适用复杂推理、数学题、深度思考、视觉定位；**mini** 适用简单任务、高并发、成本敏感。

## 扩展场景

### 视频理解

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

### 音频理解

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

### 深度思考模式

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

### 联网搜索

```python
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "2026年最新诺贝尔和平奖得主是谁？"}],
    tools=[{"type": "web_search"}],
)
```

### 知识库检索

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

> 需先在火山引擎控制台创建知识库并获取 `resource_id`。

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

> 不支持：`frequency_penalty`、`presence_penalty`

## content 元素格式

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

## 参考链接

- Chat API 完整文档：https://www.volcengine.com/docs/82379/1494384
- Responses API 文档：https://www.volcengine.com/docs/82379/1569618
- 深度思考文档：https://www.volcengine.com/docs/82379/1449737
- File API 文档：https://www.volcengine.com/docs/82379/1902647
