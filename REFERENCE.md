# Doubao Skill — 参考手册

## 安装

将三个 skill 目录分别复制/链接到你的 Agent skills 目录：

```
doubao-general/           ← 对话 & 多模态理解
doubao-generate-image/    ← Seedream 图片生成
doubao-generate-video/    ← Seedance 视频生成（含 scripts/poll_video.py）
```

```bash
# Claude Code
ln -s /path/to/doubao-skill/doubao-general ~/.claude/skills/doubao-general
ln -s /path/to/doubao-skill/doubao-generate-image ~/.claude/skills/doubao-generate-image
ln -s /path/to/doubao-skill/doubao-generate-video ~/.claude/skills/doubao-generate-video

# Hermes Agent / OpenClaw
# 复制或链接到 Agent 的 skills 目录即可
```

> 本仓库其余文件（`CLAUDE.md`、`REFERENCE.md`）为项目开发档案，无需安装。

## 配置（必读）

**不要替换你的 `.env` 文件！** 在项目根目录的 `.env` 文件中**追加**以下内容：

```env
# ===== 豆包/火山方舟 =====
ARK_API_KEY=你的APIKey
```

`ARK_API_KEY` 从 [火山方舟控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) 获取。

三个 skill 共用同一个 Key。可选覆盖默认模型：

| 变量 | 默认模型 | 说明 |
|------|----------|------|
| `ARK_API_KEY` | — | 鉴权 Key（必填，三个 skill 共用） |
| `DOUBAO_CHAT_MODEL` | `doubao-seed-2-0-lite-260428` | doubao-general 对话模型 |
| `DOUBAO_IMAGE_MODEL` | `doubao-seedream-5-0-260128` | doubao-generate-image 图片模型 |
| `DOUBAO_VIDEO_MODEL` | `doubao-seedance-2-0-260128` | doubao-generate-video 视频模型 |

> 也可直接设置系统环境变量（如 `export ARK_API_KEY=xxx`），优先级高于 `.env` 文件。

## 安装依赖

```bash
pip install volcengine-python-sdk python-dotenv
```

## Agent 集成

### Claude Code

Claude Code 根据 frontmatter 的 `description` 自动匹配。直接对话即可触发。

### Hermes Agent

| Skill | 加载命令 |
|-------|----------|
| 通用对话 | `skill_view("doubao-general")` |
| 图片生成 | `skill_view("doubao-generate-image")` |
| 视频生成 | `skill_view("doubao-generate-video")` |

### OpenClaw

与 Hermes Agent 相同，使用 `skill_view("skill-name")` 加载对应 skill。

## 自动重试

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

## 文档验证（出错时触发）

API 返回 `model not found`、`invalid parameter` 或 400/404 错误时：

1. 优先使用文档查询工具（如 Context7 MCP），搜索豆包/火山方舟相关文档
2. 若无文档查询工具，使用 WebFetch 抓取对应文档页：
   - Chat API: https://www.volcengine.com/docs/82379/1494384?lang=zh
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

## 参考链接

- 错误码参考: https://www.volcengine.com/docs/82379/1299023
- 模型列表: https://www.volcengine.com/docs/82379/1330310
- 价格参考: https://www.volcengine.com/docs/82379/1544106
