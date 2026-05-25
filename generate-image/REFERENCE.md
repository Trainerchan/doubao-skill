# Doubao Generate Image — 参考手册

## 模型速查

| 模型 ID | 分辨率 | 组图 | 联网搜索 | 输出格式 |
|---------|--------|------|----------|----------|
| `doubao-seedream-5-0-260128` ⭐默认 | 2K/3K/4K | ✓ | ✓ | png/jpeg |
| `doubao-seedream-4-5-251128` | 2K/4K | ✓ | ✗ | jpeg |
| `doubao-seedream-4-0-250828` | 1K/2K/4K | ✓ | ✗ | jpeg |

> 限流：500 张/分钟 (IPM)

## 扩展场景

### 流式组图

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

### 联网搜索生图（仅 5.0）

```python
result = client.images.generate(
    model=model,
    prompt="制作一张上海未来5日天气预报图",
    tools=[{"type": "web_search"}],
    size="2048x2048",
)
```

### Base64 返回格式

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

## 自定义尺寸限制

| 模型 | 最小总像素 | 最大总像素 | 宽高比 |
|------|-----------|-----------|--------|
| 5.0 | 3,686,400 | 16,777,216 | [1/16, 16] |
| 4.5 | 3,686,400 | 16,777,216 | [1/16, 16] |
| 4.0 | 921,600 | 16,777,216 | [1/16, 16] |

## 推荐尺寸速查

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

## 图片输入限制

- 格式：jpeg, png, webp, bmp, tiff, gif, heic, heif
- 单张 ≤ 30 MB
- 总像素 ≤ 6000×6000 (3600万)
- 宽高比 [1/16, 16]
- 最小边长 > 14 px

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

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 图片 URL 过期 | 超过 24 小时 | 重新生成 |
| `guidance_scale` 报错 | 5.0/4.5/4.0 不支持 | 去掉该参数 |
| 自定义尺寸无效 | 不满足总像素/宽高比限制 | 使用预设或查表选值 |
| 总图片数超限 | 参考图 + 生成 > 15 | 减少参考图或生成数 |

## 参考链接

- 完整 API 参考：https://www.volcengine.com/docs/82379/1541523
- 示例教程：https://www.volcengine.com/docs/82379/1824121
- 提示词指南：https://www.volcengine.com/docs/82379/1829186
