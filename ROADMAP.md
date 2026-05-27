# Roadmap

## Completed

### MVP — `init`

Project initialization: environment check, git init, scaffold files, permission preset, environment probe, initial commit.

### v2 — stack-claude-md / review / scan

| Feature | Description |
|---------|-------------|
| `stack-claude-md` | Tech-stack-aware CLAUDE.md generation (generic, spring-boot, react) |
| `review` | Pre-commit project health check (copy consistency, import validity, dangerous permissions, stale content) |
| `scan` | Settings compliance audit (dangerous permission detection across projects) |

## Planned

### v3

_TBD_ — validate review/scan adoption first before committing to a specific feature.

### v4+

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
