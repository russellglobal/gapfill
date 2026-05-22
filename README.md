# gapfill（溜缝儿）

AI 开发者的通用工具箱 —— 类似 Java 生态的 Hutool，为 AI 辅助开发流程中的各种小痛点提供轻量解决方案。

## 安装

```bash
pip install -e .
```

或使用 pipx（推荐）：

```bash
pipx install -e .
```

## 使用

### 初始化新项目

```bash
# 在当前目录初始化
gapfill init

# 在指定目录初始化
gapfill init ./my-project

# 创建公开仓库
gapfill init --public

# 指定 Git 平台
gapfill init --platform gitee
```

### init 做了什么

1. **环境检查** — 检测 git、SSH key 等
2. **Git 初始化** — 如果目录没有 .git，自动 git init
3. **创建文件** — .gitignore、README.md、CLAUDE.md、settings.local.json、env-info.txt
4. **权限预置** — 基础级 + 低风险级权限，减少 AI 交互轮次
5. **环境探测** — 自动记录可用工具和版本
6. **远程仓库** — 如果有 gh CLI，自动创建 GitHub 仓库并推送

## 开发路线图

| 版本 | 功能 |
|------|------|
| MVP | init（项目初始化） |
| v2 | sync（跨项目配置同步）、perm（权限管理）、lang（语言设置）、feedback（一键提报） |
| v3 | roadmap（决策自动沉淀） |
| v4 | capture（高价值交互记录） |
| v5 | audit（Skill 安全扫描）、skill-localize（开源 Skill 本地化） |

## 许可证

MIT
