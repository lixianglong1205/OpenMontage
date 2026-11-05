---
name: text-animations
description: Remotion 中排版与文字动画模式。
metadata:
  tags: typography, text, typewriter, highlighter ken
---

## 文字动画

基于 `useCurrentFrame()`，逐字符缩短字符串以实现打字机效果。

## 打字机效果

查看 [Typewriter](assets/text-animations-typewriter.tsx) 获取进阶示例：带闪烁光标，并在第一句后暂停。

打字机效果应始终使用字符串切片，切勿使用逐字符 opacity。

## 词语高亮

查看 [Word Highlight](assets/text-animations-word-highlight.tsx) 了解词语高亮动画示例，类似荧光笔效果。
