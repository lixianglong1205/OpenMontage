# Beat Builder 指南

你正在构建多 beat 视频合成中的**一个 beat**。本文件说明应阅读哪些内容、如何构建、如何验证以及如何回报。

## 步骤 1：阅读与理解

**必读（每个 beat）：**

1. **加载 `hyperframes` 技能** — 合成规则、data 属性、时间轴契约、确定性渲染。通读整份技能。
2. **[capabilities.md](capabilities.md)** — HyperFrames 能力完整清单（24 个章节）。先读目录，再深入 beat 所需章节。
3. **主 agent 提供的 beat 规格** — 概念、编排、资产、品牌值、时间。

**按 beat 需要选读（勾选相关项）：**

| 资源                                                                                  | 涵盖内容                                                                                                                      | 何时阅读                                          |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| [techniques.md](../../hyperframes/references/techniques.md)                           | 13 种基础动画技法：SVG 路径绘制、Canvas 2D、CSS 3D、 kinetic type、可变字体、MotionPath 等。                                    | beat 使用这些技法之一                             |
| [text-effects.md](../../hyperframes/references/text-effects.md)                       | 来自 `pixel-point/animate-text` 的 24 种命名文本动画（独立技能 — 通过 `/animate-text` 加载规格）                              | beat 含文本动画                                   |
| [html-in-canvas-patterns.md](../../hyperframes/references/html-in-canvas-patterns.md) | HTML-in-Canvas：iPhone/MacBook  mockup、liquid glass、magnetic、portal、shatter、文本光标                                      | beat 使用设备 mockup 或 HTML 上的 WebGL 效果      |
| [transitions.md](../../hyperframes/references/transitions.md)                         | Shader 转场 API、HyperShader.init() 模式、全部 14 个 WebGL shader                                                               | beat 含 shader 转场                               |
| [transitions/](../../hyperframes/references/transitions/)                             | 14 个 CSS 转场分类文件：push、scale、dissolve、blur、3D flip、light leak、distortion、grid、mechanical、destruction             | beat 使用 CSS 转场                                |
| [css-patterns.md](../../hyperframes/references/css-patterns.md)                       | 文本标记：highlight sweeps、手绘圆圈、burst lines、scribble、sketchout                                                          | beat 使用文本强调/标记                            |
| [audio-reactive.md](../../hyperframes/references/audio-reactive.md)                   | Bass→scale、mid→shape、treble→glow 映射                                                                                       | beat 随音乐/音频反应                              |
| [captions.md](../../hyperframes/references/captions.md)                               | 逐词卡拉 OK、语气自适应样式、定位                                                                                              | beat 含字幕                                       |
| [typography.md](../../hyperframes/references/typography.md)                           | 字体层级、可变字体、响应式字号缩放                                                                                              | beat 含复杂排版                                   |
| [motion-principles.md](../../hyperframes/references/motion-principles.md)             | 速度匹配、easing 哲学、运动连续性                                                                                             | beat 需要 polished  motion design                 |
| [dynamic-techniques.md](../../hyperframes/references/dynamic-techniques.md)           | 计数器动画、数据驱动视觉、动态内容                                                                                              | beat 含计数器或数据可视化                         |
| [video-composition.md](../../hyperframes/references/video-composition.md)             | 画面构图、色彩存在感、缩放、密度规则                                                                                            | 通用合成质量                                      |

**可按需加载的其他技能：**

- `/gsap` 或 `/gsap-core`、`/gsap-timeline`、`/gsap-plugins` — 更深入的 GSAP 参考
- `/animate-text` — 精选文本动画目录及精确 JSON 规格
- `/hyperframes-registry` — 需要安装并接入 registry 块时
- `/hyperframes-contrast` — 审核色彩对比度（WCAG）
- `/lottie`、`/three`、`/waapi`、`/animejs`、`/css-animations` — beat 使用这些引擎时

**设计 beat 前务必打开 captured 资产文件夹：**

- `capture/assets/svgs/` — 品牌 logo、图标、装饰标记。SVG 可无限缩放且可描边动画（路径绘制、dash offset）。logo SVG 自行绘制到画面上可以撑起整个 beat。
- `capture/assets/` — 主视觉插画、截图、产品图、渐变、摄影。这些是 beat 的一级主体，不是背景装饰。一张会「呼吸」的主视觉插画加一行 kinetic type 就是完整镜头。
- 在画面上放文字前**查看**每一张图。检查安全区、对比度、实际内容、焦点位置。

**若 beat 规格点名某 captured 资产，必须使用。** 不要用 CSS 重制替代。用户从真实品牌站点抓取这些，正是为了让视频携带品牌真实视觉身份。

## 步骤 2：构建合成

保存到主 agent 指定路径（通常为 `compositions/beat-N-name.html`）。

```html
<template>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    /* your styles */
  </style>

  <div
    id="beat-N-name"
    data-composition-id="beat-N-name"
    data-width="1920"
    data-height="1080"
    style="width:1920px; height:1080px; position:relative; overflow:hidden; background:#YOUR_BG;"
  >
    <!-- your elements -->
  </div>

  <script>
    (function () {
      var BEAT = 5.5; // MUST match data-duration on the host div in index.html
      window.__timelines = window.__timelines || {};
      var tl = gsap.timeline({ paused: true });

      // your GSAP animations

      window.__timelines["beat-N-name"] = tl;
    })();
  </script>
</template>
```

**关键：** 根 div 上的 `data-composition-id`、`data-width`、`data-height` 必须与 index.html 中的 host div 一致。

## 步骤 3：Lint

```bash
npx hyperframes lint .
```

修复**全部**错误。必须零错误。

## 步骤 4：快照与验证

```bash
npx hyperframes snapshot . --frames 3
```

**阅读** contact sheet（`snapshots/contact-sheet.jpg`）。对每一帧：

- 内容是否可见？（非黑屏、空白或加载中）
- 文字是否可读、位置正确、字体/颜色正确？
- 资产尺寸与位置是否正确？
- 该时间戳的动画状态是否与 beat 规格一致？

**若有任何问题：** 修复、重新快照、再检查。仅当每一帧都符合规格时才算完成。

## 步骤 5：如实回报

lint 通过、快照已拍、且你已修复所见问题后 — 向主 agent 回报**具体观察**，而非「0 错误，看起来不错」。这类措辞曾导致成片出现品牌色不匹配、缺少 logo、标题小到无法阅读等问题。

**主 agent 会打开你的合成文件并通读**，对照 DESIGN.md 与 STORYBOARD.md — 品牌背景/强调色 hex 是否真出现在 CSS 里、storyboard 要求的 captured 资产是否被引用、标题是否 ≥80px、GSAP 时间轴是否覆盖完整 beat 时长。你无法通过声称未做之事通过该检查；文件在磁盘上，真相在文件里。

因此在回报中写明你使用的 hex、放置的 captured 资产路径、标题的 `font-size`、GSAP 时间轴最后一条 `tl.fromTo(...)` 的时间戳。简短、具体、真实。若与 DESIGN.md 或 storyboard 有偏差，明确说明 — 主 agent 可决定接受偏差或让你回去修。交接时发现的意外成本是分钟级；到步骤 6 才发现则是多轮迭代。

### FLAG 协议 — 非阻塞问题的必填表述

发现以下任一情况时，在回报中以 **FLAGS** 形式 surfaced，而非条件性建议：

- 短暂看起来破损的视觉状态（空容器、悬空元素、间隙时刻）
- 规格模糊而你必须靠猜测解决的点
- 你绕过的 linter bug
- 因无法适配规格而改动的 tween 值

**禁止表述：**「若 X 感觉太长，你可以…」「考虑微调 Y」「可能想要…」

**必填表述 — 具体、可执行、带行号：**

```
FLAG: at beat-local t=1.2s the doc card is visible but its inner content is still
       opacity 0 — a 0.4s empty-panel window.
       RECOMMENDED FIX: pull title typewriter from 1.6s → 1.4s
       in compositions/beat-5-name.html line 234.
```

主 agent 对每条 FLAG **必须**应用其修复建议，或写一句带理由的拒绝。静默丢弃 FLAG 属于验证失败，会在步骤 6（或更糟，在用户预览中）被抓住。

### 规格歧义 — 升级，不要掩盖

若 STORYBOARD.md 给出转场或变换但未定义**起始**状态，**不要猜测**。值得 FLAG 的歧义示例：

- 「Row 1 在 3.5s 从 Huly Blue 过渡到 Huly Orange」— 但 Row 1 初始颜色未指定
- 「标题放大」— 但起始尺寸未指定
- 「卡片滑入」— 但屏外位置未指定
- 「副标题在标题之后出现」— 但精确时间偏移未指定

**必填动作：** 在回报中逐字 FLAG 歧义：

```
FLAG: STORYBOARD.md beat 3 says "Row 1 transitions blue → orange at 3.5s" but
       Row 1's initial color is not specified anywhere. I interpreted Row 1 starts
       blue and tweened to orange. CONFIRM or correct.
```

主 agent 随后在步骤 6 推进前确认或纠正。静默选择一种解释会让成片「看起来没问题」却偏离意图 — 用户只在动态中才注意到。

### 子 agent 诊断是未验证主张，不是事实

当子 agent 报告「这是 linter 误报」/「这是已知 bug」/「该属性与文档不符」— 那些是**假设**，不是结论。子 agent 从单一症状诊断，没有全仓库上下文。

在传播任何子 agent 诊断之前（例如对另一 beat 套用相同「变通」，或告诉用户「这是已知 bug」），**必须**做以下之一：

1. **读源码验证。** 打开子 agent 声称有 bug 的文件。确认 bug 存在。示例：「我读了 `packages/core/src/lint/utils.ts:42`，确认正则错误匹配 `url(\"data:image/svg+xml...\")`。变通方案是对 URI 做 base64 编码。」
2. **披露未验证主张。** 不要压制 —  surfaced 它。示例：「beat 2 的子 agent 将 `root_missing_composition_id` 诊断为 inline SVG data URI 的 linter 误报。我在**未验证**底层主张的情况下对 beat 4 套用了相同变通。值得对 `packages/core/src/lint/utils.ts` 提 regression 以确认。」

**禁止：** 静默采纳变通模式并把「lint 通过」当作证据。若变通来自未验证诊断，「lint 通过因为诊断正确且我绕过了它」与「lint 通过因为诊断错误但变通碰巧消除了症状」皆可能。未验证则不知是哪一种。下一 session 会继承变通**和**未验证诊断。

### 当你接受子 agent 偏离规格 — 更新规格

若子 agent 报告「我因…偏离 STORYBOARD.md」且你接受偏离，**必须**更新 STORYBOARD.md 以反映实际实现。否则规格与产物不符。

示例：

- 子 agent：「Storyboard 写 'HULY' 大写但实际 logo 资产是小写 'huly'。我用了小写。」接受 → 编辑 STORYBOARD.md 该 beat 为 lowercase「huly」，内联注明变更。
- 子 agent：「Storyboard 写单元格 56px 但在 1920×1080 上太小。我用了 96px。」接受 → 编辑 STORYBOARD.md 该 beat 单元格尺寸为 96px。
- 子 agent：「Storyboard 写 SFX 在 t=4.7s 但视觉时刻在 t=5.2s；我把 SFX 对齐视觉。」接受 → 编辑 STORYBOARD.md SFX 行为 t=5.2s。

**禁止：** 静默接受偏离却 leave storyboard 错误规格。下一 session 读 STORYBOARD.md 会把它当 ground truth。规格是契约；若你打破契约，更新契约。

---

## 持续运动 — 最重要规则

beat 是影片中的**一个镜头**，不是带入场动画的网页。GSAP 时间轴应在**整个 beat 时长**内分布事件 — 而非仅前 1–2 秒入场 tween 之后无事可做。元素在屏上就应有所动作。入场后添加持续 hold 运动：镜头 dolly、不同速度的视差层、beat 中段出现的次要元素、真实景深变化。

## 你在构建镜头，不是网页

storyboard 告诉你镜头景别（特写 / 中景 / 全景等）与镜头运动。去实现它们。beat 是一个时刻，不是截图。区别在于**镜头在做什么**，而非主体是 UI 还是 logo — 对产品真实截图的 tight push-in 是镜头； parked 相机上的居中卡片是网页。

**会把镜头变回网页的模式：**

这些是**默认应避免**，**非绝对禁止。** 若 storyboard  genuinely 要求某 beat 以「看板 app 界面」或「浏览器 chrome」为主体（产品导览、「这样工作」演示、片尾 stylized 窗口 mockup），则应构建。规则是：storyboard 没要求时不要默认套用这些模式。

- ⚠ **用 CSS 复刻 macOS / 浏览器窗口 chrome** — 交通灯、URL 栏、标签页。当 storyboard 以 chrome 为主体时合适（例如 closer 的「stylized macOS 窗口框住产品 UI」）。当只是为让卡片「像 app」而加的框时**不合适**。
- ⚠ **完整网页布局**（侧栏 + 顶栏 + 页脚 + 主内容区）— beat  genuinely 是产品导览镜头时合适。beat 本应是**看板那一刻**却默认画整个 app 时**不合适**。
- ❌ **Parked-camera 构图** — 四边 60–120px 边距的居中卡片且无镜头运动。几乎总是错的。要么给 real push-in / dolly / parallax，要么重新取景。
- ❌ **「Hold with breathing」** 实现为 `y: ±1–2px` 或 `scale: 1.01` — 在 1920×1080+ 尺度上不可见。若需要持续运动，用镜头 dolly（scale 1.0 → 1.05）、视差平移（x/y ±30–80px）或渐进 reveal。
- ❌ **Hover 状态模拟** — 视频没有 hover。若品牌用 hover 效果，在时间轴上用离散帧展示 BEFORE 与 AFTER。
- ❌ **计数器脉冲 + 点脉冲 + 微小 scale 晃动** 作为 hold 期间唯一运动 — 这是「没想法了」的填充。

检验：若 storyboard 说**「本 beat 是产品导览，观众看到 app 界面」**，构建带 chrome 的 CSS dashboard 正确。若 storyboard 说**「本 beat 是看板时刻，单卡滑入到位」**，画整个 app 是错的。仔细读 beat 规格。

**确实是镜头的模式（可自由使用）：**

- ✅ **Captured SVG logo 描边逐笔绘制**（DrawSVG / path dashoffset）— 完整 opener 或 stinger。
- ✅ **Captured 主视觉插画 + 镜头 dolly** — 4s 内 1.0 → 1.08 push-in，焦点元素占满画面。
- ✅ **Captured 产品截图 + 视差层** — 前景 UI 与背景面板分离、不同速度移动，或用 HTML-in-Canvas 做 iPhone/MacBook mockup。
- ✅ **Captured 资产作底，kinetic type 作 punchline** — 品牌主图占画面，一行信息到达、分裂、重排。
- ✅ **由 div 组成的 UI 时刻** 当 beat  specifically 关于该 UI 交互（卡滑入列、搜索结果 resolve）— 这是 CSS-only 合成的 legit 场景。

**所需运动幅度**（更小者在视频尺度上不可见）：

| 运动类型        | 最小幅度                                      |
| --------------- | --------------------------------------------- |
| Translate (y/x) | 30px（入场）/ 8px（hold 期间 drift）          |
| Scale           | 0.05 变化（1.0 → 1.05 或更大）                |
| Opacity         | reveal 时完整 0 → 1 或反向                    |
| Rotate          | 至少 4° 才可读（Dutch 角、刻度）              |
| Camera dolly    | beat 时长内 scale 1.0 → 1.06 最小             |

**每个 beat 所需摄影**（storyboard 应提供；若没有则升级）：

- **景别**（特写 / 中景 / 全景 / 过肩 / Dutch）
- **镜头运动**（dolly in/out、push、视差 pan、orbit、rack focus）
- **景深策略**（前景 / 中景 / 背景各是什么）
- **目的**（该镜头交付的具体感受或注意点）

若 beat 规格缺少任一项，beat 定义不足。不要用「居中布局 + breathing」填 gap — 重读规格，若确实缺失则问主 agent。

## 规则

- SCRIPT PLACEMENT：脚本在 `<template>` 内，永不在 `</template>` 之后。外部脚本看不到 DOM。
- GSAP FROM TRAP：勿对 CSS `opacity:0` 的元素 `gsap.from(el, {opacity:0})`。会动画 0→0。用 `tl.fromTo()`。
- STYLE：避免对 GSAP 动画元素用 CSS `opacity:0`。用 GSAP fromTo 设初始状态。
- ASSET PATHS：相对项目根。`capture/assets/file.png` ✅ `../capture/assets/file.png` ❌
- SVG VIA IMG：`<img src="logo.svg">` 无法继承 CSS 颜色。内联 SVG 或 `filter: brightness(0) invert(1)`。
- CSS CENTERING：GSAP transform 时不要 `transform: translate(-50%, -50%)`。用 flexbox 或 `xPercent/yPercent`。
- QUERYSELECTOR：`document.getElementById("id")` 带 null 守卫。无 null 检查勿调方法。
- CHARACTER SPANS：空格上 `display:inline-block` 会 collapse。用 `&nbsp;` 或 per-word spans。
- COUNTERS：数值计数器勿用 `onUpdate` — 在时间戳用离散 `tl.set(el, {textContent: "42"}, 2.5)`。canvas/WebGL 渲染循环与逐字 typing **支持** `onUpdate` 与 `tl.call()` — 见 capabilities.md §10。
- TIMELINE：`window.__timelines["beat-N-name"] = tl` 同步执行。Key = `data-composition-id`。
- DETERMINISTIC：无 `Math.random()`、`Date.now()`、`requestAnimationFrame`、`repeat:-1`。
- 入场始终 `tl.fromTo()` 而非 `tl.from()`。
- 勿在同一元素同一时间堆叠两个 transform tween。
- FONTS：从 DESIGN.md Fonts 节**逐字复制** `@font-face` 块。勿猜测哪个 `.woff2` 属于哪个 family — capture 文件名是 content-hash（`14d7ce3e41dcbb66-s.p.woff2`），无可见映射。若 DESIGN.md 未含每个 family 的精确 `src:` 路径，**停止**并请主 agent 补充；切勿凭记忆随意配对 `.woff2` 与 family 名。

## Easing — 按意图选择

勿对所有东西默认 `power2.out`。

| 意图            | GSAP Ease             | 用于                                 |
| --------------- | --------------------- | ------------------------------------ |
| Snap (iOS feel) | `power4.out`          | 主标题文字、UI 元素                  |
| Whip overshoot  | `back.out(1.7)`       | 数字、徽章、冲击                     |
| Soft land       | `expo.out`            | 逐词 reveal、柔和入场                |
| Mechanical      | `power1.out`          | 终端文字、代码打字                   |
| Bounce settle   | `elastic.out(1, 0.5)` | 计数器、CTA 按钮                     |
| Dramatic        | `expo.inOut`          | 全屏陈述、主视觉 reveal              |
| Drift           | `"none"`              | 视差、Ken Burns、镜头 drift          |

交错项：`power4.out`，`stagger: 0.08` 至 `0.15`。
