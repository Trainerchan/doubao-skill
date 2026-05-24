---
name: doubao-skill
description: Use when calling Doubao (豆包) / Volcengine Ark models — chat, vision, document understanding, image generation (Seedream), or video generation (Seedance). Load this first; it routes to the appropriate sub-skill.
version: 1.0.0
author: Trainerchan
license: MIT
metadata:
  tags: [doubao, volcengine, ark, seed, seedream, seedance, multimodal, image-generation, video-generation, bytedance]
---

# Doubao Skill (豆包技能集)

火山方舟(Volcengine Ark)豆包大模型调用技能集。提供三个独立子技能，覆盖通用对话/多模态理解、图片生成、视频生成。

## 安装

复制以下文件到你的 skills 目录，**保持目录结构不变**：

```
doubao-skill/
├── SKILL.md
├── .env.example
├── general/SKILL.md
├── generate-image/SKILL.md
└── generate-video/SKILL.md
```

> 本仓库其余文件（`CLAUDE.md`、`task.md`、`docs/`）为项目开发档案，无需安装。

### 子 skill 独立加载

三个子 skill 可独立注册和加载：

| Skill 名称 | 能力 | 触发场景 |
|-----------|------|----------|
| `doubao-general` | 对话、多模态理解 | 聊天、图片/文档/视频/音频识别与分析 |
| `doubao-generate-image` | 图片生成 | 文生图、图生图、组图、海报设计 |
| `doubao-generate-video` | 视频生成 | 文生视频、图生视频、多模态参考生视频 |

## Agent 集成

### Claude Code

Claude Code 根据 frontmatter 的 `description` 自动匹配。直接对话即可触发，例如：

- "帮我用豆包生成一张图片"
- "分析这份 PDF 文档的内容"
- "生成一段视频"

### Hermes Agent

通过 `skill_view()` 显式加载：

| 总入口 | `skill_view("doubao-skill")` |
| 通用对话 | `skill_view("doubao-general")` |
| 图片生成 | `skill_view("doubao-generate-image")` |
| 视频生成 | `skill_view("doubao-generate-video")` |

Hermes 技能文件位于 `~/.hermes/skills/doubao-skill/`、`doubao-general/`、`doubao-generate-image/`、`doubao-generate-video/`。

## 前置配置

### 1. 获取 API Key

1. 访问 [API Key 管理](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)
2. 点击「创建 API Key」，输入名称后确认
3. 复制生成的 Key（仅显示一次）

### 2. 配置 API Key

将 Key 写入项目根目录的 `.env` 文件（参考 `.env.example`）：

```
ARK_API_KEY=your-api-key-here
```

> 严禁将 API Key 硬编码到代码中。必须通过环境变量或 `.env` 文件管理。

如果用户尚未配置，引导用户完成以上步骤后再继续。

### 3. 代码中加载 Key

每个子 skill 在代码示例开头统一使用 `python-dotenv` 加载：

```python
from dotenv import load_dotenv
load_dotenv()
```

安装依赖：`pip install python-dotenv`

### 4. 安装 SDK

**仅需一个 SDK** 覆盖所有三个子技能：

```bash
pip install volcengine-python-sdk
```

所有子技能统一使用 `volcenginesdkarkruntime.Ark` 客户端。

### 5. 可选：按子技能配置不同模型

每个子技能可通过独立环境变量覆盖默认模型：

| 变量 | 用途 | 默认值 |
|------|------|--------|
| `ARK_API_KEY` | 鉴权 Key（必填） | — |
| `DOUBAO_CHAT_MODEL` | 通用对话模型 | `doubao-seed-2-0-lite-260428` |
| `DOUBAO_IMAGE_MODEL` | 图片生成模型 | `doubao-seedream-5-0-260128` |
| `DOUBAO_VIDEO_MODEL` | 视频生成模型 | `doubao-seedance-2-0-260128` |

## 子技能导航

父 skill 根据用户意图路由到对应子 skill。路由决策表：

| 用户说了什么 | 加载哪个子 skill |
|-------------|----------------|
| 对话、聊天、分析图片、识别文档、提取 PDF/PPTX/XLSX、视频/音频理解、函数调用 | `doubao-general` |
| 生成图片、画图、文生图、图生图、海报、组图、漫画分镜 | `doubao-generate-image` |
| 生成视频、文生视频、图生视频、视频编辑 | `doubao-generate-video` |

### 1. doubao-general — 通用对话 & 多模态

**触发条件**：对话、文本生成、图片理解、视频理解、文档理解（PDF/PPTX/XLSX）、音频理解、函数调用

**使用模型**：`doubao-seed-2-0-lite/pro/mini` 系列

**核心能力**：
- 文本对话（含深度思考模式）
- 图片理解/识别（传入图片 URL 或 Base64）
- 文档理解（PDF、PPTX、XLSX 等）
- 视频理解（抽帧分析）
- 音频理解（mp3/wav 等）
- 联网搜索、知识库检索
- 函数调用 / 工具调用
- 大文件上传（File API）

→ 源码：[general/SKILL.md](general/SKILL.md)

### 2. doubao-generate-image — 图片生成

**触发条件**：生成图片、文生图、图生图、组图、海报设计

**使用模型**：`doubao-seedream-5-0-260128`（推荐）、`doubao-seedream-4-5-251128`、`doubao-seedream-4-0-250828`

**核心能力**：
- 文生图（文本描述 → 单图/组图）
- 图生图（参考图 + 文本 → 编辑/变换）
- 多图融合
- 组图生成（连环画、分镜等，最多 15 张）
- 2K/3K/4K 分辨率
- 支持流式输出

→ 源码：[generate-image/SKILL.md](generate-image/SKILL.md)

### 3. doubao-generate-video — 视频生成

**触发条件**：生成视频、文生视频、图生视频、视频编辑

**使用模型**：`doubao-seedance-2-0-260128`（推荐，有声/无声）

**核心能力**：
- 文生视频
- 图生视频（首帧/首尾帧）
- 多模态参考生视频（图片+视频+音频+文本）
- 音画同生
- 异步任务模式（提交 → 轮询 → 下载）

> 前置条件：账户余额 ≥ 200 元或已购买资源包

→ 源码：[generate-video/SKILL.md](generate-video/SKILL.md)

## 公共约定

1. **Base URL**：`https://ark.cn-beijing.volces.com/api/v3`
2. **鉴权 Header**：`Authorization: Bearer $ARK_API_KEY`
3. **Content-Type**：`application/json`
4. **API Key 作用域**：仅限创建时的项目空间，不支持跨项目访问
5. **错误码参考**：https://www.volcengine.com/docs/82379/1299023
6. **模型列表**：https://www.volcengine.com/docs/82379/1330310
7. **价格参考**：https://www.volcengine.com/docs/82379/1544106

### 自动重试

遇到限流（429）或服务繁忙（503）时，使用指数退避重试，最多 3 次：

```python
import time

def call_with_retry(fn, max_retries=3):
    for i in range(max_retries):
        try:
            return fn()
        except Exception as e:
            err = str(e)
            if "429" in err or "503" in err or "rate" in err.lower():
                wait = 2 ** i  # 1s, 2s, 4s
                print(f"服务繁忙，{wait}s 后重试 ({i+1}/{max_retries})...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError(f"重试 {max_retries} 次后仍失败")
```

### 文档验证（出错时触发）

API 返回 `model not found`、`invalid parameter` 或 400/404 错误时：

1. 优先使用文档查询工具（如 Context7 MCP），搜索豆包/火山方舟相关文档
2. 若无文档查询工具，使用网页获取工具（如 WebFetch、web_fetch、browser 等）抓取对应文档页：
   - Chat API 文档: https://www.volcengine.com/docs/82379/1494384?lang=zh
   - 模型列表: https://www.volcengine.com/docs/82379/1330310?lang=zh
   - 图片生成 API: https://www.volcengine.com/docs/82379/1541523?lang=zh
   - 视频生成 API: https://www.volcengine.com/docs/82379/1520757?lang=zh

修正参数后重试最多一次，不再递归重试。

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
