# webpage — 类别模块（搜索驱动）

**对网页 / 链接做动画**（「网站动画」用例）。搜索驱动：用户提供或指定 URL → 抓取/捕获 → 为其制作动画（滚动浏览、UI 揭示、光标演示、区域标注）。与为现有 _video file_（视频文件）加字幕（见 `/embedded-captions`）以及站点的旁白视频（见 `/website-to-video`）不同；此处源是 _web page_（网页），输出是简短的、无旁白的高光镜头。

## 源（Step 2）

通过 `hyperframes capture`（DOM + 截图）或用户提供的截图抓取页面 → 冻结为项目本地的 image(s)/DOM。`asset_needs`：`{ kind: web, source: <url>, treatment: none }`。

## 词汇 / 依赖

- Rules：`hyperframes-animation/rules/{3d-page-scroll, demo-page-scroll-spotlight, cursor-click-ripple, coordinate-target-zoom, viewport-change}`。
- Primitives：scroll pan · spotlight/dim · cursor move + click-ripple · zoom-to-region · callout pin + label。

## 构建（优先复用）

将捕获的页面作为底层；为其制作 **scroll-through**（沿页面高度 translateY 滚动浏览）、**spotlight** 关键区域（dim + highlight）、会移动并点击（ripple）的 **cursor**、向坐标 **zoom**，以及锚定在页面区域上的 **callout** 图钉/标签。遵守 `builder-contract.md`。

**与新闻文章高亮场景匹配的两条规则（见 `../news/module.md`）：**

- **高亮是扫入/动画开启的，而非预先应用** — spotlight 框擦入（`scaleX 0→1`），标记扫过某区域，callout 在 zoom 落定 _之后_ 弹出；页面从不以预标注状态开始。
- **锚定到真实元素位置** — `hyperframes capture` 提供页面 HTML/DOM，因此测量目标元素（`getBoundingClientRect` → stage-local）并精确 zoom/高亮，逐步进行（「高亮真实元素」技法）。不要凭目测坐标。
