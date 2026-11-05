# Registry 发现

## 阅读 registry 清单

顶层 `registry.json` 列出所有可用条目：

```bash
curl -s https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json
```

每个条目包含 `name` 和 `type`（`hyperframes:example`、`hyperframes:block` 或 `hyperframes:component`）。

## 阅读条目的 manifest

每个条目都有包含完整元数据的 `registry-item.json`：

```
<base>/<type-dir>/<name>/registry-item.json
```

其中 `<type-dir>` 为 `examples`、`blocks` 或 `components`。

## 条目 manifest 字段

| 字段                   | 类型     | 必填 | 说明                                           |
| ---------------------- | -------- | ---- | ---------------------------------------------- |
| `name`                 | string   | 是   | kebab-case 标识符                              |
| `type`                 | string   | 是   | `hyperframes:block` 或 `hyperframes:component` |
| `title`                | string   | 是   | 人类可读标题                                   |
| `description`          | string   | 是   | 单行描述                                       |
| `tags`                 | string[] | 否   | 筛选标签（例如 `["data", "chart"]`）           |
| `dimensions`           | object   | block | `{ width, height }` — 仅 block                |
| `duration`             | number   | block | 时长（秒）— 仅 block                           |
| `files`                | array    | 是   | 要安装的文件（`path`、`target`、`type`）       |
| `registryDependencies` | string[] | 否   | 本条目依赖的其他 registry 条目                 |

## 可用条目

### Block

要获取始终最新的列表，请运行 `npx hyperframes catalog --type block`。下表按类别分组列出 97 个 block。**Block 名称 ≠ shader 名称**：shader-transition 类 block（例如 `domain-warp-dissolve`）包装一个 HyperShader 运行时，其内部名称会省略 `-dissolve`/`-warp` 后缀 — 规范名称见与 block 一同安装的 showcase HTML。

#### Shader 转场（14）

单 shader block；每个会安装一个 HyperShader 运行时 + 一个 showcase 合成。每个视频建议 ≤2 个。

| 名称                     | 说明                                                                     |
| ------------------------ | ------------------------------------------------------------------------ |
| `chromatic-radial-split` | 色差径向分裂                                                             |
| `cinematic-zoom`         | 戏剧性缩放模糊                                                           |
| `cross-warp-morph`       | 交叉扭曲 morph                                                           |
| `domain-warp-dissolve`   | 分形噪声域扭曲                                                           |
| `flash-through-white`    | 白色闪光交叉淡化（很少作为中性默认 — 见 SKILL.md 指引）                  |
| `glitch`                 | 数字 glitch 伪影                                                         |
| `gravitational-lens`     | 引力透镜畸变                                                             |
| `light-leak`             | 电影感漏光叠加                                                           |
| `ridged-burn`            | 脊状湍流 burn                                                            |
| `ripple-waves`           | 同心涟漪波畸变                                                           |
| `sdf-iris`               | 有符号距离场 iris 揭示                                                   |
| `swirl-vortex`           | 漩涡扭曲                                                                 |
| `thermal-distortion`     | 热霾式热畸变                                                             |
| `whip-pan`               | 快速镜头 whip-pan                                                        |

#### 转场画廊（13）

按系列分组展示多种 CSS / GSAP 转场风格的 showcase 合成。用作挑选 CSS 场景转场的参考；不宜原样嵌入。

| 名称                      | 说明                                |
| ------------------------- | ----------------------------------- |
| `transitions-3d`          | 3D 透视翻转与旋转                   |
| `transitions-blur`        | 基于模糊的场景转场                  |
| `transitions-cover`       | 覆盖 /  uncover 滑动                |
| `transitions-destruction` | 破坏性碎裂                          |
| `transitions-dissolve`    | 溶解与淡出                          |
| `transitions-distortion`  | 扭曲与畸变                          |
| `transitions-grid`        | 基于网格的 tile                     |
| `transitions-light`       | 基于光的 glow 与闪光                |
| `transitions-mechanical`  | 机械快门与 iris                     |
| `transitions-other`       | 其他创意（VHS、重力、morph）         |
| `transitions-push`        | 推入与滑动                          |
| `transitions-radial`      | 径向 wipe 与揭示                    |
| `transitions-scale`       | 缩放与 zoom                         |

#### Liquid Glass（7）

WebGPU + html-in-canvas 磨砂玻璃表面。**需要启用 WebGPU 的 Brave / Chrome canary** — 将 `PRODUCER_HEADLESS_SHELL_PATH` 指向该浏览器；引擎会自动传入 `--enable-unsafe-webgpu`。见 `/hyperframes-animation` → `adapters/typegpu.md`。

| 名称                          | 说明                                                                                    |
| ----------------------------- | --------------------------------------------------------------------------------------- |
| `ios26-liquid-glass`          | 3D iPhone（GLTF）+ iOS 26 主屏，玻璃 app 图标、shader 壁纸、通知                        |
| `macos-tahoe-liquid-glass`    | 3D MacBook（GLTF）+ macOS Tahoe 风格桌面，玻璃菜单栏、Finder、dock                      |
| `liquid-glass-widgets`        | 磨砂统计卡片、展示面板、aurora shader 上的 pill 芯片                                    |
| `liquid-glass-notification`   | 漂浮在 aurora shader 上的磨砂通知卡片                                                   |
| `liquid-glass-context-menu`   | 漂浮在 aurora shader 上的磨砂上下文菜单面板                                             |
| `liquid-glass-media-controls` | 在 aurora shader 上展开的磨砂媒体控制面板                                               |
| `vfx-liquid-glass`            | 用于 liquid-glass 效果的裸 VFX 合成外壳                                                 |

#### VFX（6）

HTML-in-canvas + WebGL 合成 block。底层 API 见 `/hyperframes-animation` → `adapters/three.md` 与 `adapters/html-in-canvas-patterns.md`。

| 名称                    | 说明                                                                                                    |
| ----------------------- | ------------------------------------------------------------------------------------------------------- |
| `vfx-iphone-device`     | GLTF iPhone 15 Pro Max + MacBook Pro，带 live HTML-in-canvas 屏幕、玻璃镜头 morph、360° 转台              |
| `vfx-liquid-background` | 有机液体模拟 — 细分平面上的顶点位移，HTML 浮于上方                                                      |
| `vfx-magnetic`          | VFX 外壳（磁力线效果）                                                                                  |
| `vfx-portal`            | VFX 外壳（portal 揭示）                                                                                 |
| `vfx-shatter`           | VFX 外壳（碎裂成片段）                                                                                  |
| `vfx-text-cursor`       | 黑色舞台上的光标 glow + 色差阴影射线 + 光谱边缘                                                         |

#### Showcase（6）

叙事驱动的 showcase 合成 — 带旁白的 YouTube 风格插入片段。多数包含捆绑 SFX。

| 名称                       | 说明                                                              |
| -------------------------- | ----------------------------------------------------------------- |
| `app-showcase`             | 三块漂浮智能手机屏幕，健身 app 产品展示                           |
| `apple-money-count`        | 计数器 $0 → $10,000，绿色闪光，钱币图标 burst，SFX                |
| `blue-sweater-intro-video` | 暖色 AI 创作者 intro，收束为 X follow 卡片                        |
| `north-korea-locked-down`  | 地图 zoom + 红色 scribble 圆圈，locked-down 弹出标签                |
| `nyc-paris-flight`         | 地图动画，飞机 NYC → Paris，标记圆圈，着陆弹出，SFX               |
| `vpn-youtube-spot`         | App Store 滚动，VPN 安装流程，SFX                                 |

#### 地图 + 数据可视化（8）

D3 + GSAP 动画地理与图表。

| 名称                               | 说明                                                                                               |
| ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| `us-map`                           | 美国 choropleth，分阶段州揭示，数值标签，渐变图例                                                  |
| `us-map-bubble`                    | 美国 bubble 地图 — 比例城市标记、标注、连接线                                                      |
| `us-map-flow`                      | 美国 flow 地图 — 动画起讫弧线                                                                      |
| `us-map-hex`                       | 美国 hex 网格地图 — 每州等权 hex + 数据填充                                                        |
| `spain-map`                        | 西班牙按自治区 choropleth — D3 conic conformal                                                     |
| `world-map`                        | 世界 choropleth + 旋转地球 inset，D3 Natural Earth                                                 |
| `data-chart`                       | 动画柱状 + 折线图，分阶段揭示，NYT 风格 typography                                                 |
| `flowchart` / `flowchart-vertical` | 决策树，SVG 连接线，便签节点，光标 + 打字修正（vertical = 竖屏）                                   |

#### 社交叠加层（7）

平台可识别的 UI 叠加。叠在节拍上或用作节拍结尾。

| 名称                 | 说明                                             |
| -------------------- | ------------------------------------------------ |
| `instagram-follow`   | 资料卡 + follow 按钮                             |
| `tiktok-follow`      | 资料卡 + follow 按钮                             |
| `yt-lower-third`     | YouTube 订阅 lower third，带头像                 |
| `x-post`             | X/Twitter 帖子卡片，带互动指标                   |
| `reddit-post`        | 帖子卡片，带 upvote 与评论                       |
| `spotify-card`       | 正在播放卡片，带专辑封面与进度条                 |
| `macos-notification` | macOS 风格横幅，带 app 图标与消息                |

#### 品牌 + 3D UI（2）

| 名称           | 说明                                                                |
| -------------- | ------------------------------------------------------------------- |
| `logo-outro`   | 逐块组装 logo，glow bloom，标语淡入，URL pill                       |
| `ui-3d-reveal` | UI 元素的透视 3D 揭示                                               |

#### 代码片段（24）

一个**逐字符键入代码或 shell 会话**的代码/终端窗口。主题 = 仅视觉 chrome；结构、接线与安装在所有 24 个中完全相同 — 按名称选一个，像任意 block 一样接线（`data-composition-id` + `data-start` + `data-track-index`，见 `wiring-blocks.md`）。两类 chrome：

**VS Code workbench（12）** — 完整编辑器 chrome（活动栏、侧边栏、标签页、集成终端、状态栏）。主题变体：`code-snippet-dark-2026`、`code-snippet-dark-modern`、`code-snippet-dark-plus`、`code-snippet-light-2026`、`code-snippet-light-modern`、`code-snippet-light-plus`、`code-snippet-high-contrast`、`code-snippet-high-contrast-light`、`code-snippet-monokai`、`code-snippet-solarized-light`、`code-snippet-visual-studio-dark`、`code-snippet-visual-studio-light`。

**Apple Terminal（12）** — macOS Terminal.app 窗口键入 shell 会话。配置文件 = 窗口配色：

| 名称                                         | 外观                                     |
| -------------------------------------------- | ---------------------------------------- |
| `code-snippet-apple-terminal-basic`          | 白底黑字                                 |
| `code-snippet-apple-terminal-clear-dark`     | 半透明深色背景                           |
| `code-snippet-apple-terminal-clear-light`    | 半透明浅色背景                           |
| `code-snippet-apple-terminal-grass`          | 黑底绿字                                 |
| `code-snippet-apple-terminal-homebrew`       | 黑底亮绿字，lime 光标                    |
| `code-snippet-apple-terminal-man-page`       | 淡黄底黑字                               |
| `code-snippet-apple-terminal-novel`          | 暖色 parchment 底，深棕字                |
| `code-snippet-apple-terminal-ocean`          | 深蓝底白字                               |
| `code-snippet-apple-terminal-pro`            | 黑底灰字，lime 光标                      |
| `code-snippet-apple-terminal-red-sands`      | 深红底沙色字                             |
| `code-snippet-apple-terminal-silver-aerogel` | 深灰底白字                               |
| `code-snippet-apple-terminal-solid-colors`   | 深紫底白字                               |

#### 代码动画（9）

上文静态 `code-snippet-*` 窗口主题的更丰富、以动效为先的对应物：每个都是自包含 1920×1080 block（约 5–8s），带暂停、确定性的 GSAP 时间线，_动画化_代码 — 打字、diff、morph、聚光或 GPU 英雄揭示 — 而非在编辑器/终端 chrome 内键入固定片段。**复用优先**：`npx hyperframes add <name>`，然后在原位定制内置代码/diff 内容；仅当没有 block 覆盖所需动效时才手写。

**DOM / 文本揭示（6）：**

| 名称                  | 说明                                                                                                                       |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `code-typing`         | 按 token 流式打字揭示，caret 跟随前沿（无 CSS 动画）— 屏幕上的 live-coding                                               |
| `code-diff`           | 以彩色 diff 展示编辑：删除行红色折叠，新增行绿色展开 — 行级 before/after                                                   |
| `code-morph`          | 一段 snippet 变为另一段，token 在位置间滑动（Shiki Magic Move）— 重构 / 一种状态到另一种                                   |
| `code-highlight`      | 高亮带扫过目标行，周围上下文变暗 — 聚光一行                                                                                |
| `code-scroll`         | 相机滚动长文件以居中 + 聚光目标行 — 浏览真实模块                                                                           |
| `code-snippet-flight` | 离散 snippet 从侧方飞入并堆叠成程序（block 级 FLIP）                                                                       |

**GPU / WebGL 英雄揭示（3）：** 更重，用于标题卡 / 英雄代码时刻。

| 名称                     | 说明                                                                                                        |
| ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `code-3d-extrude`        | 语法高亮代码在 lit 倒角 3D  slab 上，在真实空间中旋转并落定（真实 WebGL 深度）                              |
| `code-shader-dissolve`   | 代码从 seeded 噪声中解析，带色差 dissolve 前沿 + 边缘 glow，然后保持清晰                                    |
| `code-particle-assemble` | 数千 GPU 点飞向精确 glyph 像素并解析为可读语法高亮代码                                                      |

### Component

| 名称                 | 说明                                                                                                      | 标签                                             |
| -------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| `grain-overlay`      | 动画胶片颗粒纹理叠加                                                                                      | texture, grain, overlay, film                    |
| `shimmer-sweep`      | 用于 AI 点缀的 CSS 渐变光扫                                                                               | text, shimmer, highlight, effect                 |
| `morph-text`         | Gooey 文本 morph，循环可编辑词表（SVG threshold + GSAP blur）                                             | text, text-effect, typography, morph, gooey      |
| `grid-pixelate-wipe` | 场景间网格溶解转场                                                                                        | transition, wipe, grid, pixelate                 |
| `parallax-zoom`      | 中心卡片放大填满画面， siblings 视差向外（单一 `--pz-progress` 0→1）                                      | transition, zoom, parallax, grid, hero           |
| `parallax-unzoom`    | `parallax-zoom` 的逆过程 — 焦点卡片从全画幅缩小，siblings 视差进入（`--pu-progress`）                     | transition, reveal, unzoom, parallax, grid, hero |
