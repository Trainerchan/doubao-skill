---
name: doubao-skill
description: Doubao (豆包) / Volcengine Ark models — chat, vision, document understanding, image generation (Seedream), video generation (Seedance). Use when the user mentions 豆包, 火山方舟, Volcengine Ark, or wants to generate images/videos with domestic Chinese AI models. Load this first; it routes to the appropriate sub-skill.
version: 1.0.0
author: Trainerchan
license: MIT
metadata:
  tags: [doubao, volcengine, ark, seed, seedream, seedance, multimodal, image-generation, video-generation, bytedance]
---

# Doubao Skill (豆包技能集)

火山方舟(Volcengine Ark)豆包大模型调用技能集，提供三个子技能。

## 子技能速览

| Skill | 能力 | 触发场景 |
|-------|------|----------|
| `doubao-general` | 对话、多模态理解 | 聊天、图片/文档/视频/音频分析 |
| `doubao-generate-image` | Seedream 图片生成 | 文生图、图生图、组图、海报 |
| `doubao-generate-video` | Seedance 视频生成 | 文生视频、图生视频、多模态参考 |

## 路由决策

| 用户意图 | 加载子 skill |
|----------|-------------|
| 对话、分析图片/文档/视频/音频、函数调用 | → [doubao-general](general/SKILL.md) |
| 生成图片、画图、文生图、图生图、海报、组图 | → [doubao-generate-image](generate-image/SKILL.md) |
| 生成视频、文生视频、图生视频、视频编辑 | → [doubao-generate-video](generate-video/SKILL.md) |

## 快速开始

```bash
# 1. 安装 SDK
pip install volcengine-python-sdk python-dotenv

# 2. 在项目根目录 .env 中配置 API Key
# ARK_API_KEY=your-key-here
```

```python
from dotenv import load_dotenv
load_dotenv()
import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.getenv("ARK_API_KEY"))
```

各子 skill 完全自包含，可直接按需加载。

## 公共约定

- **Base URL**: `https://ark.cn-beijing.volces.com/api/v3`
- **Auth**: `Authorization: Bearer $ARK_API_KEY`
- **Content-Type**: `application/json`
- 统一使用 `volcenginesdkarkruntime.Ark` 客户端

详细配置、安装步骤、Agent 集成方式、错误处理参见 [REFERENCE.md](REFERENCE.md)。
