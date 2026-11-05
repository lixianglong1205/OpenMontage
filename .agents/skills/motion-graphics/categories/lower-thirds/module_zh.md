# lower-thirds — 分类模块

**姓名/标题条、标注层、社交叠加层** — 旨在叠在其他画面素材（footage）之上的图形。无需额外资产（+ 可选 logo）。通常使用 `export: alpha-overlay`（透明）。时长约 3–6 秒（或循环/保持）。

## 计划（Director）

`content`：`{ name, role, position (lower-left / lower-third / corner), brand_colors[] }`。默认 `export: alpha-overlay`。

## 词汇 / 依赖项

- 块：`caption-*`（pill-karaoke、neon-accent、editorial-emphasis）+ 注册表 **overlay** 块（`instagram-follow`、`tiktok-follow`、`yt-lower-third`、`x-post`、`spotify-card`、`macos-notification`）。
- 基元：slide/wipe-in · bar reveal · `glow` · fade/slide-out。

## 构建（复用优先）

复用最接近的 overlay/caption 块并设置 name / role / handle / 品牌色 / position；**或**手写一条从左擦入的条带（`scaleX` 从 0，`transform-origin:left`），文字在其后向上滑入，保持，再滑出。**透明背景**（`export: alpha-overlay` → `render --format webm/mov`）以便叠在画面素材上。保持在安全标题区（title-safe）下方条带内。
