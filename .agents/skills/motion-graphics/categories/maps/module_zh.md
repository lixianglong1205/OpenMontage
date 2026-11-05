# maps — 分类模块

地理动效：高亮区域、连接地点、缩放到某一位置。**首要决策：镜头是否需要真实底图**（卫星/街道/地形影像、地球仪，或缩放到真实地址）？据此选择通道（lane）。

## 规划（Director）

先设置 `content.lane`：

- **vector**（默认）— 风格化区域形状，无真实影像。原生支持且在 HF 中可实时运行，成本低。`asset_needs: []`。
- **basemap** — 需要真实卫星/暗色瓦片、地球仪，或缩放到真实地点。`asset_needs: [{ type: "map-bake", … }]`。**在 Source 阶段烘焙影像**：HF 禁止渲染时联网且要求确定性，因此实时瓦片（会重新拉取且每次渲染可能变化）不能作为影像层 — 烘焙将其冻结（顺带也更平滑）。见 Basemap 通道 + 确定性（Determinism）。

`content`：`{ lane, shot: highlight|flow|choropleth|labels|flag|pin-rollout|zoom-to, regions[], points[], basemap: satellite|dark, palette, headline, overlays: [label|pin|callout-card] }`。

`overlays` 与 `shot` 独立，两种通道均可用。**`callout-card`** = 固定卡片（旗帜芯片 + 统计 + 进度条）— 即「纪录片弹窗」（top #13）；可叠在任何 zoom-to/highlight 镜头上，不必单独作为一种 shot。

## 词汇 / 依赖

**Vector 通道**（D3 + TopoJSON — 复用现有地图族，勿重复造轮子）：

- 复用：`us-map`（+bubble/hex/flow）、`world-map`、`spain-map`。
- **手写实现**下列项（**不在**目录中 — 按下方签名构建，勿指望 `add`）：`geo-highlight`（N 国着色 + 标签 + 边界脉冲）、`geo-flow`（世界弧线 / 枢纽网络）、`flag-borders`（旗帜裁剪至国界内）、`pin-rollout`（城市依次脉冲 + 计数器）。
- 签名：国家填充交错 · 图钉落下 + 脉冲环 · 弧线 `stroke-dashoffset` 绘制 + 飞线 · choropleth 颜色揭示 · **viewBox** 缩放。

**Basemap 通道**（MapLibre，在 Source 烘焙 — 已验证流水线，`bake-basemap.mjs`，完全由环境变量驱动 — 适用于任意国家，不限于原型）：

- **烘焙** `bake-basemap.mjs`（puppeteer + MapLibre；环境驱动：`NAME STYLE COUNTRIES CENTER ZSTART ZEND PITCH BEARING FPS DUR`）：驱动相机 **zoom→hold**（`easeInOutCubic`），且**每帧前 `await map.once('idle')`**，确保每帧瓦片完整（Remotion `delayRender` 技巧 → 无瓦片弹出）。辅助脚本自行解析 Chrome、精确锁定依赖、按主体推导海外领土过滤，并在 **idle 超时时 loud fail**（可疑帧 → 非零退出）。_外部依赖：钉死的 CDN 库（maplibre/topojson/world-atlas）及 Esri/CARTO 瓦片端点为第三方 — 任何版本升级需重新核实可用性与 ToS。_ `preserveDrawingBuffer:true`，`fadeDuration:0`。辅助脚本随后**自行将帧编码为全 I 帧 MP4**（`ffmpeg -framerate FPS -i f%04d.png -c:v libx264 -g 1 -pix_fmt yuv420p`），并写入 **`$OUT`（默认 `cwd`）**，而非 skill 目录 → `<NAME>.mp4` + `<NAME>-coords.json`。
- **在 hold 视图导出 geo→screen**：对各国 `map.project()` → `<NAME>-coords.json` = `{ view, countries: [{ name, color, d (SVG path), bbox, label }] }`。zoom 后相机保持静态，路径与像素对齐。`label` 为**近似**锚点（本土环顶点平均 — 凹形国家按可读性微调）。消费 `coords.countries[i]`；`smooth-frde2`/`smooth-flag` 示例目录早于该辅助脚本，使用扁平 `{fr,de,…}` 形状，需适配接线。
- **Builder**：track 0 上 `<video>` 底图 + **SVG  overlay**，在 hold 期间动画国家**边界（`stroke-dashoffset` 绘制）** + **填充（色块揭示）** + 标签/图钉/卡片 — 均通过 `coords.json` 地理对齐。复现 Hera「卫星 + 动画彩色边界/标注」观感。
  - 同一投影路径也可作 SVG **`clipPath`**：将**旗帜（或任意纹理）裁剪进真实国界**，实现 _flag-in-borders_ — 比 flat 填色更丰富，叠在真实地图语境上（已验证：法国三色旗 + 暗色底图，`smooth-flag`）。导出要素的屏幕 **bbox** 与 path，以便旗帜条纹/纹理按国家尺寸缩放。
- **扩展 / 数据缺口**（按需扩展 `bake-basemap.mjs` — eval agent 已做）：**地球仪开场**（「从地球开始」）= MapLibre `projection:{type:'globe'}` 开场，再 ease 到 mercator 目标（辅助脚本默认 mercator）。**次国家级**区域（州/省）不在 world-atlas（仅国家）→ 使用 Natural Earth **admin-1** TopoJSON，或将质心投影为图钉（`pin-rollout`）。

## 构建（复用优先）

Vector：`npx hyperframes add <block>` → 就地编辑 regions/data/palette。Basemap：烘焙 `map.mp4` 作 track-0 `<video>`，将 overlay 绑定到锚点。

**克制（避免 cheesy — 自动建图最常翻车之处）：** 每个动画元素必须服务信息 — 区域、连线、标签、图钉、相机。**禁止**装饰性环境光晕、背景光斑、漂浮粒子、镜头光晕或 gratuitous bloom。动效 = 连续相机运动（viewBox 推/缩）+ 有目的、交叠的元素揭示 — 不是灯光秀。调色：颜色必须**承载含义** — 数据尺度（choropleth）、区分区域的分类填充（政治地图），或 1–2 个强调主体（高亮国家/路线）叠在中性底上。勿把颜色当**装饰**（某国琥珀色只为对比、光晕表「能量」）。画面应像干净广播地图，而非屏保。

**可读性（硬规则）：** 标签相对高亮形状及彼此偏移；限制在安全区内；标注 pill 不得压在其他标签或边界上（eval 曾出现 DE/PL「Oder–Neisse」pill 与 POLAND 标签重叠）。关键元素至少 ~0.3s 可读。

**署名（硬规则）：** 真实底图影像附带使用条款 — 底图在屏时须在合成中烘焙 credits 元素（Esri 卫星 → "Esri, Maxar, Earthstar Geographics"；CARTO → "© CARTO, © OpenStreetMap"）。小角标（见 `smooth-jp`）。对外发布不可省略。

**确定性（硬规则 — 原型中每条都踩过坑）：**

- 一切由 seek 时钟驱动；**勿用 `tl.call`** 做有状态更新（计数器、文本）→ proxy tween + `onUpdate`（tl.call 在 HF seek 下会冻结时间线）。
- SVG 缩放 = 动画 **viewBox**（勿手算 group transform 原点）。
- 居中 overlay（卡片/标签用 `transform: translate(-50%,…)` 居中）：仅动画 **opacity**，或外包一层居中 div — GSAP 动画 `y`/`scale` 会覆盖整个 transform 并破坏居中。
- 国家几何：过滤到**主体周围 lon/lat 框内**的多边形 — world-atlas 打包海外领土会撑爆 bbox（法国 + 圭亚那）。保留近岛（科西嘉、西西里），丢弃远岛。（`bake-basemap.mjs` 以顶点最多多边形 ± `KEEPMARGIN` 锚定 — 无大陆专用常量。）
- **瓦片世界尺度**：MapLibre 内部世界宽度为 `512·2^zoom`，与 raster `tileSize` 无关。Esri/CARTO raster → `tileSize:256`（正确）；512px / @2x / retina / vector 源需 `tileSize:512`，否则每级 zoom 差一级（曾静默 over-zoom 一次 — 法国顶底溢出画幅）。
- **反子午线**：跨越 ±180° 的要素（俄罗斯、斐济、新西兰）在逐顶点 `map.project()` 下会 smear。`bake-basemap.mjs` 在投影前**以相机中心为参考 unwrap 经度**；unwrap 后仍 span >180° 会 warn。
- **平滑 = 每帧完整瓦片 + eased 相机。** 烘焙中每截图前 `await map.once('idle')`（= Remotion `delayRender`），相机用 `easeInOutCubic` ease（= interpolate+Easing）。`preserveDrawingBuffer:true`，`fadeDuration:0`，大 `maxTileCacheSize`。
- **Overlay 对齐**：在**静止**相机下投影国界，仅在 hold 期间动画 overlay — 运动相机 + 固定投影 path 会漂移。
- **Hold 前隐藏态**：在 hold 才出现的 overlay 须在构建时用 `gsap.set` 设为隐藏（`scaleX:0`、满 `stroke-dashoffset`、`opacity:0`）— 裸 `fromTo` 在 tween 开始前**不会**应用「from」，否则 zoom-in 期间会以自然（可见、错位）状态显示。
- **为何必须烘焙**（真正原因 — 不只平滑）：烘焙将影像冻成**确定性**像素。实时 raster 瓦片每次渲染重拉且可能变化，且禁止渲染时联网。MapLibre **可以**在 HF 内实时渲染（只是卡顿：瓦片 pop、深 zoom 追不上加载）；暴露引擎每帧 `onBeforeCapture` hook（存在 — `frameCapture.ts:~1250`）可让实时**平滑** — 但**不能**消除为**确定性 + 离线可复现**而冻结瓦片的需求。故 `onBeforeCapture` 可替代烘焙的_平滑_角色，不能替代_冻结_角色。

## 范围外

3D  photorealistic 地标（Cesium 领域）· 按国/按模板 block（应参数化）· 图表（→ `charts`）。（引擎内_实时_ MapLibre 可行但今日仍卡顿 — 优先 bake；若引擎具备每帧 ready hook 再 revisit。）

## 注册

`director.md` 分类器行（通道分叉）+ `catalog-map.md` 的 `maps/geo` 行（加入 basemap 通道）。Phase 流水线不动。
