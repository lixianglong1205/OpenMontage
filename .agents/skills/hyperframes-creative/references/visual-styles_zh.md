# 视觉风格库

HyperFrames 视频的可命名视觉身份。每种风格都植根于真实的平面设计传统，并表达为与 DESIGN.md 兼容的 token 块。可作为起点使用——将 YAML 复制到项目的 `design.md` front matter 中，再按需定制。

**如何挑选：** 先匹配情绪，再匹配内容。自问：_「观众应该感受到什么？」_

**如何使用：** 将风格的 YAML token 块复制到 `design.md` 的 front matter。补充 `## Overview`、`## Colors`、`## Typography`、`## Elevation`、`## Components`、`## Do's and Don'ts` 等 prose 章节以完成文件。

## 目录

- 快速参考
- Swiss Pulse
- Velvet Standard
- Deconstructed
- Maximalist Type
- Data Drift
- Soft Signal
- Folk Frequency
- Shadow Cut
- 情绪 → 风格指南
- 创建自定义风格

## 快速参考

| 风格            | 情绪                  | 最适合                             | 转场 shader                       |
| --------------- | --------------------- | ---------------------------------- | --------------------------------- |
| Swiss Pulse     | 冷静、精准            | SaaS、数据、开发工具、指标         | Cinematic Zoom 或 SDF Iris        |
| Velvet Standard | 高端、永恒            | 奢侈品、企业级、主题演讲           | Cross-Warp Morph                  |
| Deconstructed   | 工业感、粗粝          | 科技发布、安全、朋克气质           | Glitch 或 Whip Pan                |
| Maximalist Type | 张扬、动感            | 重大发布、产品上线                 | Ridged Burn                       |
| Data Drift      | 未来感、沉浸          | AI、ML、前沿科技                   | Gravitational Lens 或 Domain Warp |
| Soft Signal     | 私密、温暖            |  wellness 品牌、个人故事、品牌叙事 | Thermal Distortion                |
| Folk Frequency  | 文化感、鲜明          | 消费类应用、美食、社区             | Swirl Vortex 或 Ripple Waves      |
| Shadow Cut      | 暗调、电影感          | 戏剧化揭示、安全、调查类内容       | Domain Warp                       |

---

## 1. Swiss Pulse — Josef Müller-Brockmann

**情绪：** 冷静、精准 | **最适合：** SaaS 仪表盘、开发者工具、API、指标

```yaml
name: Swiss Pulse
colors:
  primary: "#1a1a1a"
  on-primary: "#ffffff"
  accent: "#0066FF"
typography:
  headline:
    fontFamily: Helvetica Neue
    fontSize: 5rem
    fontWeight: 700
  label:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
  stat:
    fontFamily: Helvetica Neue
    fontSize: 7rem
    fontWeight: 700
rounded:
  none: 0px
  sm: 2px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
motion:
  energy: high
  easing:
    entry: "expo.out"
    exit: "power4.in"
    ambient: "none"
  duration:
    entrance: 0.4
    hold: 1.5
    transition: 0.6
  atmosphere:
    - grid-lines
    - registration-marks
  transition: cinematic-zoom
```

网格锁定构图。每个元素对齐隐形的 12 栏网格。数字在 80–120px 尺度上主导画面。动画计数器从 0 递增。硬切，无装饰性转场。没有任何元素漂浮。

---

## 2. Velvet Standard — Massimo Vignelli

**情绪：** 高端、永恒 | **最适合：** 奢侈品、企业软件、主题演讲、投资人 deck

```yaml
name: Velvet Standard
colors:
  primary: "#0a0a0a"
  on-primary: "#ffffff"
  accent: "#1a237e"
typography:
  headline:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 300
    letterSpacing: 0.15em
    textTransform: uppercase
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 300
    lineHeight: 1.6
rounded:
  sm: 0px
  md: 2px
spacing:
  sm: 16px
  md: 32px
  lg: 64px
motion:
  energy: calm
  easing:
    entry: "sine.inOut"
    exit: "power1.in"
    ambient: "sine.inOut"
  duration:
    entrance: 1.2
    hold: 3.0
    transition: 1.5
  atmosphere:
    - subtle-grain
    - hairline-rules
  transition: cross-warp-morph
```

大量留白。对称、居中、建筑般的精确。细 sans-serif、全大写、宽字距。顺序揭示，长时间停留。没有任何元素猛跳——一切有意图地滑入。奢华感从不赶时间。

---

## 3. Deconstructed — Neville Brody

**情绪：** 工业感、粗粝 | **最适合：** 科技新闻、开发者发布、安全产品、朋克能量揭示

```yaml
name: Deconstructed
colors:
  primary: "#1a1a1a"
  on-primary: "#f0f0f0"
  accent: "#D4501E"
typography:
  headline:
    fontFamily: Space Grotesk
    fontSize: 4rem
    fontWeight: 700
  label:
    fontFamily: Space Mono
    fontSize: 0.75rem
    fontWeight: 700
    textTransform: uppercase
rounded:
  none: 0px
spacing:
  sm: 4px
  md: 12px
  lg: 24px
motion:
  energy: high
  easing:
    entry: "back.out(2.5)"
    exit: "steps(8)"
    ambient: "elastic.out(1.2, 0.4)"
  duration:
    entrance: 0.3
    hold: 1.0
    transition: 0.5
  atmosphere:
    - scan-lines
    - glitch-artifacts
    - grain-overlay
  transition: glitch
```

文字带角度、边缘重叠、溢出画框。粗工业字重。粗粝纹理：扫描线、glitch 伪影融入设计。文字猛砸、碎裂。字母乱序后定格到最终位置。刻意的不规则——不应显得过度精致。

---

## 4. Maximalist Type — Paula Scher

**情绪：** 张扬、动感 | **最适合：** 大型产品发布、里程碑公告、高能量造势视频

```yaml
name: Maximalist Type
colors:
  primary: "#0a0a0a"
  on-primary: "#ffffff"
  accent-red: "#E63946"
  accent-yellow: "#FFD60A"
typography:
  headline:
    fontFamily: Anton
    fontSize: 8rem
    fontWeight: 400
    textTransform: uppercase
  subhead:
    fontFamily: Space Grotesk
    fontSize: 3rem
    fontWeight: 700
rounded:
  none: 0px
spacing:
  sm: 0px
  md: 8px
motion:
  energy: high
  easing:
    entry: "expo.out"
    exit: "back.out(1.8)"
    ambient: "power3.out"
  duration:
    entrance: 0.3
    hold: 0.8
    transition: 0.4
  atmosphere:
    - type-layers
    - color-blocks
  transition: ridged-burn
```

文字即视觉。不同尺度与角度的字体层叠，占画面 50–80%。粗体饱和色——最大对比。一切充满动感：猛入、滑入、缩放。2–3 秒快切场景。无静态瞬间。快速入场、硬停。

---

## 5. Data Drift — Refik Anadol

**情绪：** 未来感、沉浸 | **最适合：** AI 产品、ML 平台、数据公司、 speculative tech 类内容

```yaml
name: Data Drift
colors:
  primary: "#0a0a0a"
  on-primary: "#e0e0e0"
  accent-purple: "#7c3aed"
  accent-cyan: "#06b6d4"
typography:
  headline:
    fontFamily: Inter
    fontSize: 2.5rem
    fontWeight: 200
    letterSpacing: 0.05em
  body:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 300
rounded:
  sm: 4px
  md: 12px
  full: 9999px
spacing:
  sm: 16px
  md: 32px
  lg: 64px
motion:
  energy: moderate
  easing:
    entry: "sine.inOut"
    exit: "power2.out"
    ambient: "sine.inOut"
  duration:
    entrance: 1.0
    hold: 2.5
    transition: 1.5
  atmosphere:
    - particle-field
    - light-traces
    - radial-glow
  transition: gravitational-lens
```

纤细的未来感 sans-serif——漂浮、失重、极简。流体变形构图。极端尺度切换（微观 → 宏观）。粒子聚合成数字。光迹在画面中描绘数据路径。平滑、连续、有机。没有任何硬边。

---

## 6. Soft Signal — Stefan Sagmeister

**情绪：** 私密、温暖 | **最适合：** wellness 品牌、个人故事、生活方式产品、以人为中心的应用

```yaml
name: Soft Signal
colors:
  primary: "#FFF8EC"
  on-primary: "#2a2a2a"
  accent-amber: "#F5A623"
  accent-rose: "#C4A3A3"
  accent-sage: "#8FAF8C"
typography:
  headline:
    fontFamily: Playfair Display
    fontSize: 3rem
    fontWeight: 400
    fontStyle: italic
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 300
    lineHeight: 1.7
rounded:
  sm: 8px
  md: 16px
  lg: 24px
  full: 9999px
spacing:
  sm: 12px
  md: 24px
  lg: 48px
motion:
  energy: calm
  easing:
    entry: "sine.inOut"
    exit: "power1.inOut"
    ambient: "sine.inOut"
  duration:
    entrance: 1.0
    hold: 3.0
    transition: 1.5
  atmosphere:
    - soft-gradient
    - warm-grain
  transition: thermal-distortion
```

手写风或 humanist serif 字体。个人化、小写、 delicate 笔触。特写构图：单一元素填满画面。缓慢漂移与漂浮，从不猛跳。柔和有机动效。不应显得匆忙或过度精致。私密感，从不带 corporate 腔调。

---

## 7. Folk Frequency — Eduardo Terrazas

**情绪：** 文化感、鲜明 | **最适合：** 消费类应用、美食平台、社区产品、节庆发布

```yaml
name: Folk Frequency
colors:
  primary: "#ffffff"
  on-primary: "#1a1a1a"
  accent-pink: "#FF1493"
  accent-blue: "#0047AB"
  accent-yellow: "#FFE000"
  accent-green: "#009B77"
typography:
  headline:
    fontFamily: Fredoka One
    fontSize: 4rem
    fontWeight: 400
  body:
    fontFamily: Nunito
    fontSize: 1rem
    fontWeight: 600
rounded:
  sm: 8px
  md: 16px
  lg: 32px
  full: 9999px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
motion:
  energy: high
  easing:
    entry: "back.out(1.6)"
    exit: "elastic.out(1, 0.5)"
    ambient: "sine.inOut"
  duration:
    entrance: 0.5
    hold: 1.5
    transition: 0.8
  atmosphere:
    - pattern-tiles
    - confetti-burst
    - color-blocks
  transition: swirl-vortex
```

粗体、温暖、圆角字体。图案与重复——民间艺术的节奏与密度。分层构图，丰富视觉纹理。每帧都像手工制作。 colorful 动效：元素弹入、弹出、旋转到位，充满喜悦。 overshoot 有意为之。节庆能量。

---

## 8. Shadow Cut — Hans Hillmann

**情绪：** 暗调、电影感 | **最适合：** 安全产品、戏剧化揭示、调查类内容、高强度发布

```yaml
name: Shadow Cut
colors:
  primary: "#0a0a0a"
  on-primary: "#f0f0f0"
  surface: "#3a3a3a"
  accent: "#C1121F"
typography:
  headline:
    fontFamily: Oswald
    fontSize: 4rem
    fontWeight: 700
    textTransform: uppercase
  body:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
rounded:
  none: 0px
  sm: 2px
spacing:
  sm: 8px
  md: 16px
  lg: 48px
motion:
  energy: moderate
  easing:
    entry: "power3.out"
    exit: "power4.in"
    ambient: "sine.inOut"
  duration:
    entrance: 0.8
    hold: 2.5
    transition: 1.2
  atmosphere:
    - deep-shadow
    - vignette
    - grain-overlay
  transition: domain-warp
```

近单色：深黑、冷灰、 stark 白，辅以一点 blood-red  accent。锐利棱角文字，如同 film noir 片头卡。强烈对比，无柔和过渡。元素从黑暗中浮现——揭示本身就是叙事。缓慢 creeping 推镜与 dramatic 尺度揭示。重击前的停顿至关重要。Domain Warp 在下一场景前溶解现实。

---

## 情绪 → 风格指南

| 若内容感觉...                      | 使用...         |
| ---------------------------------- | --------------- |
| 数据驱动、分析型、技术向           | Swiss Pulse     |
| 高端、企业级、奢华                 | Velvet Standard |
| 粗粝、朋克、 aggressive、 rebellious | Deconstructed   |
| 造势、 loud、高能量发布            | Maximalist Type |
| AI、ML、 speculative、 futuristic  | Data Drift      |
|  human、温暖、 personal、 wellness | Soft Signal     |
| 文化、趣味、消费、节庆             | Folk Frequency  |
| 暗调、 dramatic、 intense、电影感  | Shadow Cut      |

---

## 创建自定义风格

这 8 种风格是起点——不是限制。创建你自己的：

1. **命名**——以设计师、艺术运动或文化参照命名
2. **编写 YAML token**——`colors`（2–5 个 token）、`typography`（2–3 档尺度）、`rounded`、`spacing`、`motion`（energy + easing + duration + atmosphere + transition）
3. **补充 prose**——一段描述感受、该做什么、该避免什么
4. **Token 引用**——在组件定义中使用 `{colors.accent}`、`{typography.headline}`

模式：**YAML token（是什么）→ 说明性文字（为什么）→ components（如何组合）。**
