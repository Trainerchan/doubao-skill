---
name: doubao-skill
description: Use when the user mentions 豆包, 火山方舟, Volcengine Ark, 字节跳动大模型, or wants to use domestic Chinese AI models for chat, image generation (Seedream), or video generation (Seedance). Also triggers on 文生图/图生图/组图/海报, 文生视频/图生视频, or any multimodal understanding task involving 豆包.
version: 1.0.0
author: Trainerchan
license: MIT
metadata:
  tags: [doubao, volcengine, ark, seed, seedream, seedance, multimodal, image-generation, video-generation, bytedance, 豆包, 火山方舟, 文生图, 图生图, 文生视频, 图生视频, 限流, 429, 503]
---

# Doubao Skill (豆包技能集)

火山方舟(Volcengine Ark)豆包大模型调用技能集，统一封装对话、图片生成、视频生成三类 API。

## Overview

这是一个 **Reference 类型技能**，通过 frontmatter description 被 Agent 自动发现。它本身不包含 API 调用细节，而是根据用户意图路由到三个自包含的子技能。每个子技能独立可用，包含完整的代码示例和参数说明。

## 子技能速览

| Skill | 能力 | 触发场景 |
|-------|------|----------|
| `doubao-general` | 对话、多模态理解 | 聊天、图片/文档/视频/音频分析 |
| `doubao-generate-image` | Seedream 图片生成 | 文生图、图生图、组图、海报 |
| `doubao-generate-video` | Seedance 视频生成 | 文生视频、图生视频、多模态参考 |

## 路由决策

| 用户意图 | 加载子 skill |
|----------|-------------|
| 对话、分析图片/文档/视频/音频、函数调用 | → [doubao-general](doubao-general/SKILL.md) |
| 生成图片、画图、文生图、图生图、海报、组图 | → [doubao-generate-image](doubao-generate-image/SKILL.md) |
| 生成视频、文生视频、图生视频、视频编辑 | → [doubao-generate-video](doubao-generate-video/SKILL.md) |

各子 skill 完全自包含，可直接按需加载。安装和配置详见 [REFERENCE.md](REFERENCE.md)。

## When NOT to Use

- 用户要求使用 OpenAI / Claude / Gemini 等其他厂商模型 → 不应加载此技能
- 用户仅做代码编写、Git 操作等通用编程任务，未提及豆包/火山方舟 → 不属于此技能范围
- 用户需要训练或微调模型 → 火山方舟有单独的微调 API，不在本技能覆盖范围内

## 公共约定

- **Base URL**: `https://ark.cn-beijing.volces.com/api/v3`
- **Auth**: `Authorization: Bearer $ARK_API_KEY`
- **Content-Type**: `application/json`
- 统一使用 `volcenginesdkarkruntime.Ark` 客户端

详细配置、安装步骤、Agent 集成方式、错误处理参见 [REFERENCE.md](REFERENCE.md)。

## Common Mistakes

| 错误 | 后果 | 正确做法 |
|------|------|----------|
| 硬编码 API Key 到代码中 | 泄露密钥 | 始终通过环境变量或 `.env` 文件读取 |
| 直接使用 URL 而不下载图片/视频 | URL 24h 后失效，数据丢失 | 生成后立即 `requests.get(url)` 保存到本地 |
| 视频生成后不检查状态直接等结果 | 任务可能失败或排队超时 | 必须轮询 `task.status`，检查 `succeeded`/`failed` |
| 忘记 `frequency_penalty` 等参数不支持 | 请求返回参数错误 | general 子技能不支持 `frequency_penalty` 和 `presence_penalty` |
| 余额不足时直接调用视频生成 | 立即失败 | 确认账户余额 ≥ 200 CNY 或已购买资源包 |
| 短时间大量调用图片生成 | 触发 429 限流 | 图片生成限制 500 张/分钟，使用指数退避重试 |
