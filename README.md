# Doubao Skill（豆包技能集）

火山方舟(Volcengine Ark)豆包大模型调用技能集，为 AI Agent 提供调用豆包 API 的能力。包含三个独立子技能。

## 子技能概览

| 技能名称 | 能力 | 使用模型 |
|---------|------|----------|
| **doubao-general** | 对话、图片/文档/视频/音频理解、联网搜索、函数调用 | doubao-seed-2.0-lite/pro/mini |
| **doubao-generate-image** | 文生图、图生图、组图、多图融合 | doubao-seedream-5.0/4.5/4.0 |
| **doubao-generate-video** | 文生视频、图生视频、多模态参考、音画同生 | doubao-seedance-2.0/1.5/1.0 |

## 前置条件

1. **API Key**：在[火山引擎控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)创建 API Key
2. **SDK**：`pip install volcengine-python-sdk python-dotenv`
3. **视频生成额外要求**：账户余额 ≥ 200 元或已购买资源包

## 快速开始

```bash
# 1. 配置 API Key
cp .env.example .env
# 编辑 .env，填入 ARK_API_KEY=your-key

# 2. 测试对话
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"doubao-seed-2-0-lite-260428","messages":[{"role":"user","content":"你好"}]}'

# 3. 测试图片生成
curl https://ark.cn-beijing.volces.com/api/v3/images/generations \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"doubao-seedream-5-0-260128","prompt":"一只可爱的橘猫坐在窗台看夕阳","size":"2K"}'
```

## 安装

### 安装到 Claude Code

将以下文件复制到你的 skills 目录，保持目录结构：

```
doubao-skill/
├── SKILL.md
├── .env.example
├── general/SKILL.md
├── generate-image/SKILL.md
└── generate-video/SKILL.md
```

Claude Code 会根据 frontmatter 的 description 自动匹配技能。直接对话即可触发，例如"帮我用豆包分析这张图片"。

### 手动安装

1. 复制上述 4 个 `SKILL.md` 文件和 `.env.example` 到你的 skills 目录
2. 复制 `.env.example` 为 `.env`，填入 `ARK_API_KEY`
3. 安装依赖：`pip install volcengine-python-sdk python-dotenv`

### 子技能独立安装

三个子技能可独立使用，每个子技能的 `SKILL.md` 都是自包含的：

- `general/SKILL.md` → 注册为 `doubao-general`
- `generate-image/SKILL.md` → 注册为 `doubao-generate-image`
- `generate-video/SKILL.md` → 注册为 `doubao-generate-video`

> 本仓库其余文件（`CLAUDE.md`、`task.md`、`docs/`）为开发档案，无需安装。

## 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|:---:|--------|------|
| `ARK_API_KEY` | ✅ | — | 火山方舟 API Key |
| `DOUBAO_CHAT_MODEL` | ❌ | `doubao-seed-2-0-lite-260428` | 覆盖对话模型 |
| `DOUBAO_IMAGE_MODEL` | ❌ | `doubao-seedream-5-0-260128` | 覆盖图片生成模型 |
| `DOUBAO_VIDEO_MODEL` | ❌ | `doubao-seedance-2-0-260128` | 覆盖视频生成模型 |

## 参考链接

- [火山方舟 Chat API 文档](https://www.volcengine.com/docs/82379/1494384)
- [图片生成 API 文档](https://www.volcengine.com/docs/82379/1541523)
- [视频生成 API 文档](https://www.volcengine.com/docs/82379/1520757)
- [API Key 管理](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)
- [错误码参考](https://www.volcengine.com/docs/82379/1299023)
- [价格参考](https://www.volcengine.com/docs/82379/1544106)

## 许可

MIT
