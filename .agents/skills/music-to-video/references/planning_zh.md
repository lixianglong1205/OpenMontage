# 规划（第 3 步）— 选定品牌，填满每一帧

在第 3 步，**你（编排者）** 将第 2 步的骨架变成完整、已批准的
`STORYBOARD.md`。你在**同一文件**中原地编辑：选定品牌主轴，再对每一
帧决定其 **groups（编组）**，为每个编组选定处理方式，绑定真实的节拍锚点，并撰写文案。

你的信条：**音乐是脊柱；模板是起点，不是牢笼； typography（版式）是地板，素材是同一节拍网格上的可选配料。**

**你负责 WHAT，不负责 HOW。** 你命名 template / primitives、内容、品牌、
锚点秒数与意图。frame-worker（第 4 步）决定 HOW — 微时机、
具体实现、帧内切镜。**永远不要在分镜里写毫秒级 tween。**

## 输入

- 已在 `STORYBOARD.md` 中的第 2 步骨架 — 带 `span_sec` + `pacing` + `mood` + `feel` 的帧。
- `audiomap.json` — 时间真相；读取每帧 span 内的真实锚点秒数。
- [`template-catalog.md`](template-catalog.md) — 模板选择菜单。
- [`motion-primitive-catalog.md`](motion-primitive-catalog.md) — 自由组合菜单（L0 配方）。
- [`montage.md`](montage.md) — 素材处理（仅当用户提供了图片/视频时）。
- 用户简报 / 提供的文案 — 主题、情绪、需保留的原文。

## 步骤 A — 选定品牌主轴（一个预设，原样不改）

整支视频共用一套字体族 + 色板。从
`../hyperframes-creative/frame-presets/` 中**选一个现成预设**，对照
`../hyperframes-creative/references/design-spec.md` 中的预设表 — 按曲目情绪 + 简报选择，
**只关心其 fonts + colors**（模板负责构图与动效；预设只定外观）。**原样**复制：

```bash
cp ../hyperframes-creative/frame-presets/<preset>/FRAME.md "$PROJECT_DIR/frame.md"
```

然后从该文件填充分镜 frontmatter 的 `style`：其 `typography:` 中的 `font`，以及其 `colors:` 中 ≤4–6 个色块的 `palette`。**逐字引用 hex / 字体族 — 禁止臆造或四舍五入。** 每个编组的 palette 参数都从这同一色板取色；这种统一性让不同模板仍像同一支片。

## 步骤 B — 逐帧决定编组

一帧通常是 **一个编组**（一个模板或一个自由组合占满整帧）。
**仅当单一处理方式无法覆盖该帧** 时才拆成 2+ 编组 — 例如忙乱的片头加结尾定版。拆分时在帧 span 内的**真实 audiomap 锚点**处切（`key_moment` / `phrase` 边界 / onset 簇间隙），**绝不在 `rolls[]` 运行段内部**，且每个编组 **≥ 约 1 小节**。密度**不会**迫使增加编组 — 高密度帧通常仍是**一个**编组，其模板在内部吸收密度（如 `poster-tile-mosaic` 这类 meta-template）。**编组数量对应 distinct treatments（不同处理方式），不是节拍数。**

## 步骤 C — 每个编组选定一种处理（三选一）

### A. 匹配模板

阅读 [`template-catalog.md`](template-catalog.md)。将该编组的 `feel` + `mood` + `pacing`
与模板的 **Reach for it when** 对齐；取最接近者。然后绑定：

- 填写 `params`（键来自 catalog 条目）— 文案填入文本槽，palette 来自品牌主轴，`duration` = 该编组的 span 长度。
- 填写 `role_bindings`，使用从 `audiomap.json` 在该编组 span 上读出的**真实锚点秒数**（不要用示例时间）。
- 若模板自然结束点与编组 span 终点不一致， snap 到最近锚点。

### B. 自由组合（没有合适模板）

写 `free_design` — 一条视觉论点，来自 [`motion-primitive-catalog.md`](motion-primitive-catalog.md)
（一个主导系统 + 具名的 L0 primitives + 密度拓扑）+ `anchors`（动效所依附的真实
beat / onset 秒数）。自由组合是**一等公民**选择，应像匹配编组一样认真撰写 — 绝不是失败退路。

### C. 素材处理（仅当用户提供了素材且合适时）

设为 `asset` 编组（见 [`montage.md`](montage.md)）。**遵守 `pacing`：** 在 `beat_cut`
帧上用 `beat_cut`（每锚点一 clip）或 `bg_under_text`；在 `phrase_flow` 帧上用
`ken_burns` 或慢 crossfade — **禁止** 按 onset 硬切。素材是附加项：若没有合适的，
回退到 template / free（版式是地板 — 完整视频可以没有素材）。

## 文案（你负责措辞）

- 保留用户原文；否则按简报情绪有品味地创作。
- **信息 vs 纹理：** 可读词 ≥1 beat（标题 3–8，句子 4–10），稳定且 focal；持有时长 <1 beat 的词是纹理（strobe / grid / ticks）。不要把信息词硬塞到 sub-beat — 降级为纹理。
- 将文案放入模板的 text params、自由编组的 anchors，或 asset 编组的 `overlay_copy`。声明 anchor + accumulate / stagger 意图；微时机留给 worker。
- 结尾 logo / CTA 落在 final hit / hard stop 上，并 hold 过 trailing silence。

## 转场（你不输出）

目前全部为 **0ms 硬切**。**帧 → 帧** 由 assembler 负责（文件首尾相接）；相邻 `span_sec` 已隐含切点。**帧内 group → group** 由 worker 在其帧时间轴上负责；你只设每个编组的 `span_sec`。

## 写入与校验

补全 `STORYBOARD.md`（见 [`storyboard-format.md`](storyboard-format.md)），然后运行
`node scripts/validate-plan.mjs` 并修复每一个 `✗`。向用户展示逐帧摘要并
迭代直至批准。

## 自检

- `frame.md` 是某一预设的逐字复制；frontmatter 的 `style.font` / `style.palette` 取自其中（精确值）。
- 每帧至少 1 个编组；编组按顺序铺满帧 span；无编组 < ~1 bar；无编组边界落在 `rolls[]` 运行段内。
- 每个编组恰好是 template / free_design / asset 之一。
- 模板 `params` 键与 catalog 条目一致；`role_bindings` / `anchors` 使用真实 audiomap 秒数。
- 素材处理遵守 `pacing`（`phrase_flow` 帧上不用 `beat_cut`）。
- 每个编组的 palette 来自同一品牌色板。
- `duration_s == audiomap.audio.duration_sec`；`validate-plan.mjs` 通过。
