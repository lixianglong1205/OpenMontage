# 步骤 5：构建 Composition

**字幕规则 — 在构建任何内容之前先读：** 切勿用空 transcript（`const script = []`）创建 `compositions/captions.html`。若 VO/转录步骤被跳过或失败，则完全不要创建字幕 composition。空的 captions 文件会静默无效并浪费一条轨道槽位。仅在 `transcript.json` 含有真实词级时间戳时才创建。

**字幕叠层 bug：** 每个字幕词组必须以 `opacity: 0`（或 `visibility: hidden`）开头，并设为 `position: absolute`。同一时刻切勿显示多于一个词组 — GSAP 按顺序控制可见性。若多个词组同时可见，说明要么 (a) 初始 CSS 未隐藏，要么 (b) 下一组入场前缺少上一组的 exit tween。构建 captions.html 后，在旁白中段取 3–4 个时间点的快照，确认每帧仅有一个词组可见。

**构建前请确认你已有：**

- **STORYBOARD.md** — 逐 beat 计划。若记不清每个 beat 的概念、素材与技术，现在重读。
- **DESIGN.md** — 若需核对具体数值（颜色、字体、组件样式）且想不起来，查阅即可。不必通读整份文件。
- **`capture/extracted/asset-descriptions.md`** — 当 storyboard 为某 beat 指定素材时，查描述以了解其内容。若记不清素材清单，重读此文件。
- **transcript.json** — 驱动场景时长的词级时间戳。

加载 `hyperframes` 技能 — 其中包含 data 属性、时间线契约、确定性渲染与布局规则。若本会话尚未读过，现在阅读。

**对于 capabilities.md 与 techniques.md：** 先读目录定位，再仅深入 storyboard 实际用到的章节。不必重读与你的 beat 无关的动画引擎、registry 块或技术章节。

---

## 1. 将 SFX 复制到项目

```bash
cp -r skills/website-to-video/assets/sfx/ <project-dir>/sfx/
# If skill is installed elsewhere:
find . -path "*/website-to-video/assets/sfx" -exec cp -r {} <project-dir>/sfx/ \;
```

## 2. 构建根 index.html

自行创建 `index.html`。这是编排器 — 容纳 beat 槽位、旁白音频、SFX，以及（若有）shader 转场。

**关键 CSS — 每个 beat 必须在同一帧内重叠：**

```css
.scene {
  position: absolute;
  top: 0;
  left: 0;
  width: 1920px;
  height: 1080px;
  overflow: hidden;
}
```

**Beat 结构：**

```html
<div
  id="root"
  data-composition-id="main"
  data-start="0"
  data-duration="TOTAL"
  data-width="1920"
  data-height="1080"
>
  <div
    id="beat-1"
    class="scene"
    data-composition-id="beat-1-hook"
    data-composition-src="compositions/beat-1-hook.html"
    data-start="0"
    data-duration="5.5"
    data-track-index="1"
    data-width="1920"
    data-height="1080"
  ></div>

  <!-- more beats... -->

  <audio
    id="narration"
    src="narration.wav"
    data-start="0"
    data-duration="NARRATION_LENGTH"
    data-track-index="0"
    data-volume="1"
  ></audio>

  <!-- SFX on content moments, NOT on shader transitions -->
  <audio
    id="sfx-impact"
    src="sfx/impact-bass-1.mp3"
    data-start="0.3"
    data-duration="2.1"
    data-track-index="41"
    data-volume="0.35"
  ></audio>
</div>
```

SFX 已在 storyboard（步骤 3）中分配 — 严格按 STORYBOARD.md 实现。每条 SFX 含文件、触发时间与音量。以 `<audio>` 元素接入，并使用 storyboard 中的精确 `data-start`、`data-duration`、`data-volume`。不得超出 storyboard 增删或替换 SFX。

**根据节奏选择架构（来自步骤 3）**

| 节奏                          | 架构                                                                                                                                                                         | 原因                                                                                     |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| **Fast**（每 beat 一屏） | 单一 `index.html`，堆叠 `<div class="beat">`，GSAP 透明度序列。无子 composition、无 HyperShader。通过 `tl.set()` 硬切。见下方 stacked-beats 模式。 | 子 composition 增加延迟；硬切需瞬时切换。单文件 = 零加载延迟。 |
| **Moderate / Slow / Arc**     | 子 composition 配合 `HyperShader.init()`。每个 beat 在 `compositions/beat-N.html`。场景间 CSS 交叉淡入或 shader 转场。                                            | 转场需要 HyperShader 合成。子 agent 可独立构建各 beat。   |

若 storyboard 标明「fast」节奏：使用下方 stacked-beats 模式。勿用 HyperShader — 它会增加场景注册开销，在硬切之间产生空隙。每一帧都是内容，无转场帧。

**Stacked-beats 模式（fast 节奏）：**

每个 beat 由 storyboard 指定的原语组合 — HTML/CSS、SVG、捕获素材、WebGL、Canvas、Three.js、 kinetic typography、Lottie — 可单独或组合使用。明确禁止：勿将全屏产品 UI 截图作为承载内容。各 beat 结构来自 storyboard 的 Composition + Accents 规格。

```html
<div
  data-composition-id="video"
  data-width="1920"
  data-height="1080"
  data-start="0"
  data-duration="TOTAL"
  style="position:relative;width:1920px;height:1080px;"
>
  <!-- Beat 1: kinetic-typography hook (composed from per-word spans) -->
  <div class="beat" id="b01" style="opacity:1;">
    <div class="mega">
      <span class="w">Stop</span>
      <span class="w">context-switching.</span>
    </div>
  </div>

  <!-- Beat 2: composed kanban — 3 columns of cards-as-divs, NOT a screenshot -->
  <div class="beat" id="b02">
    <div class="kanban">
      <div class="col">
        <div class="card">Triage tickets</div>
        <div class="card">Review PR</div>
      </div>
      <div class="col">
        <div class="card active">Design spec</div>
      </div>
      <div class="col">
        <div class="card">Ship v2.1</div>
      </div>
    </div>
  </div>

  <!-- Beat 3: SVG logo draw — composed, not an <img> -->
  <div class="beat" id="b03">
    <svg viewBox="0 0 200 200"><path class="mark" d="..." /></svg>
  </div>
  <!-- more beats — each a composed scene with its own visual world -->
</div>
```

若你发现某 beat 的主要视觉是 `<img src="capture/assets/...">` 且素材为产品 UI 截图，请停手。这正是本技能要打破的幻灯片模式。用 DESIGN.md 中的品牌色，以 div 与 CSS 构建元素。合法的 `<img>` 用途：(a) 纯栅格品牌 logo，(b) 作为环境深度叠在合成内容后的 hero 插画，(c) 作为背景 wash 的渐变/纹理图。切勿将产品 UI 截图作为承载视觉。

```css
.beat {
  position: absolute;
  inset: 0;
  width: 1920px;
  height: 1080px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  overflow: hidden;
}
```

```javascript
var beats = [
  { id: "b01", at: 0, dur: 1.8 },
  { id: "b02", at: 1.8, dur: 1.0 },
  // ...
];
beats.forEach(function (b) {
  var el = document.getElementById(b.id);
  if (b.id !== "b01") tl.set(el, { opacity: 1 }, b.at);
  gsap.set(el, { scale: 1.012 });
  tl.to(el, { scale: 1, duration: 0.25, ease: "power2.out" }, b.at);
  if (b !== beats[beats.length - 1]) tl.set(el, { opacity: 0 }, b.at + b.dur);
});
```

每个 beat 应有独立视觉世界 — 不同背景、颜色、能量。相邻 beat 不应看起来一样。每个 beat 入场时的 scale pulse（1.012→1.0）很 subtle 但可感知。

若 storyboard 标明「slow」或「cinematic」：将每个 beat 建为子 composition。使用长交叉淡入（0.8–1.2s 的 `duration` 且无 `shader` 键 = CSS 交叉淡入）。beat 内部保持连续细微动效 — 没有任何元素保持静止：

- 合成场景根上的慢速镜头漂移：`tl.fromTo(scene, {scale:1.05, x:20}, {scale:1, x:-20, duration: BEAT, ease:"none"})`（Ken-Burns 风格，但作用于合成元素 — 非截图）
- 文字层视差：`tl.fromTo(text, {y:30}, {y:-30, duration: BEAT, ease:"power1.inOut"})`
- 文字入场前 1–2s 呼吸空间（勿在 t=0 动画一切）
- 柔和缓动：入场用 `expo.out`，漂移用 `power1.inOut`

**多场景 index.html 与 HyperShader — 适用于 moderate/slow/arc 节奏**

对含子 composition beat 与场景转场的视频，`index.html` 必须使用 `HyperShader.init()`。这是完整的场景编排层。勿尝试用 registry 块子 composition（如 `compositions/domain-warp-dissolve.html`）做转场 — 那些是独立展示 demo，不是多场景 composition 中 HyperShader 的用法。

先复制本地 shader 构建：

```bash
cp packages/shader-transitions/dist/index.global.js <project-dir>/hyper-shader-local.js
```

完整可用的 `index.html` 模式 — 每个字段都重要：

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="hyper-shader-local.js"></script>

<div id="root" data-composition-id="main" data-start="0" data-duration="TOTAL"
     data-width="1920" data-height="1080">

  <!-- Host divs: MUST have both id AND data-composition-id matching the same value.
       HyperShader.init() uses getElementById() — without id="beat-1" it fails with
       "scene ids not found in DOM". -->
  <div id="beat-1" class="scene"
    data-composition-id="beat-1-hook"
    data-composition-src="compositions/beat-1-hook.html"
    data-start="0"        <!-- transition INTO this beat starts here -->
    data-duration="4.5"   <!-- must match the GSAP BEAT constant in the composition -->
    data-track-index="1"
    data-width="1920" data-height="1080"
    style="background: #YOUR_BEAT_BG_COLOR;"><!-- background here OR in sub-comp CSS — both work -->
  </div>

  <div id="beat-2" class="scene"
    data-composition-id="beat-2-features"
    data-composition-src="compositions/beat-2-features.html"
    data-start="4.0"
    data-duration="5.5"
    data-track-index="2"  <!-- use sequential track indices (1,2,3...) to avoid linter errors -->
    data-width="1920" data-height="1080"
    style="background: #YOUR_BEAT_BG_COLOR;">
  </div>

  <!-- ... more beats ... -->

  <!-- ALWAYS add a dummy s-end scene as the LAST entry.
       HyperShader renders scenes[N-1] as black in some contexts.
       s-end is invisible — it just prevents your CTA from being last. -->
  <div id="s-end" class="scene"
    data-composition-id="s-end"
    data-start="TOTAL_MINUS_0.1"
    data-duration="0.1"
    data-track-index="N"
    data-width="1920" data-height="1080">
  </div>

</div>

<script>
  window.__timelines = window.__timelines || {};
  var tl = HyperShader.init({
    bgColor: "#000000",
    accentColor: "#YOUR_ACCENT",
    scenes: ["beat-1", "beat-2", "beat-3", ..., "s-end"],
    transitions: [
      { time: 4.0, shader: "sdf-iris", duration: 0.7 },    // WebGL shader
      { time: 9.5, duration: 0.5 },                         // CSS crossfade (no shader)
      // ... one transition per scene boundary ...
      { time: TOTAL_MINUS_0.1, duration: 0.1 }              // dummy → s-end
    ],
  });
  // Add ALL beat animations to the returned tl AFTER init()
  window.__timelines["main"] = tl;
</script>
```

**Track index 与 linter：** 每个 beat 使用顺序 track index（`data-track-index="1"`、`"2"`、`"3"`…）— 不要全部放在 track `"1"`。linter 会将同 track 上重叠 clip 报错，而 HyperShader composition 的 beat 在转场窗口内必然重叠。顺序 index 可消除 linter 告警；HyperShader 通过 opacity 管理可见场景，与 track index 无关。

**场景背景色：** 在 index.html 的 host `<div id="beat-1">` 上设置 `style="background: #3139FB"` 是最简模式 — 根文件一眼可见。在子 composition CSS 内设置背景也可。二者皆可；优先 host div 以便清晰。

**关键：beat host div 须有顺序的 `data-start` 与匹配的 `data-duration`。** 勿对所有 beat 设 `data-start="0"` — 渲染引擎将各 beat 的 GSAP 时间线 seek 到 `global_time - data_start`。在 t=10s 且 `data-start=0` 时，5.5s 时间线会被 seek 到末尾之后，所有内容消失。

`data-duration` 须与子 composition 内 GSAP `BEAT` 常量一致（子 composition 内部时间线长度）。二者不一致会导致动画被截断。

**Storyboard Beat Timing 章节** 会给出两个值 — 直接使用：

- `data-start` = storyboard 中的「Transition in at:」
- `data-duration` = storyboard 中的「GSAP duration:」

**字体处理：** 常见字体由渲染器自动解析：使用 `"Inter"`（勿用 `"Inter Variable"` — 编译器只映射基础名）、`"Roboto"`、`"JetBrains Mono"`、`"Poppins"`。若 composition 使用 `"Inter Variable"` 会打编译器警告并可能错误回退 — 始终用 `"Inter"`。仅品牌专属字体（GT Walsheim、Aeonik 等）需要 `@font-face`。检查 `capture/assets/fonts/` — 哈希文件名为 Google Fonts 子集可自动解析；可识别文件名（如 `BrandSans-Bold.woff2`）为品牌字体，需 `@font-face` 声明。

**品牌字体 @font-face：** 若 storyboard 的 BRAND VALUES 列出品牌字体及 `capture/assets/fonts/` 路径，在使用该字体的每个 composition 顶部添加 `@font-face` — 除非你明确写入子 agent 提示，否则子 agent 不会添加。将精确的 `@font-face` 声明粘贴到子 agent 提示的 BRAND VALUES 段。缺少此步时各 composition 会回退到 `system-ui`，品牌字体无法加载。

**⚠ 素材路径 — 最常见的子 agent 错误（每次运行 5+ 个 agent）：** 当 composition 引用捕获 accent（logo、渐变层、hero 插画）时，路径须相对**项目根**，而非 composition 文件。

- ✅ `capture/assets/logo.svg`
- ❌ `../capture/assets/logo.svg`

Studio 预览服务器将 base URL 重写为项目根 — 本地看似可用的 `../` 路径在预览与渲染中会 404。在每个子 agent 提示的 RULES 段原样加入此说明。

## 3. 构建每个 composition — 使用子 AGENT

**派发前重读 DESIGN.md 与 STORYBOARD.md。** 你在本会话早些时候写过这些文件，你以为记得。其实你不记得 — 不是精确 hex、不是具体 font family、不是按钮 border-radius、不是 Do's/Don'ts。现在重读，以便将准确品牌规则与 beat 规格粘贴进各子 agent 提示。

**若运行时支持并行子 agent**（Claude Code、Cursor、多数 agent 框架）：每个 beat 派发一个子 agent — 比顺序构建快 3–4 倍。3 个以上 beat 时始终并行派发。1–2 个 beat 时顺序即可。

**若运行时不支持并行子 agent**（部分 Codex 配置、仅串行模型）：用下方同一 context-packing 模板顺序构建。模板为每次构建 pass 提供与子 agent 相同的上下文 — 粘贴 prev/this/next beat + 品牌值 — 输出质量相同，只是更慢。

无论哪种情况，使用模板。勿跳过模板凭记忆构建。

每个子 agent 阅读 [beat-builder-guide.md](beat-builder-guide.md) — 含规则、缓动、文件引用、验证命令。**勿试图自行粘贴全部规则。** 告诉子 agent 阅读该指南文件。你只粘贴 beat 专属上下文：storyboard 章节、品牌值、素材路径。

```
Build the composition for Beat N. Save to compositions/beat-N-name.html.

FIRST: Locate and read the beat-builder guide. Your CWD is the project directory, so
the skill lives outside it — run this to find it:

  find "$HOME" -path '*/website-to-video/references/beat-builder-guide.md' -maxdepth 10 2>/dev/null | head -1

Read that file end to end. It has your full workflow, all rules, easing vocabulary,
and file references. Follow its workflow exactly:
  build → lint (`npx hyperframes lint .`)
        → snapshot (`npx hyperframes snapshot . --frames 3`)
        → view contact sheet AND read snapshots/descriptions.md
        → fix issues

After you finish, the main agent will READ your composition HTML top-to-bottom
and cross-check it against DESIGN.md and STORYBOARD.md — does the brand bg/accent
hex actually appear in your CSS, are the captured assets the storyboard called
for actually referenced, is the headline ≥80px, does the GSAP timeline cover
the full beat duration. Do the work honestly. Reports of "looks good" without
the work being done will be caught when the main agent opens the file.

═══ PREVIOUS BEAT (Beat N-1) ═══
[paste the FULL previous beat section from STORYBOARD.md]

═══ THIS BEAT (Beat N) ═══
[paste the FULL beat section from STORYBOARD.md — this IS the build spec]

═══ NEXT BEAT (Beat N+1) ═══
[paste the FULL next beat section from STORYBOARD.md]

═══ BRAND VALUES (from DESIGN.md) ═══
Colors:
  --bg:        #[hex]   primary background
  --fg:        #[hex]   primary text
  --accent:    #[hex]   CTA / highlights
  --surface:   #[hex]   card / panel backgrounds
  [add more if needed]

Fonts:
  Headlines: [font family], [weight]
  Body:      [font family], [weight]
  [brand font path if needed: capture/assets/fonts/Brand.woff2]

Key component styles:
  [paste relevant lines from DESIGN.md]

═══ CAPTURED ASSETS FOR THIS BEAT ═══
[Paste ACTUAL file paths + descriptions from asset-descriptions.md:

- capture/assets/hero-dashboard.png — full-bleed product dashboard, dark theme
- capture/assets/logo.svg — brand wordmark, white on transparent

Do NOT say "see asset-descriptions.md". Paste the paths here.]
```

storyboard beat 已包含一切 — 概念、含精确时机的视觉编排、CSS 值、SFX 提示。子 agent 的工作是将该描述译为可用的 HTML/CSS/GSAP，而非重新发明创意方向。若认为有帮助，也可向子 agent 粘贴其他相对有用的上下文。

### 每个 composition 的流程

对每个 beat：

**1. 阅读 storyboard beat。** storyboard 即构建规格。它说明有哪些元素、如何入场、beat 期间做什么、如何退场。遵循它。若 storyboard 某处不清或看似不可行，研究做法或提问 — 勿静默跳过。

**2. 先构建静态终态。** 将每个元素置于最可见时刻。仅 HTML+CSS，尚无 GSAP。CSS 位置是 ground truth。

**3. 添加动画序列。** 遵循 storyboard 编排 — 它规定何时发生什么。入场用 `tl.fromTo()`（勿用 `tl.from()`）。按 storyboard 描述顺序构建时间线。

**4. 添加退场**（若 CSS 转场出）。若为 shader 转场 — 无需退场动画。

**5. 查看结果。** 构建后，在该 beat 不同时间点（元素应出现、动画、移动等）拍快照，从各角度、角落与位置查看。画面是否饱满、一切是否在应有位置？确定吗？？？元素可读吗？是否与 storyboard 描述一致？

### 技术规则

- **禁止 `repeat: -1`** — 根据 beat 时长计算精确重复次数
- **禁止 `Math.random()`** — 使用 seeded PRNG
- **禁止裸 `gsap.to()`** — 所有 tween 在 `tl` 上，勿 standalone
- **禁止全屏深色线性渐变** — H.264 色带
- **最小字号**：标题 80px+，正文 20px+
- **渐变背景上的 WCAG 对比度：** 对比度验证器采样文字元素下方实际背景像素 — 若背景为渐变图，加深文字色会使测得比值在图像较暗处更差而非更好。修复：将文字放在纯色区域，或对不需 WCAG 的装饰标签加 `data-layout-ignore`。背景非纯色时不要盲目加深文字色。

## 4. 所有 composition 构建完成后 — 对账检查

进入步骤 6 前，运行此健全性检查：

```bash
# List every file in compositions/ and verify each one has a host div in index.html
ls compositions/
```

对 `compositions/` 中每个 `.html` 文件，确认 `index.html` 有指向它的 `data-composition-src="compositions/<filename>"`。若有 composition 未在 `index.html` 引用，立即补 host div — 未引用的 composition 在运行时完全不可见。

**Captions 桩规则：** 切勿用空 transcript（`const script = [];`）创建 `compositions/captions.html`。若 VO/转录步骤被跳过或失败，完全不要创建 captions composition。立即返回的空 captions 比没有更糟 — 静默无效并浪费 track 槽位。

### 并行子 agent 快照已过期 — 全部完成后重新 snapshot

并行派发子 agent（每 beat 一个）时，各子 agent 快照的项目中 sibling beat 可能尚不存在。其 per-beat 快照对其 beat 隔离有效，但**在 beat 边界或 shader 转场时刻的快照会显示错误内容** — 通常是上一 beat，因下一 beat 尚未构建。

例：Beat 6 子 agent 在 t=25.7s 快照时看到 Beat 1 内容，因 Beat 6 运行时 Beat 5 尚不存在。子 agent 将其报告为「shader 转场行为显示上一场景」 — 听起来合理但诊断错误。

**所有子 agent 完成后必须：**

```bash
node /<repo-root>/packages/cli/dist/cli.js snapshot <project-dir> --frames <N>
```

其中 N 按快照公式：`max(beats × 3, ceil(duration_seconds / 2))`。这是步骤 6 DoD 使用的规范快照 — 非任一子 agent 的中间快照。

子 agent 快照仍可作为 per-beat 健全性检查，但不是交付物。完成后快照才是。勿因「子 agent 已 snapshot」而跳过。

## 5. 逐 beat 通读 HTML — 进入步骤 6 前的必过门

**此门不可跳过。**「我读过了看起来没问题」「子 agent 确认了」「快照看起来对」均不可接受。快照是 300+ 动态帧中的 3 帧 — 会隐藏其间一切出错。

**为何需要此门：** 早期会话中子 agent 回复「looks good, 0 errors」主 agent 即信任 — 于是视频带着颜色不匹配、缺 logo、标题小到无法阅读、SFX 晚 1 秒触发（agent 凭眼估时间戳而非计算）就交付了。

对每个 `compositions/beat-N.html`：

1. **打开文件通读。** 不是扫一眼。不是 grep。读 `<style>`，再 markup，再 `<script>`。
2. **填写此证据块 — 每行必填，引用文件中的值：**

```
Beat N: compositions/beat-N-NAME.html
  BG color in CSS:        <hex from line Y>      ← quote the exact line
  Accent color in CSS:    <hex from line Z>      ← quote the exact line
  Headline font-size:     <px from line>         (≥80? yes/no)
  Headline font-family:   <stack from line>      (matches DESIGN.md? yes/no)
  @font-face src paths:   <list>                 (each path exists? yes/no)
  Captured assets used:   <full list of paths from <img src=>, inline SVG ids, background-image url()>
  Storyboard called for:  <list from STORYBOARD.md beat N>
  Assets match storyboard? yes/no — if no, specify the gap
  GSAP first event:       tl.X("...", {...}, <t>)   beat-local t=<num>
  GSAP last event:        tl.X("...", {...}, <t>)   beat-local t=<num>
  Beat duration:          <N>s                   (events span full duration? yes/no)
  SFX trigger:            <element> data-start=<num>
  Storyboard SFX line:    "<quote the line>" → expected t=<num>
  SFX timestamp matches?  yes/no — if no, specify the drift
  Technical gates:        data-composition-id matches window.__timelines key? yes/no
                          script INSIDE <template>? yes/no
                          no Math.random / no repeat:-1 / no bare gsap.to? yes/no
  VERDICT: PASS / FIX (specify exactly what)
```

若某行无法填写（如「未见 SFX trigger」或「未指定 headline font-family」），即为一项发现 — 修复或升级，勿掩盖。

3. **打开 `snapshots/beat-N/` 中每一帧**，视觉确认入场/ hold/退场与 storyboard 一致。

**任何不对 — 内联修复（小 CSS/GSAP 修正）或带具体问题引用重新派发子 agent。** 每个 beat 证据块填完且 PASS 前勿进入步骤 6。

### SFX 时间戳计算 — 计算，勿凭眼估

每个 SFX 的 `data-start` 必须从 STORYBOARD.md 计算，勿视觉估计。

对每条 SFX：

1. Storyboard 给出 beat 内时间（如「Beat 2 进入 beat 后 1.2s」）。
2. 从 beat 顺序得该 beat 的全局起始（如 Beat 1: 0–3.5s → Beat 2 全局从 3.5s 起）。
3. beat 内 + 全局起始：`3.5 + 1.2 = 4.7s`。
4. 在 index.html 写 `data-start="4.7"`。

**禁止：** 读 storyboard 后凭眼写 `data-start="<approximate visual moment>"`。上述证据块必须同时引用 storyboard SFX 行与 index.html `data-start` 行 — 并确认在 ±0.1s 内匹配（30fps 约 3 帧；与 `w2h-verify.mjs` 强制及 `step-6-validate.md` 播放验证相同容差）。1 秒漂移不是四舍五入误差；是构建失败。

### 向用户 surfaced 重复的子 agent 变通

当 2+ 子 agent 独立报告同一变通（如「因 linter 对 inline SVG 误报，不得不 base64 编码 data URI」），值得 surfaced 的工具 bug。在步骤 5 最终报告的「Tooling issues encountered」下列出，即使各实例已解决。格式：

```
TOOLING ISSUES (worth filing):
- 3 sub-agents (beats 1, 4, 6) hit `root_missing_composition_id` false positive on
  inline SVG data URI in CSS. Workarounds: base64 (beat 1), removed overlay (beats 4, 6).
  Worth filing as a regression against packages/core/src/lint.
```

掩盖重复变通意味着下一会话再撞同一 bug 再变通一次。不要。

### 品牌默认检查（全片，每个 beat 通过自身阅读后）

这些是多数品牌视频的默认，非硬性要求：

- 第一 beat 引用 `capture/assets/svgs/` 中的品牌 logo / wordmark SVG
- 最后一 beat 引用品牌 logo / wordmark
- 站点标志性视觉（hero 插画、渐变波、 distinctive 的 UI 标记）至少出现一次

若缺失，查 storyboard — 若 STORYBOARD.md 为概念原因刻意延迟品牌露出或省略标志视觉，可以。若无意遗漏，修复（或在添加前询问主 agent / 用户）。

每个 beat 通读干净后，进入步骤 6（Validate & Deliver）进行 lint、validate、snapshots 与视觉审查。
