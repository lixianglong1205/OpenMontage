# 音效（SFX）

具名音效由共享音频引擎（`scripts/audio.mjs` → `scripts/lib/sfx.mjs`）产出。**按引擎的唯一开关做 Provider 门控**——是否配置了 HeyGen 凭证，在启动时决定一次（而非按每条 cue）：

- **已配置 HeyGen 凭证 → 所有 cue 均从 HeyGen 音频库检索**（`/v3/audio/sounds`，`type=sound_effects`，`min_score=0.4`）。为搜索并下载，**并非**生成。不会使用内置库。
- **无凭证 → 使用内置 21 文件库**（`assets/sfx/` + `manifest.json`）：按 cue 名称匹配，将匹配文件复制到项目中。离线、确定性、免费。

没有 `npx hyperframes sfx` 命令。SFX 从不生成——在线时为检索，离线时来自内置库。

## Cue — 请求 → meta

每一行通过 `lines[].sfx: ["whoosh", "ui click"]` 声明所需音效。引擎将这些扁平化为 cue，按上述开关解析，对相同的 `(id, name)` 去重（同一音效命名两次只下载/复制一次），并写入 `audio_meta.sfx[]`：

```jsonc
{
  "id": "3",                       // joins the cue to the caller's model (frame / scene / segment)
  "name": "whoosh",
  "file": "assets/sfx/whoosh.mp3", // downloaded or copied, relative to project root
  "source": "heygen" | "local",    // which route resolved it
  "offset_s": 0,                   // delay from the line's start
  "duration_s": 0.57,
  "volume": 0.35                   // SFX sit UNDER voice + BGM
}
```

匹配不到的 cue 会被**跳过**（记为异常）；SFX 从不会阻塞渲染。

## HeyGen 检索（已配置凭证）

`searchSounds(name, "sound_effects", { limit: 3, minScore: 0.4 })` → 取最高分 → `assets/sfx/<slug>.mp3`。结果按 `score` 排序（每条含预签名 `audio_url`、`duration`、`description`）。下限为 **0.4**，因为较好的 SFX 命中约在 0.5–0.67——低于 API 默认的 `0.7` 会静默丢弃大多数具名 cue（只有 whoosh/swoosh 一类能过 0.7）。`duration_s` 来自检索结果（否则为 1.0）。请用具体名称描述音效（`glass shatter`，而非 `dramatic sound`）；模糊查询会得到较差匹配。

## 内置库（无凭证）

`assets/sfx/` 中 21 个 curated 文件，由 `manifest.json` 索引——每个键对应 `{ file, duration, description }`（例如 `whoosh`、`pop`、`click`、`chime`、`riser`、`impact-bass-1`、`glitch-1`、`typing` 等）。cue 名称可通过 **manifest 键、文件 basename 或 slug** 解析，因此 `whoosh`、`whoosh.mp3` 或 `"ui click"`（→ slug）均可匹配。匹配文件复制到项目的 `assets/sfx/`；`duration_s` 来自 manifest，因此**离线**即可知时长——例如 `riser` 为 10.03s，应在 `climax − 10.03s` 触发。manifest 的 `description` 字段含各音效的放置提示；完整集合与用法见 `assets/sfx/manifest.json`。

## 规则

- **音量约 0.35。** SFX 须位于旁白与 BGM 之下，不可与之争抢。
- **无匹配 → 跳过，不失败。** 缺失音效记录异常并继续；绝不应成为渲染阻塞项。
- **检索（有凭证）或内置库（离线）——从不生成。** 按文本搜索 HeyGen，或按名称匹配 21 文件 manifest。
- **每个 distinct 名称一份资源。** 跨行复用会去重为单次下载/复制、多条 cue。
- **开关为全局，非按 cue。** 有凭证时，检索可覆盖长尾（不在 21 条内的音效）；无凭证时，仅 21 个内置名称可解析。
