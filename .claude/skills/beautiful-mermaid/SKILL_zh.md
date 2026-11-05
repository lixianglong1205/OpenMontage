---
name: beautiful-mermaid
description: 使用 Beautiful Mermaid 库将 Mermaid 图表渲染为 SVG 和 PNG。当用户要求渲染 Mermaid 图表时使用。
---

# Beautiful Mermaid 图表渲染

使用 Beautiful Mermaid 库将 Mermaid 图表渲染为 SVG 和 PNG 图像。

## 依赖

本技能在 PNG 渲染时需要 `agent-browser` 技能。在进行 PNG 截图前请先加载该技能。

## 支持的图表类型

- **Flowchart（流程图）** - 流程、决策树、CI/CD 流水线
- **Sequence（时序图）** - API 调用、OAuth 流程、数据库事务
- **State（状态图）** - 状态机、连接生命周期
- **Class（类图）** - UML 类图、设计模式
- **Entity-Relationship（实体关系图）** - 数据库模式、数据模型

## 可用主题

Default、Dracula、Solarized、Zinc Dark、Tokyo Night、Tokyo Night Storm、Tokyo Night Light、Catppuccin Latte、Nord、Nord Light、GitHub Dark、GitHub Light、One Dark。

若未指定主题，使用 `default`。

## 常见语法模式

### 流程图边标签

边标签使用管道语法：

```mermaid
A -->|label| B
A ---|label| B
```

避免使用空格-短横线语法，可能导致渲染不完整：

```mermaid
A -- label --> B   # May cause issues
```

### 含特殊字符的节点标签

标签中含特殊字符时用引号包裹：

```mermaid
A["Label with (parens)"]
B["Label with / slash"]
```

## 工作流

### 步骤 1：生成或校验 Mermaid 代码

若用户提供的是描述而非代码，则生成合法的 Mermaid 语法。完整语法细节请参阅 `references/mermaid-syntax.md`。

### 步骤 2：渲染 SVG

运行渲染脚本生成 SVG 文件：

```bash
bun run scripts/render.ts --code "graph TD; A-->B" --output diagram --theme default
```

或从文件读取：

```bash
bun run scripts/render.ts --input diagram.mmd --output diagram --theme tokyo-night
```

其他运行时：
```bash
npx tsx scripts/render.ts --code "..." --output diagram
deno run --allow-read --allow-write --allow-net scripts/render.ts --code "..." --output diagram
```

会在当前工作目录生成 `<output>.svg`。

### 步骤 3：创建 HTML 包装页

运行 HTML 包装脚本，为截图做准备：

```bash
bun run scripts/create-html.ts --svg diagram.svg --output diagram.html
```

会创建最小 HTML 文件，以合适内边距和背景显示 SVG。

### 步骤 4：使用 agent-browser 捕获高分辨率 PNG

使用 agent-browser CLI 捕获高质量截图。完整 CLI 文档请参阅 `agent-browser` 技能。

```bash
# Set 4K viewport for high-resolution capture
agent-browser set viewport 3840 2160

# Open the HTML wrapper
agent-browser open "file://$(pwd)/diagram.html"

# Wait for render to complete
agent-browser wait 1000

# Capture full-page screenshot
agent-browser screenshot --full diagram.png

# Close browser
agent-browser close
```

对于更复杂的图表，可进一步增大视口，或在创建 HTML 包装页时使用 `--padding` 选项为图表留出更多空间。

### 步骤 5：清理中间文件

渲染完成后删除所有中间文件。仅保留最终的 `.svg` 与 `.png`。

需要清理的文件：
- HTML 包装页（如 `diagram.html`）
- 用于存放图表代码的临时 `.mmd` 文件
- 渲染过程中创建的其他文件

```bash
rm diagram.html
```

若创建了临时 `.mmd` 文件，一并删除。

## 输出

始终会生成两种输出：
- **SVG**：矢量格式，可无限缩放，文件较小
- **PNG**：高分辨率位图，在 4K（3840×2160）视口下捕获，图表最小宽度 1200px

除非用户明确指定其他路径，文件保存在当前工作目录。

## 主题选择指南

| 主题 | 背景 | 适用场景 |
|-------|------------|----------|
| default | 浅灰 | 通用 |
| dracula | 深紫 | 偏好深色模式 |
| tokyo-night | 深蓝 | 现代深色风格 |
| tokyo-night-storm | 更深蓝 | 更高对比度 |
| nord | 深色北极 | 柔和、平静的视觉 |
| nord-light | 浅色北极 | 浅色模式、柔和色调 |
| github-dark | GitHub 深色 | 与 GitHub UI 一致 |
| github-light | GitHub 浅色 | 与 GitHub UI 一致 |
| catppuccin-latte | 暖色浅色 | 柔和 pastel 风格 |
| solarized | 棕/奶油色 | Solarized 配色 |
| one-dark | Atom 深色 | Atom 编辑器风格 |
| zinc-dark | 中性深色 | 极简、无色彩倾向 |

## 故障排除

### 主题未生效

查看渲染脚本输出中的 `bg` 与 `fg` 值，或检查 SVG 开头标签中的 `--bg`、`--fg` CSS 自定义属性。

### 图表被裁切或显示不完整

- 检查边标签语法 — 使用 `-->|label|` 管道写法，不要用 `-- label -->`
- 确认所有节点 ID 唯一
- 检查节点标签中是否有未闭合的括号

### 渲染结果为空或 SVG 格式异常

- 渲染前在 https://mermaid.live 校验 Mermaid 语法
- 检查需转义的特殊字符（用引号包裹）
- 确保指定了流程图方向（`graph TD`、`graph LR` 等）
