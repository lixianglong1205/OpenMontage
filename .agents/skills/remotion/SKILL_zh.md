---
name: remotion
description: 工具包专属的 Remotion 模式 — 自定义转场、共享组件与项目约定。核心 Remotion 框架知识（hooks、动画、渲染等）请参阅 `remotion-official` 技能。
---

# Remotion — 工具包扩展

> **核心 Remotion 知识**位于 `.claude/skills/remotion-official/`（同步自官方 [remotion-dev/skills](https://github.com/remotion-dev/skills) 仓库）。本文件仅涵盖**工具包专属**模式。

## 共享组件

可复用的视频组件位于 `lib/components/`。在模板中通过以下方式导入：

```tsx
import { AnimatedBackground, SlideTransition, Label } from '../../../../lib/components';
```

| 组件 | 用途 |
|-----------|---------|
| `AnimatedBackground` | 浮动形状背景（变体：subtle、tech、warm、dark） |
| `SlideTransition` | 场景转场（fade、zoom、slide-up、blur-fade） |
| `Label` | 浮动标签徽章，可选 JIRA 引用 |
| `Vignette` | 电影感边缘暗化叠加层 |
| `LogoWatermark` | 角落 Logo 品牌标识 |
| `SplitScreen` | 并排视频对比 |
| `NarratorPiP` | 画中画主讲人叠加 |
| `Envelope` | 带开盖动画的 3D 信封 |
| `PointingHand` | 带滑入与脉冲的动画手势 emoji |
| `MazeDecoration` | 用于角落的动画等距网格装饰 |

## 自定义转场

工具包在 `lib/transitions/` 提供转场库，用于实现超出官方 `@remotion/transitions` 包的场景间效果。

### 使用 TransitionSeries

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
// Import custom transitions from lib (adjust path based on your project location)
import { glitch, lightLeak, clockWipe, checkerboard } from '../../../../lib/transitions';
// Or import from @remotion/transitions for official ones
import { slide, fade } from '@remotion/transitions/slide';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <TitleSlide />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={glitch({ intensity: 0.8 })}
    timing={linearTiming({ durationInFrames: 30 })}
  />
  <TransitionSeries.Sequence durationInFrames={120}>
    <ContentSlide />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

### 可用的自定义转场

| 转场 | 选项 | 适用场景 |
|------------|---------|----------|
| `glitch()` | `intensity`, `slices`, `rgbShift` | 科技演示、锐利揭示、赛博朋克 |
| `rgbSplit()` | `direction`, `displacement` | 现代科技感、高能量转场 |
| `zoomBlur()` | `direction`, `blurAmount` | CTA、高能量时刻、冲击感 |
| `lightLeak()` | `temperature`, `direction` | 庆祝、胶片美学、温暖氛围 |
| `clockWipe()` | `startAngle`, `direction`, `segments` | 与时间相关的内容、趣味揭示 |
| `pixelate()` | `maxBlockSize`, `gridSize`, `scanlines`, `glitchArtifacts`, `randomness` | 复古/游戏、数字化变换 |
| `checkerboard()` | `gridSize`, `pattern`, `stagger`, `squareAnimation` | 趣味揭示、结构化转场 |

**Checkerboard 图案：** `sequential`, `random`, `diagonal`, `alternating`, `spiral`, `rows`, `columns`, `center-out`, `corners-in`

### 转场示例

```tsx
// Tech/cyberpunk feel
glitch({ intensity: 0.8, slices: 8, rgbShift: true })

// Warm celebration
lightLeak({ temperature: 'warm', direction: 'right' })

// High energy zoom
zoomBlur({ direction: 'in', blurAmount: 20 })

// Chromatic aberration
rgbSplit({ direction: 'diagonal', displacement: 30 })

// Clock sweep reveal
clockWipe({ direction: 'clockwise', startAngle: 0 })

// Retro pixelation
pixelate({ maxBlockSize: 50, glitchArtifacts: true })

// Checkerboard patterns
checkerboard({ pattern: 'diagonal', gridSize: 8 })
checkerboard({ pattern: 'spiral', gridSize: 10 })
checkerboard({ pattern: 'center-out', squareAnimation: 'scale' })
```

### 转场时长指南

| 类型 | 帧数 | 说明 |
|------|--------|-------|
| 快切 | 15-20 | 快速、有力 |
| 标准 | 30-45 | 最常见 |
| 戏剧性 | 50-60 | 慢速揭示 |
| Glitch 效果 | 20-30 | 应显得突然 |
| 漏光 | 45-60 | 需要扫过的时间 |

### 预览转场

运行展示画廊查看所有转场：

```bash
cd showcase/transitions && npm run studio
```

## 工具包最佳实践

1. **仅使用基于帧的动画** — 避免 CSS transition/animation；渲染时会导致闪烁
2. **使用 useVideoConfig() 的 fps** — 使动画与帧率无关
3. **钳制插值** — 使用 `extrapolateRight: 'clamp'` 防止数值失控
4. **使用 OffthreadVideo** — 复杂合成中性能优于 `<Video>`
5. **异步使用 delayRender** — 数据就绪前始终阻塞渲染
6. **资源使用 staticFile** — 正确引用 `public/` 文件夹中的文件
7. **所有项目使用 30fps** — 计时：帧数 = 秒数 × 30
8. **playbackRate 须为常量** — 可变或极端速度请先用 FFmpeg 预处理

## 项目时长约定

| 场景类型 | 时长 | 说明 |
|------------|----------|-------|
| 标题 | 3-5s (90-150f) | Logo + 主标题 |
| 概览 | 10-20s | 3-5 个要点 |
| 演示 | 10-30s | 调整 playbackRate 以适配 |
| 数据 | 8-12s | 3-4 张统计卡片 |
| 片尾 | 5-10s | 快速淡出 |

**节奏：** 旁白约 150 词/分钟。旁白驱动时长。

## 高级 API

有关所有 hooks、组件、renderer、Lambda 与 Player API 的详细文档，请参阅 [reference.md](reference.md)。

## 许可说明

Remotion 采用特殊许可。公司商业使用可能需要取得许可。请查阅 https://remotion.dev/license

---

## 反馈与贡献

若本技能缺少信息或可改进：

- **缺少某种模式？** 说明你需要什么
- **发现错误？** 告知问题所在
- **想要贡献？** 我可以协助你：
  1. 更新本技能以改进内容
  2. 向 github.com/digitalsamba/claude-code-video-toolkit 提交 PR

只需说「improve this skill」，我会引导你更新 `.claude/skills/remotion/SKILL.md`。
