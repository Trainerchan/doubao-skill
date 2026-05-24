# Claude Code 完整能力报告

生成时间：2026-05-24 | 工作目录：`E:\doubao-skill`

---

## 一、模型与后端配置

当前使用 **DeepSeek** 作为后端（通过 Anthropic 兼容 API 代理）：

| 配置项 | 值 |
|--------|-----|
| API 端点 | `https://api.deepseek.com/anthropic` |
| 默认模型 | `deepseek-v4-pro` (1M 上下文) |
| Haiku 替代 | `deepseek-v4-flash` |
| Sonnet 替代 | `deepseek-v4-pro[1M]` |
| Opus 替代 | `deepseek-v4-pro[1M]` |
| Effort 级别 | `max` |

---

## 二、原生工具能力（22 个内置工具）

### 文件操作
| 工具 | 功能 |
|------|------|
| **Read** | 读取文本/图片/PDF/Notebook 文件 |
| **Write** | 创建或覆写文件 |
| **Edit** | 精确字符串替换编辑（支持 replace_all） |
| **Glob** | 通配符文件搜索 |
| **Grep** | 正则表达式内容搜索（基于 ripgrep） |

### 执行
| 工具 | 功能 |
|------|------|
| **Bash** | 执行 Shell 命令（超时 2-10 分钟，支持后台运行） |
| **TaskCreate/Get/List/Update/Stop/Output** | 任务追踪系统 |
| **ScheduleWakeup** | 动态循环调度器 |
| **CronCreate/List/Delete** | 定时任务调度（支持持久化） |

### 智能协作
| 工具 | 功能 |
|------|------|
| **Agent** | 启动子 Agent 执行多步骤复杂任务（支持多种子类型） |
| **Skill** | 调用技能模块 |

### 交互
| 工具 | 功能 |
|------|------|
| **AskUserQuestion** | 向用户提问（单选/多选，支持预览） |

### 网络
| 工具 | 功能 |
|------|------|
| **WebSearch** | Web 搜索 |
| **WebFetch** | 获取并分析网页内容 |

### Git/环境
| 工具 | 功能 |
|------|------|
| **EnterPlanMode / ExitPlanMode** | 计划模式（先设计再编码） |
| **EnterWorktree / ExitWorktree** | Git Worktree 隔离环境 |
| **NotebookEdit** | Jupyter Notebook 编辑 |

---

## 三、持久记忆系统

记忆存储位置：`C:\Users\34435\.claude\projects\E--doubao-skill\memory\`

支持四种记忆类型：

| 类型 | 用途 | 示例 |
|------|------|------|
| **user** | 用户角色、偏好、知识背景 | "你是资深后端，刚接触前端" |
| **feedback** | 用户对你行为的纠正或确认 | "不要在测试里 mock 数据库" |
| **project** | 项目上下文（截止日期、动机、干系人） | "周四起冻结合入，移动端发版" |
| **reference** | 外部资源指针（Slack、Linear、Grafana 等） | "Bug 跟踪在 Linear INGEST 项目" |

记忆通过 `MEMORY.md` 索引，每条记忆独立文件。当前该项目暂无存储的记忆。

---

## 四、多 Agent 架构

### 可用 Agent 类型

| Agent 类型 | 用途 |
|------------|------|
| **general-purpose** (默认) | 通用多步骤任务 |
| **claude-code-guide** | Claude Code 使用问题（CLI/API/SDK） |
| **Explore** | 只读代码搜索与定位 |
| **Plan** | 软件架构设计与实现规划 |
| **statusline-setup** | 配置状态栏 |

### 关键用法
- 使用 `run_in_background: true` 后台运行独立任务
- 多个无依赖的 Agent 可并行启动
- Agent 之间通过 `SendMessage` 续接上下文

---

## 五、Slash 命令（内置）

| 命令 | 功能 |
|------|------|
| `/help` | 获取帮助 |
| `/clear` | 清空对话 |
| `/compact` | 压缩上下文 |
| `/config` | 打开配置面板 |
| `/cost` | 查看 Token 用量 |
| `/effort` | 设置努力级别 |
| `/fast` | 切换快速模式 |
| `/memory` | 管理记忆 |
| `/add-dir` | 添加工作目录 |
| `/init` | 初始化项目 CLAUDE.md |
| `/loop` | 循环执行任务 |
| `/hooks` | 管理 Hooks |
| `/mcp` | 管理 MCP 服务器 |
| `/agents` | 管理 Agent |
| `/plugin` | 管理插件 |
| `/statusline` | 配置状态栏 |
| `/todos` | 查看任务列表 |
| `/upgrade` | 升级 Claude Code |
| `/review` | 代码审查 |
| `/security-review` | 安全审查 |
| `/terminal-setup` | 终端设置 |

---

## 六、技能系统 (Skills)

### 项目级技能（当前目录）

| 技能 | 说明 |
|------|------|
| **doubao-skill** | 豆包/火山方舟 API 技能集入口（路由到子技能） |
| ├─ general | 通用对话、多模态理解（文/图/视频/文档/音频）+ 函数调用 |
| ├─ generate-image | Seedream 图片生成（文生图、图生图、组图、2K/3K/4K） |
| └─ generate-video | Seedance 视频生成（异步任务：创建→轮询→下载） |

入口：`SKILL.md`（本目录）

### 用户级技能（全局可用，已安装 18 个）

| 技能 | 用途 |
|------|------|
| **algorithmic-art** | 算法艺术生成 (p5.js) |
| **brand-guidelines** | Anthropic 品牌风格应用 |
| **canvas-design** | 静态视觉设计（海报等） |
| **claude-api** | Claude API / Anthropic SDK 开发调试 |
| **doc-coauthoring** | 结构化文档协作写作 |
| **docx** | Word 文档生成与编辑 |
| **frontend-design** | 前端界面设计与实现 |
| **internal-comms** | 内部沟通文档 |
| **mcp-builder** | MCP 服务器构建 |
| **pdf** | PDF 生成与处理 |
| **pptx** | PowerPoint 生成 |
| **skill-creator** | 创建新技能 |
| **slack-gif-creator** | Slack GIF 动画生成 |
| **theme-factory** | 主题样式工厂 |
| **web-artifacts-builder** | Web 构件构建 |
| **webapp-testing** | Web 应用测试（基于 Playwright） |
| **xlsx** | Excel 文件生成与处理 |
| **template** | 技能模板 |

存储路径：`C:\Users\34435\.claude\skills\`

---

## 七、插件系统

### 已注册插件市场
- **claude-plugins-official** (GitHub: `anthropics/claude-plugins-official`) — 最后更新 2026-05-24

### 官方市场可用插件（按类型）

**内置插件：**
- agent-sdk-dev, claude-code-setup, claude-md-management, code-modernization, code-review, code-simplifier, commit-commands, cwc-makers, example-plugin, explanatory-output-style, feature-dev, frontend-design, hookify, learning-output-style, math-olympiad, mcp-server-dev, mcp-tunnels, playground, plugin-dev, pr-review-toolkit, ralph-loop, security-guidance, skill-creator

**外部集成（含 MCP）：**
- asana, context7, discord, fakechat, firebase, github, gitlab, greptile, imessage, laravel-boost, linear, playwright, serena, telegram, terraform

---

## 八、MCP 支持

- 内置命令 `/mcp` 管理 MCP 服务器
- 官方市场提供 `mcp-builder` 技能用于构建自定义 MCP 服务器
- 多个预配置 MCP 集成的插件可用（GitHub、GitLab、Linear、Asana、Playwright 等）
- 当前项目级 `.mcp.json`：无

---

## 九、Hooks 系统

支持通过 Hooks 在特定事件触发自动化行为。官方市场提供以下 Hooks 相关插件：

| 插件 | Hook 类型 |
|------|-----------|
| explanatory-output-style | 输出风格 |
| hookify | Hook 创建工具 |
| learning-output-style | 学习输出风格 |
| ralph-loop | 循环触发 |
| security-guidance | 安全指导 |

---

## 十、CLAUDE.md 项目指令

当前项目 `E:\doubao-skill\CLAUDE.md` 包含：
- 项目结构说明
- 环境变量与默认模型配置
- 三个子技能的 API 规范
- 编辑规范与同步要求

---

## 十一、配置摘要

| 设置项 | 当前值 |
|--------|--------|
| 语言 | 简体中文（专业简洁风格） |
| 主题 | dark |
| 自动更新通道 | latest |
| 努力级别 | max |
| 模型后端 | DeepSeek (via api.deepseek.com) |
| 记忆存储 | `~/.claude/projects/E--doubao-skill/memory/`（当前为空） |
| 密钥管理 | `~/.claude/settings.json`（含 `ANTHROPIC_AUTH_TOKEN`） |

---

## 十二、核心工作流模式

1. **实现任务** → EnterPlanMode（复杂时）→ 编辑 → Bash 验证
2. **代码搜索** → Agent(Explore) 或直接 Glob/Grep
3. **并行独立任务** → 多个 Agent + `run_in_background`
4. **文档协作** → Skill(doc-coauthoring)
5. **前端设计** → Skill(frontend-design)
6. **API 集成** → Skill(claude-api)
7. **使用豆包模型** → Skill(doubao-skill) 自动路由到对应子技能
8. **定时/循环** → CronCreate 或 /loop
9. **代码审查** → /review 或 Skill(code-review)
10. **记忆管理** → /memory 命令
