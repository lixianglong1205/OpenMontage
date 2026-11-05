# HyperFrames — 完整能力清单

截至当前工作区，HyperFrames 中可实现的一切能力，综合自对全部 7 个包、16 项技能及完整 registry 的直接源码阅读。

> **如何阅读本文件。** 请先浏览下方 **目录**。 **请勿线性通读本文件** — 这是一份 700+ 行的清单；每次会话从上到下通读会浪费上下文。当分镜或某个节拍需要特定能力（HTML-in-Canvas、着色器转场、音频驱动、动态计数器等）时，直接跳转到对应章节。

你并不限于从网站抓取到的内容。你可以从零编写着色器、搜索并下载 registry 区块、构建 Three.js 场景、编写自定义 WebGL 效果、使用任意 Web API — 浏览器能渲染的一切皆可。

实现模式（可运行代码）见 `techniques.md`。本文件是 **WHAT**；techniques.md 是 **HOW**。

## 基本规则

- **确定性：** 禁止 `Math.random()`、`Date.now()`、`requestAnimationFrame`、`repeat: -1`。渲染引擎会精确 seek 到时间戳。
- **时间轴契约：** 必须同步设置 `window.__timelines["composition-id"] = tl`。时间轴长度定义合成时长。
- **子合成：** 通过 `data-composition-src` 加载外部 `.html` 文件。自动嵌套时间轴、作用域 CSS、作用域脚本。
- **Linter：** 60+ 条规则。渲染前运行 `npx hyperframes lint`。可捕获缺失时间轴、重叠 clip、路径错误、GSAP 错误等。

## 目录

| #   | 章节                                              | 涵盖内容                                                                                                                                                                                                                  |
| --- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **合成基础**                         | 数据属性、时间轴契约、分辨率预设（1080p、4K、竖屏、方形、自定义）                                                                                                                                    |
| 2   | **动画引擎（6 个适配器）**                   | GSAP + 15 个插件、Anime.js v4、CSS @keyframes、WAAPI、Lottie（lottie-web + dotlottie）、Three.js（hf-seek 事件）                                                                                                                |
| 3   | **着色器转场（14 种 WebGL）**                    | domain-warp、ridged-burn、whip-pan、sdf-iris、ripple-waves、gravitational-lens、cinematic-zoom、chromatic-split、swirl-vortex、thermal-distortion、flash-through-white、cross-warp-morph、light-leak、glitch — 以及自定义 GLSL |
| 4   | **CSS 场景转场（30+）**                      | 推/滑、缩放/变焦、径向/裁剪、3D 翻转、模糊、溶解、遮罩/百叶窗、漏光/胶片 burn、畸变/故障、机械/快门、网格溶解、破坏/burn、VHS/重力/变形 — 6 种时长预设                       |
| 5   | **视觉效果 + 纹理**                        | 文本标记（高亮、圆圈、爆发、涂鸦、叉线）、颗粒/噪声、漏光、胶片 burn、暗角、辉光、纸张纹理、扫光                                                                                 |
| 6   | **字幕技巧**                               | 逐词卡拉 OK、强度档位、5 种退出样式、6 种调性映射、逐词样式触发、7 种音频源格式、定位辅助                                                                                       |
| 7   | **音频驱动动画**                         | 低音→缩放、中频→形状、高音→辉光；任意 GSAP 属性；频段提取脚本；禁止模式                                                                                                                                  |
| 8   | **HTML-in-canvas**                                   | 实时 DOM 作为 GPU 纹理（drawElementImage）、Three.js 平面、HTML 上的 WebGL 着色器、7 个 VFX 区块（iPhone/MacBook 设备、液体、玻璃、磁吸、传送门、碎裂、文本光标）                                                 |
| 9   | **Three.js / WebGL 自定义场景**                   | 完整 3D：AnimationMixer、自定义 GLSL、后处理、GLTF 模型、灯光、相机、材质 — 均通过 hf-seek 保持确定性                                                                                                  |
| 10  | **SVG / canvas / 可变字体**                    | SVG 路径绘制、Canvas 2D 程序化艺术、CSS 3D 卡片、逐词排版、可变字体轴、逐字输入、速度匹配切镜、MotionPath                                                                                 |
| 11  | **媒体：视频、音频、TTS**                         | 视频合成 + 帧注入、音频混音器（多轨）、Kokoro TTS（54 种音色、9 种语言）、Whisper/Groq/OpenAI 转写、背景移除（u2net）                                                              |
| 12  | **Registry（51 个区块 + 4 个组件 + 8 个示例）** | 社交叠加层（8）、展示（5）、数据可视化（2）、Logo 品牌（1）、3D/VFX（7）、着色器转场（14）、转场画廊（13）、组件（grain、shimmer、pixelate、texture-mask）、8 个入门示例                    |
| 13  | **CLI（25 条命令）**                                | init、add、catalog、play、preview、publish、render（MP4/WebM/MOV/PNG、HDR、GPU、并行）、lint、validate、inspect、snapshot、capture、tts、transcribe、remove-background、doctor 等                                     |
| 14  | **Linter（60+ 条规则）**                               | Core、media、GSAP、captions、composition、adapters、textures、fonts — 以及异步 URL 检查                                                                                                                                     |
| 15  | **Player Web 组件**                             | `<hyperframes-player>`，含 seek/play/pause API、11 个事件、媒体镜像、运行时自动注入                                                                                                                                   |
| 16  | **Engine + Producer**                                | MP4/WebM/MOV/PNG 输出、HDR（PQ/HLG）、透明（ProRes）、GPU 编码（NVENC/VideoToolbox/VAAPI/QSV）、并行渲染、视频帧注入                                                                            |
| 17  | **Studio（浏览器内 NLE）**                          | 时间轴编辑器、拖拽/调整 clip、资源浏览器、渲染队列、lint 弹窗、字幕编辑器、元素拾取                                                                                                                     |
| 18  | **确定性保证**                           | 无 Math.random、无 Date.now、无 RAF、无 repeat:-1、无回调、同步构建                                                                                                                                       |
| 19  | **变量 / 参数化**                     | 类型化运行时变量（string、color、number、boolean、enum）、CLI 覆盖、严格校验                                                                                                                                 |
| 20  | **子合成**                                 | 外部文件或内联 template、自动嵌套时间轴、作用域 CSS、作用域脚本、变量继承                                                                                                                       |
| 21  | **全局运行时 API**                              | 25+ 个 window 全局变量：时间轴、player、变量、适配器、钩子                                                                                                                                                            |
| 22  | **Skills（16）**                                      | hyperframes、cli、media、registry、contrast、animation-map、website-to-video、remotion、gsap、animejs、css-animations、waapi、lottie、three、tailwind、contribute-catalog                                                       |
| 23  | **References（15 篇文档）**                             | transitions、css-patterns、dynamic-techniques、motion-principles、typography、narration、captions、audio-reactive、transcript-guide、techniques、beat-direction、visual-styles 等                                        |
| 24  | **Documentation（27 页）**                         | 指南 + 包文档，涵盖渲染、HDR、html-in-canvas、性能、prompting、排错等                                                                                                                    |

---

## 1. 合成基础

### 运行时识别的数据属性

- **根合成：** `data-composition-id`、`data-start`、`data-duration`、`data-width`、`data-height`、`data-composition-src`（外部子合成）、`data-composition-duration`、`data-composition-variables`（JSON）、`data-variable-values`（覆盖）
- **每个 clip：** `id`、`data-start`、`data-duration`、`data-track-index`、`class="clip"`，可选 `data-media-start`、`data-volume`、`data-playback-start`
- **子合成宿主：** `data-composition-id`、`data-composition-src` 或内联 `<template id="${compId}-template">`
- **解析器还会读取：** `data-type`（composition|text）、`data-end`、`data-keyframes`（JSON）、`data-x|y|scale|opacity`、`data-color|font-size|font-weight|font-family|text-shadow|outline|highlight*`、`data-layer`（z-index，时间轴已弃用但音频混音器层仍用）、`data-resolution`、`data-composition-width|height`

### 时间轴契约

- `gsap.timeline({ paused: true })` 注册在 `window.__timelines["<composition-id>"]`
- 主时钟（TransportClock + WebAudioTransport）通过 `tl.totalTime(t, false)` 或 `tl.seek(t, false)` 驱动时间轴
- 框架自动嵌套子合成时间轴
- 时长来自根上的 `data-duration`，而非 GSAP 长度
- 要求同步构建时间轴（禁止 async/await/setTimeout）
- 循环由 `<hyperframes-player>` 处理，而非 GSAP `repeat: -1`

### 分辨率预设

VALID_CANVAS_RESOLUTIONS：默认 1920×1080、竖屏 1080×1920、方形 1080×1080、4K、1440×2560，以及用于 `--resolution` CLI 标志的 `normalizeResolutionFlag`。

---

## 2. 动画引擎（6 个确定性帧适配器）

运行时按顺序注册这些适配器；每个实现 `discover()` / `seek({time})` / `pause` / `play?` / `revert`：

| 适配器                            | 驱动对象                                                                | 加载方式                                                     | 要点                                                                                                   |
| ---------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| GSAP (createGsapAdapter)           | 主时间轴 + 注册在 `window.__timelines[<id>]` 上的所有 tween    | CDN `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js` | 插件通过标准 GSAP register；HyperFrames 不 patch THREE.Clock（改用 `__hfThreeTime`） |
| Anime.js v4 (createAnimeJsAdapter) | 推入 `window.__hfAnime` 的 Anime 实例                                  | CDN `animejs@4.0.2/lib/anime.iife.min.js` 或 ESM                | 适配器将合成秒数乘以 1000 转为 ms                                                     |
| CSS animations (createCssAdapter)  | 任意具有 computed `animation-name` 的元素                                    | 声明式 `@keyframes`                                        | WAAPI 不可用时回退到负 `animation-delay`                                           |
| WAAPI (createWaapiAdapter)         | 文档上所有 Animation 对象                                             | `element.animate()`                                             | 使用 `document.getAnimations()`                                                                           |
| Lottie (createLottieAdapter)       | `window.__hfLottie` 数组；支持 lottie-web + dotlottie-web                | CDN `lottie.min.js` + `@lottiefiles/dotlottie-web`              | `goToAndStop(time*1000)` 或 `setCurrentRawFrameValue` / `seek(%)`                                         |
| Three.js (createThreeAdapter)      | `window.__hfThreeTime` + 派发 `CustomEvent("hf-seek", {detail:{time}})` | ESM CDN `three@0.181.2/+esm`                                    | 合成的渲染循环监听 `hf-seek`；模式：`mixer.setTime(time)`                            |

### GSAP 插件（文档化模式）

- **TextPlugin** — 在 `tl.call` 中做文本变更（skills/gsap/references/effects.md）
- **MotionPathPlugin** — 沿曲线约束的 tween（skills/hyperframes/references/techniques.md）
- **CustomEase** — 从 Remotion 风格时序导入的贝塞尔 ease
- **ScrollTrigger / Flip / SplitText / Draggable / Inertia / Observer / ScrambleText / CustomWiggle / CustomBounce / ScrollSmoother / GSDevTools** — 加载后且 tween 在已注册的 paused 时间轴上即可原生工作，但无专用 HyperFrames 适配器
- Producer 在需要时自动注入 ScrollTrigger CDN（packages/producer/src/services/htmlCompiler.ts）

---

## 3. 着色器转场 — @hyperframes/shader-transitions

14 个具名 WebGL 片段着色器。共享 uniform：`u_from`、`u_to`、`u_progress`、`u_resolution`、`u_accent`、`u_accent_dark`、`u_accent_bright`。

### 14 种着色器

| 名称                | 视觉效果                                                                                 | 说明                                                                                                                              |
| ------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| domain-warp         | 多 octave FBM 反向扭曲两场景；有机溶解边缘 + accent 闪白 | 使用 NQ 噪声 bundle                                                                                                               |
| ridged-burn         | Ridged multifractal 遮罩揭示 B；accent → 亮 → 白 burn 斜坡；火花          | NQ                                                                                                                                 |
| whip-pan            | 10 采样水平运动模糊 + 横向交叉淡入淡出                                   | 无噪声                                                                                                                           |
| sdf-iris            | 宽高比校正圆形 SDF 扩张 + accent 着色光晕环                       | —                                                                                                                                  |
| ripple-waves        | 径向驻波 UV 位移 + 着色交叉淡入淡出                                | —                                                                                                                                  |
| gravitational-lens  | 向中心 pinch 拉扯 + R/B 色差分离                                    | —                                                                                                                                  |
| cinematic-zoom      | 12 个 RGB 偏移径向变焦模糊采样（色差变焦拖尾）                         | —                                                                                                                                  |
| chromatic-split     | R/B 径向通道外移/内移；G 固定                                     | 区别于 CSS 色差                                                                                             |
| swirl-vortex        | 逆时针漩涡 + FBM 噪声；入场景 reciprocal                                       | NQ                                                                                                                                 |
| thermal-distortion  | 垂直 sin + FBM 水平位移；暖色薄雾                                  | NQ                                                                                                                                 |
| flash-through-white | 经白色中点淡入淡出 — 场景间可见白闪                     | 无 accent。仅当品牌明确需要白闪节拍边界时使用；**不是**中性「默认」转场。 |
| cross-warp-morph    | FBM 向量场位移两场景；第三层 FBM 偏置不规则擦除                | NQ                                                                                                                                 |
| light-leak          | 固定画外漏光 + 指数衰减 + accent 暖色 + ridge 耀斑            | 硬编码漏光锚点                                                                                                             |
| glitch              | 行位移 + RGB 横向分离 + 扫描调制 + 色调分离 + 闪烁      | 确定性                                                                                                                      |

### 公开 API

```js
HyperShader.init({
  bgColor: "#0b0f14",
  accentColor: "#f59e42",
  scenes: ["scene1", "scene2"],
  transitions: [{ time: 3, shader: "sdf-iris", duration: 0.65, ease: "power2.inOut" }],
  timeline: gsap.timeline({ paused: true }),
  compositionId: "main",
  previewCaptureFps: 30,
});
```

- 能力探测：`isHtmlInCanvasCaptureSupported()`（Chrome layoutSubtree/drawElementImage）
- 调参：`?__hf_shader_capture_scale=`（0.25–1）、`?__hf_shader_loading=`（internal|player|none）
- 缓存：PNG 快照用 IndexedDB；最多 2 个带纹理转场同时存活
- 回退（`applyFallbackTransition`）：capture / texImage2D 失败时用 smoothstep 透明度 tween
- Engine 模式在设置 `window.__HF_VIRTUAL_TIME__` 时跳过 GL/capture（producer 使用元数据）

你也可以 **从零编写自定义 GLSL 着色器** — 任意片段着色器均可配合标准 uniform 使用。

---

## 4. CSS 场景转场（30+ 具名模式）

文档位于 skills/hyperframes/references/transitions/，共 14 个分类文件。均由 GSAP 驱动，同一合成内不可与着色器转场混用。

### 按分类

| 分类                         | 模式                                                                                         |
| -------------------------------- | ------------------------------------------------------------------------------------------------ |
| Push / slide (css-push.md)       | Push slide、vertical push、elastic push、squeeze                                                 |
| Scale / zoom (css-scale.md)      | Zoom through、zoom out、scale-up swap                                                            |
| Radial / clip (css-radial.md)    | Circle iris、diamond iris、diagonal split                                                        |
| 3D (css-3d.md)                   | 3D card flip、hinge door                                                                         |
| Blur (css-blur.md)               | Crossfade、blur crossfade、focus pull                                                            |
| Dissolve (css-dissolve.md)       | Color dip（gap-to-black）、staggered color blocks（2-block、5-block）                              |
| Cover (css-cover.md)             | Horizontal blinds、vertical blinds（可变条数：6 / 12 / 20）                          |
| Light (css-light.md)             | Light leak overlays、overexposure burn、film burn                                                |
| Distortion (css-distortion.md)   | Glitch（CSS — RGB 层抖动）、chromatic aberration、ripple                                    |
| Mechanical (css-mechanical.md)   | Shutter（两半）、clock wipe（9 点旋转楔形）                                          |
| Grid (css-grid.md)               | Grid dissolve（12 或 120 格）、grid pixelate wipe                                              |
| Destruction (css-destruction.md) | Page burn（SVG clip-path + canvas char rim）                                                      |
| Other (css-other.md)             | VHS tape（条带 seeded jitter）、gravity drop、morph circle、blur through、directional blur |
| Rejected                         | Star iris、tilt-shift、lens flare（勿用 — 非 CSS 可实现的写实效果）                                |

### 时长预设

| 预设   | duration | ease                   |
| -------- | -------- | ---------------------- |
| snappy   | 0.2s     | power4.inOut           |
| smooth   | 0.4s     | power2.inOut           |
| gentle   | 0.6s     | sine.inOut             |
| dramatic | 0.5s     | power3.in → power3.out |
| instant  | 0.15s    | expo.inOut             |
| luxe     | 0.7s     | power1.inOut           |

---

## 5. 视觉效果 + 纹理

### 标记/强调模式（css-patterns.md）

| 模式      | 作用                      | 实现                            |
| --------- | --------------------------------- | ----------------------------------------- |
| highlight | 黄色条在文字后擦入      | CSS bar + GSAP scaleX 0→1                 |
| circle    | 手绘红圈绕词   | CSS border ellipse + back.out scale       |
| burst     | 从词心 12 条径向尖刺 | DOM line 数组，--len/--angle vars        |
| scribble  | 波浪下划线随时间绘制    | SVG `<path>` quadratic + stroke-dash GSAP |
| sketchout | 文字上交叉叉线       | 两条 2px 旋转线                     |

### 颗粒 / 噪声

- **grain-overlay**（registry 组件）：SVG feTurbulence data-URL + CSS keyframe jitter，`steps(1)`，默认 opacity 0.15
- **分层 radial-gradient 颗粒**（推荐模式）：无 SVG、无 canvas-taint、各处都快

### 光效 / 胶片

- Light leak 转场（CSS + 着色器变体）
- Overexposure burn — `brightness()` 斜坡 + flash 叠加层
- Film burn — 多层琥珀/橙/红 radial
- Vignette — radial-gradient 叠加层
- Paper texture（在 registry/examples/warm-grain/）

### 辉光

- 字幕文本辉光：textShadow 半径绑定高音频段（仅活动词，绝不在父容器）
- 径向辉光背景：CSS gradient / 模糊 blob

---

## 6. 字幕技巧

### 动画样式

- 基线：逐词卡拉 OK 高亮（各能量档）
- 强度档位：accent + 辉光 + 15% 缩放（高能量）→ 3% 缩放（低能量）
- 按能量退出（dynamic-techniques.md）：scatter、drop、collapse、fade+slide、fade
- 调性映射（captions.md）：scale-pop `back.out(1.7)`、fade+slide `power3.out`、typewriter、bounce、`elastic.out`、word-by-word

### 逐词样式触发

- 品牌/产品名
- 全大写
- 数字/统计
- 情感关键词
- CTA
- 标记高亮模式（上文 5 种）

### 字幕时序的音频源

| 来源                                     | 格式   | 粒度       |
| ------------------------------------------ | -------- | ----------------- |
| hyperframes transcribe（本地 whisper.cpp） | JSON     | 词级        |
| OpenAI verbose_json                        | JSON     | 词级        |
| Groq verbose_json                          | JSON     | 词级        |
| 手工编写                          | JSON     | 词级        |
| SRT                                        | text     | 仅短语级 |
| VTT                                        | text     | 仅短语级 |
| hyperframes tts → transcribe 链         | wav→json | 词级        |

### 定位辅助

- 横屏：距底 80–120px 居中
- 竖屏：距底约 600–700px
- `window.__hyperframes.fitTextFontSize(text, {maxWidth, fontFamily, fontWeight})` 动态字号

---

## 7. 音频驱动动画

### 数据结构

```js
window.AUDIO_DATA = {
  fps: 30,
  totalFrames: 900,
  frames: [{ bands: [0.42, 0.18, ...] }]  // bands normalized 0–1 per band across track
};
```

索引 0 = 低音，越高越偏高音。频段 0–1，整轨归一化。

### 文档化映射

| 频段                  | 属性                     |
| --------------------- | ---------------------------- |
| Bass (bands[0–1])     | scale（脉冲）                |
| Mid (bands[4–8])      | borderRadius、width          |
| Treble (bands[12–14]) | textShadow、boxShadow（辉光） |
| Overall amplitude     | opacity、y、backgroundColor  |

任意 GSAP 可 tween 的属性均可 — 包括 clipPath、filter、SVG 属性、CSS 变量。

### 提取

```bash
python3 .../extract-audio-data.py audio.mp3 --fps 30 --bands 8
```

仅预提取 — 渲染时不用 Web Audio。

### 音频驱动中禁止

EQ 条、频谱 UI、通用波形、音符 clip-art、通用粒子、彩虹循环、节拍白闪、抽象脉冲光球。

---

## 8. HTML-in-canvas

文档见 skills/hyperframes/references/html-in-canvas-patterns.md（504 行）。

### 能力

- Chrome 实验性 `layoutSubtree` + `drawElementImage` 将实时 DOM 光栅化到 canvas
- 特性检测：`isHtmlInCanvasCaptureSupported()`
- 着色器转场用其作为场景纹理
- 与 Three.js 结合：`CanvasTexture` + 后处理

### 可用模式

- HTML 贴在 Three.js 平面上（位移、畸变、液体模拟）
- HTML 在着色器中（VFX 纹理采样）
- 递归 HTML-in-canvas-in-shader-in-HTML

### 使用此能力的实验性 VFX 区块

- `vfx-iphone-device`（GLTF iPhone + MacBook，HTML 屏幕）
- `vfx-liquid-background`（液体模拟位移 HTML）
- `vfx-liquid-glass`
- `vfx-magnetic`
- `vfx-portal`
- `vfx-shatter`
- `vfx-text-cursor`（色差边缘、canvas 后处理）

---

## 9. Three.js / WebGL 自定义场景

### 集成模式

```js
window.addEventListener("hf-seek", (e) => {
  const time = e.detail.time;
  mixer.setTime(time);
  shaderUniforms.u_time.value = time;
  renderer.render(scene, camera);
});
```

- 加载：`import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm"`
- 确定性：每一帧必须来自 `time`，禁止 `requestAnimationFrame` / `Date.now()`
- 包含：AnimationMixer、自定义 GLSL、后处理、GLTF 模型、灯光、相机、材质

---

## 10. SVG / canvas / 可变字体（其他创作技巧）

（来自 skills/hyperframes/references/techniques.md）

| 技巧                | 机制                                                                            |
| ------------------------ | ------------------------------------------------------------------------------------ |
| SVG path drawing         | `strokeDasharray` + `getTotalLength()` + GSAP stroke offset                          |
| Canvas 2D procedural art | Seeded hash function + `tl.to` proxy `{time}` onUpdate                               |
| CSS 3D card              | GSAP `rotationY` + `perspective: 900`                                                |
| Per-word kinetic type    | GSAP timings 数组、sliding decay                                                    |
| Variable font axes       | 动画 CSS 变量 → `font-variation-settings: "opsz" var(--opsz), "wght" var(--wght)` |
| Character typing         | `tl.call` 文本变更 + `steps(1)` 光标闪烁                                    |
| Velocity-matched cuts    | 出画 blur/translate 速度与入画匹配以实现无缝节拍                |
| MotionPathPlugin         | `gsap.registerPlugin(MotionPathPlugin)` + path string                                |

---

## 11. 媒体：视频、音频、TTS

### 视频合成

- `<video muted playsinline data-start="..." data-duration="..." data-track-index="..." src="...">`
- HyperFrames 渲染时通过 videoFrameInjector 抽帧（避免无头 `<video>` 播放不可靠）
- Linter 禁止同一 `<video>` 带音频 — 拆成 `<video muted>` + `<audio>`
- 视频帧提取使用 FFmpeg
- HDR 视频：PQ 或 HLG 传递函数检测 + x265 母版元数据

### 音频混音器

- `<audio id="..." data-start="..." data-duration="..." data-volume="0.8" data-track-index="2" src="...">`
- 多轨混音：`amix normalize=0` + 每轨 adelay + volume
- 主 audioGain 来自 EngineConfig
- 输出：AAC 192kbps

### TTS（Kokoro-82M，本地）

- 54 个内置音色前缀：`a` 美式 EN、`b` 英式 EN、`e` 西语、`f` 法语、`h` 印地语、`i` 意大利语、`j` 日语、`p` 巴西葡语、`z` 普通话
- 默认音色：`af_heart`
- 语速：0.1–3.0（默认 1.0）
- 语言：en-us、en-gb、es、fr-fr、hi、it、pt-br、ja、zh（非 EN 需系统 espeak-ng）
- 输出：WAV；无 pitch/volume CLI 标志
- 无需 API key

### 转写

- Whisper.cpp 模型：tiny、base、small、medium、large-v3、small.en、medium.en（默认 small）
- Groq API：whisper-large-v3，词级粒度
- OpenAI API：whisper-1 verbose_json
- 导入：SRT、VTT、JSON
- 质量门控：音乐 token 检测、垃圾清洗、medium.en 重试

### 背景移除

- u2net ONNX 模型
- 设备：auto / cpu / coreml / cuda
- 质量预设：fast / balanced / best
- 输出：透明 WebM、ProRes MOV、PNG 序列
- 可选双输出（前景 + 提取背景）

---

## 12. Registry — 51 个区块 + 4 个组件 + 8 个示例

### 按分类的区块

**Social overlays（8）：** instagram-follow、tiktok-follow、yt-lower-third、x-post、reddit-post、spotify-card、macos-notification、blue-sweater-intro-video

**Showcases（5）：** app-showcase（3D 手机）、north-korea-locked-down（地图 + 标注）、apple-money-count（计数器 + SFX）、vpn-youtube-spot（App Store 滚动）、nyc-paris-flight（地图 + 飞机路径）

**Data viz（2）：** data-chart（动画柱+线，NYT 风格）、flowchart + flowchart-vertical（决策树 + SVG 连接器、打字修正）

**Logo / branding（1）：** logo-outro（构建 + 辉光 + tagline + URL pill）

**3D / experimental VFX（8）：** ui-3d-reveal、vfx-iphone-device（GLTF）、vfx-liquid-background、vfx-liquid-glass、vfx-magnetic、vfx-portal、vfx-shatter、vfx-text-cursor

**Single shader transitions（14）：** 每种具名着色器一个区块 — domain-warp-dissolve、ridged-burn、whip-pan、sdf-iris、ripple-waves、gravitational-lens、cinematic-zoom、chromatic-radial-split、glitch、swirl-vortex、thermal-distortion、flash-through-white、cross-warp-morph、light-leak

**Transition galleries（13 个展示）：** transitions-3d、transitions-blur、transitions-cover、transitions-destruction、transitions-dissolve、transitions-distortion、transitions-grid、transitions-light、transitions-mechanical、transitions-other、transitions-push、transitions-radial、transitions-scale

### 组件（4 个可复用片段）

- **grain-overlay** — SVG feTurbulence + CSS keyframes
- **shimmer-sweep** — 文字上的扫光渐变遮罩
- **grid-pixelate-wipe** — 网格方块交错淡出场景擦除
- **texture-mask-text** — 亮度遮罩字形 + 66 张 mask PNG（Masonry、Stone、Ground/Road、Wood、Metal、Organic/Soft 纹理分类）

### 示例（8 个入门项目）

warm-grain、play-mode、swiss-grid、vignelli、decision-tree、kinetic-type、product-promo、nyt-graph

安装：区块/组件用 `npx hyperframes add <name>`，示例用 `hyperframes init <dir> --example <name>`。

---

## 13. CLI — 25 条命令

| 命令           | 用途                                                                                                                                                                                                                                                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| init              | 从 template/example 脚手架项目（交互或 --non-interactive）                                                                                                                                                                                                                                                |
| add               | 安装 registry 区块 / 组件                                                                                                                                                                                                                                                                                       |
| catalog           | 浏览 registry 区块/组件（--type、--tag、--json、--human-friendly picker）                                                                                                                                                                                                                                       |
| play              | 轻量浏览器播放器（默认端口 3003）                                                                                                                                                                                                                                                                           |
| preview           | Studio 开发服务器（端口 3002；--force-new、--list、--kill-all）                                                                                                                                                                                                                                                           |
| publish           | Zip + 上传 + 返回 hyperframes.dev URL                                                                                                                                                                                                                                                                                |
| render            | 渲染为 MP4 / WebM / MOV / PNG 序列 — 标志：--fps 24/30/60、--quality draft/standard/high、--workers、--docker、--hdr/--sdr、--crf、--video-bitrate、--gpu、--browser-gpu auto/software/hardware、--max-concurrent-renders 1-10、--variables JSON、--variables-file PATH、--strict-variables、--resolution preset |
| lint              | 静态 lint（--json、--verbose）                                                                                                                                                                                                                                                                                          |
| validate          | 打包 + 无头 Chrome + console + 对比度（--contrast 默认 true、--timeout 3000）                                                                                                                                                                                                                                  |
| inspect / layout  | 视觉布局审计（在 N 个时间戳检测溢出；--samples 9、--at、--tolerance 2、--max-issues 80）                                                                                                                                                                                                              |
| info              | 打印项目元数据                                                                                                                                                                                                                                                                                                   |
| compositions      | 列出合成（根 + 子合成）                                                                                                                                                                                                                                                                                     |
| benchmark         | 5 种预设配置 × N 次运行（--runs 3）                                                                                                                                                                                                                                                                                     |
| browser           | 管理 Chrome（ensure/path/clear）                                                                                                                                                                                                                                                                                        |
| remove-background | u2net + FFmpeg → 透明视频                                                                                                                                                                                                                                                                                       |
| transcribe        | whisper.cpp 或导入 SRT/VTT/JSON                                                                                                                                                                                                                                                                                       |
| tts               | Kokoro-82M（--voice、--speed、--lang、--list）                                                                                                                                                                                                                                                                            |
| docs              | 打印捆绑 markdown 主题（data-attributes、examples、rendering、gsap、troubleshooting、compositions）                                                                                                                                                                                                                |
| doctor            | 环境检查清单（Node、CPU、memory、disk、FFmpeg、FFprobe、Chrome、Docker）                                                                                                                                                                                                                                         |
| upgrade           | npm update 检查 + 可选全局安装                                                                                                                                                                                                                                                                               |
| skills            | 运行 `npx skills add heygen-com/hyperframes --all`                                                                                                                                                                                                                                                                        |
| telemetry         | enable/disable/status                                                                                                                                                                                                                                                                                                    |
| snapshot          | 在时间轴时间戳截 PNG                                                                                                                                                                                                                                                                                   |
| capture           | 抓取 URL → 站点资源 + 截图 + 设计 token（Puppeteer + 可选 Gemini vision）                                                                                                                                                                                                                        |

### 网站抓取（`hyperframes capture <url>`）

在抓取站点上检测这些库（用于上下文标注）：GSAP / ScrollTrigger、Three.js、Lottie、Anime.js、PixiJS、Babylon.js、Rive、Matter.js、Lenis、Framer Motion、Tailwind CSS、WebGL（着色器指纹）。抓取结果供 website-to-video 技能工作流使用。

---

## 14. Linter — 60+ 条规则

分布在 packages/core/src/lint/rules/ 的 8 个文件中：

| 规则文件   | 捕获                                                                                                                                                                                                                                                            |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| core        | 缺失 composition-id、缺失尺寸、缺失时间轴注册、registry 不匹配、无效脚本语法、作用域 CSS 问题、非确定性代码                                                                                                         |
| media       | 重复 media id、video 未 muted、video 嵌套在 timed 元素内、占位 URL、禁止 base64、缺失 src/start/id、命令式 play()/pause()/seek()                                                                                                |
| gsap        | 重叠 tween、退出缺少 hard kill、GSAP 动画 .clip 元素、未作用域选择器、CSS transform 冲突、缺失 GSAP 脚本、无限 repeat（repeat: -1）、repeat ceil overshoot、场景层 visibility kill、audio-reactive 每组单 tween |
| captions    | 字幕退出缺少 kill、文本溢出风险、transcript 未内联、解析错误、容器位置、缩放不匹配、父容器 textShadow                                                                                                              |
| composition | 文件过大、轨道过密、缺失 class="clip"、已弃用 data-layer/data-end、拆分 attribute 选择器、外部脚本依赖、合成内 RAF、无效 variable JSON                                                                                     |
| adapters    | 缺失 Lottie 脚本、缺失 Three 脚本                                                                                                                                                                                                                        |
| textures    | 文本 drop-shadow、class 缺失 base、文本缺失 mask、未知 texture class                                                                                                                                                                                  |
| fonts       | Google Fonts import（应使用 @font-face）、font-family 无 @font-face                                                                                                                                                                                               |

另有异步 URL 检查（`lintMediaUrls`、`lintScriptUrls` — HEAD 探测）。

`validateCompositionGsap` 还禁止：`Math.random`、`Date.now`、`new Date`、`setTimeout`、`setInterval`、`requestAnimationFrame`、`repeat: -1`。

**注意：** `onUpdate` 回调、`tl.call()` 以及 GSAP 事件回调（`onComplete`、`onStart` 等）**不被** linter 禁止 — canvas/WebGL 渲染与逐字输入模式需要它们。linter 仅捕获上述确定性违规。

---

## 15. Player — `<hyperframes-player>` Web 组件

### 属性

`src`、`srcdoc`、`width`、`height`、`controls`、`muted`、`volume`、`poster`、`playback-rate`、`audio-src`、`shader-capture-scale`、`shader-loading`（internal|player|none）、`loop`、`autoplay`、`speed-presets`

### 公开 API

`seek(t)`（同源时同步 — 直接使用 `iframe.contentWindow.__player.seek`）、`play()`、`pause()`、`currentTime`、`duration`、`paused`、`ready`、`playbackRate`、`iframeElement`

### 事件

`ready`、`timeupdate`、`play`、`pause`、`ended`、`volumechange`、`ratechange`、`shadertransitionstate`、`playbackerror`、`error`、`audioownershipchange`

### 媒体镜像

带 `data-start` 的父级 audio/video 元素被代理；`_mirrorParentMediaTime` 修正漂移；若 autoplay 被拦则 `_audioOwner` 提升到父级。

### 运行时自动注入

若缺少 `__hf`/`__player` 但存在 timelines，则加载 `RUNTIME_CDN_URL`（`@hyperframes/core/dist/hyperframe.runtime.iife.js`）。

---

## 16. Engine + Producer — 渲染管线

### 输出格式

mp4、webm、mov、png-sequence — 支持 HDR（PQ / HLG / SDR / auto-detect）、透明（ProRes MOV / WebM / PNG）或标准 8-bit SDR

### 编码控制

- `--fps`：24 / 30 / 60
- `--quality`：draft / standard / high
- `--crf`：整数（与 `--video-bitrate` 互斥）
- `--video-bitrate`：如 `8M`
- `--gpu`：NVENC、VideoToolbox、VAAPI、QSV
- `--browser-gpu`：auto / software / hardware
- `--workers`：并行渲染 worker
- `--max-concurrent-renders`：1–10（设置 `PRODUCER_MAX_CONCURRENT_RENDERS`）
- `--resolution`：预设（1080p、4k、portrait 等）
- `--docker`：在 Dockerfile.test 镜像内渲染（可复现）
- `--hdr` / `--sdr`：强制 HDR 或 SDR 管线

### Engine 子系统

- 帧捕获：Linux headless-shell 上 BeginFrame（快、无 alpha）或 `Page.captureScreenshot`（alpha + 超采样）
- Video frame injector：预提取视频为图像，捕获期间将 `<video>` 换为 `<img>`（按路径 + 字节预算 LRU 缓存）
- Audio mixer：基于 FFmpeg；每轨 delay、volume、主 gain、AAC 192k 输出
- Chunk encoder：H.264 / H.265 / VP9 / ProRes 预设，可选 GPU
- Streaming encoder：`streamingEncodeMaxDurationSeconds` 用于长渲染
- HDR 合成：`rgba16float` WebGPU readback（有界面 Chrome）、PQ OETF 辅助
- Layer compositor：按 z-order 分组 DOM；HDR 元素拆成独立层
- Alpha blit：matrix3d 仿射提取、`blitRgba8OverRgb48le`、`blitRgb48leAffine`
- Parallel coordinator：并发、coresPerWorker、minParallelFrames、largeRenderThreshold
- Browser pool：可选，带超时配置

### 仅 Producer

- `RenderConfig` 含 `hdrMode`（auto / force-hdr / force-sdr）、`outputResolution` 映射到 `deviceScaleFactor`
- File server 注入 `HF_EARLY_STUB`、`HF_BRIDGE_SCRIPT`、virtual-time，使 `window.__hf` 桥接 `window.__player.renderSeek`
- 通过 `window.__hf.transitions` 元数据做 HDR 感知着色器转场合成

---

## 17. Studio — 浏览器内 NLE

完整编辑器位于 packages/studio/：

- **NLELayout**：NLE 预览 + 时间轴 + 控制
- **Timeline**：clip 渲染、拖拽移动（`data-start`）、调整大小（`data-duration`）、`data-track-index` 重分配、资源拖放、文件拖放
- **PlayerControls**： scrub、播放、暂停、逐帧（`stepFrameTime`）、`STUDIO_PREVIEW_FPS`
- **useTimelinePlayer**：解析 `__player` / `__timeline` / `__timelines`
- **LeftSidebar**：合成列表、资源浏览器
- **RenderQueue + useRenderQueue**：队列多任务渲染
- **LintModal**：应用内 lint 输出
- **MediaPreview + AudioWaveform**：波形渲染
- **CaptionOverlay、CaptionTimeline、CaptionPropertyPanel**：字幕编辑器
- **useCaptionSync**：词级同步
- **useElementPicker**：点击检查拾取模式
- 使用 Tailwind v3 构建（与合成使用的 Tailwind v4 浏览器运行时分离）。

---

## 18. 确定性保证

- 禁止 `Math.random()`（使用 seeded PRNG；skills 中模式为 mulberry32）
- 禁止 `Date.now()` / `new Date()`
- 时间轴构建中禁止 `setTimeout` / `setInterval`
- 禁止 `requestAnimationFrame`（时间轴驱动；引擎逐帧 seek）
- 禁止 `repeat: -1`（计算精确重复：`Math.ceil(duration / cycleDuration) - 1`）
- 禁止 `onComplete`/`onStart`/`onRepeat` 回调（引擎不触发）。**例外：** `onUpdate` 与 `tl.call()` **支持** — canvas/WebGL 渲染、逐字输入、计数器模式需要。见 §10（Canvas 2D procedural art）文档模式。
- 禁止对后续场景的 clip 使用 `gsap.set`（用 `tl.set(selector, vars, position)`）
- 同步构建时间轴（无 async）
- 主时钟可在合成结尾 clamp

---

## 19. 变量 / 参数化

合成支持类型化运行时变量：

```html
<html
  data-composition-variables='[
  {"name":"brand","type":"string","default":"Stripe"},
  {"name":"primary","type":"color","default":"#635BFF"},
  {"name":"duration","type":"number","default":15},
  {"name":"darkMode","type":"boolean","default":false},
  {"name":"layout","type":"enum","options":["hero","split","stacked"]}
]'
></html>
```

通过 `window.__hyperframes.getVariables()` 访问。渲染时覆盖：

```bash
npx hyperframes render --variables '{"brand":"Linear","primary":"#5E6AD2"}'
npx hyperframes render --variables-file vars.json
npx hyperframes render --strict-variables  # 未使用/不匹配则报错
```

`validateVariables()` 在 CLI/工具边界按声明校验值。

---

## 20. 子合成

两种加载机制：

- **外部文件：** `data-composition-src="compositions/act-1.html"` — 运行时 fetch
- **内联 template：** `<template id="<id>-template">` — 由 `loadInlineTemplateCompositions` 提取

每个子合成：

- 自有 `data-composition-id`
- 自有 `window.__timelines[<id>]`
- 自动嵌套进根时间轴
- 作用域 CSS：`scopeCssToComposition`（`[data-composition-id="<id>"]` 选择器）
- 包装脚本：`wrapScopedCompositionScript`
- 读取 `data-variable-values` 与自身默认值合并到 `window.__hfVariablesByComp[<id>]`
- 外部脚本加载带 `EXTERNAL_SCRIPT_LOAD_TIMEOUT_MS` 超时。失败时发出 `external_composition_load_failed` / `external_composition_script_load_issue` 诊断。

---

## 21. 全局运行时 API（`window.*`）

| 全局                                | 用途                                                                 |
| ------------------------------------- | ----------------------------------------------------------------------- |
| `__hyperframes`                       | `{ fitTextFontSize, getVariables }`                                     |
| `__timelines`                         | `{ [compositionId]: GsapTimeline }`                                     |
| `__player`                            | 内部 player 桥：seek、play、pause、renderSeek 等             |
| `__clipManifest`                      | 计算的 clip 数组（供 Studio）                                        |
| `__playerReady`                       | player 就绪时 resolve                                              |
| `__renderReady`                       | 可渲染捕获时 resolve                                                  |
| `__HF_PARITY_MODE`                    | Engine parity 标志                                                      |
| `__HF_FPS`                            | 渲染 FPS 提示                                                         |
| `__HF_MAX_DURATION_SEC`               | Engine clamp                                                            |
| `__HF_VIRTUAL_TIME__`                 | 渲染模式由 engine 设置（shader-transitions 切换路径）        |
| `__hfThreeTime`                       | Three.js 适配器当前时间                                       |
| `__HF_PICKER_API`                     | Studio 元素拾取钩子                                                     |
| `__hfAnime`                           | Anime.js 实例数组                                             |
| `__hfLottie`                          | Lottie 动画数组                                              |
| `__hfVariables`                       | 解析后的根变量                                                 |
| `__hfVariablesByComp`                 | 每合成变量映射                                            |
| `__hfRuntimeTeardown`                 | 清理函数                                                        |
| `__tailwindReady`                     | Tailwind 浏览器构建就绪（门控捕获）                            |
| `__hf.transitions`                    | 着色器转场元数据（producer 读取以 HDR 感知合成） |
| `__beforeTimeline`, `__afterTimeline` | 可选用户钩子                                                     |
| `__afterRender`, `__beforeRender`     | 可选用户钩子                                                     |
| `gsap`, `THREE`, `anime`, `lottie`    | 库全局变量                                                         |

Control bridge 动作：play、pause、seek、set-muted、set-playback-rate、enable-pick-mode、disable-pick-mode、set-volume、set-media-output-muted。

---

## 22. 可用 Skills — 16

| Skill                     | 用途                                                                 |
| ------------------------- | ----------------------------------------------------------------------- |
| hyperframes               | 核心框架技能（合成创作）                            |
| hyperframes-cli           | 全部 CLI 命令作为 agent 技能                                      |
| hyperframes-media         | 媒体工作流（TTS、转写、字幕集成）                 |
| hyperframes-registry      | 安装区块/组件                                            |
| hyperframes-contrast      | WCAG 审计（scripts/contrast-report.mjs）                                |
| hyperframes-animation-map | 每 tween bbox + 标志报告                                           |
| website-to-video          | Capture → DESIGN.md → brief → storyboard+script → VO → build → validate |
| remotion-to-hyperframes   | 迁移模式 + API 映射 + CustomEase                               |
| gsap                      | GSAP API + 插件参考                                            |
| animejs                   | Anime.js v4 模式                                                    |
| css-animations            | @keyframes 模式                                                     |
| waapi                     | Web Animations API                                                      |
| lottie                    | Lottie 集成                                                      |
| three                     | Three.js + 确定性 seek                                           |
| tailwind                  | Tailwind 浏览器运行时 v4                                             |
| contribute-catalog        | 向 registry 添加区块                                               |

---

## 23. References 清单（skills/hyperframes/references/）

16 篇参考文档，涵盖：

- text-effects.md — 24 种具名文本动画效果（逐字、逐词、逐行、整段）— 独立 `pixel-point/animate-text` 技能的词汇参考（通过 `npx skills add pixel-point/animate-text` 或 `/animate-text` 加载）。规格在上游技能中，不在本仓库。
- transitions.md + transitions/catalog.md + 14 个分类子文件
- css-patterns.md（标记模式）
- dynamic-techniques.md（字幕动画）
- motion-principles.md（ease 即情绪、编排）
- typography.md（禁用字体列表、配对规则、可变字体）
- narration.md（脚本 + VO 节奏）
- captions.md（字幕创作契约）
- audio-reactive.md（频段映射 + 提取）
- transcript-guide.md（whisper、Groq、OpenAI 工作流）
- techniques.md（大型技巧目录 — SVG、canvas 2D、3D、kinetic、lottie、可变字体、MotionPath、audio-reactive）
- beat-direction.md、design-picker.md、prompt-expansion.md、video-composition.md
- visual-styles.md（8 种具名视觉风格：Swiss Pulse、Velvet Standard、Deconstructed、Maximalist Type、Data Drift、Soft Signal、Folk Frequency、Shadow Cut — 通过 `visual-style` 技能可用）

---

## 24. 文档页面（docs/）

docs/guides/ 与 docs/packages/ 中共 27 个 mdx 页面：

**Guides：** 4k-rendering、claude-design、common-mistakes、deploy、gsap-animation、hdr、html-in-canvas、hyperframes-vs-remotion、open-design、performance、prompting、remove-background、rendering、timeline-editing、troubleshooting、video-editor-cheatsheet、website-to-video 等。

**Packages：** cli.mdx、core.mdx、engine.mdx、player.mdx、producer.mdx、studio.mdx
