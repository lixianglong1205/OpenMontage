---
name: web-design-guidelines
description: 审查 UI 代码是否符合 Web Interface Guidelines。在用户要求「审查我的 UI」「检查无障碍」「设计审计」「审查 UX」或「对照最佳实践检查我的站点」时使用。
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

对照 Web Interface Guidelines 审查文件。

## 工作原理

1. 从下方源 URL 获取最新指南
2. 读取指定文件（或向用户询问文件/匹配模式）
3. 对照已获取指南中的全部规则进行检查
4. 以简洁的 `file:line` 格式输出发现

## 指南来源

每次审查前先获取最新指南：

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

使用 WebFetch 获取最新规则。获取的内容包含全部规则及输出格式说明。

## 用法

当用户提供文件或匹配模式参数时：
1. 从上述源 URL 获取指南
2. 读取指定文件
3. 应用已获取指南中的全部规则
4. 按指南中指定的格式输出发现

若未指定文件，请询问用户要审查哪些文件。
