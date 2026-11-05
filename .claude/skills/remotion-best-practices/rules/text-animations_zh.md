---
name: text-animations
description: Remotion 的排版与文字动画模式。
metadata:
  tags: typography, text, typewriter, highlighter ken
---

## 文字动画

基于 `useCurrentFrame()`，逐字符缩短字符串以实现打字机效果。

## 打字机效果

参见 [Typewriter](assets/text-animations-typewriter.tsx) 的高级示例：带闪烁光标，并在第一句后出现停顿。

打字机效果务必使用字符串切片。切勿使用逐字符透明度。

## 词语高亮

参见 [Word Highlight](assets/text-animations-word-highlight.tsx) 示例，了解词语高亮动画（类似荧光笔效果）。
