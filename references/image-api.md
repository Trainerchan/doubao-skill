# Image Generation API 完整参考

> 来源：https://www.volcengine.com/docs/82379/1541523
> 更新时间：2026-05

## 端点

```
POST https://ark.cn-beijing.volces.com/api/v3/images/generations
```

鉴权：`Authorization: Bearer $ARK_API_KEY`

## 完整请求参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `model` | string | ✓ | — | 模型 ID 或 Endpoint ID |
| `prompt` | string | ✓ | — | 提示词，中文≤300字/英文≤600词 |
| `image` | str/arr | | — | 参考图 URL 或 Base64，最多14张 |
| `size` | string | | 2048x2048 | 预设(2K/3K/4K)或自定义像素 |
| `response_format` | string | | url | url / b64_json |
| `watermark` | bool | | true | 是否添加"AI生成"水印 |
| `output_format` | string | | jpeg | png / jpeg（仅 5.0 lite） |
| `sequential_image_generation` | string | | disabled | auto / disabled |
| `sequential_image_generation_options` | object | | — | max_images: [1,15] |
| `stream` | bool | | false | 流式输出 |
| `tools` | array | | — | 仅 5.0 lite：[{"type":"web_search"}] |
| `optimize_prompt_options` | object | | — | mode: standard / fast（仅4.0）|
| `seed` | int | | — | 随机种子，可复现 |

> 不支持：`guidance_scale`（5.0/4.5/4.0）、`n`（旧版）

## size 参数详细限制

### 预设方式

| 模型 | 支持预设 | 默认 |
|------|---------|------|
| 5.0 lite | 2K, 3K, 4K | 2048x2048 |
| 4.5 | 2K, 4K | 2048x2048 |
| 4.0 | 1K, 2K, 4K | 2048x2048 |

### 自定义像素

| 模型 | 最小总像素 | 最大总像素 | 宽高比 |
|------|-----------|-----------|--------|
| 5.0 lite | 3,686,400 | 16,777,216 | [1/16, 16] |
| 4.5 | 3,686,400 | 16,777,216 | [1/16, 16] |
| 4.0 | 921,600 | 16,777,216 | [1/16, 16] |

## 完整尺寸表

### 2K

| 宽高比 | 像素 |
|--------|------|
| 1:1 | 2048×2048 |
| 4:3 | 2304×1728 |
| 3:4 | 1728×2304 |
| 16:9 | 2848×1600 |
| 9:16 | 1600×2848 |
| 3:2 | 2496×1664 |
| 2:3 | 1664×2496 |
| 21:9 | 3136×1344 |

### 3K（仅 5.0 lite）

| 宽高比 | 像素 |
|--------|------|
| 1:1 | 3072×3072 |
| 4:3 | 3456×2592 |
| 3:4 | 2592×3456 |
| 16:9 | 4096×2304 |
| 9:16 | 2304×4096 |
| 2:3 | 2496×3744 |
| 3:2 | 3744×2496 |
| 21:9 | 4704×2016 |

### 4K

| 宽高比 | 像素 |
|--------|------|
| 1:1 | 4096×4096 |
| 4:3 | 4704×3520 |
| 3:4 | 3520×4704 |
| 16:9 | 5504×3040 |
| 9:16 | 3040×5504 |
| 2:3 | 3328×4992 |
| 3:2 | 4992×3328 |
| 21:9 | 6240×2656 |

## 响应格式（非流式）

```json
{
  "model": "doubao-seedream-5-0-260128",
  "created": 1716000000,
  "data": [
    {
      "url": "https://...",          // response_format=url（24h有效）
      "b64_json": "...",             // response_format=b64_json
      "size": "2048x2048"            // 仅 5.0/4.5/4.0
    }
  ],
  "tools": [{"type": "web_search"}], // 工具配置
  "usage": {
    "generated_images": 1,           // 计费依据
    "tool_usage": {"web_search": 3}  // 联网搜索次数
  }
}
```

## 流式事件类型

| 事件 | 说明 |
|------|------|
| `image_generation.partial_succeeded` | 单张图片生成成功 |
| `image_generation.partial_failed` | 单张图片生成失败 |
| `image_generation.partial_image` | 流式传输中的 b64_json chunk |
| `image_generation.completed` | 全部完成 |
