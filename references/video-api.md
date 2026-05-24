# Video Generation API 完整参考

> 来源：https://www.volcengine.com/docs/82379/1520757
> 更新时间：2026-05

## 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v3/contents/generations/tasks` | 创建视频生成任务 |
| GET | `/v3/contents/generations/tasks/{id}` | 查询任务状态/结果 |
| DELETE | `/v3/contents/generations/tasks/{id}` | 取消任务 |
| GET | `/v3/contents/generations/tasks` | 列出任务 |

Base URL: `https://ark.cn-beijing.volces.com/api/v3`

鉴权：`Authorization: Bearer $ARK_API_KEY`

## 模型能力矩阵

| 能力 | 2.0 | 1.5 pro | 1.0 pro | 1.0 pro fast |
|------|-----|---------|---------|--------------|
| 文生视频 | ✓ | ✓ | ✓ | ✓ |
| 图生视频-首帧 | ✓ | ✓ | ✓ | ✓ |
| 图生视频-首尾帧 | ✓ | ✓ | ✓ | ✗ |
| 多模态参考（图+视+音） | ✓ | ✗ | ✗ | ✗ |
| 音画同生 | ✓ | ✓ | ✗ | ✗ |
| 联网搜索 | ✓ | ✗ | ✗ | ✗ |
| 样片模式(draft) | ✗ | ✓ | ✗ | ✗ |
| flex 离线推理 | ✗ | 部分 | 部分 | ✗ |

## 创建任务请求参数（完整）

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `model` | string | ✓ | — | 模型 ID |
| `content` | array | ✓ | — | 输入内容（text/image_url/video_url/audio_url） |
| `duration` | int | | 5 | 时长秒数，2.0/1.5pro: [4,15]或-1；1.0: [2,12] |
| `ratio` | string | | adaptive | 16:9/4:3/1:1/3:4/9:16/21:9/adaptive |
| `resolution` | string | | 720p/1080p | 480p/720p/1080p（2.0 fast 不支持1080p） |
| `generate_audio` | bool | | true | 是否音画同生（2.0/1.5pro） |
| `watermark` | bool | | false | AI生成水印 |
| `seed` | int | | -1 | [-1, 2³²-1] |
| `camera_fixed` | bool | | false | 固定摄像头（2.0暂不支持） |
| `callback_url` | string | | — | 完成回调 POST |
| `return_last_frame` | bool | | false | 返回尾帧 PNG |
| `execution_expires_after` | int | | 172800 | 超时秒数 [3600,259200] |
| `service_tier` | string | | default | default/flex（2.0不支持flex） |
| `priority` | int | | 0 | [0,9]，仅 2.0 |
| `safety_identifier` | string | | — | 用户标识 ≤64，安全监控 |
| `tools` | array | | — | 仅 2.0：[{"type":"web_search"}] |
| `draft` | bool | | false | 样片模式，仅 1.5 pro |

## content 元素完整参考

### text

```json
{"type": "text", "text": "提示词，中文≤500字，英文≤1000词"}
```

### image_url

```json
{
  "type": "image_url",
  "image_url": {
    "url": "https://... 或 data:image/...;base64,... 或 asset://<ASSET_ID>"
  },
  "role": "first_frame"        // first_frame | last_frame | reference_image
}
```

图片限制：
- 格式：jpeg/png/webp/bmp/tiff/gif（2.0/1.5pro增 heic/heif）
- 单张 ≤ 30 MB
- 宽高比 [0.4, 2.5]，宽/高 [300, 6000]
- 2.0 不支持含真人人脸的参考图

### video_url（仅 2.0）

```json
{
  "type": "video_url",
  "video_url": {"url": "https://... 或 asset://<ASSET_ID>"},
  "role": "reference_video"    // 必填
}
```

视频限制：
- 格式：mp4/mov（H.264/H.265；AAC/MP3 音频）
- 分辨率：480p/720p/1080p
- 时长：2-15s/个，最多3个，总≤15s
- 尺寸：宽高比 [0.4,2.5]，像素 [300,6000]，总像素 [409600, 2086876]
- 单文件 ≤ 50 MB，帧率 [24,60] fps

### audio_url（仅 2.0）

```json
{
  "type": "audio_url",
  "audio_url": {"url": "https://... 或 data:audio/...;base64,... 或 asset://<ASSET_ID>"},
  "role": "reference_audio"    // 必填
}
```

音频限制：
- 格式：wav/mp3
- 时长：2-15s/段，最多3段，总≤15s
- 单文件 ≤ 15 MB
- 不能单独输入，必须至少含1个图片或视频

## 查询任务响应

```json
{
  "id": "cgt-xxxxxxxxxx",
  "model": "doubao-seedance-2-0-260128",
  "status": "succeeded",            // queued | running | succeeded | failed | cancelled
  "content": {
    "video_url": "https://...",     // MP4 下载地址
    "video_url_expires_at": 1716000000,
    "last_frame_url": "https://..." // 仅 return_last_frame=true
  },
  "usage": {
    "input_tokens": 100,
    "output_tokens": 200,
    "generated_videos": 1
  },
  "error": {                        // 仅失败时
    "code": "xxx",
    "message": "..."
  },
  "created_at": 1716000000,
  "updated_at": 1716000120,
  "submitted_at": 1716000005,
  "completed_at": 1716000120
}
```

## 宽高比 × 分辨率 像素对照

| 分辨率 | 16:9 | 4:3 | 1:1 | 3:4 | 9:16 | 21:9 |
|--------|------|-----|-----|-----|------|------|
| 480p | 864×480 | 640×480 | 480×480 | 480×640 | — | — |
| 720p | 1280×720 | 960×720 | 960×960 | 720×960 | 720×1280 | 1680×720 |
| 1080p | 1920×1080 | 1440×1080 | 1440×1440 | 1080×1440 | 1080×1920 | 2520×1080 |
