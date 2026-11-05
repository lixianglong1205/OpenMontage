# 要求与缓存

## 凭证与密钥优先级

运行 `npx hyperframes auth status` 可查看已配置项以及工作流将使用的引擎（参见技能中的 **Preflight** 章节）。密钥按以下顺序解析——**先匹配者优先**：

| 提供商                             | 解析顺序（首个非空值生效）                                                                                                                                    | 使用时的本地依赖                             |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **HeyGen**（TTS + BGM/SFX 检索） | `$HEYGEN_API_KEY` → `$HYPERFRAMES_API_KEY` → `~/.heygen/credentials`（与 heygen-cli 共用；`$HEYGEN_CONFIG_DIR` 可覆盖目录；由 `hyperframes auth login` 写入） | 无（REST）                                      |
| **ElevenLabs**（TTS 回退）        | `$ELEVENLABS_API_KEY`                                                                                                                                                      | `pip install elevenlabs`                         |
| **Lyria**（BGM 回退）             | `$GEMINI_API_KEY` → `$GOOGLE_API_KEY`                                                                                                                                      | `pip install google-genai`                       |
| **Kokoro**（TTS，无需密钥）             | 始终可用 — 最终语音回退                                                                                                                                              | `pip install kokoro-onnx soundfile`              |
| **MusicGen**（BGM，无需密钥）           | 始终可用 — 最终音乐回退                                                                                                                                              | `pip install transformers torch soundfile numpy` |

`hyperframes auth login`（浏览器 OAuth）是推荐的设置方式：一次登录，所有项目通用，无需每个仓库单独配置 `.env`。OAuth 登录使用 `Authorization: Bearer` 发送；API 密钥使用 `X-Api-Key`。若无 HeyGen 凭证，语音/BGM 将完全在本地运行（Kokoro / MusicGen）——`hyperframes auth status` 与 `hyperframes doctor` 都会报告这些本地依赖是否已安装。

## 模型缓存与系统依赖

每条命令在首次运行时会下载各自模型，并缓存在 `~/.cache/hyperframes/` 下：

- **TTS (HeyGen)** — 无本地依赖；需要 HeyGen 凭证 + PATH 上的 `ffmpeg`（将 mp3 响应转码为 `.wav`）。凭证解析与 CLI 相同：`$HEYGEN_API_KEY` → `$HYPERFRAMES_API_KEY` → `~/.heygen/credentials`（与 heygen-cli 共用；运行 `npx hyperframes auth login`）。OAuth 登录使用 `Authorization: Bearer` 发送；API 密钥使用 `X-Api-Key`。
- **TTS (ElevenLabs)** — 与 HeyGen 相同：API 密钥 + `ffmpeg`。
- **TTS (Kokoro)** — Kokoro-82M（约 311 MB）+ 语音包（约 27 MB）位于 `tts/`。需要 Python 3.8+ 及 `kokoro-onnx`、`soundfile`（`pip install kokoro-onnx soundfile`）。非英文文本还需系统级安装 `espeak-ng`。
- **BGM (Lyria)** — 需要 `$GEMINI_API_KEY` 或 `$GOOGLE_API_KEY` + `pip install google-genai`。无本地模型缓存。
- **BGM (MusicGen)** — `pip install transformers torch soundfile`。首次运行时将 `facebook/musicgen-small`（约 300 MB）缓存在 `~/.cache/huggingface/`。
- **Transcribe** — 按所选 Whisper 模型大小（75 MB – 3.1 GB）缓存在 `whisper/`。捆绑 `whisper.cpp`。
- **Remove-background** — `u2net_human_seg`（约 168 MB ONNX）位于 `background-removal/models/`。推理峰值 RAM 约 1.5 GB。

若命令因缺少依赖而失败，请运行 `npx hyperframes doctor`。
