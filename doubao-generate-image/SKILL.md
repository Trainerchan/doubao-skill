---
name: doubao-generate-image
description: Use when the user asks to generate, draw, or design images with 豆包/Seedream, mentions 生成图片/画图/文生图/图生图/海报/组图/AI绘画, or wants text-to-image, image-to-image editing, multi-image fusion, or sequential group image generation.
version: 1.0.0
metadata:
  tags: [doubao, seedream, image-generation, text-to-image, volcengine, 文生图, 图生图, 组图, 海报, 图片生成, 限流, 429, URL过期]
---

# Doubao Generate Image — 图片生成

调用火山方舟 Seedream 模型生成图片：文生图、图生图、组图、多图融合。

## Overview

封装 `client.images.generate()` 调用 `/v3/images/generations` 端点。默认模型 `doubao-seedream-5-0-260128`。输出为 URL（24h 有效期）或 base64 JSON。核心原则：写好 prompt 决定质量，生成后立即下载保存，注意限流。

## When to Use

- 用户要求生成/画/设计图片，提到 文生图/图生图/组图/海报/AI 绘画
- 需要参考图编辑（换色、换背景、风格迁移）
- 需要多张参考图融合成一张
- 需要连续生成多张关联图片（组图）

## When NOT to Use

- 图片理解/分析 → 路由到 `doubao-general`
- 生成视频 → 路由到 `doubao-generate-video`
- 非豆包/Seedream 模型 → 退出此技能

## 前置条件

```python
from dotenv import load_dotenv
load_dotenv()

import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.getenv("ARK_API_KEY"))
model = os.getenv("DOUBAO_IMAGE_MODEL", "doubao-seedream-5-0-260128")
```

默认 `doubao-seedream-5-0-260128`（2K/3K/4K，组图，联网搜索）。旧版可用 `doubao-seedream-4-5-251128`、`doubao-seedream-4-0-250828`。

## 使用场景

### 1. 文生图（文字描述 → 图片）

```python
result = client.images.generate(
    model=model,
    prompt="一只可爱的橘猫坐在窗台上，窗外是夕阳，室内温馨，柔和的暖光，写实风格",
    size="2K",
    watermark=False,
)
print(result.data[0].url)  # URL 24小时有效，请及时下载
```

### 2. 图生图（参考图 + 文字 → 编辑/变换）

```python
result = client.images.generate(
    model=model,
    prompt="保持模特姿势，将服装颜色从红色改为蓝色",
    image="https://example.com/fashion.jpg",
    size="2K",
)
```

### 3. 多图融合（多张参考图 → 一张）

```python
result = client.images.generate(
    model=model,
    prompt="将图1的服装款式应用到图2的模特身上",
    image=["https://example.com/clothes.jpg", "https://example.com/model.jpg"],
    sequential_image_generation="disabled",
    size="2K",
)
```

### 4. 组图生成（多张关联图片）

```python
from volcenginesdkarkruntime.types.images.images import SequentialImageGenerationOptions

result = client.images.generate(
    model=model,
    prompt="生成一组4张电影级科幻风格影视分镜：外星飞船降临城市的四个关键时刻",
    size="2K",
    sequential_image_generation="auto",
    sequential_image_generation_options=SequentialImageGenerationOptions(max_images=4),
)
for i, img in enumerate(result.data):
    print(f"图{i+1}: {img.url}")
```

## 提示词技巧

格式：**主体 + 行为 + 环境 + 风格/色彩/光影**

> 「一位穿汉服的少女」站在「开满桃花的庭院」中，「春日午后柔和的阳光透过花瓣洒落」，「工笔画风格，淡雅色调」

中文 ≤ 300 汉字，英文 ≤ 600 单词。

> URL 有效期仅 **24 小时**，请及时下载保存！

流式组图、Base64 输出、联网搜索生图、完整参数表、尺寸矩阵等参见 [REFERENCE.md](REFERENCE.md)。

## Common Mistakes

| 错误 | 后果 | 正确做法 |
|------|------|----------|
| 生成后只保留 URL 不下载 | 24h 后 URL 失效，图片丢失 | 生成后立即 `requests.get(url)` 保存到本地 |
| 短时间内大量连续请求 | 触发 429 限流 | 限制 ≤ 500 张/分钟，使用指数退避重试 |
| prompt 过长（中文 > 300 字） | 部分内容被截断忽略 | 中文 ≤ 300 汉字，英文 ≤ 600 单词 |
| `sequential_image_generation` 未设 `max_images` | 生成数量不可控 | 设置 `SequentialImageGenerationOptions(max_images=N)` |
| 图生图传本地路径 | 模型无法访问 | 使用可访问的 URL 或 base64 编码 |
| 多图融合传入超过 14 张参考图 | API 拒绝请求 | 限制 ≤ 14 张 |
