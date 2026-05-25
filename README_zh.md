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

| 手动操作 | 用 gapfill |
|---------|-----------|
| 手动 `git init` | `gapfill init` 一次完成仓库初始化、配置，空仓库自动提交 |
| 每个命令都要点"允许" | 预置权限，确认次数减少约 80% |
| 从旧项目拷 `settings.local.json` | `gapfill init` 一键生成安全默认值 |
| 从零写 CLAUDE.md | `gapfill init --stack spring-boot` 初始化时一步到位，或已有项目用 `gapfill stack-claude-md` |
| 提交前不检查 | `gapfill review` 7 项预提交检查，几秒跑完 |
| 手动审计 10 个项目的权限 | `gapfill scan` 几秒钟扫完 |

## 子命令

### `init` — 项目初始化

**什么时候用：** 从零开始创建新项目。

```
gapfill init                           # 基础初始化
gapfill init ./my-project              # 指定目录初始化
gapfill init --stack spring-boot       # 初始化 + 一步生成 CLAUDE.md
gapfill init --stack spring-boot --lang zh  # 初始化 + 中文版 CLAUDE.md
```

创建 `.gitignore`、`README.md`、`settings.local.json`、`env-info.txt`。
自动检测 git 和 SSH key 状态。
加上 `--stack` 还会生成技术栈专属 CLAUDE.md。

1. **环境检查** — 检测 git、SSH key 等
2. **Git 初始化** — 如果目录没有 .git，自动 git init
3. **创建文件** — .gitignore、README.md、settings.local.json、env-info.txt
4. **权限预置** — 基础级 + 低风险级权限，减少 AI 交互轮次
5. **环境探测** — 自动记录可用工具和版本
6. **首次提交** — 自动 commit 所有文件

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
| v2 | `stack-md`（技术栈感知 CLAUDE.md 生成）**已完成**，`review`（提交前全局审查）**已完成**，`scan`（设置合规扫描）**已完成**，`auto-guard`（Auto Mode 兜底规则） |
| v3 | `perm`（权限管理）、`lang`（语言设置）、`feedback`（一键提报） |
| v4 | `capture`（高价值交互记录） |
| v5 | `publish`（中英发布工作流） |

### 暂缓功能
- `sync` — 跨项目权限对比（已实现，暂停 — 用户基数太小）
- `roadmap` — 决策自动沉淀（已被可行性研究流程替代）
- `audit` — Skill 安全扫描（已被 `scan` 设置合规扫描替代）
- 团队配置同步 — Anthropic Enterprise Admin 已覆盖

## 许可证

Apache 2.0

---

术语表请参阅 [docs/glossary.md](docs/glossary.md)。
项目哲学请参阅 [PHILOSOPHY_zh.md](PHILOSOPHY_zh.md) / [English](PHILOSOPHY.md)。
