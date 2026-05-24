---
name: doubao-generate-video
description: Doubao video generation using Seedance — text-to-video, image-to-video, multimodal reference. Use when the user asks to generate, create, or edit videos with Doubao.
version: 1.0.0
metadata:
  tags: [doubao, seedance, video-generation, text-to-video, volcengine]
---

# Doubao Generate Video — 视频生成

调用火山方舟 Seedance 模型生成视频：文生视频、图生视频、多模态参考生视频。

> 前置条件：账户余额 ≥ 200 元或已购买资源包，否则无法开通。

## 前置条件

- `ARK_API_KEY` 已配置（`.env` 文件或环境变量）
- （可选）`DOUBAO_VIDEO_MODEL` 覆盖默认模型

```python
from dotenv import load_dotenv
load_dotenv()

import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.getenv("ARK_API_KEY"))
```

## 工作流程（异步）

视频生成是**异步**的，三步完成：

```
1. POST /v3/contents/generations/tasks    →  获得 task_id
2. GET  /v3/contents/generations/tasks/{id}  →  轮询状态（每 10s）
3. 状态 = succeeded → 从 content.video_url 下载 MP4
```

## API 端点

- **创建任务**：`POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`
- **查询任务**：`GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}`
- **取消任务**：`DELETE https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}`
- **列出任务**：`GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`

## 推荐模型

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

## 提示词技巧

- 格式：**主体 + 动作 + 场景 + 镜头 + 风格**
- 中文 ≤ 500 汉字，英文 ≤ 1000 单词
- 示例：`「一只金毛犬」在「阳光明媚的草原上」「奔跑跳跃」，「慢动作镜头从侧面跟拍」，「电影质感，暖色调」`
- 镜头运镜：推拉摇移、手持跟拍、航拍俯视、一镜到底
- 时长建议：5 秒适合单一动作特写，10-15 秒适合多段叙事或复杂场景

## 使用场景

### 1. 文生视频

```python
import time, requests

model = os.getenv("DOUBAO_VIDEO_MODEL", "doubao-seedance-2-0-260128")

# Step 1: 创建任务
resp = client.content_generation.tasks.create(
    model=model,
    content=[
        {"type": "text", "text": "一只橘猫在樱花树下追蝴蝶，阳光透过花瓣洒落，镜头缓慢推进，电影质感，4K"}
    ],
    ratio="16:9",
    duration=5,
    watermark=False,
)
task_id = resp.id
print(f"任务已创建: {task_id}")

# Step 2: 轮询等待完成（带超时保护）
max_wait = 600  # 最长等待 10 分钟
elapsed = 0
while elapsed < max_wait:
    task = client.content_generation.tasks.get(task_id)
    print(f"状态: {task.status}")
    if task.status == "succeeded":
        print(f"视频 URL: {task.content.video_url}")
        # Step 3: 下载视频
        r = requests.get(task.content.video_url)
        with open("output.mp4", "wb") as f:
            f.write(r.content)
        print("下载完成: output.mp4")
        break
    elif task.status == "failed":
        print(f"任务失败: {task.error}")
        break
    time.sleep(10)
    elapsed += 10
else:
    print(f"任务超时（{max_wait}s），请在控制台查看任务 {task_id}，或调用取消接口。")
```

**cURL（创建任务）**：
```bash
curl https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seedance-2-0-260128",
    "content": [
      {"type": "text", "text": "一只橘猫在樱花树下追蝴蝶，阳光透过花瓣洒落，电影质感"}
    ],
    "ratio": "16:9",
    "duration": 5,
    "watermark": false
  }'
# 返回: {"id": "cgt-xxxxx"}
```

**cURL（查询任务）**：
```bash
curl https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/cgt-xxxxx \
  -H "Authorization: Bearer $ARK_API_KEY"
# 返回包含 status 和 video_url
```

### 2. 图生视频（首帧图）

传入一张图片作为视频起始帧：

```python
resp = client.content_generation.tasks.create(
    model=model,
    content=[
        {"type": "text", "text": "女孩睁开眼，温柔地看向镜头，头发被风吹动"},
        {"type": "image_url", "image_url": {"url": "https://example.com/first_frame.jpg"}}
    ],
    duration=5,
    generate_audio=True,
)
```

### 3. 图生视频（首尾帧）

传入首帧和尾帧，模型生成中间的平滑过渡：

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

### 4. 多模态参考（Seedance 2.0 专属）

同时传入图片、视频、音频作为参考：

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

### 5. 有声视频

```python
resp = client.content_generation.tasks.create(
    model=model,
    content=[...],
    generate_audio=True,      # 音画同生
    duration=5,
)
```

### 6. 使用回调（替代轮询）

```python
resp = client.content_generation.tasks.create(
    model=model,
    content=[...],
    callback_url="https://your-server.com/webhook",  # 任务完成后 POST 通知
    duration=5,
)
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

### content 元素格式

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

### 宽高比与分辨率对照

| 分辨率 | 16:9 | 4:3 | 1:1 | 3:4 | 9:16 | 21:9 |
|--------|------|-----|-----|-----|------|------|
| 480p | 864×480 | 640×480 | 480×480 | 480×640 | — | — |
| 720p | 1280×720 | 960×720 | 960×960 | 720×960 | 720×1280 | 1680×720 |
| 1080p | 1920×1080 | 1440×1080 | 1440×1440 | 1080×1440 | 1080×1920 | 2520×1080 |

### 输入媒体限制

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

## 完整的轮询脚本模板

```python
import os, time, requests
from dotenv import load_dotenv
load_dotenv()

from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.getenv("ARK_API_KEY"))

def generate_video(prompt, image_url=None, duration=5, ratio="16:9"):
    model = os.getenv("DOUBAO_VIDEO_MODEL", "doubao-seedance-2-0-260128")
    content = [{"type": "text", "text": prompt}]
    if image_url:
        content.append({"type": "image_url", "image_url": {"url": image_url}})

    resp = client.content_generation.tasks.create(
        model=model, content=content,
        duration=duration, ratio=ratio, generate_audio=True,
    )
    print(f"任务ID: {resp.id}")

    max_wait = 600  # 最长等待 10 分钟
    elapsed = 0
    while elapsed < max_wait:
        task = client.content_generation.tasks.get(resp.id)
        print(f"状态: {task.status}...")
        if task.status == "succeeded":
            video_url = task.content.video_url
            r = requests.get(video_url)
            filename = f"output_{resp.id}.mp4"
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"下载完成: {filename}")
            return filename
        elif task.status == "failed":
            print(f"失败: {task.error}")
            return None
        time.sleep(10)
        elapsed += 10
    print(f"任务超时（{max_wait}s），请手动查看任务 {resp.id}")
    return None

# 使用
generate_video("一只金毛在草地上奔跑，慢动作，阳光明媚")
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

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 开通失败 | 余额 < 200 元 | 充值或购买资源包 |
| 任务超时 | 超过 48 小时 | 检查 execution_expires_after |
| 含真人人脸被拒 | 2.0 限制 | 使用预置虚拟人像 |
| task_id 过期 | 仅保存 7 天 | 重新创建任务 |
| 请求体过大 | > 64 MB | 压缩图片或减少参考素材 |

→ 如 API 返回未预期的错误，参考父 skill 的"文档验证"章节获取最新文档。

## 参考链接

- Seedance 2.0 API 参考：https://www.volcengine.com/docs/82379/1520757
- SDK 示例教程：https://www.volcengine.com/docs/82379/2298881
- Seedance 2.0 高级教程：https://www.volcengine.com/docs/82379/2291680
- 提示词指南：https://www.volcengine.com/docs/82379/2222480
