---
name: acestep
description: 使用 ACE-Step 1.5 进行 AI 音乐生成 — 背景音乐、人声曲目、翻唱、分轨提取，适用于视频制作。在生成音乐、配乐、广告歌、处理音频分轨时使用。触发词包括背景音乐、配乐、广告歌、音乐生成、分轨提取、翻唱、风格迁移或音乐创作等任务。
---

# ACE-Step 1.5 音乐生成

通过 `tools/music_gen.py` 使用开源音乐生成（MIT 许可证）。在 RunPod serverless 上运行。
需在 `.env` 中配置 `RUNPOD_API_KEY` 与 `RUNPOD_ACESTEP_ENDPOINT_ID`（运行 `--setup` 可创建端点）。

## 快速参考

```bash
# Basic generation
python tools/music_gen.py --prompt "Upbeat tech corporate" --duration 60 --output bg.mp3

# With musical control
python tools/music_gen.py --prompt "Calm ambient piano" --duration 30 --bpm 72 --key "D Major" --output ambient.mp3

# Scene presets (video production)
python tools/music_gen.py --preset corporate-bg --duration 60 --output bg.mp3
python tools/music_gen.py --preset tension --duration 20 --output problem.mp3
python tools/music_gen.py --preset cta --brand digital-samba --duration 15 --output cta.mp3

# Vocals with lyrics
python tools/music_gen.py --prompt "Indie pop jingle" --lyrics "[verse]\nBuild it better\nShip it faster" --duration 30 --output jingle.mp3

# Cover / style transfer
python tools/music_gen.py --cover --reference theme.mp3 --prompt "Jazz piano version" --duration 60 --output jazz_cover.mp3

# Stem extraction
python tools/music_gen.py --extract vocals --input mixed.mp3 --output vocals.mp3

# List presets
python tools/music_gen.py --list-presets
```

## 创作歌曲（分步指南）

### 1. 纯器乐背景轨（最简单）
```bash
python tools/music_gen.py --prompt "Upbeat indie rock, driving drums, jangly guitar" --duration 60 --bpm 120 --key "G Major" --output track.mp3
```

### 2. 带人声与歌词的歌曲
将歌词写入临时文件或内联传入。使用结构标签控制歌曲段落。

```bash
# Write lyrics to a file first (recommended for longer songs)
cat > /tmp/lyrics.txt << 'LYRICS'
[Verse 1]
Walking through the morning light
Coffee in my hand feels right
Another day to build and dream
Nothing's ever what it seems

[Chorus - anthemic]
WE KEEP MOVING FORWARD
Through the noise and doubt
We keep moving forward
That's what it's about

[Verse 2]
Screens are glowing late at night
Shipping code until it's right
The deadline's close but so are we
Almost there, just wait and see

[Chorus - bigger]
WE KEEP MOVING FORWARD
Through the noise and doubt
We keep moving forward
That's what it's about

[Outro - fade]
(Moving forward...)
LYRICS

# Generate the song
python tools/music_gen.py \
  --prompt "Upbeat indie rock anthem, male vocal, driving drums, electric guitar, studio polish" \
  --lyrics "$(cat /tmp/lyrics.txt)" \
  --duration 60 \
  --bpm 128 \
  --key "G Major" \
  --output my_song.mp3
```

### 3. 使用预设作为视频背景
```bash
python tools/music_gen.py --preset tension --duration 20 --output problem_scene.mp3
```

### 获得良好效果的关键技巧
- **Caption（说明）= 整体风格**（流派、乐器、情绪、制作质感）
- **Lyrics（歌词）= 时间结构**（主歌/副歌走向、人声表现）
- **歌词中的大写** = 高人声强度
- **括号** = 背景和声：「We rise (together)」
- **每行保持 6–10 音节** 以形成自然节奏
- **不要在 caption 里描述旋律** — 描述*听感*与*感受*
- **使用 `--seed`** 在迭代 prompt/歌词时锁定随机性

## 场景预设

| 预设 | BPM | 调性 | 用途 |
|--------|-----|-----|----------|
| `corporate-bg` | 110 | C Major | 专业背景、演示文稿 |
| `upbeat-tech` | 128 | G Major | 产品发布、科技演示 |
| `ambient` | 72 | D Major | 概览幻灯片、反思类内容 |
| `dramatic` | 90 | D Minor | 揭晓、公告 |
| `tension` | 85 | A Minor | 问题陈述、挑战 |
| `hopeful` | 120 | C Major | 方案揭晓、解决 |
| `cta` | 135 | E Major | 行动号召、收尾能量 |
| `lofi` | 85 | F Major | 录屏、编程演示 |

## 任务类型

### text2music（默认）
根据文本 prompt 及可选歌词生成音乐。

### cover
基于参考音频进行风格迁移。用 `--cover-strength`（0.0–1.0）控制融合程度：
- **0.2** — 松散风格借鉴（创作自由度更高）
- **0.5** — 平衡的风格迁移
- **0.7** — 接近原曲结构（默认）
- **1.0** — 最大程度贴近源音频

### extract
分轨分离 — 从混音中分离单轨。
轨道：`vocals`、`drums`、`bass`、`guitar`、`piano`、`keyboard`、`strings`、`brass`、`woodwinds`、`other`

### repaint（未来）
在保留其余部分的前提下，重新生成现有音频中的指定时间段。

### lego（未来，需 base 模型）
在现有音频上下文中生成单件乐器轨。

### complete（未来，需 base 模型）
通过添加指定乐器扩展不完整编曲。

## Prompt 工程

### Caption 撰写 — 分层维度

撰写 caption 时叠加多个描述维度，而非单词式描述。

**应包含的维度：**
- **Genre/Style（流派/风格）**：pop、rock、jazz、electronic、lo-fi、synthwave、orchestral
- **Emotion/Mood（情绪）**：melancholic、euphoric、dreamy、nostalgic、intimate、tense
- **Instruments（乐器）**：acoustic guitar、synth pads、808 drums、strings、brass、piano
- **Timbre（音色）**：warm、crisp、airy、punchy、lush、polished、raw
- **Era（年代）**：「80s synth-pop」「modern indie」「classical romantic」
- **Production（制作）**：lo-fi、studio-polished、live recording、cinematic
- **Vocal（人声）**：breathy、powerful、falsetto、raspy、spoken word（或「instrumental」）

**好**：「Slow melancholic piano ballad with intimate female vocal, warm strings building to powerful chorus, studio-polished production」
**差**：「Sad song」

### 核心原则

1. **具体优于模糊** — 描述乐器、情绪、制作风格
2. **避免矛盾** — 不要同时要求「classical strings」与「hardcore metal」
3. **重复强化优先级** — 重复重要元素以强调
4. **稀疏 caption = 更高创作自由** — 详细 caption 会约束模型
5. **BPM/调性用元数据参数** — 不要在 caption 里写「120 BPM」，用 `--bpm 120`

### 歌词格式

**结构标签**（写在歌词中，而非 caption）：
```
[Intro]
[Verse]
[Chorus]
[Bridge]
[Outro]
[Instrumental]
[Guitar Solo]
[Build]
[Drop]
[Breakdown]
```

**人声控制**（作为行或段落前缀）：
```
[raspy vocal]
[whispered]
[falsetto]
[powerful belting]
[harmonies]
[ad-lib]
```

**能量指示：**
- 大写 = 高强度（「WE RISE ABOVE」）
- 括号 = 背景和声（「We rise (together)」）
- 各段落内每行保持 6–10 音节以形成自然节奏

**示例 — 科技产品广告歌：**
```
[Verse]
Build it better, ship it faster
Every feature tells a story

[Chorus - anthemic]
THIS IS YOUR PLATFORM
Your vision, your stage
Digital Samba, every page

[Outro - fade]
(Build it better...)
```

## 视频制作集成

### 各场景类型配乐

| 场景 | 预设 | 时长 | 说明 |
|-------|--------|----------|-------|
| 片头 | `dramatic` 或 `ambient` | 3-5s | 短、定调 |
| 问题 | `tension` | 10-15s | 阴暗、不安 |
| 方案 | `hopeful` | 10-15s | 释然、乐观 |
| 演示 | `lofi` 或 `corporate-bg` | 30-120s | 不抢戏，匹配演示长度 |
| 数据 | `upbeat-tech` | 8-12s | 建立可信度 |
| CTA | `cta` | 5-10s | 最大能量、有力 |
| 片尾 | `ambient` | 5-10s | 轻柔淡出 |

### 时长工作流

1. 先规划各场景时长（来自旁白脚本）
2. 生成匹配时长的音乐：`--duration <scene_seconds>`
3. 音乐时长精确（与请求值误差在 0.1s 内）
4. 跨多场景的背景音乐：生成一条长轨

### 与旁白结合

背景音乐在 Remotion 中应以 10–20% 音量混音：
```tsx
<Audio src={staticFile('voiceover.mp3')} volume={1} />
<Audio src={staticFile('bg-music.mp3')} volume={0.15} />
```

旁白下的音乐：使用纯器乐预设（`corporate-bg`、`ambient`、`lofi`）。
以音乐为主的场景（片头、CTA）：可使用更高音量或人声曲目。

### 品牌一致性

使用 `--brand <name>` 从 `brands/<name>/brand.json` 加载提示。
使用 `--cover --reference brand_theme.mp3` 基于品牌 sonic identity 创作变体。
项目内声音一致：固定 seed（`--seed 42`），仅改变时长/prompt。

## 技术细节

- **输出**：48kHz MP3/WAV/FLAC
- **时长范围**：10–600 秒
- **BPM 范围**：30–300
- **推理**：GPU 上约 2–3s（turbo，8 steps），Mac MPS 上约 40–60s
- **Turbo 模型**：8 steps，无需 CFG，快速且质量良好
- **Shift 参数**：turbo 推荐 3.0（提升质量）

### 何时不应使用 ACE-Step
- **声音克隆** — 改用 Qwen3-TTS 或 ElevenLabs
- **音效** — 使用 ElevenLabs SFX（`tools/sfx.py`）
- **语音/旁白** — 使用旁白工具，而非音乐生成
- **从视频分轨** — 先用 FFmpeg 提取音频，再使用 `--extract`
