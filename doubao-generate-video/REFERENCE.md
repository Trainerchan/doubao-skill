# Doubao Generate Video — 参考手册

## 模型速查

| 模型 ID | 能力 |
|---------|------|
| `doubao-seedance-2-0-260128` ⭐默认 | 最强：多模态参考、音画同生、首尾帧、联网搜索、视频编辑 |
| `doubao-seedance-1-5-pro-251128` | 首尾帧、首帧、文生、样片模式 |
| `doubao-seedance-1-0-pro-250828` | 首尾帧、首帧、文生 |
| `doubao-seedance-1-0-pro-fast-250828` | 首帧、文生（更快） |

### 模型能力矩阵

| 能力 | 2.0 | 1.5 pro | 1.0 pro | 1.0 pro fast |
|------|-----|---------|---------|--------------|
| 文生视频 | ✓ | ✓ | ✓ | ✓ |
| 图生视频-首帧 | ✓ | ✓ | ✓ | ✓ |
| 图生视频-首尾帧 | ✓ | ✓ | ✓ | ✗ |
| 多模态参考（图+视+音） | ✓ | ✗ | ✗ | ✗ |
| 音画同生 | ✓ | ✓ | ✗ | ✗ |
| 联网搜索 | ✓ | ✗ | ✗ | ✗ |
| 样片模式(draft) | ✗ | ✓ | ✗ | ✗ |

## 扩展场景

### 图生视频（首尾帧）

```python
resp = client.content_generation.tasks.create(
    model=model,
    content=[
        {"type": "text", "text": "从白天渐变到夜景的延时摄影"},
        {"type": "image_url", "image_url": {"url": "https://example.com/day.jpg"}, "role": "first_frame"},
        {"type": "image_url", "image_url": {"url": "https://example.com/night.jpg"}, "role": "last_frame"}
    ],
    duration=5,
)
```

### 多模态参考（Seedance 2.0 专属）

```python
resp = client.content_generation.tasks.create(
    model="doubao-seedance-2-0-260128",
    content=[
        {"type": "text", "text": "参考输入素材的风格，生成一段电影级画面"},
        {"type": "image_url", "image_url": {"url": "..."}, "role": "reference_image"},
        {"type": "video_url", "video_url": {"url": "..."}, "role": "reference_video"},
        {"type": "audio_url", "audio_url": {"url": "..."}, "role": "reference_audio"}
    ],
    duration=5,
)
```

### 有声视频

```python
resp = client.content_generation.tasks.create(
    model=model,
    content=[...],
    generate_audio=True,      # 音画同生
    duration=5,
)
```

### 使用回调（替代轮询）

```python
resp = client.content_generation.tasks.create(
    model=model,
    content=[...],
    callback_url="https://your-server.com/webhook",
    duration=5,
)
```

### 取消和查询任务

```python
# 查询任务列表
tasks = client.content_generation.tasks.list()
for t in tasks.data:
    print(f"{t.id}: {t.status}")

# 取消任务
client.content_generation.tasks.delete("cgt-xxxxxxxxxx")
```

## 参数速查

### 必选

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 模型 ID |
| `content` | array | 输入内容数组（见下方 content 格式） |

### 可选

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `ratio` | string | adaptive | 16:9/4:3/1:1/3:4/9:16/21:9/adaptive |
| `duration` | int | 5 | 2.0/1.5pro: [4,15]或-1（智能）；1.0: [2,12] |
| `resolution` | string | 720p/1080p | 480p/720p/1080p（2.0 fast 不支持 1080p） |
| `generate_audio` | bool | true | 是否音画同生（2.0/1.5pro） |
| `watermark` | bool | false | 是否添加 AI 水印 |
| `seed` | int | -1 | 随机种子 [-1, 2³²-1] |
| `callback_url` | string | — | 完成回调 URL |
| `return_last_frame` | bool | false | 是否返回尾帧 PNG |
| `execution_expires_after` | int | 172800 | 任务超时秒数 [3600, 259200] |
| `priority` | int | 0 | 优先级 [0, 9]，仅 2.0 |
| `safety_identifier` | string | — | 用户唯一标识 ≤ 64 字符 |
| `tools` | array | — | 仅 2.0：[`{"type":"web_search"}`] |
| `draft` | bool | false | 样片模式，仅 1.5 pro |

## content 元素格式

```json
// 文本
{"type": "text", "text": "提示词，中文≤500字，英文≤1000词"}

// 图片（role: first_frame / last_frame / reference_image）
{"type": "image_url", "image_url": {"url": "..."}, "role": "first_frame"}

// 视频（仅 2.0，role 必填 reference_video）
{"type": "video_url", "video_url": {"url": "..."}, "role": "reference_video"}

// 音频（仅 2.0，role 必填 reference_audio）
{"type": "audio_url", "audio_url": {"url": "..."}, "role": "reference_audio"}
```

## 宽高比与分辨率对照

| 分辨率 | 16:9 | 4:3 | 1:1 | 3:4 | 9:16 | 21:9 |
|--------|------|-----|-----|-----|------|------|
| 480p | 864×480 | 640×480 | 480×480 | 480×640 | — | — |
| 720p | 1280×720 | 960×720 | 960×960 | 720×960 | 720×1280 | 1680×720 |
| 1080p | 1920×1080 | 1440×1080 | 1440×1440 | 1080×1440 | 1080×1920 | 2520×1080 |

## 输入媒体限制

| 类型 | 数量 | 时长 | 格式 | 大小 |
|------|------|------|------|------|
| 图片 | 0-9张 | — | jpeg/png/webp/bmp/tiff/gif/heic/heif | ≤ 30MB/张 |
| 视频 | 0-3个 | 2-15s/个，总≤15s | mp4/mov (H.264/H.265) | ≤ 50MB/个 |
| 音频 | 0-3段 | 2-15s/段，总≤15s | wav/mp3 | ≤ 15MB/段 |

> 整个请求体 ≤ 64 MB。2.0 不支持含真人人脸的参考图。

## 任务状态

| 状态 | 说明 |
|------|------|
| `queued` | 排队中 |
| `running` | 生成中 |
| `succeeded` | 成功，可从 content.video_url 下载 |
| `failed` | 失败，查看 error 字段 |
| `cancelled` | 已取消 |

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 开通失败 | 余额 < 200 元 | 充值或购买资源包 |
| 任务超时 | 超过 48 小时 | 检查 execution_expires_after |
| 含真人人脸被拒 | 2.0 限制 | 使用预置虚拟人像 |
| task_id 过期 | 仅保存 7 天 | 重新创建任务 |
| 请求体过大 | > 64 MB | 压缩图片或减少参考素材 |

## 参考链接

- Seedance 2.0 API 参考：https://www.volcengine.com/docs/82379/1520757
- SDK 示例教程：https://www.volcengine.com/docs/82379/2298881
- Seedance 2.0 高级教程：https://www.volcengine.com/docs/82379/2291680
- 提示词指南：https://www.volcengine.com/docs/82379/2222480
