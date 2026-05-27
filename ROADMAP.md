# Roadmap

## Completed

### MVP — `init`

Project initialization: environment check, git init, scaffold files, permission preset, environment probe, initial commit.

### v2 — stack-md / review / scan

| Feature | Description |
|---------|-------------|
| `stack-md` | Tech-stack-aware CLAUDE.md generation (generic, spring-boot, react) |
| `review` | Pre-commit project health check (copy consistency, import validity, dangerous permissions, stale content) |
| `scan` | Settings compliance audit (dangerous permission detection across projects) |

## Planned

### v3 — 多平台适配

扩展 gapfill 到 Claude Code 之外的 AI 编码平台（Cursor、Codex CLI、Copilot 等），保持核心 Python 引擎不变，为每个平台添加 adapter。

| Feature | Description |
|---------|-------------|
| `adapters/` 架构 | 平台抽象层，`init --platform <name>` 生成对应平台配置 |
| `cursor` adapter | Cursor 的 `.cursor/rules/` 配置生成 |
| `codex` adapter | OpenAI Codex CLI 配置生成 |
| `copilot` adapter | GitHub Copilot 配置生成 |
| `review` 扩展 | 识别新平台配置文件格式，适配权限审计 |
| `scan` 扩展 | 扫描多平台配置文件 |

**决策记录**：不使用 skillkit。gapfill 核心是配置治理逻辑（review/scan/sync），不是 skill 文件翻译，自建更合适。

### v4

`publish` (deferred) — Multi-language documentation sync and consistency check. Valuable but not urgent until user base grows internationally.

## Not Pursuing

| Feature | Reason |
|---------|--------|
| `perm` | JSON editing doesn't need CLI wrapper (scan is sufficient) |
| `feedback` | `gh issue create` already covers this |
| `lang` | Merged into `publish` |
| `capture` | Concept valuable but scope unclear; revisit with real user feedback |
| `auto-guard` | Overlaps with init/scan, competes with Anthropic's official Auto Mode evolution |
| `sync` | Built, paused — user base too small currently |
| `roadmap` | Replaced by this feasibility research process |
| `audit` | Replaced by `scan` for settings compliance |
