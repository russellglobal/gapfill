# 开发路线图

## 已完成

### MVP — `init`

项目初始化：环境检查、git init、创建文件、权限预置、环境探测、首次提交。

### v2 — stack-claude-md / review / scan

| 功能 | 说明 |
|------|------|
| `stack-claude-md` | 技术栈感知 CLAUDE.md 生成（generic、spring-boot、react） |
| `review` | 提交前全局审查（副本一致性、导入有效性、危险权限、过期内容） |
| `scan` | 设置合规扫描（跨项目危险权限检测） |

## 计划中

### v3 — 多平台适配

扩展 gapfill 到 Claude Code 之外的 AI 编码平台（Cursor、Codex CLI、Copilot 等），保持核心 Python 引擎不变，为每个平台添加 adapter。

| 功能 | 说明 |
|------|------|
| `adapters/` 架构 | 平台抽象层，`init --platform <name>` 生成对应平台配置 |
| `cursor` adapter | Cursor 的 `.cursor/rules/` 配置生成 |
| `codex` adapter | OpenAI Codex CLI 配置生成 |
| `copilot` adapter | GitHub Copilot 配置生成 |
| `review` 扩展 | 识别新平台配置文件格式，适配权限审计 |
| `scan` 扩展 | 扫描多平台配置文件 |

**决策记录**：不使用 skillkit。gapfill 核心是配置治理逻辑（review/scan/sync），不是 skill 文件翻译，自建更合适。

### v4

`publish`（延期）—— 多语言文档同步与一致性检查。有价值但不紧急，等用户群国际化后再做。

## 不 pursued

| 功能 | 原因 |
|------|------|
| `perm` | JSON 编辑不需要 CLI 包装（scan 已足够） |
| `feedback` | `gh issue create` 已覆盖 |
| `lang` | 合并到 `publish` |
| `capture` | 概念有价值但边界不清，待真实用户反馈再审视 |
| `auto-guard` | 与 init/scan 重叠，且与 Anthropic 官方 Auto Mode 演进冲突 |
| `sync` | 已实现，暂停 — 用户基数太小 |
| `roadmap` | 已被可行性研究流程替代 |
| `audit` | 已被 `scan` 设置合规扫描替代 |
