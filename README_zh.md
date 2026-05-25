# gapfill（溜缝儿）

AI 开发者的通用工具箱 —— 为新项目自动初始化 Claude Code 权限、配置和文档骨架，让 AI 助手开箱即用。

[English](README.md) · [中文](README_zh.md)

## 安装

将 `skills/gapfill/` 目录复制到 Claude Code 的 skills 目录：

```bash
cp -r skills/gapfill ~/.claude/skills/gapfill
```

需要 **Python 3.8+** 和 **git**。零外部依赖。

## 使用

安装后，在 Claude Code 中直接说：

> "帮我初始化一个新项目"

或

> "帮我在 ./my-project 目录创建一个项目"

Claude 会调用 gapfill skill 执行初始化。

## init 做了什么

1. **环境检查** — 检测 git、SSH key 等
2. **Git 初始化** — 如果目录没有 .git，自动 git init
3. **创建文件** — .gitignore、README.md、settings.local.json、env-info.txt
4. **权限预置** — 基础级 + 低风险级权限，减少 AI 交互轮次
5. **环境探测** — 自动记录可用工具和版本
6. **首次提交** — 自动 commit 所有文件

## 架构

```
用户 ←→ gapfill Skill（对话层，SKILL.md）
                ↓ 调用
        内部 Python 脚本（执行层，scripts/init.py）
```

- **Skill 是用户界面**：处理对话、审查、异常
- **脚本是执行引擎**：保证速度和确定性，不消耗 token
- **不发布 PyPI**：随 skill 一起分发

## 开发路线图

| 版本 | 功能 |
|------|------|
| MVP | `init`（项目初始化）、`.gitignore`、`settings.local.json` 权限预置 |
| v2 | `stack-md`（技术栈感知 CLAUDE.md 生成）**已完成**，`scan`（设置合规扫描），`auto-guard`（Auto Mode 兜底规则） |
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

术语表请参阅 [docs/glossary.md](docs/glossary.md)
