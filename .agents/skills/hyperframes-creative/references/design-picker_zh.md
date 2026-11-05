# 设计选择器（Design Picker）

两阶段视觉选择器：先选情绪板（选定完整方向），再在各分类中微调。

## 目录

- 前提条件
- 构建选择器
- 提供访问与用户选择

## 前提条件

生成选项前请先阅读以下文档——它们定义了选项必须遵循的规则：

- `references/typography.md`
- `house-style.md`
- `references/video-composition.md`
- `visual-styles.md`
- `references/beat-direction.md`

## 构建选择器

1. 生成的选项须**与用户提示深度契合**。每个分类——不仅是架构——都要体现具体产品、品牌、受众与情绪。若选项泛化到可出现在任意选择器上，即为失败。

   **情绪板（Mood boards）** — 按创意空间需要数量而定（4–8 块）。每块板必须讲述关于品牌的**不同故事**，而非仅重排相同元素。自问：「定位这款产品有哪些真正不同的方式？」例如猫粮品牌可以是： playful 混乱、高端定位、舒适温馨、社交原生、风味展示、幽默主导、感官/食欲感。每种是不同叙事，而非同一布局换字体。

   **架构（Architectures）** — 每块情绪板至少一种，且视觉上彼此区分。使用 `{{prompt_headline}}` 与 `{{prompt_sub}}` 占位符。若用户提供了媒体资源，用作背景图（使用 `url(path)`，路径**不要**加引号——在 `style='...'` 内使用单引号会破坏属性）。

   **调色板（Palettes）**（5–6 组）— 以品牌世界命名，而非泛化情绪名。名称与色值应属于**这一**具体产品。始终混合深色 + 浅色 +  tinted。 **每组调色板在色块尺寸下必须视觉可辨。** 若两组背景明度相近且强调色色相相近，删掉其一。自测：用户在 14px 色块芯片上能否看出差异？不能则视为重复。

   **字体配对（Type pairings）**（5–6 组）— **在生成配对之前必须运行 typography.md 中的字体发现脚本。** 这不是可选项。下载 Google Fonts 元数据、运行脚本，并从输出中选取。否则你会反复落到训练数据里常见的 8 款字体（Bricolage Grotesque、Instrument Serif、Fraunces、Archivo Black、DM Serif Display、Space Grotesk、Fredoka）——那是默认偏好，不是 contextual 选择。匹配品牌能量与受众。按 typography.md 跨类别配对（切勿两个 sans-serif）。

2. 执行 `mkdir -p .hyperframes`，再将 [../templates/design-picker.html](../templates/design-picker.html) 复制到 `.hyperframes/pick-design.html`。
3. 用 Python 替换下列占位符（勿在 sed 中手工转义引号）：
   - `__ARCHITECTURES_JSON__` — 架构对象数组
   - `__PALETTES_JSON__` — 调色板对象数组
   - `__TYPEPAIRS_JSON__` — 字体配对对象数组
   - `__MOODBOARDS_JSON__` — 情绪板对象数组（格式见下）
   - `__PROMPT_JSON__` — 含提示上下文的对象（格式见下）

### 架构数据格式

每个架构对象须包含 `preview_html` 字段——在预览面板中渲染的 HTML。使用模板在运行时替换的占位 token：`{{bg}}`、`{{fg}}`、`{{ac}}`、`{{mt}}`、`{{hf}}`、`{{hw}}`、`{{bf}}`、`{{bw}}`、`{{cr}}`（圆角）、`{{pad}}`、`{{gap}}`、`{{shadow}}`、`{{g}}`（网格线颜色）、`{{fg3}}`/`{{fg6}}`/`{{fg8}}`/`{{fg15}}`（前景色透明度）、`{{ac3}}`/`{{ac5}}`/`{{ac25}}`（强调色透明度）。

**每个 token 都必须被使用。** 对所有卡片、按钮、容器应用 `{{cr}}`。对 elevated 元素（卡片、按钮、代码块）应用 `{{shadow}}`。用 `{{pad}}` 与 `{{gap}}` 控制间距。若某 token 未出现在 `preview_html` 中，该选项将无可见效果。

**密度很重要。** 每个架构预览须包含 **15+** 个不同元素，让用户真实感受布局。应包含：标题、副标题、正文段落、标签/overline、带数字的统计、次要统计、引用/证言、署名、带标题+正文的卡片、第二张卡片（不同处理）、代码/命令块、主按钮、次按钮、列表或标签、强调分隔线/规则，以及数据元素（表格行、进度条或图表）。

可选包含 `components`（组件样式规则）与 `dos`（注意事项）字符串——它们会出现在生成的 design.md 中。

**布局约束：** 所有预览 HTML 须使用百分比宽度或 `max-width: 100%`。所有 flex 行使用 `flex-wrap: wrap`。绝对定位装饰须留在带 `overflow: hidden` 的父级内。

**安全：** 架构 `preview_html` 不得包含 `<script>` 标签、事件处理器（`onclick`、`onerror` 等）或 `javascript:` URL。它通过 `innerHTML` 注入。

**图片 URL：** 在 `preview_html` 中使用背景图时，路径使用 `url(path/to/image.jpg)`，**不要**在路径外加引号。像 `url('path.jpg')` 这样的单引号会破坏结构，因为 `preview_html` 位于 `style='...'` 属性内——内层单引号会终止外层属性。

**调色板多样性：** 6 组调色板中始终混合浅色、深色与 tinted 背景——即便面向 calm/wellness 类提示亦然。

### 架构对象示例

```json
{
  "name": "Editorial Stack",
  "description": "Vertical rhythm with large type, pull quotes, and data callouts",
  "tag": "editorial / longform / narrative",
  "mood": "Confident, unhurried, typographically driven",
  "preview_html": "<div style='background:{{bg}};color:{{fg}};padding:{{pad}};min-height:100vh;font-family:\"{{bf}}\",sans-serif;font-weight:{{bw}};'><div style='max-width:100%;display:flex;flex-direction:column;gap:{{gap}};'><div style='font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:{{mt}};'>Overline Label</div><div style='font-family:\"{{hf}}\",serif;font-weight:{{hw}};font-size:48px;line-height:1.1;letter-spacing:-0.02em;'>The Headline Goes Here</div><div style='font-size:20px;color:{{mt}};max-width:70%;line-height:1.5;'>Subheading text that introduces the narrative arc of this composition with enough words to fill two lines.</div><div style='font-size:15px;line-height:1.7;color:{{fg}};max-width:65%;'>Body paragraph with real sentences. The quick brown fox jumps over the lazy dog. This gives a sense of text density and reading rhythm at the chosen type size.</div><div style='display:flex;gap:{{gap}};flex-wrap:wrap;'><div style='background:{{fg6}};border-radius:{{cr}};padding:{{pad}};flex:1;min-width:200px;box-shadow:{{shadow}};'><div style='font-size:36px;font-family:\"{{hf}}\",serif;font-weight:{{hw}};color:{{ac}};'>2.4M</div><div style='font-size:12px;color:{{mt}};margin-top:4px;'>Primary Stat</div></div><div style='background:{{fg6}};border-radius:{{cr}};padding:{{pad}};flex:1;min-width:200px;box-shadow:{{shadow}};'><div style='font-size:36px;font-family:\"{{hf}}\",serif;font-weight:{{hw}};color:{{fg}};'>87%</div><div style='font-size:12px;color:{{mt}};margin-top:4px;'>Secondary Stat</div></div></div><div style='border-left:3px solid {{ac}};padding:12px {{pad}};background:{{ac3}};border-radius:0 {{cr}} {{cr}} 0;'><div style='font-size:18px;font-style:italic;color:{{fg}};line-height:1.5;'>\"A pull quote that captures the key insight of the piece.\"</div><div style='font-size:12px;color:{{mt}};margin-top:8px;'>— Attribution Name</div></div><div style='background:{{fg3}};border-radius:{{cr}};padding:{{pad}};box-shadow:{{shadow}};'><div style='font-size:14px;font-weight:{{hw}};margin-bottom:8px;'>Card Title</div><div style='font-size:13px;color:{{mt}};line-height:1.5;'>Card body text with a different treatment than the main content area.</div></div><div style='background:{{ac5}};border:1px solid {{ac25}};border-radius:{{cr}};padding:{{pad}};box-shadow:{{shadow}};'><div style='font-size:14px;font-weight:{{hw}};color:{{ac}};margin-bottom:8px;'>Accent Card</div><div style='font-size:13px;color:{{fg}};line-height:1.5;'>Second card with a tinted accent treatment for variety.</div></div><div style='font-family:monospace;font-size:13px;background:{{fg8}};border-radius:{{cr}};padding:{{pad}};color:{{fg15}};box-shadow:{{shadow}};'>$ hyperframes render --output video.mp4</div><div style='display:flex;gap:12px;flex-wrap:wrap;'><button style='background:{{ac}};color:{{bg}};border:none;padding:10px 24px;border-radius:{{cr}};font-size:14px;font-weight:600;box-shadow:{{shadow}};cursor:pointer;'>Primary Action</button><button style='background:transparent;color:{{fg}};border:1px solid {{fg15}};padding:10px 24px;border-radius:{{cr}};font-size:14px;cursor:pointer;'>Secondary</button></div><div style='display:flex;gap:8px;flex-wrap:wrap;'><span style='background:{{fg6}};border-radius:100px;padding:4px 12px;font-size:11px;color:{{mt}};'>Tag One</span><span style='background:{{fg6}};border-radius:100px;padding:4px 12px;font-size:11px;color:{{mt}};'>Tag Two</span><span style='background:{{ac5}};border-radius:100px;padding:4px 12px;font-size:11px;color:{{ac}};'>Accent Tag</span></div><div style='height:1px;background:linear-gradient(to right,{{ac25}},{{fg6}},{{ac25}});'></div><div style='display:flex;justify-content:space-between;font-size:12px;color:{{mt}};border-bottom:1px solid {{g}};padding:8px 0;'><span>Data row label</span><span style='color:{{fg}};font-weight:600;'>1,234</span></div></div></div>"
}
```

### 情绪板数据格式

每块情绪板为各分类预选一项。用户在阶段 1 选情绪板，阶段 2 微调时这些选项已预填。

```json
{
  "name": "Terminal Precision",
  "description": "Code-forward, data-dense, CLI energy. Dark canvas, monospace body, sharp corners.",
  "theme": "dark",
  "arch_index": 0,
  "palette_index": 0,
  "type_index": 0,
  "corners_index": 0,
  "density_index": 0,
  "depth_index": 1,
  "easing_index": 0,
  "corners": "0px",
  "padding": "12px",
  "gap": "8px",
  "shadow": "0 2px 16px rgba(0,230,255,0.15)"
}
```

索引指向 ARCHITECTURES、PALETTES、TYPEPAIRS 数组。模板用各情绪板对应架构的 `preview_html`，并应用该板的调色板/字体，渲染迷你预览。

### 提示上下文数据格式

```json
{
  "title": "AI Coding Assistant",
  "headline": "Your Code, Understood.",
  "subline": "An AI coding assistant that reads your entire codebase.",
  "section_desc": "Layout options for your product launch"
}
```

`title` 显示在阶段 1 页眉。`headline` 与 `subline` 替换架构 `preview_html` 中的 `{{prompt_headline}}` 与 `{{prompt_sub}}`，使预览展示真实文案而非泛化占位。

### preview_html 中的内容 token

除标准设计 token（`{{bg}}`、`{{fg}}`、`{{ac}}` 等）外，架构 `preview_html` 还可使用：

- `{{prompt_headline}}` — 用户实际标题文案
- `{{prompt_sub}}` — 用户实际副标题文案

这使预览具备上下文——用户看到的是自己的内容被样式化，而非泛化占位符。

## 提供访问与用户选择

4. 提供文件：`cd <project-dir> && python3 -m http.server 8723 &`（使用 8723 或任意 8000 以上未占用端口；若 curl 检查失败，换下一端口）。验证：`curl -s -o /dev/null -w "%{http_code}" http://localhost:8723/.hyperframes/pick-design.html` — 仅当返回 200 时再分享链接。选择器**不要**用 `npx hyperframes preview`——会阻塞。仅从主对话线程启动 HTTP 服务。若作为派发任务或 subagent 运行，返回文件路径，由调用方提供服务。
5. 用户选定后，告知：「请从选择器复制 design.md 并粘贴到这里。」用户将 markdown 贴回对话。原样保存到项目根目录的 `design.md`——已是规范格式（YAML frontmatter + 散文章节）。用户粘贴后，结束后台服务：`kill %1` 或 `kill $(lsof -ti:8723)`。然后继续构建。

选择器输出符合 [google-labs-code/design.md](https://github.com/google-labs-code/design.md) 规范的文件：YAML frontmatter 含 `colors`、`typography`、`rounded`、`spacing` token，随后为 `## Overview`、`## Colors`、`## Typography`、`## Layout`、`## Elevation`、`## Components`、`## Do's and Don'ts` 等散文章节。
