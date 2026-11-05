# 动画与动态图形流水线

> 来源：School of Motion 课程、After Effects 文档、Remotion 文档、
> HyperFrames 文档、迪士尼动画 12 原则（Frank Thomas & Ollie
> Johnston）、Motion Design School、《动画师生存手册》（Richard Williams）

## 运行时选择 — Remotion 与 HyperFrames

OpenMontage 中的动画工作可在两种合成运行时之一上运行。二者均为
一等公民；选择是创意层面的，而非降级方案：

- **Remotion（基于 React）** — 当场景是 React 组件、使用现有
  chart/text-card/comparison/kpi 栈，或需要通过 `useCurrentFrame()` +
  `interpolate()` 做像素级精确帧插值时。数据密集型解说片的默认选择。
- **HyperFrames（HTML/GSAP）** — 当动效自然表达为 CSS + GSAP
  时间轴时： kinetic typography、产品宣传片、发布短片、
  网站/UI 驱动合成、registry-block 驱动场景。当 brief 以动态图形
  为主导且 `remotion-composer/` 中的场景库尚未覆盖目标观感时的默认选择。

完整决策矩阵见 `skills/core/hyperframes.md` 与
`skills/meta/animation-runtime-selector.md`。提案阶段选定的运行时须
锁定在 `edit_decisions.render_runtime`，并在 compose 全流程中保持不变。

## 速查卡

```
FRAME RATE:       30fps for web video | 24fps for cinematic feel | 60fps for UI/smooth motion
EASE DEFAULT:     easeInOutCubic (0.65, 0, 0.35, 1) — never use linear
TRANSITION:       0.5-1.0s between scenes
ANTICIPATION:     2-3 frames before main action
OVERSHOOT:        10-15% past target, settle back in 3-5 frames
HOLD FRAMES:      6-12 frames (0.2-0.4s) on key poses
COLOR:            Max 5 colors from playbook palette
EXPORT:           H.264 CRF 18-20 for web, ProRes 422 for editing
```

## 帧率选择

| 风格 | FPS | 适用场景 |
|-------|-----|-------------|
| **电影感动画** | 24 | 胶片感、角色动画、有机运动 |
| **Web/解说标准** | 30 | YouTube/Web 视频默认。OpenMontage 默认。 |
| **流畅 UI 动画** | 60 | 软件演示、UI 过渡、滚动 |
| **风格化/有限帧** | 12-15 on 2s/3s | 刻意卡顿、艺术选择 |

**OpenMontage 默认：** 30fps。Manim 以 60fps 渲染，再转码为 30fps，以便在交付帧率下获得更平滑的运动。

## 时间原则（应用于动态图形）

### 最重要的 4 条原则

| 原则 | 应用 | 时间 |
|-----------|------------|--------|
| **缓入缓出（Ease In/Out）** | 每次运动先慢后慢 | 使用 cubic 或 quart 缓动，勿用 linear |
| **预备动作（Anticipation）** | 主动作前短暂反向运动 | 2-3 帧（30fps 下约 66-100ms） |
| **过冲（Overshoot）** | 物体越过目标再弹回 | 越过目标 10-15%，3-5 帧内 settle |
| **舞台调度（Staging）** | 同一时刻只动一个元素 | 动画错开 3-6 帧 |

### 缓动曲线

| 曲线 | Cubic Bezier | 用途 |
|-------|-------------|---------|
| **easeOutCubic** | `(0.33, 1, 0.68, 1)` | 物体进入画面 |
| **easeInCubic** | `(0.32, 0, 0.67, 0)` | 物体离开画面 |
| **easeInOutCubic** | `(0.65, 0, 0.35, 1)` | 场景内位置变化 |
| **easeOutBack** | `(0.34, 1.56, 0.64, 1)` | 弹性 pop-in（活泼） |
| **easeOutElastic** | spring simulation | 抓眼球的揭示 |
| **linear** | `(0, 0, 1, 1)` | **勿用于运动** — 仅用于 opacity 或 color |

### 定格帧（Hold Frames）

运动完成后，**保持 pose**，再开始下一段动画：

| 场景 | 保持时长 |
|---------|--------------|
| 关键信息在屏 | 1.0-2.0s（依旁白而定） |
| 动画节拍之间 | 0.3-0.5s（30fps 下 8-15 帧） |
| 揭示之后 | 1.5-3.0s（让观众消化） |
| 快速过渡 | 0.1-0.2s（3-6 帧） |

## 场景过渡

| 过渡 | 时长 | 适用场景 |
|-----------|----------|-------------|
| **硬切（Hard cut）** | 即时 | 同一主题、不同角度/缩放 |
| **交叉叠化（Crossfade）** | 0.5-1.0s | 换题、柔和切换 |
| **划像/滑动（Wipe/slide）** | 0.5-0.8s | 顺序步骤、递进 |
| **推近（Zoom in）** | 0.8-1.2s | 深入细节 |
| **拉远（Zoom out）** | 0.8-1.2s | 展现更大图景 |
| **匹配剪辑（Match cut）** | 即时 | 相同形状/位置、不同内容 |
| **变形/变换（Morph/transform）** | 1.0-2.0s | 概念演变、前后对比 |

### 过渡规则

1. **过渡一致** — 选定 2-3 种类型，全片坚持使用
2. **过渡即语义** — 划像表示「下一步」，推近表示「更深细节」
3. **勿过度过渡** — 硬切最隐形、也最专业
4. **声先于画** — 过渡音效比画面变化早 10-20ms

## 动态图形构图

### 布局

- **三分法** — 焦点元素放在交点
- **视觉层级** — 最大/最亮元素 = 最重要
- **留白** — 四边至少 10% 边距（在 title-safe 内）
- **运动方向** — 左→右 = 前进/进展，右→左 = 后退/回溯

### 色彩

- **最多 5 色**，来自 style playbook 色板
- **1 个强调色** — 少量使用
- **背景** 应为饱和度最低的颜色
- **前景与背景对比度** 至少 3:1

### 错开与编排（Stagger and Choreography）

多元素入场时：
- 元素之间错开 **3-6 帧**（100-200ms）
- 成组元素从同一方向进入
- 使用 `LaggedStart`（Manim）或 Remotion 的 staggered `delay`，`lag_ratio=0.1-0.2`

## 导出设置

| 目标 | 编解码器 | 设置 |
|--------|-------|----------|
| YouTube/Web 成片 | H.264 | CRF 18-20, `-pix_fmt yuv420p`, `-movflags +faststart` |
| 剪辑中间文件 | ProRes 422 | 供进一步剪辑/合成 |
| 透明叠加层 | ProRes 4444 | 叠在其他素材上时 |
| GIF 预览 | GIF | 宽 480px，15fps，256 色 |

## 在 OpenMontage 中的应用

构建动画/动态图形内容时：

1. **以 30fps 渲染**（OpenMontage 默认）— Manim 60fps，再转码降帧
2. **勿用 linear 缓动** — 所有运动默认 `easeInOutCubic`
3. **多元素入场错开 100-200ms** — 不要同时全部揭示
4. **揭示后关键帧保持 1.0-2.0s**（与旁白同步）
5. **一致使用 2-3 种过渡** — 硬切 + 交叉叠化覆盖多数需求
6. **声先于画** — SFX 比过渡早 10-20ms（见 sound-design.md）
7. **色板最多 5 色** — 从 style playbook 强制执行
8. **重要运动加预备 + 过冲** 以提升精致感
9. **成片导出 H.264 CRF 18-20**，经 `video_compose`
