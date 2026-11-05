---
name: remotion-best-practices
description: Remotion 最佳实践 — 在 React 中创建视频
metadata:
  tags: remotion, video, react, animation, composition
---

## 何时使用

在处理 Remotion 代码时，请使用本技能以获取领域相关知识。

## 字幕

处理字幕或副标题时，请加载 [./rules/subtitles.md](./rules/subtitles.md) 以获取更多信息。

## 使用 FFmpeg

对于部分视频操作（例如裁剪视频或检测静音），应使用 FFmpeg。请加载 [./rules/ffmpeg.md](./rules/ffmpeg.md) 以获取更多信息。

## 音频可视化

需要可视化音频（频谱条、波形、低音响应效果）时，请加载 [./rules/audio-visualization.md](./rules/audio-visualization.md) 以获取更多信息。

## 音效

需要使用音效时，请加载 [./rules/sound-effects.md](./rules/sound-effects.md) 以获取更多信息。

## 如何使用

阅读各条规则文件以了解详细说明与代码示例：

- [rules/3d.md](rules/3d.md) - 在 Remotion 中使用 Three.js 与 React Three Fiber 的 3D 内容
- [rules/animations.md](rules/animations.md) - Remotion 基础动画技能
- [rules/assets.md](rules/assets.md) - 在 Remotion 中导入图片、视频、音频与字体
- [rules/audio.md](rules/audio.md) - 在 Remotion 中使用音频与声音 — 导入、裁剪、音量、速度、音高
- [rules/calculate-metadata.md](rules/calculate-metadata.md) - 动态设置 composition 时长、尺寸与 props
- [rules/can-decode.md](rules/can-decode.md) - 使用 Mediabunny 检查浏览器能否解码视频
- [rules/charts.md](rules/charts.md) - Remotion 图表与数据可视化模式（柱状、饼图、折线、股票图）
- [rules/compositions.md](rules/compositions.md) - 定义 composition、still、文件夹、默认 props 与动态 metadata
- [rules/extract-frames.md](rules/extract-frames.md) - 使用 Mediabunny 在指定时间戳从视频提取帧
- [rules/fonts.md](rules/fonts.md) - 在 Remotion 中加载 Google Fonts 与本地字体
- [rules/get-audio-duration.md](rules/get-audio-duration.md) - 使用 Mediabunny 获取音频文件时长（秒）
- [rules/get-video-dimensions.md](rules/get-video-dimensions.md) - 使用 Mediabunny 获取视频文件的宽高
- [rules/get-video-duration.md](rules/get-video-duration.md) - 使用 Mediabunny 获取视频文件时长（秒）
- [rules/gifs.md](rules/gifs.md) - 显示与 Remotion 时间轴同步的 GIF
- [rules/images.md](rules/images.md) - 使用 Img 组件在 Remotion 中嵌入图片
- [rules/light-leaks.md](rules/light-leaks.md) - 使用 @remotion/light-leaks 的光斑叠加效果
- [rules/lottie.md](rules/lottie.md) - 在 Remotion 中嵌入 Lottie 动画
- [rules/measuring-dom-nodes.md](rules/measuring-dom-nodes.md) - 在 Remotion 中测量 DOM 元素尺寸
- [rules/measuring-text.md](rules/measuring-text.md) - 测量文本尺寸、使文本适配容器并检测溢出
- [rules/sequencing.md](rules/sequencing.md) - Remotion 序列模式 — 延迟、裁剪、限制条目时长
- [rules/tailwind.md](rules/tailwind.md) - 在 Remotion 中使用 TailwindCSS
- [rules/text-animations.md](rules/text-animations.md) - Remotion 排版与文本动画模式
- [rules/timing.md](rules/timing.md) - Remotion 插值曲线 — 线性、easing、spring 动画
- [rules/transitions.md](rules/transitions.md) - Remotion 场景转场模式
- [rules/transparent-videos.md](rules/transparent-videos.md) - 渲染带透明通道的视频
- [rules/trimming.md](rules/trimming.md) - Remotion 裁剪模式 — 切掉动画开头或结尾
- [rules/videos.md](rules/videos.md) - 在 Remotion 中嵌入视频 — 裁剪、音量、速度、循环、音高
- [rules/parameters.md](rules/parameters.md) - 通过添加 Zod schema 使视频可参数化
- [rules/maps.md](rules/maps.md) - 使用 Mapbox 添加地图并为其添加动画
- [rules/voiceover.md](rules/voiceover.md) - 使用 ElevenLabs TTS 为 Remotion composition 添加 AI 生成的旁白
