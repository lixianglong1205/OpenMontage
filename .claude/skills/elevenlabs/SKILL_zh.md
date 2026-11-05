---
name: elevenlabs
description: 使用 ElevenLabs API 生成 AI 旁白、音效和音乐。适用于为视频、播客或游戏创建音频内容。触发场景包括：生成旁白、解说、对话、根据描述生成音效、背景音乐、配乐生成、声音克隆，或任何音频合成任务。
---

# ElevenLabs 音频生成

需要在 `.env` 中配置 `ELEVENLABS_API_KEY`。

## 文本转语音（Text-to-Speech）

```python
from elevenlabs.client import ElevenLabs
from elevenlabs import save, VoiceSettings
import os

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

audio = client.text_to_speech.convert(
    text="Welcome to my video!",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    voice_settings=VoiceSettings(
        stability=0.5,
        similarity_boost=0.75,
        style=0.5,
        speed=1.0
    )
)
save(audio, "voiceover.mp3")
```

### 模型

| 模型 | 质量 | SSML 支持 | 说明 |
|-------|---------|--------------|-------|
| `eleven_multilingual_v2` | 一致性最高 | 无 | 稳定、可用于生产，29 种语言 |
| `eleven_flash_v2_5` | 良好 | `<break>`、`<phoneme>` | 速度快，支持停顿/发音标签 |
| `eleven_turbo_v2_5` | 良好 | `<break>`、`<phoneme>` | 延迟最低 |
| `eleven_v3` | 表现力最强 | 无 | Alpha — 不够稳定，需要提示词工程 |

**选择建议：** 追求可靠用 multilingual_v2；需要 SSML 控制用 flash/turbo；追求最大表现力用 v3（需预期多次重录）。

### 按风格的语音设置

| 风格 | stability | similarity | style | speed |
|-------|-----------|------------|-------|-------|
| 自然/专业 | 0.75-0.85 | 0.9 | 0.0-0.1 | 1.0 |
| 对话感 | 0.5-0.6 | 0.85 | 0.3-0.4 | 0.9-1.0 |
| 高能量/YouTuber | 0.3-0.5 | 0.75 | 0.5-0.7 | 1.0-1.1 |

### 段落之间的停顿

**使用 flash/turbo 模型时：** 在文本中内联使用 SSML break 标签：
```
...end of section. <break time="1.5s" /> Start of next...
```
单次 break 最长 3 秒。过多 break 可能导致语速异常。

**使用 multilingual_v2 / v3 时：** 不支持 SSML。可选方案：
- 段落换行（空行）— 约产生 0.3–0.5 秒自然停顿
- 用 ffmpeg 后处理：切分音频并插入静音

**警告：** `...`（省略号）**不能**可靠地表示停顿 — 可能被读成词/音效。不要用省略号作为停顿手段。

### 发音控制

**音标拼写（任意模型）：** 按期望读音书写：
- `Janus` → `Jan-us`
- `nginx` → `engine-x`
- 用连字符、大写、撇号引导发音

**SSML phoneme 标签（仅 flash/turbo）：**
```
<phoneme alphabet="ipa" ph="ˈdʒeɪnəs">Janus</phoneme>
```

### 迭代工作流

1. 生成 → 试听 → 找出发音/节奏问题
2. 调整：音标拼写、break 标签、语音设置
3. 重新生成。若停顿仍不够精确，用 ffmpeg 后期加静音，而不是与 TTS 引擎硬扛。

## 声音克隆（Voice Cloning）

### 即时声音克隆（Instant Voice Clone）

```python
with open("sample.mp3", "rb") as f:
    voice = client.voices.ivc.create(
        name="My Voice",
        files=[f],
        remove_background_noise=True
    )
print(f"Voice ID: {voice.voice_id}")
```

- 使用 `client.voices.ivc.create()`（不要用 `client.voices.clone()`）
- 以二进制模式（`"rb"`）传入文件句柄，不要只传路径
- m4a 需先转换：`ffmpeg -i input.m4a -codec:a libmp3lame -qscale:a 2 output.mp3`
- 多个样本（2–3 段）可提高准确度
- 保存 voice ID 以便复用

**专业声音克隆（Professional Voice Clone）：** 需要 Creator 计划及以上，30+ 分钟音频。详见 [reference.md](reference.md)。

## 音效（Sound Effects）

单次生成最长 22 秒。

```python
result = client.text_to_sound_effects.convert(
    text="Thunder rumbling followed by heavy rain",
    duration_seconds=10,
    prompt_influence=0.3
)
with open("thunder.mp3", "wb") as f:
    for chunk in result:
        f.write(chunk)
```

**提示词技巧：** 要具体 — 例如「Heavy footsteps on wooden floorboards, slow and deliberate, with creaking」（木地板上沉重、缓慢、刻意的脚步声，带吱嘎声）

## 音乐生成（Music Generation）

时长 10 秒至 5 分钟。使用 `client.music.compose()`（不要用 `.generate()`）。

```python
result = client.music.compose(
    prompt="Upbeat indie rock, catchy guitar riff, energetic drums, travel vlog",
    music_length_ms=60000,
    force_instrumental=True
)
with open("music.mp3", "wb") as f:
    for chunk in result:
        f.write(chunk)
```

**提示词结构：** 流派、情绪、乐器、 tempo、使用场景。背景音乐可加 “no vocals” 或设置 `force_instrumental=True`。

## Remotion 集成

### 完整工作流：从脚本到同步场景

```
VOICEOVER-SCRIPT.md → voiceover.py → public/audio/ → Remotion composition
        ↓                  ↓               ↓                 ↓
  Scene narration    Generate MP3    Audio files     <Audio> component
  with durations     per scene       with timing     synced to scenes
```

### 步骤 1：按场景生成音频

使用工具包中的 voiceover 工具为每个场景生成音频：

```bash
# Generate voiceover files for each scene
python tools/voiceover.py --scene-dir public/audio/scenes --json

# Output:
# public/audio/scenes/
#   ├── scene-01-title.mp3
#   ├── scene-02-problem.mp3
#   ├── scene-03-solution.mp3
#   └── manifest.json  (durations for each file)
```

`manifest.json` 包含各文件时长信息：
```json
{
  "scenes": [
    { "file": "scene-01-title.mp3", "duration": 4.2 },
    { "file": "scene-02-problem.mp3", "duration": 12.8 },
    { "file": "scene-03-solution.mp3", "duration": 15.3 }
  ],
  "totalDuration": 32.3
}
```

### 步骤 2：在 Remotion 合成中使用音频

```tsx
// src/Composition.tsx
import { Audio, staticFile, Series, useVideoConfig } from 'remotion';

// Import scene components
import { TitleSlide } from './scenes/TitleSlide';
import { ProblemSlide } from './scenes/ProblemSlide';
import { SolutionSlide } from './scenes/SolutionSlide';

// Scene durations (from manifest.json, converted to frames at 30fps)
const SCENE_DURATIONS = {
  title: Math.ceil(4.2 * 30),      // 126 frames
  problem: Math.ceil(12.8 * 30),   // 384 frames
  solution: Math.ceil(15.3 * 30),  // 459 frames
};

export const MainComposition: React.FC = () => {
  return (
    <>
      {/* Scene sequence */}
      <Series>
        <Series.Sequence durationInFrames={SCENE_DURATIONS.title}>
          <TitleSlide />
        </Series.Sequence>
        <Series.Sequence durationInFrames={SCENE_DURATIONS.problem}>
          <ProblemSlide />
        </Series.Sequence>
        <Series.Sequence durationInFrames={SCENE_DURATIONS.solution}>
          <SolutionSlide />
        </Series.Sequence>
      </Series>

      {/* Audio track - plays continuously across all scenes */}
      <Audio src={staticFile('audio/voiceover.mp3')} volume={1} />

      {/* Optional: Background music at lower volume */}
      <Audio src={staticFile('audio/music.mp3')} volume={0.15} />
    </>
  );
};
```

### 步骤 3：按场景单独挂音频（备选）

需要更细控制时，可在每个场景内单独添加音频：

```tsx
// src/scenes/ProblemSlide.tsx
import { Audio, staticFile, useCurrentFrame } from 'remotion';

export const ProblemSlide: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{ /* slide styles */ }}>
      <h1>The Problem</h1>
      {/* Scene content */}

      {/* Audio starts when this scene starts (frame 0 of this sequence) */}
      <Audio src={staticFile('audio/scenes/scene-02-problem.mp3')} />
    </div>
  );
};
```

### 让画面与旁白同步

根据音频时长计算场景长度，而不是反过来：

```tsx
// src/config/timing.ts
import manifest from '../../public/audio/scenes/manifest.json';

const FPS = 30;

// Convert audio durations to frame counts
export const sceneDurations = manifest.scenes.reduce((acc, scene) => {
  const name = scene.file.replace(/^scene-\d+-/, '').replace('.mp3', '');
  acc[name] = Math.ceil(scene.duration * FPS);
  return acc;
}, {} as Record<string, number>);

// Usage in composition:
// <Series.Sequence durationInFrames={sceneDurations.title}>
```

### 音频时间模式

```tsx
import { Audio, Sequence, interpolate, useCurrentFrame } from 'remotion';

// Fade in audio
export const FadeInAudio: React.FC<{ src: string; fadeFrames?: number }> = ({
  src,
  fadeFrames = 30
}) => {
  const frame = useCurrentFrame();
  const volume = interpolate(frame, [0, fadeFrames], [0, 1], {
    extrapolateRight: 'clamp',
  });
  return <Audio src={src} volume={volume} />;
};

// Delayed audio start
export const DelayedAudio: React.FC<{ src: string; delayFrames: number }> = ({
  src,
  delayFrames
}) => (
  <Sequence from={delayFrames}>
    <Audio src={src} />
  </Sequence>
);

// Usage:
// <FadeInAudio src={staticFile('audio/music.mp3')} fadeFrames={60} />
// <DelayedAudio src={staticFile('audio/sfx/whoosh.mp3')} delayFrames={45} />
```

### 旁白与演示视频同步

某场景同时有旁白和演示视频时：

```tsx
import { Audio, OffthreadVideo, staticFile, useVideoConfig } from 'remotion';

export const DemoScene: React.FC = () => {
  const { durationInFrames, fps } = useVideoConfig();

  // Calculate playback rate to fit demo into voiceover duration
  const demoDuration = 45; // seconds (original demo length)
  const sceneDuration = durationInFrames / fps; // seconds (from voiceover)
  const playbackRate = demoDuration / sceneDuration;

  return (
    <>
      <OffthreadVideo
        src={staticFile('demos/feature-demo.mp4')}
        playbackRate={playbackRate}
      />
      <Audio src={staticFile('audio/scenes/scene-04-demo.mp3')} />
    </>
  );
};
```

### 错误处理

```tsx
import { Audio, staticFile, delayRender, continueRender } from 'remotion';
import { useEffect, useState } from 'react';

export const SafeAudio: React.FC<{ src: string }> = ({ src }) => {
  const [handle] = useState(() => delayRender());
  const [audioReady, setAudioReady] = useState(false);

  useEffect(() => {
    const audio = new window.Audio(src);
    audio.oncanplaythrough = () => {
      setAudioReady(true);
      continueRender(handle);
    };
    audio.onerror = () => {
      console.error(`Failed to load audio: ${src}`);
      continueRender(handle); // Continue without audio rather than hang
    };
  }, [src, handle]);

  if (!audioReady) return null;
  return <Audio src={src} />;
};
```

### 工具包命令：/generate-voiceover

`/generate-voiceover` 命令覆盖完整工作流：

```
/generate-voiceover

1. Reads VOICEOVER-SCRIPT.md
2. Extracts narration for each scene
3. Generates audio via ElevenLabs API
4. Saves to public/audio/scenes/
5. Creates manifest.json with durations
6. Updates project.json with timing info
```

## 常用音色

- George: `JBFqnCBsd6RMkjVDRZzb`（温暖旁白）
- Rachel: `21m00Tcm4TlvDq8ikWAM`（清晰女声）
- Adam: `pNInz6obpgDQGcFmaJgB`（专业男声）

列出全部：`client.voices.get_all()`

完整 API 文档见 [reference.md](reference.md)。
