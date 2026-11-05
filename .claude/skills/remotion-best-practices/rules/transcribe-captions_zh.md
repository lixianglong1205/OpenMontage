---
name: transcribe-captions
description: 在 Remotion 中转录音频以生成字幕
metadata:
  tags: captions, transcribe, whisper, audio, speech-to-text
---

# 转录音频

要在 Remotion 中转录音频并生成字幕，可以使用 [`@remotion/install-whisper-cpp`](https://www.remotion.dev/docs/install-whisper-cpp) 包中的 [`transcribe()`](https://www.remotion.dev/docs/install-whisper-cpp/transcribe) 函数。

## 前提条件

首先需要安装 `@remotion/install-whisper-cpp` 包。
若尚未安装，请使用以下命令：

```bash
npx remotion add @remotion/install-whisper-cpp
```

## 转录

编写 Node.js 脚本，下载 Whisper.cpp 与模型，并对音频进行转录。

```ts
import path from "path";
import {
  downloadWhisperModel,
  installWhisperCpp,
  transcribe,
  toCaptions,
} from "@remotion/install-whisper-cpp";
import fs from "fs";

const to = path.join(process.cwd(), "whisper.cpp");

await installWhisperCpp({
  to,
  version: "1.5.5",
});

await downloadWhisperModel({
  model: "medium.en",
  folder: to,
});

// Convert the audio to a 16KHz wav file first if needed:
// import {execSync} from 'child_process';
// execSync('ffmpeg -i /path/to/audio.mp4 -ar 16000 /path/to/audio.wav -y');

const whisperCppOutput = await transcribe({
  model: "medium.en",
  whisperPath: to,
  whisperCppVersion: "1.5.5",
  inputPath: "/path/to/audio123.wav",
  tokenLevelTimestamps: true,
});

// Optional: Apply our recommended postprocessing
const { captions } = toCaptions({
  whisperCppOutput,
});

// Write it to the public/ folder so it can be fetched from Remotion
fs.writeFileSync("captions123.json", JSON.stringify(captions, null, 2));
```

请分别转录每个片段，并生成多个 JSON 文件。

有关如何在 Remotion 中显示字幕，请参阅 [显示字幕](display-captions.md)。
