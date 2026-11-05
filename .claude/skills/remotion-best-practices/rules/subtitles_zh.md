---
name: subtitles
description: 字幕与 caption 规则
metadata:
  tags: subtitles, captions, remotion, json
---

所有 caption 必须经 JSON 处理。caption 必须使用如下 `Caption` 类型：

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

## 生成 caption

要对视频和音频文件转写以生成 caption，请参阅 [./transcribe-captions.md](./transcribe-captions.md) 中的说明。

## 显示 caption

要在视频中显示 caption，请参阅 [./display-captions.md](./display-captions.md) 中的说明。

## 导入 caption

要从 .srt 文件导入 caption，请参阅 [./import-srt-captions.md](./import-srt-captions.md) 中的说明。
