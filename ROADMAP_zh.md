# 开发路线图

## 已完成

### MVP — `init`

项目初始化：环境检查、git init、创建文件、权限预置、环境探测、首次提交。

### v2 — stack-md / review / scan

| 功能 | 说明 |
|------|------|
| `stack-md` | 技术栈感知 CLAUDE.md 生成（generic、spring-boot、react） |
| `review` | 提交前全局审查（副本一致性、导入有效性、危险权限、过期内容） |
| `scan` | 设置合规扫描（跨项目危险权限检测） |

## 计划中

### v3

_待定_ — 优先验证 review/scan 的实际使用，再确定具体方向。

### v4+

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
