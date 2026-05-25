# Doubao Skill — 参考手册

## 安装

复制以下文件到你的 skills 目录，**保持目录结构不变**：

```
doubao-skill/
├── SKILL.md
├── REFERENCE.md
├── .env.example
├── general/
│   ├── SKILL.md
│   └── REFERENCE.md
├── generate-image/
│   ├── SKILL.md
│   └── REFERENCE.md
└── generate-video/
    ├── SKILL.md
    ├── REFERENCE.md
    └── scripts/
        └── poll_video.py
```

> 本仓库其余文件（`CLAUDE.md`、`task.md`、`docs/`）为项目开发档案，无需安装。

## Agent 集成

### Claude Code

Claude Code 根据 frontmatter 的 `description` 自动匹配。直接对话即可触发。

### Hermes Agent

通过 `skill_view()` 显式加载：

| 总入口 | `skill_view("doubao-skill")` |
| 通用对话 | `skill_view("doubao-general")` |
| 图片生成 | `skill_view("doubao-generate-image")` |
| 视频生成 | `skill_view("doubao-generate-video")` |

### OpenClaw

通过 `skill_view()` 显式加载，方式同 Hermes Agent。

## 完整配置

### 1. 获取 API Key

1. 访问 [API Key 管理](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)
2. 点击「创建 API Key」，输入名称后确认
3. 复制生成的 Key（仅显示一次）

### 2. 配置 Key

将 Key 写入项目根目录的 `.env` 文件（参考 `.env.example`）：

```
ARK_API_KEY=your-api-key-here
```

> 严禁将 API Key 硬编码到代码中。

### 3. 可选：按子技能配置不同模型

| 变量 | 用途 | 默认值 |
|------|------|--------|
| `ARK_API_KEY` | 鉴权 Key（必填） | — |
| `DOUBAO_CHAT_MODEL` | 通用对话模型 | `doubao-seed-2-0-lite-260428` |
| `DOUBAO_IMAGE_MODEL` | 图片生成模型 | `doubao-seedream-5-0-260128` |
| `DOUBAO_VIDEO_MODEL` | 视频生成模型 | `doubao-seedance-2-0-260128` |

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
