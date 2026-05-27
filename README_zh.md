# gapfill（溜缝儿）

**告别 Claude Code 的反复确认。一键初始化项目权限、文档和 git 骨架。**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache_2.0-green.svg)](LICENSE)
[![零依赖](https://img.shields.io/badge/dependencies-0-lightgrey.svg)]()

[English](README.md) · [中文](README_zh.md)

## 为什么需要它

Claude Code 很强大，但开始一个新项目时：

- 🔁 **不停点"允许"**——每次 `git status`、`npm install`、`pip show` 都要确认
- 📋 **从旧项目复制 `settings.local.json`**，然后祈祷能用
- 📄 **从零手写 CLAUDE.md**，找不到模板参考
- 🔍 **永远不知道**自己的权限里有没有 `Write(/**)` 这种危险规则

Gapfill 用几秒钟解决这四个问题——零 LLM 调用、零依赖，只要 Python。

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

| 手动操作 | 用 gapfill |
|---------|-----------|
| 手动 `git init` | `gapfill init` 一次完成仓库初始化、配置和提交 |
| 每个命令都要点"允许" | 预置权限，确认次数减少约 80% |
| 从旧项目拷 `settings.local.json` | `gapfill init` 一键生成安全默认值 |
| 从零写 CLAUDE.md | `gapfill init --stack spring-boot` 初始化时一步到位，或已有项目用 `gapfill stack-claude-md` |
| 提交前不检查 | `gapfill review` 发现死引用、过期内容、权限漂移 |
| 手动审计 10 个项目的权限 | `gapfill scan` 几秒钟扫完 |

## 子命令

### `init` — 项目初始化

**什么时候用：** 从零开始创建新项目。

```
gapfill init                           # 基础初始化
gapfill init ./my-project              # 指定目录初始化
gapfill init --stack spring-boot       # 初始化 + 一步生成 CLAUDE.md
```

创建 `.gitignore`、`README.md`、`settings.local.json`、`env-info.txt` 并自动提交。自动检测 git 和 SSH key 状态。
加上 `--stack` 还会生成技术栈专属 CLAUDE.md。

### `stack-claude-md` — CLAUDE.md 生成

**什么时候用：** 已有项目需要 CLAUDE.md。（新项目直接用 `gapfill init --stack` 一步完成。）

```
gapfill stack-claude-md                        # 通用模板
gapfill stack-claude-md --stack spring-boot    # Spring Boot 3.x
gapfill stack-claude-md --stack react          # React 19 + TypeScript
```

预定义模板——不调用 LLM。绝不覆盖已有的 CLAUDE.md。

### `review` — 提交前审查

**什么时候用：** `git commit` 之前，检查近期改动引入的问题。

```
gapfill review
```

检查项：副本一致性、死引用、模板中的危险权限、过时的项目名。有错误时退出码为 1。

### `scan` — 权限审计

**什么时候用：** 审计一个目录下所有项目的 settings.local.json。

```
gapfill scan /path/to/projects
```

扫描所有项目的权限配置，标记高危（`Write(/**)`、`Bash(curl:*)`）和低风险（`Bash(find:*)`、`Bash(python:*)`）权限。

### `sync` — 权限对比

**什么时候用：** 多个项目的权限规则不一致，想合并统一。

```
gapfill sync
```

展示差异并建议合并配置。只报告，不修改文件。

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

请参阅 [ROADMAP_zh.md](ROADMAP_zh.md)。

## 贡献

发现问题？提一个 [issue](https://github.com/russellglobal/gapfill/issues)。
想贡献代码？Fork 仓库后提交 PR。

如果觉得 gapfill 有用，一颗 ⭐ 能帮更多人找到它。

## 许可证

Apache 2.0

---

术语表请参阅 [docs/glossary.md](docs/glossary.md)。
项目哲学请参阅 [PHILOSOPHY_zh.md](PHILOSOPHY_zh.md) / [English](PHILOSOPHY.md)。
