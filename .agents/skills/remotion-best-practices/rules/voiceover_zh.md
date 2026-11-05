---
name: voiceover
description: 使用 ElevenLabs TTS 为 Remotion composition 添加 AI 生成的旁白
metadata:
  tags: voiceover, audio, elevenlabs, tts, speech, calculateMetadata, dynamic duration
---

# 为 Remotion composition 添加 AI 旁白

使用 ElevenLabs TTS 为每个场景生成语音音频，然后使用 [`calculateMetadata`](./calculate-metadata) 动态调整 composition 时长以匹配音频。

## 前提条件

需要 **ElevenLabs API 密钥**（`ELEVENLABS_API_KEY` 环境变量）。

若未设置 `ELEVENLABS_API_KEY`，**必须**向用户索取 ElevenLabs API 密钥。**禁止**回退到其他 TTS 工具。

运行生成脚本时，请确保环境变量可用：

```bash
node --strip-types generate-voiceover.ts
```

## 使用 ElevenLabs 生成音频

创建一个脚本：读取配置、为每个场景调用 ElevenLabs API，并将 MP3 文件写入 `public/` 目录，以便 Remotion 通过 `staticFile()` 访问。

单个场景的核心 API 调用：

```ts title="generate-voiceover.ts"
const response = await fetch(
  `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
  {
    method: "POST",
    headers: {
      "xi-api-key": process.env.ELEVENLABS_API_KEY!,
      "Content-Type": "application/json",
      Accept: "audio/mpeg",
    },
    body: JSON.stringify({
      text: "Welcome to the show.",
      model_id: "eleven_multilingual_v2",
      voice_settings: {
        stability: 0.5,
        similarity_boost: 0.75,
        style: 0.3,
      },
    }),
  },
);

const audioBuffer = Buffer.from(await response.arrayBuffer());
writeFileSync(`public/voiceover/${compositionId}/${scene.id}.mp3`, audioBuffer);
```

## 使用 calculateMetadata 动态设置 composition 时长

使用 [`calculateMetadata`](./calculate-metadata.md) 测量[音频时长](./get-audio-duration.md)，并据此设置 composition 长度。

```tsx
import { CalculateMetadataFunction, staticFile } from "remotion";
import { getAudioDuration } from "./get-audio-duration";

const FPS = 30;

const SCENE_AUDIO_FILES = [
  "voiceover/my-comp/scene-01-intro.mp3",
  "voiceover/my-comp/scene-02-main.mp3",
  "voiceover/my-comp/scene-03-outro.mp3",
];

export const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const durations = await Promise.all(
    SCENE_AUDIO_FILES.map((file) => getAudioDuration(staticFile(file))),
  );

  const sceneDurations = durations.map((durationInSeconds) => {
    return durationInSeconds * FPS;
  });

  return {
    durationInFrames: Math.ceil(sceneDurations.reduce((sum, d) => sum + d, 0)),
  };
};
```

计算得到的 `sceneDurations` 通过 `voiceover` prop 传入组件，以便组件知道每个场景应持续多久。

若 composition 使用 [`<TransitionSeries>`](./transitions.md)，则从总时长中减去过渡重叠部分：[./transitions.md#calculating-total-composition-duration](./transitions.md#calculating-total-composition-duration)

## 在组件中渲染音频

有关如何在组件中渲染音频的更多信息，请参阅 [audio.md](./audio.md)。

## 延迟音频开始

有关如何延迟音频开始的更多信息，请参阅 [audio.md#delaying](./audio.md#delaying)。
