# 文本转语音（Text To Speech）

`npx hyperframes tts` 会根据环境变量自动检测 provider；也可通过 `--provider` 显式指定。

> **请先完成 Preflight——没有凭证并不代表可以静默使用本地语音。** 在生成旁白之前，请完成登录 **Preflight**（见 `../SKILL.md` → Preflight）：运行 `npx hyperframes auth status`，建议用户登录，并 **等待用户选择**（登录以使用 HeyGen 语音，或离线继续使用本地 Kokoro）。无论是单次「生成旁白」请求，还是完整工作流中的步骤，均适用。

## Provider 链

| 顺序 | Provider          | 环境变量触发                                 | Voice ID                                   | 词级时间戳                           | 音频格式         |
| ----- | ----------------- | ------------------------------------------- | ------------------------------------------- | ----------------------------------------- | -------------------- |
| 1     | HeyGen (Starfish) | `$HEYGEN_API_KEY` / `~/.heygen/credentials` | 来自 `GET /v3/voices?engine=starfish` 的 UUID | **是**（响应中的 `word_timestamps[]`） | mp3 → 经 ffmpeg 转为 wav |
| 2     | ElevenLabs        | `$ELEVENLABS_API_KEY`                       | 来自 elevenlabs.io 控制台的 UUID          | 否                                        | mp3 → 经 ffmpeg 转为 wav |
| 3     | Kokoro-82M        | 始终可用（本地回退）                     | `am_michael`、`af_heart`、…（54 种语音）     | 否                                        | 直接输出 wav           |

```bash
# Auto-detect (HeyGen if key set, else ElevenLabs, else Kokoro)
npx hyperframes tts "Welcome to HyperFrames" -o narration.wav

# Pin the provider explicitly
npx hyperframes tts "Hello" --provider kokoro
npx hyperframes tts "Hello" --provider heygen --voice <heygen-uuid>
npx hyperframes tts "Hello" --provider elevenlabs --voice 21m00Tcm4TlvDq8ikWAM

# HeyGen path: capture word timestamps in one call (skips a Whisper pass)
npx hyperframes tts "Hi there" --words narration.words.json
```

## 自包含 HeyGen（无需 CLI）— `scripts/heygen-tts.mjs`

已发布的 `hyperframes tts` CLI 仅使用 Kokoro 在本地合成。若你需要 **HeyGen**——最佳音质 **且** 一次调用即可获得词级时间戳——请使用技能自带的脚本，它直接调用 HeyGen v3 REST API，无需 CLI 的 provider 接入逻辑：

脚本解析 HeyGen 凭证的方式与 CLI 相同——先找到的来源优先：`$HEYGEN_API_KEY` → `$HYPERFRAMES_API_KEY` → 项目 `.env`（自动加载，向上遍历 ≤5 层目录）→ `~/.heygen/credentials`（与 heygen-cli 共享；`$HEYGEN_CONFIG_DIR` 可覆盖目录）。OAuth 登录使用 `Authorization: Bearer`；API key 使用 `X-Api-Key`。若唯一凭证是已过期的 OAuth token，会停止并提示运行 `npx hyperframes auth refresh`。

```bash
# Only needed if you haven't run `npx hyperframes auth login`:
export HEYGEN_API_KEY=...   # or put it in a project .env

# Synthesize + capture word timestamps in one call (skips a Whisper pass)
node skills/hyperframes-media/scripts/heygen-tts.mjs \
  "Welcome to HyperFrames." -o narration.wav --words narration.words.json

node skills/hyperframes-media/scripts/heygen-tts.mjs ./script.txt -o narration.wav
node skills/hyperframes-media/scripts/heygen-tts.mjs --list   # public starfish voices
```

- **Voice：** `--voice <id>` 必须是 **starfish** 的 voice_id（`--list`，或 `GET /v3/voices?engine=starfish`）。v2 目录中的 id 会被拒绝并返回 HTTP 400。省略 `--voice`（英语）时默认 **Marcia**（`05f19352e8f74b0392a8f411eba40de1`，固定默认值以保证选择可复现）。非英语且未指定 `--voice` 时，回退到目录中第一个匹配的语音。
- **Output：** `.wav` → 经 ffmpeg 转码为 44.1k 单声道；`.mp3` → 原始字节（无需 ffmpeg）。
- **Words：** `--words <path>` 写入下方扁平的 `[{id,text,start,end}]` 结构，可直接用于字幕流水线。HeyGen 的 `<start>`/`<end>` 边界标记会被过滤，id 会重新连续编号。
- **Non-English：** `--lang <code>`（非 `en`）会作为请求的 `language` 发送。

## 何时使用哪个 Provider

| 目标                                                      | 使用                                                 |
| --------------------------------------------------------- | --------------------------------------------------- |
| 最佳音质 + 一次调用获得词级时间戳          | **HeyGen**                                          |
| 即插即用云端 TTS，语音库丰富                      | **ElevenLabs**                                      |
| 离线、无需 API key、快速迭代                       | **Kokoro**                                          |
| 非英语多语言且音素化可预期 | **Kokoro**（`ef_dora`、`jf_alpha`、`zf_xiaobei` 等） |

## 表现力旁白约定

生成旁白前，先写一份精简的语音表演计划：

- `performance_intent` - 叙述者是谁、应带何种情绪
- `pacing_profile` - 沉思、对话、活泼、技术说明或自定义
- `energy_curve` - 整段朗读中能量如何变化
- `pause_policy` - 何处需要静音及原因
- 分段级提示 - `pace`、`energy`、`emphasis_words`、`pause_before_seconds`、
  `pause_after_seconds`，以及可选的 provider 就绪文本

不要依赖「听起来自然一点」这类模糊指令。把方向写进文本或 provider 设置：

- 使用短句和有目的的标点。
- 在 provider 支持 SSML 风格 break 标签时，用 `<break time="0.4s"/>` 到 `<break time="1.0s"/>` 标记重要停顿。
- 批量生成前，先对最依赖表演的分段做样本合成。
- 若样本听起来单调、赶词或忽略停顿，在生成其余内容前修订计划或 provider 设置。

## ffmpeg 要求

HeyGen 与 ElevenLabs 返回 mp3。当 `--output` 以 `.wav` 结尾时（默认，也是下游 `ffprobe` + Whisper 所期望的），CLI 会转码为 wav。若不想转码，可传 `-o file.mp3`。云端 provider 输出 `.wav` 时，若 PATH 中没有 `ffmpeg` 会失败——请安装 ffmpeg 或改用 `.mp3`。

## 语音选择（Kokoro）

默认 `af_heart`。精选推荐：

| 内容类型      | Voice                  |
| ----------------- | ---------------------- |
| 产品演示      | `af_heart`, `af_nova`  |
| 教程 / 操作指南 | `am_adam`, `bf_emma`   |
| 营销 / 宣传 | `af_sky`, `am_michael` |
| 文档     | `bf_emma`, `bm_george` |
| 休闲 / 社交   | `af_heart`, `af_sky`   |

运行 `npx hyperframes tts --list` 查看内置集合。

## 多语言（Kokoro 语音前缀 → 语言）

Kokoro voice ID 的首字母决定音素器语言；`--lang` 可覆盖自动检测。

| 前缀 | 语言             |
| ------ | -------------------- |
| `a`    | 美式英语     |
| `b`    | 英式英语      |
| `e`    | 西班牙语              |
| `f`    | 法语               |
| `h`    | 印地语                |
| `i`    | 意大利语              |
| `j`    | 日语             |
| `p`    | 巴西葡萄牙语 |
| `z`    | 普通话             |

```bash
npx hyperframes tts "La reunión empieza a las nueve" --voice ef_dora --provider kokoro
npx hyperframes tts "Today is a nice day" --voice af_heart --provider kokoro
```

有效的 `--lang` 代码（仅在需要覆盖语音自动检测语言时使用）：`en-us`、`en-gb`、`es`、`fr-fr`、`hi`、`it`、`pt-br`、`ja`、`zh`。

非英语音素化需要系统级安装 `espeak-ng`（`brew install espeak-ng` / `apt-get install espeak-ng`）。

## 语速

- `0.7-0.8` — 教程、复杂内容、无障碍
- `1.0` — 自然语速（默认）
- `1.1-1.2` — 片头、转场、轻快内容
- `1.5+` — 很少合适，需仔细试听

Kokoro 与 HeyGen 会尊重 `--speed`；ElevenLabs 忽略 `--speed`（请在其控制台调整 voice 设置）。

## 长脚本

超过几段话时，将文本写入 `.txt` 文件并传入路径。超过约 5 分钟语音的输入，可考虑拆成多段。

## HeyGen 词级时间戳结构

向 HeyGen 调用传入 `--words <path>` 时，文件以与 `transcribe` 相同的扁平结构写入——可直接用于字幕流水线：

```json
[
  { "id": "w0", "text": "Hi", "start": 0.0, "end": 0.21 },
  { "id": "w1", "text": "there", "start": 0.22, "end": 0.55 }
]
```

ElevenLabs / Kokoro 请运行 `npx hyperframes transcribe narration.wav --model small.en` 得到相同结构。
