# 帧骨架（Step 2）— 读懂音乐，布局帧

在 Step 2，**你（编排者）** 读取 `audiomap.json`，并直接写入 `STORYBOARD.md` 的**骨架**：将曲目切分为**帧**（一帧 = 一个 composition 文件 = 一个场景），并为每一帧设定其**跨度**、**节奏**（这一段更适合硬切到节拍，还是按乐句/能量平缓流动？）、**情绪**，以及一行**感受**说明。

你**只做分类与脊柱布局。** 不选模板、不写文案、不选颜色/字体，也不决定帧内的 groups — 这些属于 Step 3（计划会在原位填满每一帧）。每一帧的 `### Groups` 保持为 `TBD (Step 3)`，frontmatter 中的 `style` 留空。

**没有中间 JSON** — 骨架就是 `STORYBOARD.md` 的起点。Step 3 编辑同一文件。

## 信任边界（请先读）

`audiomap.json` 是某一分析器的输出。部分字段对**任意**音乐都稳健；部分仅在音乐**确实具有节奏感**时才可靠。这决定每一帧的 `pacing`：

| 字段                                                                                                                                                                                               | 信任度                                                                                                                                                                                                                        |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `energy_phases[]`（level / energy / density / feel）、`events[]` + `onset_rate`、`rolls[]`（及其**缺失**）、`silences[]`、`hard_stops[]`、`key_moments[]`、`phrases[]`、`audio.duration_sec` | **始终** — 稳健测量                                                                                                                                                                                             |
| `tempo.bpm`、`grid.beats_sec` / `downbeats_sec` **精度**                                                                                                                                       | **仅当音乐有节奏感时。** 在平静/稀疏素材上，节拍网格是追踪器**强加**的 metronome（常为八度加倍）— 通常 **grid 上的 beat 多于真实 onset**。此类情况**不要**把切点锚定在 grid 上。 |

- **Grid 可靠** 当：存在 rolls，和/或 dense 阶段，和/或 `onset_rate` 高且 grid 稳定。
- **Grid 不可信** 当：`rolls`≈0、多为 `sparse` 阶段、`onset_rate` 低 → 按 `phrases[]` + `energy_phases[]` 定节奏，而非 beat。

## 如何布局帧（按顺序执行）

1. **整体印象。** 从 `summary` / `tempo` / `audio.duration_sec` 与 roll 数量，写入 frontmatter 的 `compositionId`、`duration_s`（== `audio.duration_sec`）、`canvas`，以及一行曲目密度弧线解读。
2. **切分为帧。** 遍历 `energy_phases[]`，在音乐**真正**变化状态处切分 — `hard_stops[]`、`SURGE` / `DROP` 的 `key_moments`、`rolls[]` 段起止、**onset 荒漠**（`events[]` 中长间隔）、或能量层级大幅跳变。合并相邻但属同一手势的阶段。预期 **约 1–6 帧**；短片段可能只有一帧。
   **每个边界先对齐 audiomap 锚点**，**仅当 grid 可靠时**再对齐最近的 `beats_sec`（容差 ≤ ½ beat）；平静素材则对齐 `phrases[]` / `energy_phases[]` 边界。帧**铺满整轨**（首帧从 0 起，末帧止于 `duration_s`，无缺口/重叠）。
3. **每帧设定 `pacing`** — 信任边界判断：
   - **`beat_cut`** — 确有节奏感：存在 roll，**或** dense，**或**（`onset_rate` 明显偏高 **且** grid 稳定）。硬切 / 按 onset 揭示可锚定 beat。
   - **`phrase_flow`** — 平静/稀疏：`rolls`≈0、多为 sparse、`onset_rate` 低。**不要**把硬切锚定在 grid 上；按 `phrases[]` + 能量包络定节奏（慢 crossfade、长 hold）。
4. **每帧标注 `mood`**（1–3 个：`warm` · `dark` · `hype` · `elegant` · `glitch` ·
   `cinematic` · `playful` · `tense` · `dreamy` · `aggressive`），依据 `energy_phases[].feel` +
   energy + brief/标题中的流派线索。
5. **每帧写一行 `feel`** — 用 plain language 描述音乐情境，供 Step 3 对照模板（例如「onset 流加速并汇入一次 held downbeat」、「平静的 held pad，一段长 onset 荒漠」、「快速 sustained-fill roll，无可读信息」）。规划者据此对照目录中的 **Reach for it when** — 要具体、来自稳健字段，不要编造。

## 骨架长什么样

一份有效的 `STORYBOARD.md`：脊柱已设好，每帧的具体处理留给 Step 3
（完整语法见 [`storyboard-format.md`](storyboard-format.md)）：

```markdown
---
compositionId: bgm
duration_s: 30.0 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
style: # blank — Step 3 fills it from the chosen frame.md preset
build_notes: ["one paused timeline per frame", "no remote assets"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 7.198s # = span length; assembler sums these for cumulative data-start
- span_sec: [0.0, 7.198] # track seconds; frames tile the track
- pacing: beat_cut
- mood: [hype]
- feel: accelerating onset stream building into a held downbeat

### Groups

- TBD (Step 3)

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 10.4s
- span_sec: [7.198, 17.598]
- pacing: phrase_flow
- mood: [warm, cinematic]
- feel: calm held pad, one long onset desert

### Groups

- TBD (Step 3)
```

## 自检

- `duration_s == audiomap.audio.duration_sec`；帧无隙铺满整轨（首帧 0，末帧 `duration_s`）。
- 每帧具备 `src` + `span_sec` + `duration` + `pacing` + `mood` + 一行 `feel`。
- `pacing` 来自**稳健**字段（energy / density / rolls / onset_rate），而非单独依赖 `bpm` / `beats_sec`。
- 无帧边界落在 `rolls[]` 段内，也不留下不足 1 bar 的碎片。
- 每帧 `### Groups` 为 `TBD (Step 3)`；`style` 为空。**任何地方都不出现模板、文案、颜色或字体。**
