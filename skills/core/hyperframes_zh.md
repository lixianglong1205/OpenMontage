# HyperFrames 技能（Layer 2）

这是 **OpenMontage 专用** 的 HyperFrames 指南。它说明 OpenMontage 流水线何时应选用 HyperFrames 而非 Remotion、OpenMontage 产物如何映射到 HyperFrames 项目文件，以及 compose 阶段如何驱动 HyperFrames CLI。

关于 HyperFrames 的底层知识（创作契约、`data-*` 属性、GSAP 时间轴规则、CLI 标志、registry 块、website-to-video），请阅读 Layer 3 技能：

- `.agents/skills/hyperframes/` — 路由至下方聚焦技能（HF 0.7+ 将原单体技能拆分）
- `.agents/skills/hyperframes-core/` — 合成契约：`data-*` 时序、轨道、子合成、确定性渲染规则
- `.agents/skills/hyperframes-creative/` — 非动画创意方向：调色板、字体、旁白、节拍规划
- `.agents/skills/hyperframes-media/` — TTS/BGM/SFX/转写/字幕/抠图
- `.agents/skills/hyperframes-animation/` — 全部动效知识（规则、蓝图、转场、运行时适配器）
- `.agents/skills/hyperframes-cli/` — init、add、lint、validate、inspect、snapshot、preview、render、benchmark、lambda、doctor（0.7+）
- `.agents/skills/hyperframes-registry/` — `hyperframes add` 与块接线
- `.agents/skills/website-to-video/` — 捕获转视频工作流（0.7 中自 website-to-video 重命名）
- `.agents/skills/music-to-video/` — 使用 `hyperframes beats` 的节拍同步音乐驱动视频
- `.agents/skills/motion-graphics/` — 短设计导向动效图形模式
- `.agents/skills/media-use/` — 任意流水线、任意运行时的 BGM/SFX/图片/图标 `resolve` 动词
- `.agents/skills/remotion-to-hyperframes/` — **仅当**用户明确要求移植 Remotion 源码时用于迁移

本文件讲授两者之间的桥梁。

---

## OpenMontage 何时选用 HyperFrames（对比 Remotion 与 FFmpeg）

OpenMontage 区分两个概念：

- **`renderer_family`** — 创意语法（`explainer-data`、`cinematic-trailer`、`product-reveal` 等）。在提案阶段选定。
- **`render_runtime`** — 实现该语法的技术引擎（`remotion`、`hyperframes`、`ffmpeg`）。同样在提案阶段选定。

二者锁定在 `proposal_packet.schema.json` 中，并经由 `edit_decisions` 原样传递，除非在 `decision_log` 中记录 `render_runtime_selection` 决策。静默更换运行时是契约违规。

### 决策矩阵

| 场景 | 优先 | 原因 |
|----------|--------|-----|
| 既有解说片、React 场景组件栈（text_card、stat_card、chart 场景、caption overlay、TalkingHead、CinematicRenderer） | **Remotion** | 这些合成已存在于 `remotion-composer/`。复用零成本；在 HTML 中复刻则不然。 |
| 词级字幕烧录 / 卡拉 OK 字幕 | **Remotion** | `remotion_caption_burn` 为 Remotion 专有，HyperFrames 首日尚未对等。 |
| 数字人 / 口型同步主讲 | **Remotion** | `TalkingHead` 合成在 Remotion 中。HyperFrames 尚无对等物。 |
| Kinetic typography、重度文字动效、GSAP 原生动画 | **HyperFrames** | HTML/GSAP 是自然媒介。用 Remotion 的 `interpolate()` 表达既慢又脆弱。 |
| 产品宣传片 / 发布 reel / 营销标题卡 | **HyperFrames** | CSS/GSAP 合成语法与设计师现有思路一致。模板（`kinetic-type`、`product-promo`、`swiss-grid`）提供强起点。 |
| Website-to-video / UI 驱动合成 | **HyperFrames** | `website-to-video` 工作流专为此设计。 |
| 需要 registry 块（数据图表、颗粒 overlay、shimmer 扫光、shader 转场） | **HyperFrames** | registry 仅 HyperFrames 具备。Remotion 没有 `hyperframes add`。 |
| 合成 UI / 假终端 / 假浏览器演示 | 视现有覆盖而定 | OpenMontage 已提供 Remotion `TerminalScene`（见 `synthetic-screen-recording` Layer 3）。终端以外的 UI chrome，HyperFrames HTML 更易。 |
| 纯拼接 / 裁剪源片段、无合成 | **FFmpeg** | Remotion 与 HyperFrames 均无增值。 |
| 本机未安装 Remotion | **HyperFrames**（若可用）或 **FFmpeg** | 勿静默降级。降级前告知用户。 |

### 硬规则：两种运行时均可用时必须同时呈现

上述决策矩阵是与用户对话的输入，**不是**静默选「默认」的许可。当本机 Remotion 与 HyperFrames 均可用时，提案阶段**必须**：

1. 向用户呈现两者及与 brief 相关的利弊。
2. 结合 `delivery_promise` 与 `visual_approach` 给出推荐理由。
3. 等待批准。
4. 在 `render_runtime_selection` 决策的 `options_considered` 中记录两者。

完整契约见 `AGENT_GUIDE.md` →「Present Both Composition Runtimes (HARD RULE)」；CRITICAL 级发现执行见 `skills/meta/reviewer.md`。

### 硬规则：需要动效的交付物

若 brief 的 `delivery_promise.motion_required` 为 `true`（科幻预告、电影感 teaser、hype 剪辑，或任何承诺依赖真实动效的 brief），则提案所选运行时是**承诺**，而非提示。Compose **不得**降级为 FFmpeg Ken Burns。若所选运行时失败（Remotion 未安装、`npx hyperframes doctor` 报阻塞项），按 `AGENT_GUIDE.md` >「Escalate Blockers Explicitly」 surfaced 阻塞并等待用户批准后再切换运行时。

---

## 仍属 Remotion 专有（Phase 1）

**不要**在首日尝试将这些移植到 HyperFrames。它们需要专门的对等工作：

- `remotion_caption_burn`（逐词烧录字幕）
- `TalkingHead` 合成（数字人/口型同步主讲）
- 既有 documentary-montage 片尾 overlay 栈（依赖特定 Remotion 组件）
- 任何假设资源 staging 在 `remotion-composer/public/` 并由既有 React 场景组件消费的内容

对此类场景保持 `render_runtime = "remotion"`，按现有流程进行。

---

## 项目工作区布局

HyperFrames 需要独立的项目工作区。**不要**复用 `remotion-composer/public/` — 那是 Remotion 的共享 staging 目录，混用运行会导致跨项目冲突。

```
projects/<project-name>/
├── artifacts/
├── assets/
│   ├── images/
│   ├── video/
│   ├── audio/
│   └── music/
├── hyperframes/                ← 选中 HyperFrames 时的运行时工作区
│   ├── index.html              ← 根合成
│   ├── compositions/           ← 子合成与 registry 块
│   │   └── components/         ← registry 组件（颗粒 overlay 等）
│   ├── assets/                 ← 项目资源的 symlink 或拷贝
│   ├── hyperframes.json        ← CLI 配置（registry URL、安装路径）
│   ├── DESIGN.md               ← 源自 playbook 的视觉 brief（可选）
│   └── narration.wav           ← 适用时的 TTS 输出
└── renders/
    └── final.mp4
```

模板化工作区在 compose 阶段由 `hyperframes_compose` 根据 `edit_decisions` + `asset_manifest` + 活跃 playbook 生成。Atelier 工作区在 assets 阶段编写，经 `hyperframes_compose.render_existing` 原样传递。二者均位于 `projects/` 下，与其余生产工作区一并 gitignore。

### 为何每项目独立工作区

- HyperFrames 相对项目根解析 `data-composition-src`、`src=` 与 registry 块。共享工作区会破坏这一点。
- `npx hyperframes lint | validate | render` 均针对项目目录操作，不像 Remotion 那样接受抽象 composition ID。
- 资源与引用它们的 HTML 相邻，与 `website-to-video` 参考工作流一致。

---

## 产物 → HyperFrames 映射

当 `render_runtime = "hyperframes"` 时，compose 阶段将 OpenMontage 产物翻译为 HyperFrames 项目文件：

| OpenMontage 产物字段 | HyperFrames 目标 |
|---|---|
| `edit_decisions.cuts[]`（场景序列） | `index.html` 时间轴，每个 cut 一个 `<div data-composition-id data-composition-src>` |
| `edit_decisions.cuts[i].in_seconds / out_seconds` | 片段元素上的 `data-start` / `data-duration` |
| `edit_decisions.cuts[i].type`（场景类型） | 经 `hyperframes add` 安装的 registry 块，或手写子合成模板 |
| `asset_manifest.assets[]` 路径 | 拷贝或 symlink 至 `projects/<p>/hyperframes/assets/`，以相对 `src=` 引用 |
| `audio.narration.segments[]` | 匹配 `data-start` / `data-duration` 的 `<audio>` 元素 |
| `audio.music` | 第二个 `<audio>` 元素，较低 `data-volume` |
| `subtitles`（启用 + 来源） | registry `captions` 块或手写逐词 span — **非** `remotion_caption_burn` |
| 所选 playbook（`flat-motion-graphics`、`clean-professional` 等） | `:root` CSS 自定义属性 + `DESIGN.md`。见 `lib/hyperframes_style_bridge.py`。 |
| `renderer_family` | 控制使用哪套顶层 HTML 模板及预装哪些 registry 块 |

具体渲染：`hyperframes_compose` 向工作区写入文件，执行 `lint → validate → render`，并返回带生成 MP4 路径的 `render_report`。见 `tools/video/hyperframes_compose.py`。

### 工作区本地创作产物

上游 `website-to-video` 技能使用 `DESIGN.md`、`SCRIPT.md`、`STORYBOARD.md` 作为分步工作区文件。OpenMontage **不会**用这些取代 canonical 产物契约 — `brief`、`script`、`scene_plan`、`edit_decisions` 等仍是 `projects/<p>/artifacts/` 下的真源。将上游文件视为写入 HyperFrames 工作区的**便利副本**，使运行时工作流更自然：

- `DESIGN.md` — 源自所选 playbook，由 `hyperframes_compose` 或 `lib/hyperframes_style_bridge.py` 写入。可在工作区内作工作 brief。
- `SCRIPT.md` — 可选旁白文案供人工审阅。Canonical script 仍在 `artifacts/script.json`。
- `STORYBOARD.md` — 可选逐 beat 创意方向。Canonical 场景计划在 `artifacts/scene_plan.json`。

若工作区本地文件与 canonical 产物不一致，以 canonical 产物为准。

---

## 运行时选择规则

1. **提案阶段**选定 `render_runtime`，在 `decision_log` 中以类别 `render_runtime_selection` 记录决策。须考虑上述决策矩阵及各运行时的实际可用性。
2. **Preflight** 报告哪些运行时可用（见下）。不可用的运行时不是有效提案选项，除非用户明确批准安装。
3. **Edit 阶段**原样传递 `render_runtime`。
4. **Compose 阶段**读取 `edit_decisions.render_runtime`，经 `video_compose` → `hyperframes_compose`（HyperFrames）或既有 Remotion 路径路由。Compose 不得在无新 `render_runtime_selection` 决策时更换运行时。
5. **终审**记录 `render_runtime_used`；若与提案不一致则设 `runtime_swap_detected = true`。

---

## Preflight — HyperFrames 可用性

Preflight 时，provider 菜单报告 HyperFrames 可用性。`hyperframes_compose` 工具的 `get_info()` 返回：

```json
{
  "runtime_available": true | false,
  "node_major": 22,
  "ffmpeg_available": true,
  "doctor_ok": true,
  "install_instructions": "…"
}
```

下限要求（以下全部满足时 `runtime_available: true`）：

- Node.js 主版本 ≥ 22
- PATH 上有 `ffmpeg` 二进制
- PATH 上有 `npx`（随 Node.js 捆绑）
- `npx hyperframes doctor` 退出码为 0，或等价轻量检查通过

**不要求** `bun` — HyperFrames 可通过 `npx hyperframes` 使用（npm 包名为 `hyperframes`； monorepo 内部的 `@hyperframes/cli` **未**在公共 npm registry 发布，会 404）。

当 `runtime_available: false` 时，preflight 须 surfaced 原因与安装说明。按 `AGENT_GUIDE.md` Setup Offer Protocol，按工作量分组修复：

- 缺少 Node 22 → 约 5 分钟安装，说明解锁能力
- 缺少 FFmpeg → macOS/Linux 约 1 分钟，Windows 更长
- `doctor` 报错 → 原样展示 doctor 输出

---

## 验证协议

HyperFrames 提供完整验证栈。在声明渲染完成前**全部**执行：

1. **`npx hyperframes lint`** — 静态契约检查（重复 id、轨道重叠、缺少 `data-composition-id`、未注册时间轴）。渲染前**必须**通过。
2. **`npx hyperframes validate`** — 基于浏览器的运行时检查：seek 到暂停的合成、截图、采样像素、计算 WCAG 对比度、验证 `window.__timelines` 注册及 timed 元素上的 `class="clip"`。渲染前**必须**通过（迭代可用 `--no-contrast` 推迟对比度，终稿不可）。
3. **`npx hyperframes render --quality standard`** — 产出 MP4。
4. **渲染后终审** — ffprobe 探测、采样帧、转写音频、与 script 比对。与 Remotion 路径相同契约。见 `final_review.schema.json`。

若 lint 或 validate 失败，**不要**渲染。修复合成后重跑。对失败合成静默渲染是契约违规 — HyperFrames 的价值在于 validate 能捕获 FFmpeg 或 Remotion 无法捕获的问题。

---

## 风格桥接（playbook → CSS）

OpenMontage playbook 当前翻译为 Remotion `themeConfig` 对象。对 HyperFrames，等价翻译产出：

- `:root` 上一块 CSS 自定义属性（`--color-bg`、`--color-fg`、`--color-accent`、`--font-heading`、`--font-body`、`--ease-primary`、`--duration-primary` 等）。
- 简短 `DESIGN.md`，用平实语言说明视觉系统。
- 可选 typography `@import`（仅 HyperFrames 字体编译器支持的字体）。

见 `lib/hyperframes_style_bridge.py`。Playbook **无需**分叉 — 现有 playbook schema 已足够驱动 Remotion 与 HyperFrames 输出。

---

## 成本模型

HyperFrames 渲染在本地：API 成本 $0，但 CPU 密集（无头 Chrome + FFmpeg）。经 `cost_tracker` 跟踪：

- `estimate` — 基于合成时长 × 分辨率 × `--workers`
- `reserve` — 0（无 API 花费）
- `reconcile` — 墙钟渲染时间

与 Remotion 相同模式。

---

## 实践中的坑（血泪经验）

上游文档未警告、却可能让你用 60 分钟渲染才发现的事项。在**创作时**修复，而非渲染时。

### 全帧背景视频：源分辨率陷阱（**非**框架 bug）

现象：背景视频渲染为居中黑边小框，尽管你已告诉 HyperFrames 片段为 1920×1080。六次渲染调试表明这**几乎总是源质量问题，而非 HyperFrames 框架 bug。**修输入，别修 CSS。

根因（Pexels + Pixabay 库存观察）：许多免费库存片段即使用「大尺寸」档仍只有 640×360 或 960×540。若预变换为
`scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:...`
会得到 1920×1080 文件，可见内容却是居中 640×360 矩形加黑边。HyperFrames 忠实播放 — 你看到的「小视频在黑框里」是正确渲染的 letterbox 输入。

诊断优先：怪 CSS 前，对源片段与预变换片段运行
`ffprobe -v error -select_streams v -show_entries stream=width,height`。
若预变换已在 1920×1080 padding 内显示 640×360 有效区域，问题在上游。

预变换改为 scale-to-COVER 并 crop，而非 scale-to-FIT 并 pad：

```
-vf "scale=1920:1080:force_original_aspect_ratio=increase,\
     crop=1920:1080,unsharp=3:3:0.6"
```

将小片段放大至少覆盖 1920×1080、裁切溢出，unsharp 抵消感知 softness。输出满帧，HyperFrames 会 edge-to-edge 渲染。

canonical wrapper-div 模式（`patterns.md`）仍是背景的正确 HTML 形状：

```html
<div style="position:absolute;top:0;left:0;width:1920px;height:1080px;overflow:hidden;">
  <video
    data-start="0" data-duration="60" data-track-index="0"
    src="..." muted playsinline
    style="width:100%;height:100%;object-fit:cover;"
  ></video>
</div>
```

使用它是因为 wrapper 上 `overflow: hidden` 在视频宽高比略偏离 16:9 时优雅裁切，内层 `<video>` 上 `object-fit: cover` 处理（少见）源宽高比非 16:9。**不是**框架布局 bug 的变通 — 若源文件内容填满整帧，框架也会正确 sizing `<video class="clip">`。

在 wrapper 或 scoped 选择器如 `.bg-slot video { filter: ... }` 上应用视觉处理（`filter`、`border-radius` 等）。

隐式 vs 明显失败模式：叠加 dim 滤镜（`brightness(0.25–0.35)`）或满帧 typography 时 letterbox 读作「暗调氛围」，陷阱被隐藏。一旦 footage-forward（brightness > 0.5、lower-third typography）立刻明显。若从一开始就 footage-forward，在 asset 阶段探测源分辨率。

若确实无法获得 HD 素材，切换流水线：FFmpeg 混合合成（在外部 b-roll reel 中 scale-to-cover + crop + unsharp，再经 chromakey 叠加 HyperFrames typography）。`projects/quantum-willow-multiverse/` 在六次 640×360 Pexels 源的 HyperFrames 渲染后采用该模式。

### 渲染前务必 preview-scrub footage-forward 场景

60 分钟渲染昂贵。全量渲染前，打开 Launch 预览面板（或 `npx hyperframes preview`），至少 scrub 到每个 b-roll 应占主导的章节之一场景。tiny-video bug — 及类似「lower-third 文字在 1080p 屏外」— 预览时 2 秒视觉检查，渲染时 60 分钟回归成本。

### 提升库存 footage 可读性，而非 opacity

在 b-roll 上叠 typography 时，别只降视频 opacity — 两层都糊。应：

- 视频保持 `filter: brightness(0.55) saturate(0.85)`（可见但压暗）。
- 在特定文字后加局部 CSS scrim（`radial-gradient` 或带 `rgba(7,7,12,0.5)` 的 `linear-gradient`），尺寸贴合文字块。
- 文字本身 `text-shadow: 0 2px 24px rgba(0,0,0,0.8)` 作与背景无关的局部 halo。

footage 仍显生动，任意帧上 caption 与标题可读。

### 渲染前库存片段需密集关键帧

当库存片段关键帧间隔 > 5s 时，渲染失败 `video_heavy_parallel_timeout` 或帧冻结。下载的库存经 `ffmpeg ... -c:v libx264 -r 30 -g 30 -keyint_min 30 -sc_threshold 0 -movflags +faststart` 重编码后再 staging 到工作区。见 `hyperframes_compose` 现有工作区 prep — 尚未自动执行。

### 视频重度合成用 `--workers 1` 渲染

默认并行 capture 在大量视频同时加载时会压垮无头 Chrome。合成中 >5 个背景 video 元素时，`hyperframes render` **始终**传 `--workers 1`。

### 使用 Outfit / Inter / JetBrains Mono，而非 Space Grotesk

HyperFrames 确定性字体编译器仅内联其有映射的字体。`Space Grotesk` 即使用 Google Fonts 加载也常回退 Arial。查编译器警告或 `deterministicFonts.ts` 映射表。稳妥选择：`Outfit`、`Montserrat`、`Inter`、`JetBrains Mono`、`Poppins`、`Playfair Display`。

## 反模式

- ❌ 为 HyperFrames 分叉 playbook 数据，而当前 schema 已携带颜色、字体与动效。
- ❌ 编写引用 `remotion-composer/public/` 的 HyperFrames 合成 — HyperFrames 工作区独立且自包含。
- ❌ 从 OpenMontage orchestrator 运行 `hyperframes init`。`init` 创建自有项目语义并安装 agent skills — 面向人类 bootstrap 项目，非流水线。`hyperframes_compose` 直接生成项目文件。
- ❌ 把 HyperFrames 当「没有 Remotion 的 React」。HyperFrames 是 HTML 优先 + GSAP。若场景以 React JSX 编写，应属 Remotion。
- ❌ 在 HyperFrames 内 GSAP 使用 `repeat: -1`。无限 tween 破坏确定性 seek-and-capture 渲染。始终有界 repeat。
- ❌ 在时间轴构建期间从 `async` 上下文、`setTimeout` 或 Promise 做动画。页面加载后 `window.__timelines` 必须**同步**完全填充。

---

## 采用 HyperFrames 的流水线

| 流水线 | 状态 |
|----------|--------|
| `animation` | Wave 1 — 动效图形重度 brief 的一等选项 |
| `animated-explainer` | Wave 1 — HTML/GSAP 原生概念可用 HyperFrames；数据图表重度解说仍以 Remotion 为默认 |
| `screen-demo` | Wave 1 — 合成产品 UI 可用 HyperFrames；终端专用 demo 仍优先 Remotion `TerminalScene` |
| `cinematic` | Wave 2 |
| `hybrid` | Wave 2 |
| `documentary-montage` | Wave 2 |
| `talking-head` | 推迟 — 依赖 TalkingHead 对等 |
| `avatar-spokesperson` | 推迟 — 依赖 TalkingHead 对等 |
| `clip-factory`、`podcast-repurpose`、`localization-dub` | 推迟 — 当前 compose 路径依赖 Remotion caption burn |
| `framework-smoke` | N/A（测试流水线） |

已采用流水线的 proposal 与 compose director 明确描述运行时选择 — 见各流水线 `proposal-director.md` 与 `compose-director.md`。
