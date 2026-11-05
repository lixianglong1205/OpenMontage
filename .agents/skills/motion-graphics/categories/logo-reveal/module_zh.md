# logo-reveal — 分类模块

一段 **logo sting / 品牌锁定（brand lockup）**。Logo 由用户提供（`asset_needs` = 一个 logo `source`，而非搜索）。约 3–5 秒。常为 `export: alpha-overlay`（可叠加到其他素材上的 sting）。

## 方案（Director）

`content`：`{ logo: <asset path>, tagline, url }`。封装：品牌色板（或从 logo 取色），优雅节奏。

## 词汇 / 依赖

- Block：**`logo-outro`**（逐块组装 + 光晕 bloom + 标语淡入 + URL 胶囊）。
- Rules：`rules/svg-path-draw`（矢量 logo 描边绘制）· `rules/scale-swap-transition` · `rules/3d-text-depth-layers`。
- Primitives：draw-on / mask-reveal / particle-assemble · `glow` bloom · `underline_sweep` · hold。

## 构建（复用优先）

复用 `logo-outro` 并替换 logo / tagline / url / palette；**或** 手写：将 logo 置于 hero 帧（CSS），通过 draw-on（SVG `stroke-dashoffset`）或 mask/scale 揭示，添加 glow bloom + 强调 underline sweep，再 hold。SVG logo 优先 draw-on；位图 logo 用 mask/scale + glow。以 overlay 导出时使用透明背景。
