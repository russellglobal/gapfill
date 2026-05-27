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

安装后，在 Claude Code 中告诉它运行 gapfill 子命令：

```
gapfill init              # 初始化新项目
gapfill init ./my-project # 在指定目录初始化
gapfill stack-md          # 生成技术栈专属 CLAUDE.md
gapfill review            # 提交前全局审查
gapfill scan              # 扫描危险权限
gapfill sync              # 跨项目权限对比
```

或直接使用 CLI：

```bash
python scripts/init.py [path]
python scripts/stack_md.py [path] [--stack name]
python scripts/review.py [path]
python scripts/scan.py [path]
python scripts/sync.py [root] [--base project_name]
```

**注意**：不要只说"初始化项目"——这可能会触发 Claude Code 的内置逻辑。请明确提到 gapfill 或溜缝儿。

## 子命令

### `init` — 项目初始化

1. **环境检查** — 检测 git、SSH key 等
2. **Git 初始化** — 如果目录没有 .git，自动 git init
3. **创建文件** — .gitignore、README.md、settings.local.json、env-info.txt
4. **权限预置** — 基础级 + 低风险级权限，减少 AI 交互轮次
5. **环境探测** — 自动记录可用工具和版本
6. **首次提交** — 自动 commit 所有文件

### `stack-md` — 技术栈专属 CLAUDE.md

根据预定义模板生成 CLAUDE.md，不调用 LLM。

| 技术栈 | 说明 |
|--------|------|
| `generic`（默认） | 通用项目，含分支工作流程和安全规则 |
| `spring-boot` | Spring Boot 3.x 约定、反模式、构建命令 |
| `react` | React 19 + TypeScript 约定、反模式、构建命令 |

如果 CLAUDE.md 已存在，建议写入 `.claude/gapfill-suggestions.md`（绝不覆盖）。

### `review` — 提交前全局审查

扫描项目：
- 副本一致性（src/ vs skills/src/）
- 导入有效性（通过 AST 检测死引用）
- settings 模板中的危险权限
- 过期内容（旧项目名、废弃引用）

如有错误，退出码为 1。

### `scan` — 设置合规扫描

扫描目录下所有项目的 `settings.local.json`，检查危险权限：
- **高危**: Write(/**), Edit(/**), Bash(curl:*), Bash(wget:*), WebFetch(domain:*)
- **低风险**: Bash(find:*), Bash(npx:*), Bash(python:*)

### `sync` — 跨项目权限同步

对比多个项目的权限，建议合并配置。

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

术语表请参阅 [docs/glossary.md](docs/glossary.md)
