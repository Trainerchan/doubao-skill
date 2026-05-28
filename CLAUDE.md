# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repo contains three standalone Claude Code skills wrapping Volcengine Ark (火山方舟) Doubao model APIs. Each skill is self-contained and can be installed independently.

```
doubao-skill/
├── doubao-general/
│   ├── SKILL.md              ← Chat, vision, document understanding, function calling, streaming
│   └── REFERENCE.md          ← Extended scenarios, full parameter table, error reference
├── doubao-generate-image/
│   ├── SKILL.md              ← Text-to-image, image-to-image, multi-fusion, group images
│   └── REFERENCE.md          ← Streaming, web search, full parameter table, size matrix
├── doubao-generate-video/
│   ├── SKILL.md              ← Async workflow, text-to-video, image-to-video first frame
│   ├── REFERENCE.md          ← Extended scenarios, full parameter table, resolution matrix, limits
│   └── scripts/
│       └── poll_video.py     ← Reusable: create task → poll → download MP4
├── REFERENCE.md              ← Installation, agent integration, retry logic, doc verification
├── CLAUDE.md                 ← This file
└── .env.example              ← Env var template (ARK_API_KEY + model overrides)
```

## Environment & Configuration

- **Required**: `ARK_API_KEY` — Volcengine Ark API key (set via env var or `.env` file)
- **Optional overrides**: `DOUBAO_CHAT_MODEL`, `DOUBAO_IMAGE_MODEL`, `DOUBAO_VIDEO_MODEL`
- **Default models**:
  - Chat: `doubao-seed-2-0-lite-260428`
  - Image: `doubao-seedream-5-0-260128`
  - Video: `doubao-seedance-2-0-260128`

## API Conventions (all sub-skills)

- **Base URL**: `https://ark.cn-beijing.volces.com/api/v3`
- **Auth header**: `Authorization: Bearer $ARK_API_KEY`
- **Content-Type**: `application/json`
- **SDK**: `pip install volcengine-python-sdk` — provides `volcenginesdkarkruntime.Ark` client for all three sub-skills

## Skill Architecture

### general — Chat & Multimodal

- **Endpoint**: `POST /v3/chat/completions` (also `/v3/responses` for new API)
- **Capabilities**: text chat, image understanding (URL or base64), document understanding (PDF/DOCX/XLSX/PPTX), video understanding, audio transcription, deep thinking mode, function calling, streaming
- **Models**: `doubao-seed-2-0-lite/pro/mini` series (256K context)
- **Not supported**: `frequency_penalty`, `presence_penalty`

### generate-image — Seedream

- **Endpoint**: `POST /v3/images/generations`
- **SDK client**: `client.images.generate(...)`
- **Capabilities**: text-to-image, image-to-image (single ref), multi-image fusion (up to 14 refs), group/sequential images (up to 15), web-search-assisted generation, streaming output
- **Resolutions**: 2K/3K/4K presets or custom pixels
- **Output**: URL (24h expiry) or base64 JSON
- **Rate limit**: 500 images/minute

### generate-video — Seedance

- **Endpoint**: `POST /v3/contents/generations/tasks` (create), `GET .../tasks/{id}` (poll), `DELETE .../tasks/{id}` (cancel)
- **SDK client**: `client.content_generation.tasks.create(...)` / `.get(id)`
- **Workflow**: async only — create task → poll every ~10s for status → download MP4 on `succeeded`
- **Task states**: `queued` → `running` → `succeeded` / `failed` / `cancelled`
- **Capabilities**: text-to-video, image-to-video (first frame or first+last frame), multimodal reference (image+video+audio, Seedance 2.0 only), audio generation
- **Prerequisite**: account balance ≥ 200 CNY or purchased resource pack
- **Key constraints**: duration 2-15s, up to 9 images / 3 videos / 3 audio clips as reference, request body ≤ 64 MB

## When Editing This Skill

- Each skill `SKILL.md` must be self-contained — an agent loading it should have everything needed to make API calls without external dependencies
- When updating model IDs or defaults, sync across: the relevant skill's SKILL.md, `.env.example`, and REFERENCE.md
- API doc sources: https://www.volcengine.com/docs/82379 (Chat: 1494384, Image: 1541523, Video: 1520757)

## Agent skills

### Issue tracker

GitHub issues at https://github.com/Trainerchan/doubao-skill.

### Triage labels

Uses the canonical default labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`.
