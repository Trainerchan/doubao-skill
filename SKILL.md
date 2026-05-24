---
name: doubao-skill
description: Use when calling Doubao (豆包) / Volcengine Ark models — chat, vision, document understanding, image generation (Seedream), or video generation (Seedance). Load this first; it routes to the appropriate sub-skill.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [doubao, volcengine, ark, seed, seedream, seedance, multimodal, image-generation, video-generation, bytedance]
    related_skills: [doubao-general, doubao-generate-image, doubao-generate-video]
---

# Doubao Skill (豆包技能集)

火山方舟(Volcengine Ark)豆包大模型调用技能集。提供三个子技能，覆盖通用对话/多模态理解、图片生成、视频生成。

## 架构

### 源码（E:\doubao-skill\）

```
doubao-skill/
├── SKILL.md               ← 本文件：配置说明 + 子技能导航
├── .env.example           ← 环境变量模板
├── general/SKILL.md       ← 通用对话/多模态
├── generate-image/SKILL.md ← 图片生成 (Seedream)
├── generate-video/SKILL.md ← 视频生成 (Seedance)
└── references/            ← 详细 API 参数参考
    ├── chat-api.md
    ├── image-api.md
    └── video-api.md
```

### Hermes Agent 集成

三个子技能已注册为**独立 skill**，在 Hermes 中可直接加载：

| 方式 | 命令 |
|------|------|
| 总入口 | `skill_view("doubao-skill")` |
| 通用对话 | `skill_view("doubao-general")` |
| 图片生成 | `skill_view("doubao-generate-image")` |
| 视频生成 | `skill_view("doubao-generate-video")` |

Hermes 技能文件位于 `~/.hermes/skills/doubao-skill/`、`doubao-general/`、`doubao-generate-image/`、`doubao-generate-video/`。

## 前置配置（所有子技能共用）

### 1. 获取 API Key

1. 访问 [API Key 管理](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)
2. 点击「创建 API Key」，输入名称后确认
3. 复制生成的 Key（注意：仅显示一次！）

### 2. 配置环境变量

必须设置环境变量 `ARK_API_KEY`：

```bash
export ARK_API_KEY="your-api-key-here"
```

或在项目根目录的 `.env` 文件中：

```
ARK_API_KEY=your-api-key-here
```

> ⚠️ **安全提醒**：严禁将 API Key 硬编码到代码中。必须通过环境变量或 `.env` 文件管理。API Key 泄露会导致配额被盗用，产生额外费用。

### 3. 可选：按子技能配置不同模型

每个子技能可通过独立环境变量覆盖默认模型：

| 变量 | 用途 | 默认值 |
|------|------|--------|
| `ARK_API_KEY` | 鉴权 Key（必填） | — |
| `DOUBAO_CHAT_MODEL` | 通用对话模型 | `doubao-seed-2-0-lite-260428` |
| `DOUBAO_IMAGE_MODEL` | 图片生成模型 | `doubao-seedream-5-0-260128` |
| `DOUBAO_VIDEO_MODEL` | 视频生成模型 | `doubao-seedance-2-0-260128` |

### 4. 安装 SDK

不同子技能依赖不同 SDK：

| 子技能 | SDK | 安装命令 |
|--------|-----|----------|
| general（Chat API） | `openai` | `pip install openai` |
| generate-image | `volcengine-python-sdk` | `pip install volcengine-python-sdk` |
| generate-video | `volcengine-python-sdk` | `pip install volcengine-python-sdk` |

> ARK Chat API 兼容 OpenAI 格式，直接用 `openai` SDK 更轻量。图片/视频生成需要用 `volcenginesdkarkruntime`。

## 子技能导航

### 1. general — 通用对话 & 多模态

**触发条件**：对话、文本生成、图片理解、视频理解、文档理解（PDF/PPTX/XLSX）、音频理解、函数调用

**使用模型**：`doubao-seed-2-0-lite/pro/mini` 系列

**核心能力**：
- 文本对话（含深度思考模式）
- 图片理解/识别（传入图片 URL 或 Base64）
- 文档理解（PDF、PPTX、XLSX 等）
- 视频理解（抽帧分析）
- 音频理解（mp3/wav 等）
- 函数调用 / 工具调用

→ 源码：[general/SKILL.md](general/SKILL.md)　|　Hermes：`skill_view("doubao-general")`

### 2. generate-image — 图片生成

**触发条件**：生成图片、文生图、图生图、组图、海报设计

**使用模型**：`doubao-seedream-5-0-260128`（推荐）、`doubao-seedream-4-5-251128`、`doubao-seedream-4-0-250828`

**核心能力**：
- 文生图（文本描述 → 单图/组图）
- 图生图（参考图 + 文本 → 编辑/变换）
- 多图融合
- 组图生成（连环画、分镜等，最多 15 张）
- 2K/3K/4K 分辨率
- 支持流式输出

→ 源码：[generate-image/SKILL.md](generate-image/SKILL.md)　|　Hermes：`skill_view("doubao-generate-image")`

### 3. generate-video — 视频生成

**触发条件**：生成视频、文生视频、图生视频、视频编辑

**使用模型**：`doubao-seedance-2-0-260128`（推荐，有声/无声）

**核心能力**：
- 文生视频
- 图生视频（首帧/首尾帧）
- 多模态参考生视频（图片+视频+音频+文本）
- 音画同生
- 异步任务模式（提交 → 轮询 → 下载）

> ⚠️ 前置条件：账户余额 ≥ 200 元或已购买资源包

→ 源码：[generate-video/SKILL.md](generate-video/SKILL.md)　|　Hermes：`skill_view("doubao-generate-video")`

## 公共约定

1. **Base URL**：`https://ark.cn-beijing.volces.com/api/v3`
2. **鉴权 Header**：`Authorization: Bearer $ARK_API_KEY`
3. **Content-Type**：`application/json`
4. **API Key 作用域**：仅限创建时的项目空间，不支持跨项目访问
5. **错误码参考**：https://www.volcengine.com/docs/82379/1299023
6. **模型列表**：https://www.volcengine.com/docs/82379/1330310
7. **价格参考**：https://www.volcengine.com/docs/82379/1544106

## 快速测试

```bash
# 测试通用对话
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"doubao-seed-2-0-lite-260428","messages":[{"role":"user","content":"你好"}]}'

# 测试图片生成
curl https://ark.cn-beijing.volces.com/api/v3/images/generations \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"doubao-seedream-5-0-260128","prompt":"一只可爱的橘猫坐在窗台看夕阳","size":"2K"}'
```
