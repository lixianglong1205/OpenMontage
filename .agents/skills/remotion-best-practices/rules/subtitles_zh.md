---
name: subtitles
description: 字幕与说明文字规则
metadata:
  tags: subtitles, captions, remotion, json
---

所有字幕必须以 JSON 格式处理。字幕必须使用 `Caption` 类型，定义如下：

```ts
import type { Caption } from "@remotion/captions";
```

类型定义如下：

```ts
type Caption = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
};
```

## 生成字幕

要对视频和音频文件进行转录以生成字幕，请参阅 [./transcribe-captions.md](./transcribe-captions.md) 获取更多说明。

## 显示字幕

要在视频中显示字幕，请参阅 [./display-captions.md](./display-captions.md) 获取更多说明。

## 导入字幕

要从 .srt 文件导入字幕，请参阅 [./import-srt-captions.md](./import-srt-captions.md) 获取更多说明。
