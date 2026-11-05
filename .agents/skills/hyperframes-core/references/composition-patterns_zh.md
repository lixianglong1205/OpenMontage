# 组合模式

如何架构项目——何时把所有内容内联在一个 HTML 里、何时拆成子组合、`index.html` 编排器在规模变大时长什么样，以及真实项目中常见的子组合原型。可与 `minimal-composition.md`（单文件形态）和 `sub-compositions.md`（子组合文件机制）对照阅读。

## 两种架构

|                       | 单体（单文件）                                          | 模块化（子组合）                                                                     |
| --------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| 项目布局              | 仅 `index.html`                                         | `index.html` + 每个场景一个 `compositions/<scene>.html`                            |
| 场景所在位置          | 根节点下内联的 `<section class="clip">` 兄弟节点        | 每个场景是包在 `<template>` 里的独立文件                                             |
| 时间轴注册            | 在根的 `data-composition-id` 上注册一条时间轴           | 根时间轴（常接近空）+ 每个子组合各一条时间轴，各自按 `id` 注册                       |
| 路由入口              | `references/minimal-composition.md`                     | `references/sub-compositions.md`                                                     |

两种架构使用相同的运行时契约——`data-*` 属性 + `window.__timelines[id]`。选择是结构上的，不是行为上的。

### 何时选单体

- 整段视频是连续单场景、没有硬切。
- 场景共享大量状态（整段视频共用一个 canvas/WebGL 上下文、单个 SVG 在所有节拍间变形）。
- 总规模较小（约 200–400 行 markup + script）。
- 没有场景会在多个项目中复用。

### 何时选模块化

- 视频有明确的场景切——每个场景是时间轴上独立一段。
- 某些场景很大（>100 行 markup 或较重的脚本动画）。
- 某场景可复用（ kinetic 片头、片尾 logo 定版、转场等）。
- 视频有多段视觉但有一条连续音轨。音轨放在根，视觉段作为子组合。
- 希望单独编写/迭代场景（直接预览单个子组合文件）。

### 在两种架构间重构

转换是机械且可逆的。要把单体场景提升为子组合：将该场景的 markup + 作用域 CSS + 父时间轴中对应片段包进 `<template>`，存为 `compositions/<scene>.html`，在 `index.html` 里用插槽 `<div data-composition-src="compositions/<scene>.html">` 替换内联内容，并让子组合在 `window.__timelines["<scene>"]` 注册自己的时间轴。父时间轴相应缩短。

若单体项目已接近三个或更多场景切，在加下一场景之前优先模块化。部分场景内联、部分在 `compositions/` 的混合项目最难维护。

## 模块化编排器模式

使用子组合时，`index.html` 应**尽量薄**。它的职责是声明插槽、在时间轴上排布、挂载音轨，并注册一条（通常空的）根时间轴。所有场景动画都在子组合内部。

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        background: #000;
      }
      #root {
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
      }
      /* Sub-comp slots stretch to fill the root. */
      [data-composition-id="root"] > div[data-composition-src] {
        position: absolute;
        inset: 0;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="root"
      data-width="1920"
      data-height="1080"
      data-duration="30"
    >
      <!-- Sequential scenes — each one a sub-composition slot. -->
      <div
        id="el-intro"
        data-composition-id="intro"
        data-composition-src="compositions/intro.html"
        data-start="0"
        data-duration="6"
        data-track-index="1"
      ></div>

      <div
        id="el-body"
        data-composition-id="body"
        data-composition-src="compositions/body.html"
        data-start="6"
        data-duration="18"
        data-track-index="1"
      ></div>

      <div
        id="el-outro"
        data-composition-id="outro"
        data-composition-src="compositions/outro.html"
        data-start="24"
        data-duration="6"
        data-track-index="1"
      ></div>

      <!-- Continuous audio at the root — survives scene cuts. -->
      <audio
        id="el-bgm"
        src="assets/bgm.mp3"
        data-start="0"
        data-duration="30"
        data-track-index="10"
        data-volume="0.6"
      ></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["root"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
```

该布局的关键特性：

- **视觉场景使用相同 `data-track-index`**（例如 `1`）。顺序排列——同一轨道上不能重叠。若两场景交叉淡入淡出，把其一放到更高轨道，并按淡入淡出时长重叠时间。
- **音频使用单独、更高的轨道索引**（例如 `10`）。避免与 linter 的重叠规则在视觉上冲突。
- **根时间轴接近空。** 所有动画在子组合里。结尾全黑淡出放在根上可以；不要从根再开一条并行动画轨。
- **宿主插槽 id** 用 `el-<name>` 或 `<scene-id>`。插槽的 `data-composition-id` 仍须与子组合内部 id 一致（见 `sub-compositions.md`）。

## 子组合原型

### A. 内容场景（默认）

子组合包含该场景的完整 DOM、作用域 CSS 与时间轴。这是 `sub-compositions.md` 中的标准模式——多数场景属于此类。

### B. 宿主媒体 + 主时间轴驱动（任何 `<video>`/`<audio>` 均**必须**）

媒体播放仅当 `<video>`/`<audio>` 是**宿主根的直接子节点**时才有效——绝不能放在子组合 `<template>` 内（会渲染成空白/黑屏）。这不是可选项，也不是「仅跨场景媒体」；适用于每一个片段，包括场景专属片段。场景的子组合保留画框/外壳；媒体是叠在其上的宿主兄弟节点。

子组合时间轴**不能**驱动宿主元素（全局选择器或 `document.querySelector` 无法跨边界解析）。因此把媒体在各场景内的运动（scale/opacity/morph/tilt/breathing）写在 `index.html` 的**主时间轴**上，**全局时间** = 场景本地时间 + 场景插槽的 `data-start`。

```html
<!-- index.html (host) -->
<div
  id="el-final"
  data-composition-id="final-anim"
  data-composition-src="compositions/final-anim.html"
  data-start="20"
  data-duration="6"
  data-track-index="1"
></div>

<!-- media is a DIRECT root child; sits over the sub-comp's frame -->
<video
  id="final-video"
  class="clip"
  src="assets/final.mp4"
  data-start="20"
  data-duration="6"
  data-track-index="2"
  muted
  playsinline
  style="position:absolute; left:360px; top:100px; width:1200px; height:680px; object-fit:cover; border-radius:24px;"
></video>

<script>
  // MAIN timeline drives the host video. Global time: scene starts at 20.
  window.__timelines = window.__timelines || {};
  const main = window.__timelines["main"];
  main.fromTo(
    "#final-video",
    { scale: 1.4, filter: "blur(14px)" },
    { scale: 1.0, filter: "blur(0px)", duration: 0.9, ease: "power3.out" },
    20,
  ); // = slot data-start (+ any scene-local offset)
</script>

<!-- compositions/final-anim.html — frame/shell only, no <video>, no host-element animation -->
<template>
  <div
    data-composition-id="final-anim"
    data-width="1920"
    data-height="1080"
    data-duration="6"
    style="position:absolute; inset:0; pointer-events:none;"
  >
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      // animate ONLY this sub-comp's own elements here (labels, frame, overlays)
      window.__timelines["final-anim"] = tl;
    </script>
  </div>
</template>
```

注意：

- 宿主媒体必须是直接根子节点且存在于 DOM 中（静态写在 `index.html`）——通常如此。
- 片段生命周期在 `[data-start, data-start+data-duration]` 窗口内控制媒体元素可见性。主时间轴上的 opacity/scale 补间可以与之叠加；若要做 opacity  reveal/交叉淡入淡出，优先用宿主**包装层**，避免与媒体元素本身的生命周期打架。
- 两个媒体元素共享相同 `src` + `data-start` 会触发 `duplicate_media_discovery_risk`（良性——两者仍会渲染）。

### C. 多场景合并

当多个节拍级场景共享连续状态——不断增长的聊天线程、切镜后仍保留的标题词、带内部阶段变化的单 canvas——应合并为一个子组合，用**内部 phase div** 而非多个子组合插槽。

```html
<!-- compositions/act2-merged.html -->
<template>
  <div data-composition-id="act2-merged" data-width="1920" data-height="1080" data-duration="9">
    <style>
      [data-composition-id="act2-merged"] .phase {
        position: absolute;
        inset: 0;
        opacity: 0;
      }
    </style>
    <div class="phase" id="phase-a">…</div>
    <div class="phase" id="phase-b">…</div>
    <div class="phase" id="phase-c">…</div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      tl.set("#phase-a", { opacity: 1 }, 0);
      tl.to("#phase-a", { opacity: 0, duration: 0.4 }, 3.0);
      tl.set("#phase-b", { opacity: 1 }, 3.0);
      // …
      window.__timelines["act2-merged"] = tl;
    </script>
  </div>
</template>
```

在场景共享 DOM、共享 canvas，或需要在阶段间交叉淡入淡出且保留元素（切镜后仍存在的标题）时，优先于多个顺序插槽。每个 phase 只是同一子组合内的一个 div——父时间轴无需知道内部 phase 边界。

### D. 根级音频，子组合内响应式视觉

音频始终在宿主（`index.html`）以根级 `<audio>` 存在，以便切镜后仍播放。可视化音频的子组合应在初始化时读取**预烘焙**频谱曲线，再从其时间轴采样该曲线——视觉仍必须是 `tl.time()` 的确定性函数，而非 `audio.currentTime`。见 `determinism-rules.md` 与 `hyperframes-creative` 中的编写模式。

## 命名约定

| 对象                                | 约定                                        | 示例                                       |
| ----------------------------------- | ------------------------------------------- | ------------------------------------------ |
| 子组合文件                          | `compositions/<scene-id>.html`              | `compositions/act0-intro-bell.html`        |
| 子组合 `<template>` id（可选）      | `<scene-id>-template`                       | `<template id="act0-intro-bell-template">` |
| 子组合根 `data-composition-id`      | `<scene-id>`（须与宿主插槽一致）            | `data-composition-id="act0-intro-bell"`    |
| 时间轴注册键                        | 与 `data-composition-id` 一致               | `window.__timelines["act0-intro-bell"]`    |
| 宿主插槽 `id`                       | `el-<short>` 或 `<scene-id>`                | `id="el-intro"`, `id="act0"`               |
| 子组合内元素 id                     | 以场景 id 为前缀                            | `#act0-bell`, `#b1-tape`                   |
| 根级音频                            | `data-track-index` 明显高于视觉轨           | 视觉用 `1` 时用 `10`                       |

`<template>` 上的 `-template` 后缀是惯例而非必需——运行时从 `<body>` 中 whichever `<template>` 提取内容，与 id 无关。内层元素 id 的前缀是多个子组合同时挂载到同一宿主页面时避免 id 冲突的唯一保障。

## 编辑现有项目

在添加或修改场景前，先确认使用的架构：

```bash
ls compositions/ 2>/dev/null && echo "modular" || echo "monolithic"
```

- 在**单体**项目中，新场景加为内联 `<section class="clip">`，使用不重叠的 `data-start` 与合理的 `data-track-index`，并扩展现有单条时间轴。
- 在**模块化**项目中，遵循同一模式：在 `compositions/` 下新增文件、在 `index.html` 增加插槽、保持根时间轴薄。当兄弟场景已是子组合时，**不要**在 `index.html` 内联新场景——不一致是两种架构最差的一面。
- 若单体项目需要第三、第四个场景切，在继续添加前先逐个提升为子组合。转换是机械性的（见上文「在两种架构间重构」）。

选择插槽的 `data-start`/`data-duration` 时，优先延续现有顺序约定（首尾相接的 start、为交叉淡入淡出刻意重叠）。除非确实需要并行视觉层，否则不要引入新轨道索引——多数顺序场景项目只使用一条视觉轨。
