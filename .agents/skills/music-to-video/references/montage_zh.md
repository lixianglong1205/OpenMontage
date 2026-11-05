# 素材处理 — 将用户媒体编织到节拍骨架上

当用户提供图片/视频时，某个编组可以是**素材处理（asset treatment）**，而不是字排模板或自由编排。素材是**同一节拍骨架上的附加成分** — 绝不是独立流水线。字排/模板仍是基线：若没有素材适配某编组，则回退到模板/自由编组（完整视频可以零素材）。

规划器（Step 3）选定处理方式以及片段 + 锚点（WHAT）；frame-worker 在 frame 文件内实现（HOW）。**遵守 frame 的 `pacing`。**

## 三种处理方式

### `beat_cut` — 每个锚点一段 clip（仅用于 `beat_cut` frame）

素材驱动的、类似「每个 onset 一组字排」的编组：在每个锚点切到新 clip（来自 audiomap 的 frame 节拍/onset）。每段 clip 是 `class="clip"` 元素（照片用 `<img>`，动态片段用**静音** `<video>`），按核心 clip 约定在其锚点放置，并设置 `data-start`/`data-duration`/`data-track-index`。片段之间，在**下一个锚点处**将 outgoing 内容 crossfade 到 `opacity:0`，随后立即用 `tl.set(..., {opacity:0}, anchor)` **硬清除** — 这一对操作是必需的（`gsap_exit_missing_hard_kill` lint 规则；否则非线性 seek 会残留旧帧）。在**强**锚点上切；在 `key_moment`/downbeat 上落 hero clip。

### `ken_burns` — 单 clip 慢推（适配 `phrase_flow` frame）

用于平静 frame：整段 span 内持有一段 clip，缓慢 scale/translate 推进（例如 scale 1.0→1.08 + 小幅漂移），在整段 `span_sec` 上缓动 — 由 frame 定节奏，而非按 beat。无硬切。在 frame 边缘 crossfade 进/出。当 beat 网格不可靠（平静音乐）时，这是合适的素材处理方式。

### `bg_under_text` — clip 压暗衬于模板/自由编组之下

全幅 clip 压暗约 30–50%，作为编组背景；前景为模板或自由编排的字排处理。文字仍骑在同一批锚点上；clip 是底床。当用户希望出现其 footage 但信息必须可读时使用。

## 规则

- **`pacing` 决定处理方式**：`beat_cut` 仅用于 `beat_cut` frame；在 `phrase_flow` frame 上用 `ken_burns` 或慢 crossfade — **切勿**在（不可靠的）平静网格上做 per-onset 硬切。
- **Clip 静音；根节点拥有音频。** 将每个 `<video class="clip">` **muted** 挂载，作为 frame 根的直接子节点（切勿嵌套在其它 timed 元素内，否则 renderer 会冻结）。v1 中 BGM 是唯一音频。
- **Crossfade 动画 `opacity`/`autoAlpha`**，勿对 `.clip` 使用 `visibility`/`display`（框架拥有 clip 可见性 — 会触发 `gsap_animates_clip_element`）。
- **背景压暗约 30–50%**，保证前景文字可读。
- 锚点为 **`audiomap.json` 中的轨道秒**；worker 减去 frame 起点得到 frame 本地时间。
- 仅本地 staged 素材（经 `stage-assets.mjs` 的 `assets/`）；禁止远程 URL。

## 延后挂钩（非 v1）

需要播放**自身声音**的 clip（采访片段、歌词 clip）需要在**根**上由 assembler 挂载兄弟 `<audio>`，并在其下 duck BGM（时间轴音量自动化：`tl.to("#el-bgm",{volume:0.15,…},clipStart)` … `tl.to(…,{volume:0.9,…}, clipEnd)`）。frame-worker 不挂载 audio。v1 保持 clip 静音；仅在用户要求时再接入 clip-audio + ducking。
