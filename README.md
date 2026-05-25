<div align="center">

# 豆包.skill

> *「让每一个 AI Agent 都能调用豆包——省时省力，不用每次翻文档」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

**把豆包大模型的能力封装成即装即用的 AI Agent 技能——对话、识图、读文档、生成图片、生成视频。**

<br>

[效果示例](#效果示例) · [安装](#安装) · [子技能概览](#子技能概览) · [工作原理](#工作原理)

<br>

**其他语言 / Other Languages:**

[English](README.en.md) · [日本語](README.jp.md) · [한국어](README.ko.md) · [Русский](README.ru.md)

</div>

---

## 效果示例

**对话 & 多模态理解（doubao-general）**

```
用户      ❯ 帮我分析这张财报截图里，Q3 营收同比变化是多少？

豆包      ❯ 根据截图数据，Q3 营收为 48.7 亿元，去年同期为 38.2 亿元，
            同比增长 27.5%。主要增长驱动来自广告业务（+35%）和云服务（+22%）。
            毛利率从 58% 提升至 62%，显示盈利能力同步改善。
```

```
用户      ❯ 这份 PDF 合同的核心条款是什么？用表格列出来

豆包      ❯ | 条款 | 内容 | 风险等级 |
            |------|------|---------|
            | 违约责任 | 逾期每日万分之五违约金 | 中 |
            | 知识产权 | 委托方拥有全部成果产权 | 低 |
            | 保密条款 | 双方永久保密义务 | 低 |
            | 排他条款 | 乙方 3 年内不得服务竞品 | ⚠️ 高 |
            排他条款限制了贵司未来业务空间，建议争取缩短至 1 年或增加补偿条款。
```

**图片生成（doubao-generate-image）**

```
用户      ❯ 生成一张海报：秋天银杏大道，穿米色风衣的女孩背影，
            电影级光影，竖版

豆包      ❯ [生成 9:16 竖版图片]
            已生成 4K 分辨率图片：https://ark-cn-beijing.volces.com/...
            ⚠️ URL 有效期 24 小时，请及时下载保存。
```

```
用户      ❯ 帮我生成一组 4 张产品展示图，白色背景，不同角度

豆包      ❯ 正在生成组图...
            [图1] ✅ 正面 45° 视角
            [图2] ✅ 侧面视角
            [图3] ✅ 顶部俯视
            [图4] ✅ 手持场景特写
            全部完成，共生成 4 张图片。
```

**视频生成（doubao-generate-video）**

```
用户      ❯ 生成一段 5 秒视频：金毛犬在草地上奔跑，慢动作，午后阳光

豆包      ❯ 任务已创建: cgt-s6xcyoSh4BRx
            状态: queued → running → succeeded (耗时 47s)
            下载完成: output.mp4 (1080p, 5s)
```

这不是简单的 API 封装。每个子技能都是自包含的——Agent 加载后直接知道怎么调、传什么参数、遇到错误怎么处理，**不需要再翻火山引擎文档**。

---

## 安装

```bash
npx skills add Trainerchan/doubao-skill
```

安装后在 Claude Code 里直接对话即可触发：

```
> 帮我用豆包分析这张图片
> 生成一张宣传海报
> 用豆包 API 总结这份 PDF
```

### 手动安装

```bash
git clone https://github.com/Trainerchan/doubao-skill.git
cd doubao-skill
cp .env.example .env
# 编辑 .env 填入 ARK_API_KEY
pip install volcengine-python-sdk python-dotenv
```

### 安装需要复制的文件

> 本仓库其余文件（`CLAUDE.md`、`docs/` 等）为开发档案，无需分发安装。

```
doubao-skill/
├── SKILL.md                  ← 父技能：配置共享、子技能路由
├── .env.example              ← 环境变量模板
├── general/SKILL.md          ← 子技能：通用对话 & 多模态
├── generate-image/SKILL.md   ← 子技能：图片生成 (Seedream)
└── generate-video/SKILL.md   ← 子技能：视频生成 (Seedance)
```

---

## 子技能概览

| 技能 | 能力 | 模型 | 触发场景 |
|------|------|------|---------|
| 🔥 **doubao-general** | 对话、识图、文档/视频/音频理解、联网搜索、函数调用 | doubao-seed-2.0-lite/pro/mini | 聊天、分析图片/PDF/视频、提取信息 |
| 🔥 **doubao-generate-image** | 文生图、图生图、组图、多图融合 | doubao-seedream-5.0/4.5/4.0 | 生成图片、海报设计、漫画分镜 |
| **doubao-generate-video** | 文生视频、图生视频、多模态参考、音画同生 | doubao-seedance-2.0/1.5/1.0 | 生成视频、视频编辑 |

> 视频生成需要账户余额 ≥ 200 元或已购买资源包。

---

## 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|:---:|--------|------|
| `ARK_API_KEY` | ✅ | — | 火山方舟 API Key（[获取地址](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)） |
| `DOUBAO_CHAT_MODEL` | ❌ | `doubao-seed-2-0-lite-260428` | 覆盖对话模型 |
| `DOUBAO_IMAGE_MODEL` | ❌ | `doubao-seedream-5-0-260128` | 覆盖图片生成模型 |
| `DOUBAO_VIDEO_MODEL` | ❌ | `doubao-seedance-2-0-260128` | 覆盖视频生成模型 |

---

## 工作原理

Agent 加载豆包技能后，按三步完成调用：

**1. 路由匹配**——父 skill 根据用户意图匹配子技能。"分析图片"路由到 doubao-general，"生成海报"路由到 doubao-generate-image，"生成视频"路由到 doubao-generate-video。

**2. 子技能自执行**——每个子技能是自包含的：前置检查（`.env` → `os.getenv` → 引导配置）、参数速查表、代码示例（cURL + Python）、常见错误及解决方案。Agent 不需要查外部文档。

**3. 异常回退**——如果 API 返回 `model not found` 或 `invalid parameter`，Agent 自动：
- 优先使用文档查询工具（如 Context7 MCP）查最新参数
- 若无，使用网页获取工具抓取火山方舟官方文档
- 修正后重试一次

---

## 仓库结构

```
doubao-skill/
├── SKILL.md                      # 父技能：配置共享、子技能路由
├── .env.example                  # 环境变量模板
├── general/
│   └── SKILL.md                  # 通用对话 & 多模态
├── generate-image/
│   └── SKILL.md                  # 图片生成 (Seedream)
├── generate-video/
│   └── SKILL.md                  # 视频生成 (Seedance)
├── docs/
│   └── agents/                   # Agent 配置（issue tracker、标签等）
└── CLAUDE.md                     # 项目开发指引
```

所有 API 参数细节、尺寸矩阵、模型能力对比直接写在对应的子技能 SKILL.md 中——Agent 只读一个文件就够。

---

## 背后的故事

每次想让 AI Agent 调用豆包 API，Agent 都得去翻火山方舟文档——哪个 endpoint、什么参数、模型 ID 叫啥、错误码是什么意思。每次都要查，费时费力。

做这个技能集的初衷很简单：**把这些查文档的工作做一次封装好，以后每次直接调用就行。**

豆包模型底层能力很强——256K 上下文、深度思考、多模态理解、图片视频生成——但文档分散在不同的页面。把三个子技能各自的完整调用知识集中到一个文件中，Agent 加载一次就够了。

**doubao-skill** 不创造能力。它消除调用成本。

---

## 关于作者

**Trainerchan** — [GitHub](https://github.com/Trainerchan)

## 许可证

MIT — 随便用，随便改，随便集成。

---

<div align="center">

让每一次豆包调用，都像呼吸一样自然。<br>
*不用翻文档。不用查参数。直接说需求就行。*

<br>

MIT License © [Trainerchan](https://github.com/Trainerchan)

</div>

---

## English

**[doubao-skill](https://github.com/Trainerchan/doubao-skill)** wraps the Volcengine Ark (火山方舟) Doubao model APIs into plug-and-play AI Agent skills. Three self-contained sub-skills covering chat/multimodal understanding, image generation (Seedream), and video generation (Seedance).

Not just an API wrapper — each sub-skill is a complete knowledge package. The agent loads it and immediately knows: which endpoint to call, what parameters to pass, how to handle errors, and where to fall back if something changes.

**Install**: `npx skills add Trainerchan/doubao-skill`

**Sub-skills**:
- `doubao-general` — Chat, vision, document/video/audio understanding, web search, function calling
- `doubao-generate-image` — Text-to-image, image-to-image, group images (Seedream)
- `doubao-generate-video` — Text-to-video, image-to-video, multimodal reference (Seedance)

**Config**: Set `ARK_API_KEY` in `.env`, then just talk to your agent.

See the Chinese README above for live examples and full documentation.
