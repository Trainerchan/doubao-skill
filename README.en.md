<div align="center">

# Doubao.skill

> *"Let every AI Agent call Doubao — no more digging through docs every time."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

**Package Doubao model capabilities into plug-and-play AI Agent skills — chat, vision, document understanding, image generation, video generation.**

<br>

[Examples](#examples) · [Install](#install) · [Sub-skills](#sub-skills) · [How It Works](#how-it-works)

<br>

**Other Languages:**

[中文](README.md) · [日本語](README.jp.md) · [한국어](README.ko.md) · [Русский](README.ru.md)

</div>

---

## Examples

**Chat & Multimodal (doubao-general)**

```
User      ❯ Analyze this earnings report screenshot — what was the Q3 YoY
            revenue change?

Doubao    ❯ Based on the screenshot, Q3 revenue was 4.87 billion yuan,
            compared to 3.82 billion in the same period last year,
            a 27.5% YoY increase. Growth was driven primarily by
            advertising (+35%) and cloud services (+22%).
            Gross margin improved from 58% to 62%.
```

```
User      ❯ What are the key clauses in this PDF contract? Present as a table.

Doubao    ❯ | Clause | Content | Risk |
            |--------|---------|------|
            | Breach | 0.05% daily penalty | Medium |
            | IP | Client owns all results | Low |
            | NDA | Perpetual mutual obligation | Low |
            | Exclusivity | No competing clients for 3 years | ⚠️ High |
            The exclusivity clause limits your future business — suggest
            shortening to 1 year or adding compensation terms.
```

**Image Generation (doubao-generate-image)**

```
User      ❯ Generate a poster: ginkgo tree avenue in autumn, a girl in a
            beige trench coat walking away, cinematic lighting, portrait

Doubao    ❯ [Generates 9:16 portrait image]
            Generated 4K image: https://ark-cn-beijing.volces.com/...
            ⚠️ URL expires in 24 hours — download promptly.
```

```
User      ❯ Generate 4 product showcase shots, white background, different angles

Doubao    ❯ Generating group images...
            [1/4] ✅ Front 45° angle
            [2/4] ✅ Side view
            [3/4] ✅ Top-down
            [4/4] ✅ Handheld close-up
            Complete — 4 images generated.
```

**Video Generation (doubao-generate-video)**

```
User      ❯ Generate a 5-second clip: golden retriever running through a meadow,
            slow motion, afternoon sunlight

Doubao    ❯ Task created: cgt-s6xcyoSh4BRx
            Status: queued → running → succeeded (47s)
            Downloaded: output.mp4 (1080p, 5s)
```

This isn't just an API wrapper. Each sub-skill is self-contained — after loading it, the agent knows exactly which endpoint to call, what parameters to pass, how to handle errors. **No need to dig through Volcengine docs.**

---

## Install

```bash
npx skills add Trainerchan/doubao-skill
```

After installation, trigger directly in conversation:

```
> Analyze this image with Doubao
> Generate a promotional poster
> Summarize this PDF with Doubao
```

### Manual Install

```bash
git clone https://github.com/Trainerchan/doubao-skill.git
cd doubao-skill
cp .env.example .env
# Edit .env and set ARK_API_KEY
pip install volcengine-python-sdk python-dotenv
```

### Files to Install

> Other files (`CLAUDE.md`, `docs/`, etc.) are development artifacts — do not distribute.

```
doubao-skill/
├── SKILL.md                  ← Parent: shared config, sub-skill routing
├── .env.example              ← Environment variable template
├── general/SKILL.md          ← Sub: chat & multimodal
├── generate-image/SKILL.md   ← Sub: image generation (Seedream)
└── generate-video/SKILL.md   ← Sub: video generation (Seedance)
```

---

## Sub-skills

| Skill | Capabilities | Models | Triggers |
|-------|-------------|--------|----------|
| 🔥 **doubao-general** | Chat, vision, document/video/audio understanding, web search, function calling | doubao-seed-2.0-lite/pro/mini | Chat, analyze images/PDFs/videos, extract info |
| 🔥 **doubao-generate-image** | Text-to-image, image-to-image, group images, multi-image fusion | doubao-seedream-5.0/4.5/4.0 | Generate images, posters, comic panels |
| **doubao-generate-video** | Text-to-video, image-to-video, multimodal reference, synchronized audio | doubao-seedance-2.0/1.5/1.0 | Generate videos, video editing |

> Video generation requires account balance ≥ 200 CNY or a resource pack.

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|:-------:|---------|-------------|
| `ARK_API_KEY` | ✅ | — | Volcengine Ark API Key ([Get one here](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)) |
| `DOUBAO_CHAT_MODEL` | ❌ | `doubao-seed-2-0-lite-260428` | Override chat model |
| `DOUBAO_IMAGE_MODEL` | ❌ | `doubao-seedream-5-0-260128` | Override image generation model |
| `DOUBAO_VIDEO_MODEL` | ❌ | `doubao-seedance-2-0-260128` | Override video generation model |

---

## How It Works

After loading the skill, the agent follows three steps:

**1. Route Matching** — The parent skill matches user intent to the right sub-skill. "Analyze this image" → doubao-general, "Generate a poster" → doubao-generate-image, "Create a video" → doubao-generate-video.

**2. Self-Executing Sub-skills** — Each sub-skill is self-contained: prerequisite checks (`.env` → `os.getenv` → guided setup), parameter reference tables, code examples (cURL + Python), common errors with solutions. The agent doesn't need external docs.

**3. Fallback on Error** — If the API returns `model not found` or `invalid parameter`, the agent automatically:
- First tries a documentation query tool (e.g. Context7 MCP) for latest parameters
- Falls back to web fetching the official Volcengine docs
- Retries once with corrected parameters

---

## Repository Structure

```
doubao-skill/
├── SKILL.md                      # Parent: shared config, sub-skill routing
├── .env.example                  # Environment variable template
├── general/
│   └── SKILL.md                  # Chat & multimodal
├── generate-image/
│   └── SKILL.md                  # Image generation (Seedream)
├── generate-video/
│   └── SKILL.md                  # Video generation (Seedance)
├── docs/
│   └── agents/                   # Agent configuration (issue tracker, labels, etc.)
└── CLAUDE.md                     # Project development guide
```

All API parameter details, size matrices, and model capability comparisons live directly in the sub-skill SKILL.md files — agents only need to read a single file.

---

## The Story

Every time you want an AI agent to call the Doubao API, it has to dig through Volcengine docs — which endpoint, what parameters, what's the model ID, what do the error codes mean. Every. Single. Time.

The motivation is simple: **do the research once, package it well, and never look it up again.**

Doubao's underlying capabilities are strong — 256K context, deep thinking, multimodal understanding, image and video generation — but the documentation is scattered across different pages. By consolidating the complete calling knowledge for all three sub-skills into single files, the agent loads once and is ready.

**doubao-skill** doesn't create capabilities. It eliminates the cost of accessing them.

---

## About the Author

**Trainerchan** — [GitHub](https://github.com/Trainerchan)

## License

MIT — use it, modify it, integrate it however you want.

---

<div align="center">

Make every Doubao call as natural as breathing.<br>
*No docs. No parameter hunting. Just say what you need.*

<br>

MIT License © [Trainerchan](https://github.com/Trainerchan)

</div>
