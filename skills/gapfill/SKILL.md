---
name: gapfill
description: 溜缝儿 - AI 开发者的通用工具箱。初始化新项目、管理 Claude Code 配置、权限同步等
---

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
python "{SKILL_DIR}/scripts/init.py" <path> [选项]
```

### 参数
- **path**: 项目路径（可选，默认当前目录）
- **--public**: 创建公开仓库（默认私有）
- **--platform <平台>**: github / gitee / gitlab（默认 github）

### 示例
```bash
# 当前目录初始化
python "{SKILL_DIR}/../scripts/init.py" .

# 指定目录
python "{SKILL_DIR}/../scripts/init.py" ./my-project

# 创建公开仓库
python "{SKILL_DIR}/../scripts/init.py" ./my-project --public

# 指定平台
python "{SKILL_DIR}/../scripts/init.py" ./my-project --platform gitee
```

### 执行流程
1. 环境检查（git / SSH key）
2. Git 初始化（如无 .git）
3. 创建文件：.gitignore、README.md、CLAUDE.md、settings.local.json、env-info.txt
4. 权限预置：基础级 + 低风险级
5. 环境探测：记录可用工具和版本
6. 远程仓库：如有 gh CLI，自动创建 GitHub 仓库并推送

### 执行后
脚本执行完成后，向用户确认：
1. 显示创建的文件列表
2. 显示环境探测结果
3. 如有错误，提供解决建议
