# gapfill（溜缝儿）

**告别 Claude Code 的反复确认。一键初始化项目权限、文档和 git 骨架。**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache_2.0-green.svg)](LICENSE)
[![零依赖](https://img.shields.io/badge/dependencies-0-lightgrey.svg)]()
[![零 token](https://img.shields.io/badge/token_消耗-0-purple.svg)]()

[English](README.md) · [中文](README_zh.md)

## 为什么需要它

Claude Code 很强大，但开始一个新项目时：

- 🔁 **不停点"允许"**——每次 `git status`、`npm install`、`pip show` 都要确认
- 📋 **从旧项目复制 `settings.local.json`**，然后祈祷能用
- 📄 **从零手写 CLAUDE.md**，找不到模板参考
- 🔍 **永远不知道**自己的权限里有没有 `Write(/**)` 这种危险规则

Gapfill 用几秒钟解决这四个问题——零 LLM 调用、零依赖，只要 Python。初始化、审查、扫描全过程本地执行，**不消耗任何 token**。每个新项目手动配置大约需要 15 分钟；gapfill 一个命令搞定。

## 30 秒上手

```bash
# 1. 克隆
git clone https://github.com/russellglobal/gapfill.git

# 2. 安装 skill
cp -r gapfill/skills/gapfill ~/.claude/skills/gapfill

# 3. 使用
cd your-project
gapfill init
```

需要 **Python 3.8+** 和 **git**。就这些。

## 它做了什么

安装后，在 Claude Code 中告诉它运行 gapfill 子命令。

**注意**：不要只说"初始化项目"——这可能会触发 Claude Code 的内置逻辑。请明确提到 gapfill 或溜缝儿。

### `init` — 项目初始化

**适用场景：** 从零开始创建新项目。

**怎么说：** "用 gapfill 初始化 ./my-project" 或 "gapfill init"

**做什么：**
1. 检测 git、SSH key 等
2. 如果目录没有 .git，自动 git init
3. 创建文件：.gitignore、README.md、settings.local.json、env-info.txt
4. 预置基础级 + 低风险级权限，减少 AI 交互轮次
5. 自动记录可用工具和版本
6. 自动 commit 所有文件

**约束：** 仅限本地初始化。不创建远程仓库，不做框架专属配置。

### `stack-md` — 技术栈专属 CLAUDE.md

**适用场景：** 新项目需要 CLAUDE.md，或想为已有项目补充技术栈相关的约定。

**怎么说：** "用 gapfill 创建 Spring Boot 的 CLAUDE.md" 或 "gapfill stack-md --stack spring-boot ./my-project"

| 技术栈 | 适用场景 |
|--------|----------|
| `generic`（默认） | 技术栈未知，通用项目 |
| `spring-boot` | Java + Spring Boot 3.x 项目 |
| `react` | React 19 + TypeScript 项目 |

**约束：** 仅使用预定义模板，不调用 LLM。绝不覆盖已有的 CLAUDE.md，而是生成 `.claude/gapfill-suggestions.md` 建议文件。

### `review` — 提交前全局审查

**适用场景：** 提交前检查，防止近期改动引入碎片（死引用、副本不一致、残留危险权限等）。

**怎么说：** "用 gapfill 审查项目" 或 "gapfill review"

**检查项：**
- 副本一致性（src/ vs skills/src/）
- 导入有效性（通过 AST 检测死引用）
- settings 模板中的危险权限
- 过期内容（旧项目名、废弃引用）

**约束：** 只报告，不修改任何文件。

### `scan` — 设置合规扫描

**适用场景：** 审计一个目录下所有项目的 settings.local.json 是否有危险权限。

**怎么说：** "用 gapfill 扫描 /path/to/projects 的权限" 或 "gapfill scan /path/to/projects"

**扫描项：**
- **高危**: Write(/**), Edit(/**), Bash(curl:*), Bash(wget:*), WebFetch(domain:*)
- **低风险**: Bash(find:*), Bash(npx:*), Bash(python:*)

**约束：** 只报告，不修改任何文件。

### `sync` — 跨项目权限同步

**适用场景：** 你有多个项目，权限规则不一致，想合并一份统一的配置。

**怎么说：** "用 gapfill 同步权限" 或 "gapfill sync"

**约束：** 只报告。建议合并配置，但不自动写入文件。

## 架构

```
用户 ←→ gapfill Skill（对话层）
                ↓ 调用
        Python 脚本（执行层，不消耗 token）
```

- **Skill 是界面**：处理对话、审查、异常
- **脚本是引擎**：快速、确定、不消耗 token
- **不在 PyPI**：随 skill 分发，永远同步

## 开发路线图

| 版本 | 功能 |
|------|------|
| MVP | `init`（项目初始化）、`.gitignore`、`settings.local.json` 权限预置 |
| v2 | `stack-md`（技术栈感知 CLAUDE.md 生成）**已完成**，`review`（提交前全局审查）**已完成**，`scan`（设置合规扫描）**已完成** |
| v3 | _待定_ — 优先验证 review/scan 的实际使用 |
| v4 | _待定_ — `publish`（多语言文档同步）延期 |
| v5 | _待定_ |

### 暂缓功能
- `sync` — 跨项目权限对比（已实现，暂停 — 用户基数太小）
- `auto-guard` — Auto Mode 兜底（不 pursue — 与 init/scan 重叠，且与 Anthropic 官方 Auto Mode 演进冲突）
- `perm` — JSON 编辑不需要 CLI 包装（scan 已足够）
- `feedback` — `gh issue create` 已覆盖
- `lang` — 合并到 `publish`
- `capture` — 概念有价值但边界不清，待真实用户反馈再审视
- `publish` — 延期到 v4+；有价值但不紧急，等用户群国际化后再做
- `roadmap` — 决策自动沉淀（已被可行性研究流程替代）
- `audit` — Skill 安全扫描（已被 `scan` 设置合规扫描替代）
- 团队配置同步 — Anthropic Enterprise Admin 已覆盖

## 许可证

Apache 2.0

---

术语表请参阅 [docs/glossary.md](docs/glossary.md)。
项目哲学请参阅 [PHILOSOPHY_zh.md](PHILOSOPHY_zh.md) / [English](PHILOSOPHY.md)。
