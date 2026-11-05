# OpenMontage 音乐生成用法

> 来源：ElevenLabs Music API 文档、ElevenLabs 最佳实践指南、Artlist BPM
> 指南，以及 `.agents/skills/music/` 与 `.agents/skills/elevenlabs/` 中的现有 Layer 3 技能

## 快速参考卡

```
API MODEL:        music_v1
MIN DURATION:     3,000ms (3s)
MAX DURATION:     600,000ms (10 min)
INSTRUMENTAL:     Always set force_instrumental=true for video background
COST:             ~$0.05 per 30 seconds
KEY RULE:         Music must be 18-20 dB below narration (see sound-design.md)
```

## 按视频类型选择 BPM

| 视频类型 | BPM 范围 | 提示词片段 |
|-----------|-----------|-----------------|
| 教育类讲解 | 80-100 | "gentle ambient electronic, 90 BPM" |
| 企业 / 科技 | 100-120 | "upbeat corporate pop, 110 BPM, positive" |
| 史诗 / 戏剧式揭晓 | 60-80 | "cinematic orchestral, 70 BPM, building tension" |
| 快节奏蒙太奇 | 120-140 | "energetic electronic, 130 BPM, driving beat" |
| 冥想 / 平静 | 50-70 | "ambient drone, 60 BPM, peaceful" |
| 喜剧 / 轻松 | 100-130 | "playful ukulele pop, 120 BPM, whimsical" |
| 悲伤 / 沉思 | 60-80 | "melancholic piano, 65 BPM, minor key" |
| 动作 / 高燃 | 140-170 | "high-intensity drum and bass, 160 BPM" |

## 调性与情绪映射

| 情绪 | 调性 | 音乐特征 |
|------|-----|----------------------|
| 快乐 /  upbeat | C major, G major | 明亮、稳定、有活力 |
| 严肃 / 专业 | D minor, A minor | 沉稳、权威 |
| 神秘 / 好奇 | E minor, B minor | 张力、期待 |
| 凯旋 / 鼓舞 | D major, Bb major | 开阔、高潮感 |
| 忧郁 / 深思 | F minor, C minor | 内省、情感化 |
| 中性 /  ambient | C major, Am (no strong key) | 不抢戏、适合背景 |

## 提示词工程

### 结构

```
[GENRE/STYLE], [BPM], [KEY/MOOD], [INSTRUMENTS], [ENERGY LEVEL], [PURPOSE]
```

### 示例

**教育类讲解：**
```
Gentle lo-fi ambient electronic, 90 BPM, C major, soft synth pads and light
percussion, calm and steady energy, background music for narration
```

**企业产品演示：**
```
Modern upbeat corporate pop, 110 BPM, G major, acoustic guitar and light drums,
positive energy building gradually, underscore for product walkthrough
```

**技术深度讲解：**
```
Minimal ambient electronic, 80 BPM, A minor, soft Rhodes piano and subtle
bass, contemplative and focused, background music for technical explanation
```

### 核心提示词规则

1. **务必包含 "background" 或 "underscore"** — 让模型保持动态平稳
2. **始终使用 `force_instrumental=true`** — 歌词会与旁白争抢注意力
3. **明确写出 BPM** — 不要指望仅靠流派设定 tempo
4. **避免 "bright hi-hats" 或 "prominent vocals"** — 高频、繁忙元素会与 2–4 kHz 语音清晰度频段冲突
5. **说明能量走向** — 讲解用 "steady energy"，揭晓用 "building gradually"

## 时长匹配

### 精确时长

```python
result = music_gen.execute({
    "prompt": "Gentle ambient, 90 BPM, background underscore",
    "duration_seconds": 150,  # Match video length
    "output_path": "assets/music/background.mp3"
})
```

### 分段映射（进阶）

若视频有明显段落，可分段生成：

| 视频段落 | 时长 | 音乐风格 |
|--------------|----------|-------------|
| 开场 / hook | 8-10s | 轻柔、渐强 |
| 主体讲解 | 90-120s | 平稳、中性 |
| 关键揭晓 | 20-30s | 加强、更饱满 |
| 片尾 | 10-15s | 渐弱、柔和 |

各段单独生成音轨，在 `audio_mixer` 中交叉淡入淡出。

## 长视频循环

当视频长于生成音轨时：

1. 生成约为视频长度 30–60% 的曲目
2. 用 FFmpeg 做无缝循环：
   ```bash
   ffmpeg -stream_loop 2 -i music.mp3 -c copy music_looped.mp3
   ```
3. 在 `audio_mixer` 的循环衔接处做 2–3 秒交叉淡入淡出

**更优做法：** 按视频精确时长生成。ElevenLabs 单次生成最长支持 10 分钟。

## 分轨（Stem）隔离

为更干净的 ducking 控制，可生成独立 stem：

- `"solo electric guitar in E minor, 90 BPM"` — 仅吉他轨
- `"soft ambient pad in C major, 80 BPM"` — 仅合成 pad
- 在合成阶段用 FFmpeg 叠层，便于精确 ducking

## 在 OpenMontage 中的应用

使用 `music_gen` 工具时：

1. **按上表匹配 BPM 与内容类型** — 不要用泛化提示词应付
2. **始终设置 `force_instrumental=true`** — 旁白下不要歌词
3. **每条提示词包含 "background" 或 "underscore"**
4. **时长对齐视频长度** — 能不用循环就不用
5. **预算** — 约 $0.05/30s，3 分钟视频音乐约 $0.30
6. **音乐比旁白低 18–20 dB ducking** — 规则见 `skills/creative/sound-design.md`
7. **在 `audio_mixer` 对音乐床做 2–4 kHz 切除**，让出语音清晰度频段
8. **用手机扬声器试听** — 若旁白被音乐盖住，加大 ducking
9. **一视频一轨** — 除非叙事明确转折，否则中途不要换音乐风格
