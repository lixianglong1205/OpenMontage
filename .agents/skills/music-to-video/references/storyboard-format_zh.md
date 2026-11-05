# STORYBOARD.md 格式 — 帧 → 组

`STORYBOARD.md` 是用户在第 3 步审阅并批准的唯一可审计划，也是第 4 步各 frame-worker 遵循的**手册**。它是**层级结构**：每个**帧**一个块，以 `## Frame N — <frame_id>` 标题书写（解析器识别 `Frame`）。**一帧 = 一个场景 = 一个 composition 文件。** 每个帧块内包含其**组**（treatment 单元）。assembler 读取帧级（`duration` → `data-start`，`src`）；worker 读取各自帧块。帧的 **composition id = 其 `src` 文件主名**（`compositions/frames/01-f1.html` → `01-f1`），worker 将其用作 `data-composition-id` 与 `window.__timelines` 的键。

第 2 步写入骨架（帧字段，组为 `TBD`）；第 3 步填充组与品牌。这是构建规格，不是代码 — planner 写 WHAT，worker 决定 HOW。**切勿在此写入毫秒级 tween。**

## 文件结构

YAML frontmatter（视频级主干）+ 每帧一个 `## Frame N — <frame_id>` 块。

```markdown
---
compositionId: bgm
duration_s: 30.0 # == audiomap.audio.duration_sec, exactly
canvas: { w: 1920, h: 1080, fps: 30 }
style: # brand spine — from the chosen frame.md preset (Step 3)
  font: "EB Garamond / Inter / JetBrains Mono" # the preset's typography, verbatim
  palette: ["#FAF9F5", "#141413", "#CC785C", "#181715"] # ≤4–6 swatches from the preset's colors
assets: false # false, or a note like "assets/ has 6 user photos"
build_notes: ["one paused timeline per frame", "no remote assets"]
avoid: ["generic slideshow", "tiny unreadable hero text"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html # worker writes here; assembler refs it; stem (01-f1) = composition id
- duration: 7.198s # = span length; the assembler reads this for cumulative data-start
- span_sec: [0.0, 7.198] # track seconds; frames tile the track
- pacing: beat_cut # beat_cut | phrase_flow (from the skeleton; obey it)
- mood: [hype]
- feel: accelerating onset stream into a held downbeat

### Groups

- **g1** — template: `intro-kinetic-cascade`
  - span_sec: [0.0, 4.017] # frame-LOCAL build is 0-based; these are TRACK seconds (worker subtracts frame start)
  - params: { theme: "light", icon: "bolt", phrases: "[…]", climax: "{…}" }
  - role_bindings: { phrase: { times: [0.14, 0.55, 0.87] }, climax: { in: 3.79, iconAt: 4.9 } }
  - copy: "GROWTH THROUGH CREATIVITY"
- **g2** — free_design
  - span_sec: [4.017, 7.198]
  - free_design: { dominant_system: "per-onset typography", primitives: ["content-swap", "braam-punch"], density_topology: "accumulate" }
  - anchors: [4.10, 4.80, 5.50, 6.20] # onset seconds the reveals ride (from audiomap)
  - copy: ["BUILD", "SHIP", "REPEAT"]

## Frame 2 — f2

…
```

## 帧块 — 必填字段

| 字段                              | 含义                                                                                                                           |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| heading `## Frame N — <frame_id>` | `frame_id` 与 `src` 主名一致；`N` 为从 1 开始的索引。                                                                    |
| `src`                             | `compositions/frames/NN-<frame_id>.html` — worker 写入位置；assembler 引用。主名 = `data-composition-id`。 |
| `duration`                        | 帧跨度长度（秒）（如 `7.198s`）— **必填**；assembler 累加这些值得到 cumulative `data-start`。         |
| `span_sec`                        | 轨道秒 `[start, end]`。`duration = end − start`。                                                                        |
| `pacing`                          | `beat_cut` \| `phrase_flow` — 来自骨架；worker 必须遵守（`phrase_flow` 上不可硬切）。                          |
| `mood`, `feel`                    | 来自骨架；调性 + planner 所匹配音乐情境的一行描述。                                            |
| `### Groups` list                 | ≥1 个组；组按顺序铺满帧跨度。                                                                                 |

## 组条目 — 恰好三种之一

每个组必须是 **template** OR **free_design** OR **asset** — 不能两种兼有，也不能都没有。三者均带 `span_sec`（轨道秒，铺满帧）并可带 `copy`。

- **template** — `template: <catalog id>` + `params`（来自 catalog 条目的键）+ `role_bindings`（真实 audiomap 锚点秒）+ `copy`。
- **free_design** — `free_design: { dominant_system, primitives: [catalog ids], density_topology }` + `anchors`（真实 beat / onset 秒）+ `copy`。
- **asset** — `asset: { treatment, clips: [public/…], anchors?, overlay_copy? }`。`treatment` ∈ `beat_cut`（每个 anchor 一 clip — 仅用于 `beat_cut` 帧）| `ken_burns`（慢推 — 适合 `phrase_flow`）| `bg_under_text`（clip 在 template / free 组后方 dim）。见 [`montage.md`](montage.md)。

## 规则

- 帧铺满轨道（无间隙，首帧从 0 起，末帧止于 `duration_s`）；帧内组铺满其跨度；无组短于约 1 小节；组边界不得落在 `rolls[]` 运行段内部。
- `params` 键来自模板的 [`template-catalog.md`](template-catalog.md) 条目。
- 所有锚点秒均为 **来自 `audiomap.json` 的轨道秒** — worker 减去帧起点转为帧内局部时间。
- `phrase_flow` 帧不得使用 `beat_cut` asset treatment 或 per-onset 硬切。
- 品牌 `style` 只设一次；各组 palette 均从中取用。
- 可审阅的 prose-plus-data；保持易扫读。无 GSAP，无毫秒级 timing。

## 自检（planner 运行 `validate-plan.mjs`）

- frontmatter 含 `compositionId`、`duration_s`（== audiomap）、`canvas`、`style`。
- 每帧有 `span_sec` + `src` + 正数 `duration` + `pacing` + ≥1 组；帧铺满轨道。
- 每组恰好为 template / free_design / asset 之一；template id 存在于 catalog；anchors 为真实 audiomap 秒；`phrase_flow` 帧无 `beat_cut`。
