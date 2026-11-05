# 创意导演 — 纪录片蒙太奇流水线

## 何时使用

你要把用户提示转化为下游各阶段都会读取的 brief 工件。在本流水线中，brief 是主题核心：蒙太奇**讲什么**、**应呈现何种感受**、以及**时长**。

## 运行时选择（强制 — 呈现约束，勿静默选定）

锁定 `render_runtime = "remotion"`。**HyperFrames 在 Phase 1 本流水线中不是有效运行时** — documentary-montage 依赖 Remotion 的 `CinematicRenderer` 合成及其 ProRes-4444 透明通道片尾叠层栈，HyperFrames 尚无对等实现。

按 AGENT_GUIDE.md →「Present Both Composition Runtimes (HARD RULE)」：**不要**静默默认。告知用户：「HyperFrames 在你机器上可作为替代运行时，但 documentary-montage 依赖 Remotion CinematicRenderer + 片尾叠层栈，因此此处 remotion 是唯一可行选择 — 可以继续吗？」在 `decision_log` 中记录 `render_runtime_selection` 决策：`options_considered` 列出两种运行时，hyperframes 的 `rejected_because: "CinematicRenderer + end-tag overlay parity deferred on documentary-montage"`。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/brief.schema.json` | 工件校验 |
| 用户输入 | 对话历史 | 原始需求 |
| Meta | `skills/meta/reviewer.md` | 自检环节 |

## 流程

### 1. 提炼主题问题

纪录片蒙太奇回答的是用户无法用一句话说清的问题。你的任务是用**一行**点明该问题。

好的主题问题示例：

- "What does it feel like to come home?"（回家是什么感觉？）
- "How did the 20th century think about the future?"（20 世纪如何想象未来？）
- "What happens in a city at 4am?"（凌晨四点的城市发生什么？）
- "What do all the footprints on Earth look like?"（地球上所有的足迹合在一起像什么？）

差的主题问题（过于抽象或过于具体）：

- "A video about cities"（关于城市的视频 — 太抽象，没有感受）
- "A montage with 8 specific shots of the moon"（8 个指定月球镜头的蒙太奇 — 太具体，那是镜头表而非主题）

### 2. 确定基调

选择**一种**情绪 register。写下来。下游一切以此为准。

本流水线常见 register：

- **elegiac（挽歌式）** — 长停留、低饱和色彩、慢切（失落、记忆、归属）
- **urgent（紧迫）** — 短切、硬同步、动势强（危机、城市、当下）
- **reverent（虔敬）** — 庄重、对称、从容（自然、仪式、尺度）
- **wry（冷幽默）** — 反讽并置、在荒诞处切（消费文化、政治、mid-century 式乐观）
- **dreamlike（梦感）** — 慢溶解、重复母题、非线性（童年、哀思、记忆）

### 3. 选定时长与结构形态

时长决定 beat 数量上限。

| 时长 | Beats | 用途 |
|----------|-------|-----|
| 30-45s | 8-12 cuts | 社交/Instagram/reel — 单一感受，无弧线 |
| 60-90s | 15-25 cuts | 标准短片 — 带转折的 mini arc |
| 2-3 min | 30-50 cuts | 完整 essay 蒙太奇 — 可做三幕弧 |

结构形态选项：

- **single-image expansion（单意象展开）** — 一个想法，多角度持住（适合 60s 内 elegiac）
- **before/after（前后对照）** — 前半建立，后半转折（适合 wry 或 urgent）
- **three-act（三幕）** — 铺垫 → 转折 → 释放（Adam Curtis 式手法，需 >90s）
- **list/catalogue（清单/目录）** — 「每一个……」结构，无弧，纯累积（适合 reverent 或 elegiac）

### 4. 记录音乐意图（强制）

纪录片蒙太奇与其音乐 bed 不可分。**本流水线音乐为强制项。** 唯一例外是用户明确 opt-out（例如「不要音乐，要静音」）— 必须记为 `music_plan.source = "none"` 并填写 `music_plan.opt_out_reason`。

在创意阶段看似「纯粹」的默片 brief，到 compose 时常像 abandoned footage。勿假设静音会自行成立。若用户未提音乐，**默认需要音乐**并选择：

- 用户提供的音轨（路径写入 `music_plan.source_path`），
- 音乐库选取（查询 `registry.get_by_capability("music_library")` 并列出曲目），
- 免版税搜索（查询 `registry.get_by_capability("music_search")`，报告 provider 与 license），
- 生成（写明工具与 register 对应的 prompt seed），
- 明确 opt-out（`source: "none"` + `opt_out_reason`）。

在声明无可用来源前，还要查询 `registry.get_by_capability("music_generation")`。**若无任何音乐来源，警告用户。** 勿静默推迟 — 否则会在 asset 阶段变成昂贵意外。

### 5. 记录片尾 tag 意图（强制）

每支 documentary-montage 影片以哲学式 end-tag 收束 — 一句短而抽象的 line，赋予全片意义。由 Remotion 片尾卡渲染（「shining underlined tag」register — 粗体、字距、动画下划线）。

**默认 mode 为 `"overlay"`** — tag 在正片最后几镜上淡入，像影片的一部分而非末尾硬贴的黑卡。备选为 `"concat"`，在正片后追加独立黑卡。仅当用户明确要求分离 title card，或末镜画面过杂导致叠字难读时使用 concat。

**End-tag 为强制项。** 唯一例外是用户明确 opt-out，记为 `end_tag_plan: null` 并填写 `end_tag_opt_out_reason`。

在 brief 阶段提出 end-tag。写 3 个选项并推荐其一。预期形态：

```json
{
  "end_tag_plan": {
    "text": "WE BUILT BOTH WITH THE SAME HANDS.",
    "palette": "warm_ivory_on_black",
    "duration_seconds": 5.5,
    "render_engine": "remotion",
    "component": "EndTag",
    "mode": "overlay"
  }
}
```

字段说明：
- `text` — 3-9 词。论点，非摘要。
- `palette` — `"cool_offwhite_on_black"` 或 `"warm_ivory_on_black"`。
- `duration_seconds` — tag 屏总时长（淡入 + 停留 + 淡出）。5-8s 为甜区。
- `render_engine` — 恒为 `"remotion"`。
- `component` — 恒为 `"EndTag"`。
- `mode` — `"overlay"`（默认）或 `"concat"`。
  - **overlay**：tag 渲染为带 alpha 的 ProRes 4444 → 经 FFmpeg overlay 叠在正片末段。tag 淡入覆盖正片最后 N 秒。正片淡出与 tag 淡出应对齐。
  - **concat**：tag 渲染为不透明 MP4 → FFmpeg concat 接在正片后。总时长 = 正片 + tag。

### 6. 记录旁白意图（可选）

与音乐、end-tag 不同，旁白为**可选**。若画面 + 音乐 + end-tag 已承载 register，可无旁白。若使用旁白，写明 TTS provider 与 voice。无旁白时显式记 `narration: "none"` — 勿留空字段。

### 7. 写入 Brief

brief 至少包含：

```json
{
  "topic": "A minute in the rain",
  "thematic_question": "What does rain show you about a city?",
  "tone": "elegiac",
  "duration_seconds": 90,
  "shape": "list",
  "sources_allowed": ["pexels", "pixabay_video", "coverr", "mixkit", "archive_org", "nara", "nasa"],
  "generated_clips_allowed": false,
  "narration": "none",
  "music_plan": {
    "source": "generated",
    "provider": "elevenlabs",
    "prompt_seed": "slow ambient drone in A minor, no percussion, 60s sustained swell, Max Richter register"
  },
  "end_tag_plan": {
    "text": "THE CITY KEEPS ITS OWN VIGIL.",
    "palette": "cool_offwhite_on_black",
    "duration_seconds": 5.5,
    "render_engine": "remotion",
    "component": "EndTag"
  },
  "era_mix": "any",
  "target_platform": "social_short"
}
```

`era_mix` 为纪录片专用字段："modern" 偏向 Pexels，"vintage" 偏向 Archive.org Prelinger，"any" 由 scene director 按 slot 决定。

### 8. 质量门

- 主题问题为**一句**话。
- 基调为固定列表中的**一种** register。
- 时长与 shape 为具体数字 / 枚举值。
- `music_plan` 存在，且要么指明真实来源，要么 `source: "none"` + `opt_out_reason`（用户明确决定）。
- `end_tag_plan` 存在，且要么有非空 `text`，要么为 `null` 并带 `end_tag_opt_out_reason`（用户明确决定）。
- sources 列表非空，且 preflight 中 `corpus_builder.source_provider_menu` 显示至少一个所请求来源为 `available`。

## 常见陷阱

- 多个主题并列（「关于城市**又**科技**又**失落」）。只选一个。其余作为下游联想。
- 跳到镜头表。brief 讲的是**意义**。镜头在下一阶段。
- 忽略时长。45s 配 50 切会晕。3 分钟只有 12 切像幻灯片。
- 忘记问音乐。用户通常有偏好。
- 假设静音会自行成立。不会。除非用户明确不要，否则音乐为强制。
- 因「画面自会说话」跳过 end-tag。不会 — end-tag 是论点。每次都要提出。

---

## 关卡提醒（具约束力）

本阶段需人工批准（`human_approval_default: true`）。review 通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot 看板渲染工件），并**结束本轮**。勿在同一回复中启动下一阶段。
批准按关卡计 — 更早的「继续」不覆盖本关卡。
