---
name: doubao-generate-video
description: Doubao (豆包) Seedance video generation — text-to-video, image-to-video, multimodal reference (image+video+audio). Use when the user asks to generate, create, or edit videos, 生成视频, 文生视频, 图生视频, 视频编辑. Async workflow: create task → poll → download.
version: 1.0.0
metadata:
  tags: [doubao, seedance, video-generation, text-to-video, volcengine]
---

# Doubao Generate Video — 视频生成

调用火山方舟 Seedance 模型生成视频：文生视频、图生视频、多模态参考。

> 前置条件：账户余额 ≥ 200 元或已购买资源包。

## 前置条件

```python
from dotenv import load_dotenv
load_dotenv()

import os, time, requests
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.getenv("ARK_API_KEY"))
model = os.getenv("DOUBAO_VIDEO_MODEL", "doubao-seedance-2-0-260128")
```

默认 `doubao-seedance-2-0-260128`（最强：多模态参考、音画同生、首尾帧、联网搜索）。

## 工作流程（异步三步）

```
1. POST 创建任务 → 获得 task_id
2. GET  轮询状态（建议每 10s） → queued → running → succeeded/failed
3. 状态 = succeeded → 从 content.video_url 下载 MP4
```

## 使用场景

### 1. 文生视频

```python
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

# Step 2 & 3: 轮询 + 下载
max_wait = 600
elapsed = 0
while elapsed < max_wait:
    task = client.content_generation.tasks.get(task_id)
    print(f"状态: {task.status}")
    if task.status == "succeeded":
        r = requests.get(task.content.video_url)
        with open("output.mp4", "wb") as f:
            f.write(r.content)
        print("下载完成: output.mp4")
        break
    elif task.status == "failed":
        print(f"失败: {task.error}")
        break
    time.sleep(10)
    elapsed += 10
```

> 完整轮询模板脚本见 [scripts/poll_video.py](scripts/poll_video.py)。

### 2. 图生视频（首帧图）

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

## 提示词技巧

格式：**主体 + 动作 + 场景 + 镜头 + 风格**

> 「一只金毛犬」在「阳光明媚的草原上」「奔跑跳跃」，「慢动作镜头从侧面跟拍」，「电影质感，暖色调」

中文 ≤ 500 汉字，英文 ≤ 1000 单词。5 秒适合单一动作特写，10-15 秒适合多段叙事。

首尾帧、多模态参考、有声视频、回调、完整参数表、分辨率矩阵等参见 [REFERENCE.md](REFERENCE.md)。
