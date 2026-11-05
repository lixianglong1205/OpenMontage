# Motion-Graphics 构建器

将 `shot-plan.json` 转为一个可渲染的 HyperFrames 合成（`compositions/index.html`）。一切留在 HF 生态内 —— HTML 是唯一事实来源；单条 **paused** 的 GSAP 时间轴承载全部动效；引擎对其 seek。按类别的构建规则在 `categories/<id>/module.md`；本文件是共享契约。

## 复用优先（默认）

默认 = **组合现有目录能力，而非手写**：

- `npx hyperframes add <block>`（registry）→ 就地定制。多数 block 把内容/数据写进各自脚本（只有少数暴露 CSS 变量参数），因此复用 = **添加 + 编辑**。
- `hyperframes-animation` 的规则 / 蓝图 / 过渡用于动效；运行时适配器（默认 GSAP）。

仅在手写以下情况：(a) 没有 block/规则覆盖的空缺，(b) `asset-fusion` 的 affordance 绑定。Director 在 `shot-plan.json` 中指定 block 与定制（`content.block` + `content.customize`）；见 `catalog-map.md`。

## HF 契约（不可协商）

- 根节点 `#stage` 携带 `data-composition-id`、`data-start="0"`、`data-duration=<s>`、`data-fps`、`data-width`、`data-height`。
- 恰好 ONE 条 `gsap.timeline({ paused:true })`；注册 `window.__timelines["<id>"] = tl;`；结尾 `tl.seek(0)`。**渲染关键动效绝不用 `tl.play()`**。不用定时器 / 异步 / 事件驱动的时间轴构建。仅有限次 repeat。
- **定时 clip** 需要 `class="clip"` + 稳定 `id`。单个全时长 clip 内、由时间轴驱动的组不必各自带 timing 属性。
- **字体**：优先本地 `@font-face`（.woff2）以保证确定性 / 离线渲染；CDN Google Fonts 能渲染（编译器缓存并注入 `@font-face`）但会告警且需网络。
- **仅确定性** —— 不用 `Date.now()` / `Math.random()` / 网络。

## 动效前先布局

先在 CSS 里搭好 **hero-frame 终态**（flex + padding；内容容器绝不用 absolute 偏移；根须定尺寸）。再用 `gsap.from()` 入场到该状态；出场靠过渡或末场。完整规则：`references/builder-contract.md`。

## IR → 合成

- `content.block` → `hyperframes add`（或内联）+ 应用 `content.customize`。
- 各类别 `content`（文本场景 / 图表数据 / fusion 位置 / news-tweet 内容）→ 按 `categories/<id>/module.md` 实现。
- 已解析的 `asset_needs` → 引用 **项目内冻结的本地路径**（绝不用远程 URL 或 prompt）。
- 来自 envelope 的 `palette[-1]` / 背景 + `font`。
- `export: alpha-overlay` → 透明背景；渲染 `--format webm`（或 `mov`）。

## 关键正确性（GSAP / seek）

对延迟出现的元素做 opacity 门控（入场前保持隐藏）。在 tween 边界 clamp（勿 overshoot 越过保持值）。允许的 ease：`power1–4`、`back`、`bounce`、`circ`、`elastic`、`expo`、`sine`（`.in/.out/.inOut`）。每场景一个 motif。运行 `hyperframes inspect` 查溢出 / 碰撞。

## 验证-修复

`hyperframes lint` → `inspect` → `render -q draft`。失败则修对应元素并重跑。（来自 Remotion 的既有作品由 `/remotion-to-hyperframes` SSIM  harness 评分。）**修复过程中绝不改固定的 `data-duration`。**
