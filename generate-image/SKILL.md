---
name: doubao-generate-image
description: Doubao (豆包) Seedream image generation — text-to-image, image-to-image, multi-image fusion, group/sequential images. Use when the user asks to generate, draw, or design images, 生成图片, 画图, 文生图, 图生图, 海报, 组图.
version: 1.0.0
metadata:
  tags: [doubao, seedream, image-generation, text-to-image, volcengine]
---

# Doubao Generate Image — 图片生成

调用火山方舟 Seedream 模型生成图片：文生图、图生图、组图、多图融合。

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
