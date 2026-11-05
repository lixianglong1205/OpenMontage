# 背景音乐（BGM）

每个合成项目使用一条音乐 bed，由共享音频引擎（`scripts/audio.mjs` → `scripts/lib/bgm.mjs`）产出。引擎通过一个开关在两条路径间选择——是否存在 HeyGen 凭证：

- **HeyGen 检索 — 有凭证时的默认方式。** 按情绪搜索 HeyGen 音乐目录，下载排名第一的曲目。不生成；与 TTS 共用同一套 `~/.heygen` / `$HEYGEN_API_KEY` 凭证。
- **本地生成（Lyria → MusicGen）— 无凭证时的回退（或显式要求时）。** 根据情绪提示生成 WAV。**没有 `npx hyperframes bgm` 命令**；引擎会直接 spawn `scripts/lyria-recipe.py` 或内联 MusicGen 脚本。

> **请先完成 Preflight — 无凭证并不等于可以静默走本地生成。** 在生成之前，完成登录 **Preflight**（见 `../SKILL.md` → Preflight）：运行 `npx hyperframes auth status`，建议用户登录，并 **等待用户选择**（登录以使用 HeyGen 音乐库，或离线继续本地生成）。这既适用于一次性的「生成 BGM」请求，也适用于完整工作流内部。

## 从请求驱动

`audio_request.json` → `bgm: { mode?, query?, prompt? }`：

- **`mode`** — `retrieve | generate | none`。省略则为 **auto**（有凭证则 retrieve，否则 generate）。**显式** `retrieve` 为严格模式：无凭证 ⇒ 跳过，绝不会 detached 生成（因此没有 `wait-bgm` 步骤的调用方，例如 product-launch，不会得到它不会去等待的 pending 任务）。
- **`query`** — 情绪描述，用于检索并作为生成提示的回退种子（例如分镜的 `music:` 字段，回退链为 `message` → `arc` → `"calm cinematic underscore"`）。
- **`prompt`** — 用于生成的完整显式提示；省略时由引擎推断（见「情绪推断」）。可选的 `blob` / `archetype` / `arc` 会参与该推断。

## HeyGen 检索（默认）

`searchSounds(query, "music", { limit: 5 })` → `GET /audio/sounds?query=<mood>&type=music&limit=5`。取排名第一的结果（按 `score` 排序），从其 presigned `audio_url` 下载 → `assets/bgm/track.mp3`。同步完成。无匹配 → 跳过（BGM 为可选；绝不为 BGM 导致渲染失败）。写入 `audio_meta.json` 的 cue：

```jsonc
{
  "path": "assets/bgm/track.mp3",
  "volume": 0.8,
  "mode": "retrieve",
  "query": "calm cinematic underscore",
  "duration_s": 42.0,
}
```

`volume` 在有旁白时为 0.8，无声片（无语音）时为 0.9。`bgm_pending` 为 `false` — 引擎返回时文件已在磁盘上。

## 本地生成（回退）— Lyria → MusicGen

以 **detached** 方式 spawn，以免阻塞语音工作；完成前会设置 `audio_meta.bgm_pending: true` 以及 `bgm_pid` / `bgm_log`。**在组装前运行 `scripts/wait-bgm.mjs`** — 它会轮询输出文件 / 进程 / 日志，检测崩溃，并写入 `bgm_status.json`（`status: ready | failed | timeout | disabled`）。失败或缺失的曲目会被直接省略；从不会阻塞语音/SFX。

| 顺序 | 提供方                               | 环境 / 依赖                                                                           | 速度                                    | 质量                         |
| ---- | ------------------------------------ | ------------------------------------------------------------------------------------- | --------------------------------------- | ---------------------------- |
| 1    | Google Lyria RealTime                | `$GEMINI_API_KEY` 或 `$GOOGLE_API_KEY` + `google-genai`（按需自动安装）               | 实时流（≈ 请求时长）                    | 生产级                       |
| 2    | MusicGen（`facebook/musicgen-small`） | Python `transformers + torch + soundfile + numpy`（首次约 300 MB；自动安装）         | CPU 上较慢；Apple MPS / CUDA 上较快     | 尚可；仅通过 prompt 控制     |

输出 → `assets/bgm/track.wav`，目标时长 = 语音总时长。MusicGen 生成 **一段** 种子片段（≤28–30s，低于解码器 positional 上限），再 crossfade 循环至目标长度（若更短则裁剪），避免分段接缝。后端按实际 **能运行** 的选择：仅当 `import google.genai` 成功时用 Lyria，否则 MusicGen；若两者都无法运行，则跳过 BGM（语音 + SFX 仍会渲染）。

## 情绪推断（生成用 prompt）

`scripts/lib/bgm.mjs` 中的 `inferBgmPrompt()`：显式 `prompt` 优先；否则为行业关键词 **base** → 叙事 **archetype** 形态 → 情感 **arc** 决胜。

| 在 `blob` / `query` 中的匹配                             | 基础 prompt                                                                 | BPM |
| -------------------------------------------------------- | --------------------------------------------------------------------------- | --- |
| `crypto / nft / web3 / defi / token / blockchain`        | atmospheric electronic, deep bass, futuristic synths, restrained percussion | 100 |
| `finance / fintech / bank / payment / invest / wealth`   | calm cinematic, soft strings, subtle piano, restrained percussion           | 92  |
| `creative / agency / design / studio / art / brand`        | playful electronic, warm pads, light percussion                             | 115 |
| _（默认：SaaS / tech / platform）_                        | uplifting corporate tech, bright modern piano with synth pads               | 108 |

随后 archetype 重塑弧线 — PAS → "MINOR to MAJOR" 递进；BAB / future-pacing →  aspirational rising；feature-cascade → +10 BPM 驱动感；demo-loop → −8 BPM 极简。情感 arc 打破剩余平局（tension→relief、excitement、trust/reassurance）。

## Lyria 参数（直接使用 recipe 时）

引擎将 BPM / scale **烘焙进 prompt 文本**（通过上述推断），向 recipe 仅传递 `--output` / `--duration` / `--prompt`。若直接调用 `scripts/lyria-recipe.py`，还可设置：`--bpm`（90–110 平静，110–130  energetic）、`--brightness`（0–1，≥0.7 偏宣传感）、`--density`（0–1，越高越饱满）、`--scale`（`MAJOR` / `MINOR` / `PENTATONIC` / …）、`--negative-prompt`（要排除的风格）。MusicGen 忽略以上全部 — 把情绪写在 prompt 里即可。

## 失败模式

| 失败                                              | 行为                                                                                     |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 无音乐匹配（retrieve）                            | `bgm: null`，记录异常。渲染继续，无 BGM。                                                |
| 显式 `retrieve`，无凭证                           | 跳过（无静默 generate 回退）。需 `mode: generate` 或省略 `mode` 以使用 auto。              |
| Lyria 与 MusicGen 均无法运行（generate）          | 禁用 `bgm` 并给出 `pip install …` 提示。语音 + SFX 仍会渲染。                            |
| 组装时 generate 仍在渲染                            | `bgm_pending: true`；先由 `wait-bgm.mjs` 等待/检查并写入 `bgm_status.json`。             |
| Generate 崩溃                                     | `wait-bgm.mjs` → `bgm_status.json { status: "failed" }`；省略 `<audio>` 轨道。          |

BGM 失败从不会阻塞渲染。
