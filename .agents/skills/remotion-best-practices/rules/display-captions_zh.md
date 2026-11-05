---
name: display-captions
description: 在 Remotion 中展示字幕：TikTok 风格分页与逐词高亮
metadata:
  tags: captions, subtitles, display, tiktok, highlight
---

# 在 Remotion 中展示字幕

本指南说明如何在 Remotion 中展示字幕，并假定你已有 [`Caption`](https://www.remotion.dev/docs/captions/caption) 格式的字幕数据。

## 前提条件

请先阅读 [Transcribing audio](transcribe-captions.md)，了解如何生成字幕。

首先需安装 [`@remotion/captions`](https://www.remotion.dev/docs/captions) 包。  
若尚未安装，请执行：

```bash
npx remotion add @remotion/captions
```

## 获取字幕

先拉取字幕 JSON 文件。使用 [`useDelayRender()`](https://www.remotion.dev/docs/use-delay-render) 在字幕加载完成前暂停渲染：

```tsx
import { useState, useEffect, useCallback } from "react";
import { AbsoluteFill, staticFile, useDelayRender } from "remotion";
import type { Caption } from "@remotion/captions";

export const MyComponent: React.FC = () => {
  const [captions, setCaptions] = useState<Caption[] | null>(null);
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [handle] = useState(() => delayRender());

  const fetchCaptions = useCallback(async () => {
    try {
      // Assuming captions.json is in the public/ folder.
      const response = await fetch(staticFile("captions123.json"));
      const data = await response.json();
      setCaptions(data);
      continueRender(handle);
    } catch (e) {
      cancelRender(e);
    }
  }, [continueRender, cancelRender, handle]);

  useEffect(() => {
    fetchCaptions();
  }, [fetchCaptions]);

  if (!captions) {
    return null;
  }

  return <AbsoluteFill>{/* Render captions here */}</AbsoluteFill>;
};
```

## 创建分页

使用 `createTikTokStyleCaptions()` 将字幕分组为多个页面。`combineTokensWithinMilliseconds` 选项控制同一页同时显示多少个词：

```tsx
import { useMemo } from "react";
import { createTikTokStyleCaptions } from "@remotion/captions";
import type { Caption } from "@remotion/captions";

// How often captions should switch (in milliseconds)
// Higher values = more words per page
// Lower values = fewer words (more word-by-word)
const SWITCH_CAPTIONS_EVERY_MS = 1200;

const { pages } = useMemo(() => {
  return createTikTokStyleCaptions({
    captions,
    combineTokensWithinMilliseconds: SWITCH_CAPTIONS_EVERY_MS,
  });
}, [captions]);
```

## 使用 Sequence 渲染

遍历各页，在 `<Sequence>` 中分别渲染。根据每页的时间信息计算起始帧与时长：

```tsx
import { Sequence, useVideoConfig, AbsoluteFill } from "remotion";
import type { TikTokPage } from "@remotion/captions";

const CaptionedContent: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill>
      {pages.map((page, index) => {
        const nextPage = pages[index + 1] ?? null;
        const startFrame = (page.startMs / 1000) * fps;
        const endFrame = Math.min(
          nextPage ? (nextPage.startMs / 1000) * fps : Infinity,
          startFrame + (SWITCH_CAPTIONS_EVERY_MS / 1000) * fps,
        );
        const durationInFrames = endFrame - startFrame;

        if (durationInFrames <= 0) {
          return null;
        }

        return (
          <Sequence
            key={index}
            from={startFrame}
            durationInFrames={durationInFrames}
          >
            <CaptionPage page={page} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

## 保留空白字符

字幕对空白字符敏感。应在每个词的 `text` 字段中包含前置空格。使用 `whiteSpace: "pre"` 以保留字幕中的空白。

## 独立的字幕组件

将字幕逻辑放在独立组件中。  
为其新建一个文件。

## 逐词高亮

字幕页包含 `tokens`，可用于高亮当前正在朗读的词：

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { TikTokPage } from "@remotion/captions";

const HIGHLIGHT_COLOR = "#39E508";

const CaptionPage: React.FC<{ page: TikTokPage }> = ({ page }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Current time relative to the start of the sequence
  const currentTimeMs = (frame / fps) * 1000;
  // Convert to absolute time by adding the page start
  const absoluteTimeMs = page.startMs + currentTimeMs;

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{ fontSize: 80, fontWeight: "bold", whiteSpace: "pre" }}>
        {page.tokens.map((token) => {
          const isActive =
            token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs;

          return (
            <span
              key={token.fromMs}
              style={{ color: isActive ? HIGHLIGHT_COLOR : "white" }}
            >
              {token.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

## 与视频内容同时展示字幕

默认将字幕与视频内容叠在一起，以保持同步。  
每个视频应使用单独的字幕 JSON 文件。

```tsx
<AbsoluteFill>
  <Video src={staticFile("video.mp4")} />
  <CaptionPage page={page} />
</AbsoluteFill>
```
