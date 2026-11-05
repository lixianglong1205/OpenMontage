# 步骤 4：旁白、时间轴与字幕

## 若步骤 2 标明「无需旁白」

跳过下方 TTS 相关章节。分镜表已按节奏与韵律规划各节拍时长——这些将直接在步骤 5 中作为 `data-start` 与 `data-duration` 值使用。

**背景音乐：** 进入步骤 5 前先询问用户：

> 「你有用于本片的音乐轨吗？若没有，我可以建议去哪找：
>
> - **Artlist.io** 或 **Musicbed** — 可商用的授权音乐
> - **Uppbeat.io** 或 **Pixabay Music** — 需署名的免费曲目
> - **Freesound.org** — 免费采样与循环
>
> 或分享一条参考曲（「想要类似这种的」），我可以帮你找相近的。」

若用户提供曲目：在分镜表中记下文件路径与 BPM，供步骤 5 接入 `index.html`。若完全不用音乐，则视频仅使用音效——确认这是有意为之。

进入步骤 5。

---

## 在生成完整旁白前先做测试片段——先校准时间

**现在**用脚本开头两句生成一段 2 句测试音频，并测量实际时长。Kokoro 会把脚本压缩约 40%（计划 35 秒 → 实际约 19 秒），HeyGen 也往往比预期更快。若发现音频比预期短 40%，需在投入完整旁白生成之前，先修订分镜表的节拍时长。

**在确定节拍数量与时长之前，务必完成以下操作：**

```bash
# Quick Kokoro test (2 sentences):
npx hyperframes tts "First sentence. Second sentence." --voice af_nova --output /tmp/test-tts.wav
# Measure: seconds ÷ words × total script words = estimated full audio length
```

若估算时长与计划时长相差在 ±15% 以内，可继续。若偏差超过 15%，先重新校准脚本长度：

- **音频过短**（比计划时长短超过 15%）→ 增加策略性停顿。在 `narration.txt` 中，段落之间插入空行（约 0.6 秒/处）或句间使用 `...`（约 0.4 秒/处）。尽量让停顿落在分镜节拍边界上，使静音显得有意为之，而非尴尬空白。
- **音频过长**（比计划时长长超过 15%）→ 在分镜中找出「词/秒」密度最高的节拍，从该节拍的台词中删去一句支撑句——保留 lead 句（点明该节拍主旨的那句）。在提交完整生成前，用另一段测试音频重新测量。
- **音频总时长符合计划但节拍边界漂移** → 调整分镜时长以匹配实际旁白，而不是反过来改音频。旁白生成完成后，音频即为基准（ground truth）。

脚本公式假设恒定的词/秒，但标点、戏剧性停顿与静音提示都会拉长真实音频。始终相信实测测试片段，而非仅依赖公式。

## 背景音乐

**始终询问是否需要背景音乐**——即便已有旁白：

> 「是否要在旁白下铺背景音乐？（Artlist.io、Musicbed 为授权音乐；Uppbeat/Pixabay 为免费；或分享参考曲）。即便很轻微的环境铺底，也能让句间停顿显得有意而非空洞。」

若需要音乐，在分镜中记下曲目，供步骤 5 接入 `index.html`。

## TTS 提供商

询问用户希望使用哪家语音提供商：

> **你希望用哪家提供商生成旁白？**
>
> 1. **HeyGen TTS** — 音质较好，且自动返回词级时间戳（省掉单独转写步骤）。需要 HeyGen API key。
> 2. **ElevenLabs** — 音色库大，输出非常自然。需要 ElevenLabs API key。不返回词级时间戳——需单独转写。
> 3. **Kokoro**（免费）——本地运行，无需 API key。质量尚可但比前两者更「机器感」。适合草稿或预算有限的项目。

若用户选择 ElevenLabs 或 HeyGen 且尚未配置 key，协助其：

- **ElevenLabs：**「在项目根目录的 `.env` 中添加 `ELEVENLABS_API_KEY=your-key`，或直接粘贴 key，我来帮你配置。」
- **HeyGen：**「在 `.env` 中添加 `HEYGEN_API_KEY=your-key`，或直接粘贴 key。」

用户若在聊天中直接粘贴 key，不要评判或批评——直接使用并继续。

## 试听音色

选定提供商后，用 `SCRIPT.md` 的第一句至少试听 2 个音色。

**ElevenLabs：**

- 若可用 ElevenLabs MCP：用 `mcp__elevenlabs__search_voices` 浏览，用 `mcp__elevenlabs__text_to_speech` 生成。
- 若无 MCP：直接调用 REST API：

  ```bash
  # List voices
  curl -s "https://api.elevenlabs.io/v1/voices" \
    -H "xi-api-key: $ELEVENLABS_API_KEY" | jq '.voices[:5] | .[].name'

  # Generate speech (replace VOICE_ID with chosen voice)
  curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID" \
    -H "xi-api-key: $ELEVENLABS_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"text":"First sentence of your script","model_id":"eleven_multilingual_v2"}' \
    --output narration.mp3
  ```

- 不返回词级时间戳——生成后需单独转写。

**HeyGen TTS：**

- 若可用 HeyGen MCP：直接使用 TTS 工具。
- 若无 MCP：使用 v3 API（当前版本；v1/v2 已弃用，支持至 2026 年 10 月）。**鉴权取决于凭证类型：** 下方 `x-api-key` 头**仅适用于账户 API key**（`HEYGEN_API_KEY`）。若通过 **OAuth** 登录（如 claude.ai / HeyGen MCP 登录），`x-api-key` 会返回 401——应改用 `Authorization: Bearer $HEYGEN_OAUTH_TOKEN`，或直接使用上文 MCP TTS 工具。

  ```bash
  # List voices — response shape: { "data": [...], "has_more": bool }
  # data is a direct list (NOT data.voices — that was v2)
  curl -s "https://api.heygen.com/v3/voices?engine=starfish&type=public&limit=20" \
    -H "x-api-key: $HEYGEN_API_KEY" | python3 -c \
    "import json,sys; v=json.load(sys.stdin)['data']; [print(x['voice_id'], x['name'], x['language']) for x in v[:10]]"

  # Generate audio — response: { "data": { "audio_url": ..., "word_timestamps": [...] } }
  curl -s -X POST "https://api.heygen.com/v3/voices/speech" \
    -H "x-api-key: $HEYGEN_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"text":"Your script here","voice_id":"VOICE_ID","speed":1.0}' \
    | python3 -c "
  import json,sys
  r=json.load(sys.stdin)
  d=r['data']
  print(d['audio_url'])
  open('transcript_raw.json','w').write(json.dumps(d.get('word_timestamps',[]),indent=2))
  "

  # Then download the audio
  curl -sL "AUDIO_URL_FROM_ABOVE" --output narration.mp3
  ```

- 响应中直接包含词级时间戳——无需单独转写步骤。

**Kokoro（免费、本地）：**

```bash
npx hyperframes tts SCRIPT.md --voice af_nova --output narration.wav
```

无需 API key，无需 MCP。本地运行。使用 `--list` 查看全部 54 个可用音色。

选择听起来最自然、像对话的音色。注意节奏——句间是否有「呼吸」？像真人还是机器人？

## 脚本长度检查

生成前确认脚本与视频匹配。字数完全取决于创意方向。分镜的节奏与风格决定视频需要多少旁白。

关键检查：是否存在「什么都没发生」的段落——既无旁白，又无足够强的画面动效？那是会流失观众的空档。每一秒都需要要么有旁白，要么有强视觉动效支撑。

## 生成完整旁白

在项目目录中将完整脚本生成为 `narration.wav`（或 `.mp3`）。

**若任意命令挂起超过 60 秒——不要干等。** 用户正看着屏幕等你无事可做。升级顺序：

1. **重试**——结束进程，再跑同一命令（瞬时失败很常见）
2. **换参数**——更小模型（`--model tiny.en`）、不同音色、先用更短测试句
3. **换工具做同一任务**——若 `hyperframes transcribe` 挂起，直接对音频跑 `whisper-cli`
4. **换提供商**——ElevenLabs 不可用则试 HeyGen 或 Kokoro；Kokoro 挂起则试 ElevenLabs。

不要空等 10 分钟指望卡住的进程会自己结束。

**Kokoro 发音问题：** Kokoro 常误读产品名与技术术语。生成前务必做替换。已知问题与修复：

- `API` → `A P I`（逐字母拼读）
- `UI` → `U I`，`SaaS` → `sass`，`DevOps` → `dev ops`
- 拼写特殊的产品名：先用第一句测试并听。常见失败：`Vercel` → 读成 "versatile"，`WorkOS` → "work O S"，`One API` → "Wanna PI"
- 若某名称读音不对：在 `narration.txt` 中按音标写法（如 `Vercel` → `Ver-sell`，`Supabase` → `Soopa-base`）
- 完整音频生成前，务必用前 2 句生成短测试片段
- **不支持 SSML 标签**——Kokoro 会当字面文本朗读。`<break time="1s"/>` 会被读成 “break time equals one slash.” 在 `narration.txt` 中用空行或 `...` 表示停顿

ElevenLabs 与 HeyGen TTS 通常无需替换——它们能正确处理产品名。

**同时保存实际朗读文本**——含已应用的发音替换（如 `API` → `A P I`，`$2T` → `two trillion` 等）——为同目录下的 `narration.txt`。这是传给 TTS 的字符串，与面向人类的创意文档 `SCRIPT.md` 不同。保留 `narration.txt` 便于日后换音色重生成而无需重新推导替换。文件名必须为 `narration.txt`。

## 转写以获取词级时间戳

**若使用 HeyGen v3 TTS：** 生成调用已返回词级时间戳。保存前先规范化格式——HeyGen v3 使用 `word` 字段，而流水线期望 `text`：

```python
import json
raw = json.load(open('transcript_raw.json'))
normalized = [{"text": w["word"], "start": w["start"], "end": w["end"]} for w in raw]
json.dump(normalized, open('transcript.json', 'w'), indent=2)
```

无需单独转写步骤。

**若使用 ElevenLabs 或 Kokoro：**

```bash
npx hyperframes transcribe narration.wav
```

生成 `transcript.json`，每个词为 `[{ text, start, end }]`。这些时间戳是所有节拍时长的唯一依据（source of truth）。

## 将时间戳映射到节拍

逐节拍查阅 `STORYBOARD.md`。对每个节拍：

1. 在 `transcript.json` 中找到该节拍 VO 提示的第一个词
2. 找到该节拍 VO 提示的最后一个词
3. 设 `beat.start = firstWord.start`，`beat.end = lastWord.end`
4. 在末尾加 0.3–0.5 秒 padding，给画面留呼吸空间

用真实时长更新 `STORYBOARD.md`。将估算时间（如「0:00–0:05」）替换为尽可能精确的实测时间戳（如「0.00–3.21s」）。

节拍边界落在词起始点上——与旁白硬切对齐。

## 时间轴对账——进入步骤 5 前必做

映射全部节拍后，比较真实音频总时长与分镜计划时长：

```
real_total = last_word.end + cta_hold (typically 2–3s)
planned_total = sum of all beat planned durations
delta = |real_total - planned_total|
```

**若 delta > 计划总时长的 15%——未解决前不要进入步骤 5。** 常见原因与修复：

- **音频短于计划（Kokoro 最常见）：** Kokoro 生成压缩语速、停顿极少。按比例缩短所有非 CTA 节拍时长以匹配真实音频。例：计划 30s，音频 19s——各节拍时长（不含 CTA hold）乘以 19/30。更新 `STORYBOARD.md`。
- **音频远长于计划（>30%）：** 脚本相对目标时长过长。精简脚本（去掉某一节拍的 VO），重生成音频并重新转写。
- **CTA 节拍时间：** CTA 节拍应在最后一个词说完之后 hold 2–3 秒——不要用延长来填空白。`cta_start = last_word.end + 0.3s`，`cta_duration = 2.5s`。硬上限。CTA hold 之后长时间死寂会流失观众。

**若相对分镜计划大幅调整时长，务必告知用户。** 他们批准过特定节拍结构——若有变更，他们需要知道。

## 字幕

旁白生成并转写完成后，询问用户：

> **是否要在视频上加字幕？**
>
> - **是** — 与旁白同步的逐词字幕。适合社交媒体（多数观众静音观看）与无障碍。
> - **否** — 仅旁白音频，无文字叠加。

若选是，字幕在步骤 5 中作为独立 composition（`compositions/captions.html`）构建。`transcript.json` 驱动 timing——每个词在说出时出现/高亮。样式选项（scale-pop、typewriter、fade+slide 等）与定位规则见 [字幕参考](../../hyperframes/references/captions.md)。

## 为步骤 5 保存 timing 数据

记录最终节拍 timing（start、duration），供步骤 5（Build）在构建 `index.html` 时使用。分镜表现已有真实时间戳——在步骤 5 组装根 composition 时，这些将成为各 scene slot 上的 `data-start` 与 `data-duration` 值。
