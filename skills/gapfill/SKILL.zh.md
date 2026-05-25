---
name: gapfill
description: 溜缝儿 - AI 开发者的通用工具箱。初始化新项目、管理 Claude Code 配置、权限同步等
---

## 安装

将 `skills/gapfill/` 目录复制到 Claude Code 的 skills 目录：

```bash
cp -r skills/gapfill ~/.claude/skills/gapfill
```

需要 **Python 3.8+** 和 **git**。零外部依赖。

## 触发条件

当用户提到以下任一表述时，调用此技能：
- "初始化项目" / "新建项目" / "创建项目"
- "git init" / "创建仓库"
- "设置 Claude 配置" / "权限配置"
- "同步权限" / "更新权限"
- "项目骨架"

## init 子命令

### 用法
```bash
python "{SKILL_DIR}/scripts/init.py" [path]
```

### 参数
- **path**: 项目路径（可选，默认当前目录）

### 示例
```bash
# 当前目录初始化
python "{SKILL_DIR}/scripts/init.py" .

# 指定目录
python "{SKILL_DIR}/scripts/init.py" ./my-project
```

### 执行流程
1. 环境检查（git / SSH key）
2. Git 初始化（如无 .git）
3. 创建文件：.gitignore、README.md、settings.local.json、env-info.txt
4. 权限预置：基础级 + 低风险级
5. 环境探测：记录可用工具和版本
6. 首次提交（chore: init project by gapfill）

### 执行后
脚本执行完成后，向用户确认：
1. 显示创建的文件列表
2. 显示环境探测结果
3. 如有错误，提供解决建议

**重要**：只描述 gapfill 实际已完成的操作。不要暗示尚未实现的能力（如远程仓库设置、后端框架初始化等）。init 完成后，简单询问"接下来需要做什么？"即可，不要列出不存在的功能。

## sync 子命令

### 用法
```bash
python "{SKILL_DIR}/scripts/sync.py" [root] [--base 项目名]
```

### 参数
- **root**: 扫描目录（可选，默认当前目录的父目录）
- **--base, -b**: 基准项目名称（可选，默认根据当前工作目录自动检测）

### 示例
```bash
# 自动检测基准项目
python "{SKILL_DIR}/scripts/sync.py" /path/to/projects

# 明确指定基准项目
python "{SKILL_DIR}/scripts/sync.py" /path/to/projects --base my-project
```

### 执行流程
1. 扫描目录树，查找包含 `.claude/settings.local.json` 的项目
2. 收集每个项目的 `permissions.allow` 规则
3. 合并所有唯一规则，计算与基准项目的差异
4. 打印项目摘要和规则差异
5. 输出 JSON 供 Claude 处理并展示给用户

### 执行后
脚本执行完成后：
1. 向用户展示差异报告
2. 询问哪些规则需要同步
3. 输出更新后的 `settings.local.json` 内容（不要自动写入文件）

**重要**：生成任何文件变更前必须询问用户确认。永远不要自动修改 `settings.local.json`。
