---
name: doubao-generate-image
description: Doubao image generation using Seedream — text-to-image, image-to-image, multi-image fusion, group images. Use when the user asks to generate, draw, or design images.
version: 1.0.0
metadata:
  tags: [doubao, seedream, image-generation, text-to-image, volcengine]
---

# Doubao Generate Image — 图片生成

调用火山方舟 Seedream 模型生成图片：文生图、图生图、组图、多图融合。

## 前置条件

- `ARK_API_KEY` 已配置（`.env` 文件或环境变量）
- （可选）`DOUBAO_IMAGE_MODEL` 覆盖默认模型

```python
from dotenv import load_dotenv
load_dotenv()

import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.getenv("ARK_API_KEY"))
```

## API 端点

`POST https://ark.cn-beijing.volces.com/api/v3/images/generations`

## 推荐模型

| 模型 ID | 分辨率 | 组图 | 联网搜索 | 输出格式 |
|---------|--------|------|----------|----------|
| `doubao-seedream-5-0-260128` ⭐默认 | 2K/3K/4K | ✓ | ✓ | png/jpeg |
| `doubao-seedream-4-5-251128` | 2K/4K | ✓ | ✗ | jpeg |
| `doubao-seedream-4-0-250828` | 1K/2K/4K | ✓ | ✗ | jpeg |

> 限流：500 张/分钟 (IPM)

## 使用场景

### 1. 文生图（文字描述 → 图片）

```python
model = os.getenv("DOUBAO_IMAGE_MODEL", "doubao-seedream-5-0-260128")

result = client.images.generate(
    model=model,
    prompt="一只可爱的橘猫坐在窗台上，窗外是夕阳，室内温馨，柔和的暖光，写实风格",
    size="2K",
    watermark=False,
)
print(result.data[0].url)  # URL 24小时有效，请及时下载
```

**cURL**：
```bash
curl https://ark.cn-beijing.volces.com/api/v3/images/generations \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seedream-5-0-260128",
    "prompt": "一只可爱的橘猫坐在窗台上，窗外是夕阳，写实风格",
    "size": "2K",
    "watermark": false
  }'
```

### 2. 图生图（参考图 + 文字 → 编辑/变换）

```python
result = client.images.generate(
    model=model,
    prompt="保持模特姿势，将服装颜色从红色改为蓝色",
    image="https://example.com/fashion.jpg",  # 单张参考图
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

生成一系列连贯的图片（如漫画分镜、产品系列图）：

```python
from volcenginesdkarkruntime.types.images.images import SequentialImageGenerationOptions

result = client.images.generate(
    model=model,
    prompt="生成一组4张电影级科幻风格影视分镜：外星飞船降临城市的四个关键时刻",
    size="2K",
    sequential_image_generation="auto",
    sequential_image_generation_options=SequentialImageGenerationOptions(max_images=4),
)
# result.data 包含多张图片
for i, img in enumerate(result.data):
    print(f"图{i+1}: {img.url}")
```

### 5. 流式组图

设置 `stream=True` 逐个获取图片：

```python
stream = client.images.generate(
    model=model,
    prompt="生成不同风格的3张猫咪插画",
    size="2K",
    sequential_image_generation="auto",
    sequential_image_generation_options=SequentialImageGenerationOptions(max_images=3),
    stream=True,
)

for event in stream:
    if event is None:
        continue
    if event.type == "image_generation.partial_succeeded":
        print(f"生成完成: {event.url}")
    elif event.type == "image_generation.completed":
        print(f"全部完成，用量: {event.usage}")
```

**流式事件类型**：

| 事件 | 说明 |
|------|------|
| `image_generation.partial_succeeded` | 单张图片生成成功 |
| `image_generation.partial_failed` | 单张图片生成失败 |
| `image_generation.partial_image` | 流式传输中的 b64_json chunk |
| `image_generation.completed` | 全部完成 |

### 6. 联网搜索生图（仅 5.0）

模型自动搜索网络信息辅助生成更准确的图片：

```python
result = client.images.generate(
    model=model,
    prompt="制作一张上海未来5日天气预报图",
    tools=[{"type": "web_search"}],
    size="2048x2048",
)
```

### 7. Base64 返回格式

```python
result = client.images.generate(
    model=model,
    prompt="极简风格logo设计",
    response_format="b64_json",
)
import base64
img_bytes = base64.b64decode(result.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(img_bytes)
```

## 参数速查

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `model` | string | — | 模型 ID（必填） |
| `prompt` | string | — | 提示词（必填），中文≤300字/英文≤600词 |
| `image` | str/arr | — | 参考图 URL 或 Base64 数组，最多 14 张 |
| `size` | string | 2048x2048 | 分辨率预设(2K/3K/4K)或像素值(如"1024x1024") |
| `response_format` | string | url | `url`(24h有效) 或 `b64_json` |
| `watermark` | bool | true | 是否添加"AI生成"水印 |
| `output_format` | string | jpeg | `png` 或 `jpeg`（仅 5.0 可选） |
| `sequential_image_generation` | string | disabled | `auto`(组图) / `disabled`(单图) |
| `sequential_image_generation_options.max_images` | int | 15 | 组图最大张数 [1,15] |
| `stream` | bool | false | 流式输出 |
| `tools` | array | — | 5.0：[`{"type":"web_search"}`] |
| `optimize_prompt_options.mode` | string | — | `standard`(高质量) / `fast`(快速，仅4.0) |
| `seed` | int | — | 随机种子，用于可复现生成 |

> 不支持：`guidance_scale`（5.0/4.5/4.0）、`n`（旧版）

### 自定义尺寸限制

| 模型 | 最小总像素 | 最大总像素 | 宽高比 |
|------|-----------|-----------|--------|
| 5.0 | 3,686,400 | 16,777,216 | [1/16, 16] |
| 4.5 | 3,686,400 | 16,777,216 | [1/16, 16] |
| 4.0 | 921,600 | 16,777,216 | [1/16, 16] |

### 推荐尺寸速查

| 宽高比 | 2K | 3K | 4K |
|--------|----|----|----|
| **1:1** | 2048×2048 | 3072×3072 | 4096×4096 |
| **4:3** | 2304×1728 | 3456×2592 | 4704×3520 |
| **3:4** | 1728×2304 | 2592×3456 | 3520×4704 |
| **16:9** | 2848×1600 | 4096×2304 | 5504×3040 |
| **9:16** | 1600×2848 | 2304×4096 | 3040×5504 |
| **3:2** | 2496×1664 | 3744×2496 | 4992×3328 |
| **2:3** | 1664×2496 | 2496×3744 | 3328×4992 |
| **21:9** | 3136×1344 | 4704×2016 | 6240×2656 |

### 图片输入限制

- 格式：jpeg, png, webp, bmp, tiff, gif, heic, heif
- 单张 ≤ 30 MB
- 总像素 ≤ 6000×6000 (3600万)
- 宽高比 [1/16, 16]
- 最小边长 > 14 px

## 提示词技巧

- 格式：**主体 + 行为 + 环境 + 风格/色彩/光影**
- 中文 ≤ 300 汉字，英文 ≤ 600 单词
- 示例：`「一位穿汉服的少女」站在「开满桃花的庭院」中，「春日午后柔和的阳光透过花瓣洒落」，「工笔画风格，淡雅色调」`

## 响应格式

```json
{
  "model": "doubao-seedream-5-0-260128",
  "created": 1716000000,
  "data": [
    {"url": "https://...", "size": "2048x2048"}
  ],
  "usage": {"generated_images": 1}
}
```

> URL 有效期仅 **24 小时**，请及时下载保存！

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 图片 URL 过期 | 超过 24 小时 | 重新生成 |
| `guidance_scale` 报错 | 5.0/4.5/4.0 不支持 | 去掉该参数 |
| 自定义尺寸无效 | 不满足总像素/宽高比限制 | 使用预设或查表选值 |
| 总图片数超限 | 参考图 + 生成 > 15 | 减少参考图或生成数 |

→ 如 API 返回未预期的错误，参考父 skill 的"文档验证"章节获取最新文档。

## 参考链接

- 完整 API 参考：https://www.volcengine.com/docs/82379/1541523
- 示例教程：https://www.volcengine.com/docs/82379/1824121
- 提示词指南：https://www.volcengine.com/docs/82379/1829186
