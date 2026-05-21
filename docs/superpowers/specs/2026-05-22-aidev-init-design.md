# aidev MVP: init 子命令设计规范

## 目标

为 `aidev` 项目创建 `init` 子命令，实现一人公司新项目初始化的 0 交互体验。

## 核心功能

```bash
aidev init [路径] [--public] [--platform github|gitee|gitlab]
```

### 执行流程（自动决策，0交互）

1. **环境检查**
   - 检测 `git` 是否可用
   - 检测 SSH key（`~/.ssh/id_ed25519` 或 `~/.ssh/id_rsa`）
     - 无 → 提示用户使用 `ssh-keygen` 生成并引导配置 GitHub SSH
   - 检测 GitHub/Gitee/GitLab SSH 连通性
     - 不通 → 提示用户配置

2. **本地检测**
   - 已有 `.git` → 跳到步骤 4（绑定 remote）
   - 有目录但无 `.git` → `git init`
   - 目录不存在 → `mkdir` + `git init`

3. **项目初始化**
   - `.gitignore`（通用模板，不绑定语言）
   - `README.md`（空白模板，项目名占位）
   - `CLAUDE.md`（最小模板：角色定义 + 编码原则 + 语言规则 + 会话恢复提示 + 复合命令指令规范）
   - `.claude/settings.local.json`（权限分级预置：基础级 + 低风险级）
   - `env-info.txt`（环境探测结果：可用工具、版本、OS）
   - 首次 commit

4. **GitHub/Gitee/GitLab 仓库**
   - `gh` CLI 可用 → `gh repo create`
   - `gh` 不可用 → 通过 REST API 创建（需要 PAT 引导）
   - 绑定 remote → `git push -u origin main`

### 关键设计决策

- **认证：** SSH 优先，一次配置全局复用
- **0交互为默认，有缺失才引导**
- **幂等：** 重复执行安全，不破坏已有状态
- **语言：** 所有 skill、命令、文档使用中文
- **权限预置：** 基础级 + 低风险级（默认），高风险级不启用
- **复合命令规范：** CLAUDE.md 中写入"一次一个命令"的指令，避免 `&&` 导致权限匹配失效
- **语言规则分层：** 对话中文、代码不强制翻译

### 权限分级

**基础级（默认）：** 版本检查、只读操作、Web 只读
**低风险级（默认）：** git 写操作、mkdir/cp、包管理器安装、常见开发工具
**高风险级（不启用）：** force push、reset --hard、docker run、ssh 等

### 多平台支持

| 平台 | API | SSH host | 认证 |
|------|-----|----------|------|
| GitHub | `https://api.github.com` | `git@github.com` | SSH 或 PAT |
| Gitee | `https://gitee.com/api/v5` | `git@gitee.com` | PAT |
| GitLab | `https://gitlab.com/api/v4` | `git@gitlab.com` | SSH 或 PAT |

### 技术栈

- Python 3（纯标准库，零依赖）
- 支持 Windows/Linux/macOS
- 子命令架构，为未来插件化预留基础
