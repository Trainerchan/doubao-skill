# Chat API 完整参考

> 来源：https://www.volcengine.com/docs/82379/1494384
> 更新时间：2026-05

## 端点

```
POST https://ark.cn-beijing.volces.com/api/v3/chat/completions
```

鉴权：`Authorization: Bearer $ARK_API_KEY`

## 完整请求参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `model` | string | ✓ | — | 模型 ID 或 Endpoint ID |
| `messages` | array | ✓ | — | 消息列表 |
| `max_tokens` | int | | 4096 | 输出 token（不含思维链） |
| `max_completion_tokens` | int | | — | 总 token（含思维链），[1,65536]，与 max_tokens 互斥 |
| `temperature` | float | | 1.0 | 温度 [0,2]，260215 固定=1 |
| `top_p` | float | | 0.7 | 核采样，260215 固定=0.95 |
| `thinking` | object | | enabled | type: enabled/disabled/auto |
| `reasoning_effort` | string | | medium | minimal/low/medium/high |
| `stream` | bool | | false | SSE 流式 |
| `stream_options` | object | | null | include_usage / chunk_include_usage |
| `response_format` | object | | text | text / json_object / json_schema |
| `service_tier` | string | | auto | fast/auto/default |
| `stop` | string/arr | | null | 停止词（不支持深度思考模型） |
| `tools` | array | | — | function / web_search / mcp / knowledge / image_process |
| `tool_choice` | string/obj | | auto | none/auto/required/指定 tool |
| `user` | string | | — | 终端用户标识 |
| `logprobs` | bool | | false | 输出 logprobs（仅部分模型） |
| `top_logprobs` | int | | — | 返回前 N 个 token 的 logprobs |

## content 元素格式

```
text       → {"type": "text", "text": "..."}
image_url  → {"type": "image_url", "image_url": {"url": "...", "detail": "high"}}
video_url  → {"type": "video_url", "video_url": {"url": "...", "fps": 1}}
input_audio → {"type": "input_audio", "input_audio": {"data": "...", "format": "mp3"}}
file       → {"type": "file", "file": {"file_id": "..."}}
```

## thinking 对象

```json
{
  "type": "enabled",              // enabled | disabled | auto
  "budget_tokens": 8192,          // 可选，思考 token 预算上限
  "encrypted_continue": {         // 可选，仅 seed-2-0 系列
    "ciphertext": "...",
    "algorithm": "AES-256-GCM",
    "key_id": "..."
  }
}
```

## 响应格式

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1716000000,
  "model": "doubao-seed-2-0-lite-260428",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "回复内容",
      "reasoning_content": "思考过程（仅深度思考模式）",
      "encrypted_content": {"ciphertext": "...", "algorithm": "...", "key_id": "..."}
    },
    "finish_reason": "stop"        // stop | length | tool_calls | content_filter
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30,
    "reasoning_tokens": 100        // 思维链 token 数
  }
}
```
