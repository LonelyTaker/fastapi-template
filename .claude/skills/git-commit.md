---
name: git-commit
description: 自动提交暂存的代码变更，生成符合规范的 commit message
metadata:
  type: skill
---

# Git Commit Skill

按照以下规范执行 Git 提交：

## 格式

```
<type>: <subject>

[optional body]

[optional footer]
```

## 规则

- **type**: 必须，提交类型（小写英文）
- **subject**: 必须，简短描述（不超过 50 字符）
- **body**: 可选，详细说明（每行不超过 72 字符）
- **footer**: 可选，关联的 Issue 或 PR

## 类型 (Type)

| 类型       | 说明                         |
| ---------- | ---------------------------- |
| `feat`     | 新功能                       |
| `fix`      | 修复 Bug                     |
| `docs`     | 文档变更                     |
| `style`    | 代码格式（不影响功能）       |
| `refactor` | 重构（不是修复也不是新功能） |
| `perf`     | 性能优化                     |
| `test`     | 添加/修改测试                |
| `chore`    | 构建/工具变更                |
| `ci`       | CI 配置变更                  |
| `revert`   | 回滚提交                     |

## 提交步骤

1. 运行 `git status` 查看未提交的文件
2. 运行 `git diff` 查看具体的变更内容
3. 根据变更内容确定 type 和 subject
4. 使用 `git add` 将相关文件添加到暂存区
5. 使用 `git commit -m` 创建提交，格式必须符合规范

## 注意事项

1. 使用中文描述 subject
2. type 后紧跟 `:`，冒号后有空格
3. subject 使用动词开头（如：添加、修复、更新、删除）
4. 不要在 subject 结尾添加句号
5. body 部分解释 **为什么** 而非 **是什么**