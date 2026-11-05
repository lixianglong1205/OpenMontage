---
name: hyperframes-media
description: HyperFrames 合成所需的音频与媒体资源，由统一音频引擎（`scripts/audio.mjs`）产出 — 多供应商 TTS（HeyGen / ElevenLabs / Kokoro 本地）、背景音乐与音效（默认通过 HeyGen 音频库检索，无凭证时回退为本地 Lyria / MusicGen BGM 生成及内置 SFX 库）、Whisper 转写、背景移除与字幕创作。适用于旁白 / TTS、BGM、SFX / 音效、转写、字幕 / 歌词 / 卡拉 OK / 逐词样式、音色与供应商选择及音乐情绪提示。
---

# HyperFrames Media

为合成创建所需的音频与媒体资源 — 旁白（TTS）、背景音乐与音效、转写、字幕、背景移除 — 随后在 HTML 中消费并动画化这些数据。将资源放入合成时，参见 `hyperframes-core`。

## 音频引擎 — TTS · BGM · SFX 单一来源

工作流**不要**自行拼装音频或内嵌副本。只有一个引擎 — **`scripts/audio.mjs`** — 接收中性的 `audio_request.json`，并写入 `audio_meta.json`（以及 `assets/voice|bgm|sfx` 下的资源）：

```bash
# <MEDIA_DIR> = 本技能目录
node <MEDIA_DIR>/scripts/audio.mjs --request ./audio_request.json --hyperframes . --out ./audio_meta.json
```

三项能力在**同一开关**上降级 — 是否存在 HeyGen 凭证（从 `$HEYGEN_API_KEY` / `$HYPERFRAMES_API_KEY` / `~/.heygen` 解析，**而非** CLI）：

| 能力 | 存在 HeyGen 凭证                          | 不存在                                               |
| ---------- | -------------------------------------------------- | ---------------------------------------------------- |
| TTS        | HeyGen Starfish REST（原生词级时间戳）      | → ElevenLabs → Kokoro（链式 `transcribe` 获取词） |
| BGM        | HeyGen 音乐**检索**                         | Lyria → MusicGen 本地**生成**（分离进程）     |
| SFX        | HeyGen 音效**检索**（min_score 0.4） | 内置 21 文件库（`assets/sfx/`）              |

- **请求**（`audio_request.json`）：`{ provider?, lang?, speed?, lines: [{ id, text, sfx?: [names] }], bgm: { mode?, query?, prompt? } }`。`id` 将每行与调用方模型关联（帧号、场景 id 等）。`bgm.mode` = `retrieve | generate | none`；省略则自动（有凭证时 retrieve，否则 generate）。**显式** `retrieve` 为严格模式 — 会跳过而非启动分离的 generate（适用于没有 `wait-bgm` 步骤的调用方）。
- **输出**（`audio_meta.json`，按 id 索引）：`{ tts_provider, voice_id, bgm, bgm_pending, …, voices: [{ id, path, duration_s, words }], sfx: [{ id, name, file, source, offset_s, duration_s, volume }], total_duration_s }`。
- `--only tts,bgm,sfx` 只运行子集并**合并**到已有 `--out`（例如先 TTS+BGM，待提示就绪后再 SFX）。
- BGM generate 以**分离进程**启动（`bgm_pending: true`）— 组装前运行 `scripts/wait-bgm.mjs`。
- `scripts/heygen-tts.mjs` 是同一套代码的单次 CLI（一段文本 → wav + words），仅需 HeyGen TTS 而无请求文件时使用。

完整参数列表与 `audio_meta.json` 模式见 `scripts/audio.mjs` 文件头。下文参考文档说明各能力背后的供应商细节与边界情况。

## 预检 — 生成任何音频前先展示登录状态

**在生成旁白或 BGM 之前务必运行 — 无论是完整工作流还是一次性「给我生成 BGM/旁白」请求。** 没有 HeyGen 凭证**不是**静默回退本地引擎的理由：先建议登录，由用户决定。运行共享预检并**原样转发其输出** — 不要自行编造「缺少密钥」提示，也不要提议把密钥写入各仓库的 `.env`：

```bash
npx hyperframes auth status
```

- **已登录** → 会打印账户信息；继续执行。
- **未登录**（此处 `exit 1` 是预期 — 「未登录」是正常状态，不是失败）→ 会打印以注册为先的指引。建议登录：`npx hyperframes auth login` 为浏览器 OAuth — **登录并创建账户**（始终可通过本仓库 CLI 使用）。若使用已有 HeyGen API 密钥（来自 app.heygen.com/settings/api），运行 `npx hyperframes auth login --api-key` — 保存到共享 `~/.heygen`（无需各仓库 `.env`）。输出还会列出旁白/BGM 将回退到的本地引擎，以及依赖缺失时的 `pip` 提示。**原样转发该输出 — 不要改写成自己的措辞。** 然后**停止并等待**用户选择 — 登录，或说「go」/「local」以离线继续 — **再生成任何内容。** 这是真正的决策点，不是顺带一提：不要把它塞进另一个问题里，也不要自行越过。（例外：自主 / 非交互模式下，记录状态并离线继续。）
- `npx hyperframes auth status --json` 返回 `{ configured, recommended_action, offline_engines }` 供确定性分支。
- **若 CLI 无法运行**（不在 PATH 且 `npx` 拉取失败）→ 仍**建议登录**（`npx hyperframes auth login`）并**停止等待用户选择** — 不要把「无凭证」当作静默允许本地生成。

凭证解析、完整密钥优先级与本地依赖列表见 `references/requirements.md`。

## 供应商链（引擎背后的细节）

**TTS** — 首个可用供应商胜出（引擎，或 `npx hyperframes tts "..."`）：

| 顺序 | 供应商                      | 检测条件                                | 词级时间戳                                                  |
| ----- | ----------------------------- | -------------------------------------------- | ---------------------------------------------------------------- |
| 1     | HeyGen (Starfish)             | `$HEYGEN_API_KEY` / `hyperframes auth login` | **有，原生** — 传入 `--words narration.words.json` 以捕获 |
| 2     | ElevenLabs                    | 已设置 `$ELEVENLABS_API_KEY`                    | 无 — 之后链式 `transcribe`                                    |
| 3     | Kokoro-82M（本地，54 音色） | 始终可用（无需密钥）                     | 无 — 之后链式 `transcribe`                                    |

> 已发布的 `hyperframes tts` CLI 常为仅本地构建（其 `--help` 写「Kokoro-82M」，无 `--provider`/`--words`），即使设置了 `$HEYGEN_API_KEY` 也会静默回退 Kokoro。因此引擎的 HeyGen 路径是自包含的 `scripts/heygen-tts.mjs`（REST），**不是** CLI；CLI 仅用于 Kokoro 路径。见 `references/tts.md`。

**BGM 与 SFX** — 默认从 HeyGen 音频库**检索**（`/v3/audio/sounds`），与 HeyGen TTS 同一凭证，无凭证时回退见上表开关：

| 资源 | HeyGen `type`                   | 输出位置                                                   | 回退（无凭证）                                   |
| ----- | ------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| BGM   | `music`                         | `assets/bgm/track.mp3`（retrieve）· `track.wav`（generate） | Lyria / MusicGen 生成                                |
| SFX   | `sound_effects`（min_score 0.4） | `assets/sfx/<slug>.mp3`                                    | 内置 21 文件库（`assets/sfx/*` + `manifest.json`） |

见 `references/bgm.md` 与 `references/sfx.md`。

## 路由

| 任务                                                                | 阅读                                         |
| ------------------------------------------------------------------- | -------------------------------------------- |
| 音频引擎 — request/meta 模式、`--only`、开关        | `scripts/audio.mjs`（头注释）         |
| `npx hyperframes tts` / `heygen-tts.mjs` — 供应商、音色、词 | `references/tts.md`                          |
| BGM — HeyGen 检索 + 本地 Lyria / MusicGen 生成          | `references/bgm.md`                          |
| SFX — HeyGen 检索（min_score 0.4）+ 内置本地库      | `references/sfx.md`                          |
| `npx hyperframes transcribe` — Whisper、模型规则、输出形状   | `references/transcribe.md`                   |
| `npx hyperframes remove-background` — 透明抠图           | `references/remove-background.md`            |
| TTS → 转写 → 字幕（无录制旁白）              | `references/tts-to-captions.md`              |
| 字幕创作 — 样式检测、布局、分词、退出    | `references/captions/authoring.md`           |
| 转写处理 — 输入格式、质量门槛、清理、API   | `references/captions/transcript-handling.md` |
| 字幕动效 — 卡拉 OK、标记效果、音频响应            | `references/captions/motion.md`              |
| 模型缓存、系统依赖、故障排查                  | `references/requirements.md`                 |

## 不可协商的规则

- **一个引擎，禁止内嵌副本。** 通过 `scripts/audio.mjs`（或单次 HeyGen TTS 用 `heygen-tts.mjs`）产出音频。不要在工作流内重新实现 TTS/BGM/SFX — 编写 `audio_request.json` 适配器并调用引擎。
- **「HeyGen 可用」= 可解析的凭证，不是 CLI。** 整个开关键于 `heygenCredential()`；已发布的 `hyperframes tts` 可能仅 Kokoro，且根本没有 `hyperframes bgm` / `hyperframes sfx` 命令。
- **Voice ID 按供应商区分。** `am_michael` 仅 Kokoro；HeyGen UUID 不能用于 Kokoro。若传入 `--voice`，同时固定 `--provider`，避免用户环境变化时供应商静默漂移。
- **向 `transcribe` 始终传入 `--model`。** CLI 默认 `small.en` 会静默将非英语音频翻译。见 `references/transcribe.md` →「Language Rule」。
- **HeyGen 返回词级时间戳；ElevenLabs / Kokoro 不返回。** 引擎对后两者自动链式 `transcribe`；单独使用时，向 HeyGen 传 `--words` 或对音频文件运行 `transcribe`。
- **字幕消费扁平词数组格式**，含 `{ id, text, start, end }`。见 `references/transcribe.md` →「Output Shape」。
- **`remove-background --background-output` 是挖洞抠图，不是 inpaint。** 若要「场景中无人」，需其他工具。见 `references/remove-background.md` →「When NOT the right tool」。
- **BGM/SFX 默认 HeyGen 检索；无凭证时 BGM 为生成、SFX 为内置库。** `/audio/sounds` 按文本查询排序 — 音效命名要具体（`glass shatter`，而非 `dramatic sound`）；无匹配**跳过**，从不阻塞渲染。SFX 音量约 0.35，位于旁白 + BGM 之下。见 `references/sfx.md` / `references/bgm.md`。
- **将工作流中的字幕 HTML 视为生成物。** 对预设驱动视频，可复用皮肤源在 `.hyperframes/caption-skin.html`，工作流脚本写入 `compositions/captions.html`；不要通过编辑生成的 `compositions/captions.html` 来修皮肤。通过工作流的 `captions.mjs` 重建，或在存在时使用该工作流提供的显式覆盖机制。
