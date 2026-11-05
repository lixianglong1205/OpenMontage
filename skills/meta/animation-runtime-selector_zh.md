# 动画运行时选择器（Animation Runtime Selector）

元技能，用于回答两个问题：

1. **该视频应使用哪种合成运行时？** — Remotion、HyperFrames 或 FFmpeg。
2. **该场景应选用哪种动画库 / Layer 3 技能？** — Remotion 原语、GSAP 插件、framer-motion、Lottie、Manim、D3。

在编写任何动画组件或合成之前，以及在提案阶段选择 `render_runtime` 时，请先阅读本文。它会将你路由到正确的 Layer 3 技能，避免手搓插件已能解决的问题而浪费时间。

> **创作模式优先。** 在运行时或库之前，先决定合成*如何*构建：**模板化**（组装现成的 `cut.type` 场景）还是 **atelier**（从零手写）。英雄级作品默认 atelier，并遵循 `skills/meta/bespoke-composition.md`。以下路由在两种模式下均适用——但在 atelier 模式下，现成 scene-types 与 registry 块不可用，需自行编写。「是否有现成 cut-type 可用？」对英雄级作品**不是**有效捷径。见 `AGENT_GUIDE.md` →「Composition Authoring Mode」。

## 何时使用本技能

在以下情况应用：
- **提案阶段**需要锁定 `render_runtime`（remotion / hyperframes / ffmpeg）
- 某阶段导演（asset、edit、compose）需要编写动画组件
- 代理即将为涉及文字揭示、SVG 动效、曲线相机路径、形状变形或多段编排的场景编写 Remotion JSX
- 代理被要求构建 HyperFrames 合成
- 代理不确定该用 GSAP 插件还是内联 `interpolate()`/`spring()`

## 运行时选择（Remotion vs HyperFrames vs FFmpeg）

OpenMontage 将创作语法（`renderer_family`）与技术引擎（`render_runtime`）分离。二者在提案阶段锁定，并原样贯穿 `edit_decisions`。在 compose 阶段静默更换运行时是契约违规。

### 硬性规则 — 展示两种运行时，勿静默默认

当本机 Remotion 与 HyperFrames 均可用（查询 `video_compose.get_info()["render_engines"]`）时，代理**必须**在锁定 `render_runtime` 前向用户展示两种选项。下方决策矩阵是代理对话的输入，**不是**静默选择「默认」项的许可。完整契约见 `AGENT_GUIDE.md` →「Present Both Composition Runtimes」。

具体在提案阶段：

1. 查询 `video_compose.get_info()["render_engines"]`，确认本机可用运行时。
2. 若 Remotion 与 HyperFrames 均可用，向用户展示两者：针对简报的一句话描述、一句诚实的权衡、带理由的代理推荐。
3. 等待用户明确批准。
4. 在 `decision_log` 中记录，类别为 `render_runtime_selection`，且 `options_considered` 包含两种运行时。
5. 再将 `render_runtime` 写入 `proposal_packet.production_plan`。

当两种均可用但 `render_runtime_selection` 决策只考虑一种选项时，属于**严重**审查发现。

| 简报特征 | `render_runtime` | 阅读 |
|---|---|---|
| 现有 React 场景栈（text_card、stat_card、chart、caption overlay、TalkingHead、CinematicRenderer） | **remotion** | `skills/core/remotion.md` |
| 词级字幕烧录 / 卡拉 OK 字幕 | **remotion** | `skills/core/remotion.md` |
| 数字人 / 口型同步 / 主持人 | **remotion** | `skills/core/remotion.md` |
| Kinetic typography、HTML/GSAP 原生动效、产品 promo、发布 reel | **hyperframes** | `skills/core/hyperframes.md` + `.agents/skills/hyperframes/SKILL.md`（路由）→ `hyperframes-core`（契约）、`hyperframes-creative`（调色/字体）、`hyperframes-animation`（动效） |
| 网站 → 视频、UI 驱动合成 | **hyperframes** | `.agents/skills/website-to-video/SKILL.md`（0.7 中自 website-to-hyperframes 重命名） |
| 需要 registry 块（data-chart、grain-overlay、shader transitions 等） | **hyperframes** | `.agents/skills/hyperframes-registry/SKILL.md` |
| 可编辑、浏览器原生 3D 地形/世界与自由视点飞越 | **hyperframes** | `skills/creative/3d-world-generation.md` + `.agents/skills/threejs-world-generation/SKILL.md` |
| 参考级 Blender 渲染 3D 世界影片 | **ffmpeg 打包 Blender 帧** | `skills/creative/3d-world-generation.md` + `.agents/skills/3d-asset-generation/SKILL.md` |
| 节拍同步 MV（音频驱动场景时序） | **hyperframes** | `.agents/skills/music-to-video/SKILL.md` — 使用 `hyperframes beats` 检测 drop，在节拍网格上排布帧 |
| 将现有 Remotion 合成移植到 HyperFrames | **hyperframes** | `.agents/skills/remotion-to-hyperframes/SKILL.md` — 迁移指南，**仅**用于明确移植请求 |
| BGM / SFX / 图像 / 图标解析（任意流水线、任意运行时） | n/a | `.agents/skills/media-use/SKILL.md` — 对项目缓存 + 全局缓存 + HeyGen 目录使用 `resolve` 动词 |
| 短设计导向 motion graphic（下三分之一、数据揭示、logo sting、标题） | **hyperframes** | `.agents/skills/motion-graphics/SKILL.md` |
| 纯拼接 / 裁剪源片段，无需合成 | **ffmpeg** | `skills/core/ffmpeg.md` |
| 所选运行时不可用 | **升级处理** — 勿静默替换 | `AGENT_GUIDE.md` → Escalate Blockers |

完整 Remotion 与 HyperFrames 决策矩阵及 Phase 1 仍仅限 Remotion 的功能列表，见 `skills/core/hyperframes.md`。

## 动画库决策矩阵

| 动画需求 | 推荐运行时 | 优先阅读 |
|---|---|---|
| 简单淡入淡出 / 滑动 / 缩放 / spring | Remotion 原语（无插件） | `.agents/skills/remotion` |
| 带物理的双态 spring | Remotion `spring()` | `.agents/skills/remotion` |
| 带偏移的多步序列 | Remotion `Sequence` + `interpolate()` **或** GSAP timeline | `.agents/skills/remotion` + 可选 `.agents/skills/gsap-timeline` |
| 与旁白同步的逐词文字揭示 | Remotion `interpolate` 由词级 transcript 驱动（现有 `CaptionOverlay` 模式） | `.agents/skills/remotion` |
| 逐字符 kinetic typography（SplitText 风格） | Remotion 内 GSAP SplitText | `.agents/skills/gsap-plugins`（SplitText）、`.agents/skills/gsap-react` |
| 两路径间 SVG 形状变形 | Remotion 内 GSAP MorphSVG | `.agents/skills/gsap-plugins`（MorphSVG） |
| 沿自定义路径的曲线相机 / 物体运动 | Remotion 内 GSAP MotionPath | `.agents/skills/gsap-plugins`（MotionPath） |
| SVG 描边绘制 / stroke 揭示 | GSAP DrawSVG | `.agents/skills/gsap-plugins`（DrawSVG） |
| 定制 bezier / elastic / stutter 缓动 | GSAP CustomEase / EasePack / CustomWiggle | `.agents/skills/gsap-plugins` |
| 布局到布局过渡（FLIP） | Remotion 内 GSAP Flip | `.agents/skills/gsap-plugins`（Flip） |
| UI 动效的迪士尼 12 原则 | framer-motion + Lottie | `.agents/skills/framer-motion`、`.agents/skills/lottie-bodymovin` |
| 自 After Effects / Figma 导出 Lottie | Lottie | `.agents/skills/lottie-bodymovin` |
| 合成终端 / CLI 演示 | Remotion TerminalScene | `.agents/skills/synthetic-screen-recording` |
| 数学 / 科学可视化 | Manim | `.agents/skills/manim-composer`、`.agents/skills/manimce-best-practices` |
| D3 数据驱动可视化 | D3 | `.agents/skills/d3-viz` |
| 数据图表（柱/线/饼/KPI） | Remotion 内置 chart 组件 | `remotion-composer/SCENE_TYPES.md` |
| HyperFrames 合成 — 动效知识（规则、蓝图、过渡、运行时适配器） | HyperFrames + GSAP 默认 | `.agents/skills/hyperframes-animation`（整合动效技能）+ `.agents/skills/gsap-core`、`.agents/skills/gsap-timeline` |
| HyperFrames 合成结构（data-* 时序、轨道、子合成） | HyperFrames | `.agents/skills/hyperframes-core` |
| 显式 Three.js 世界（地形、区域、地标、相机路径） | HyperFrames + `threejs_world` | `.agents/skills/threejs-world-generation` |
| 详细 Blender 世界影片（生成/目录 mesh、PBR、相机路径） | Blender + FFmpeg 打包 | `.agents/skills/3d-asset-generation` |
| HyperFrames 创意方向（调色、字体、旁白、节拍规划） | HyperFrames | `.agents/skills/hyperframes-creative` |
| HyperFrames 音频/媒体（TTS、BGM、SFX、转写、字幕、抠背景） | HyperFrames | `.agents/skills/hyperframes-media` |
| HyperFrames 合成 CLI（lint/validate/inspect/snapshot/benchmark/render/lambda） | HyperFrames CLI 0.7+ | `.agents/skills/hyperframes-cli` |
| HyperFrames registry 块安装（`hyperframes add ...`） | HyperFrames registry | `.agents/skills/hyperframes-registry` |

## 「保持简单」倾向

在动用 GSAP 之前，先问：**Remotion 原语 API 能否在 ≤ 20 行内解决？**

- 淡入淡出/滑动/缩放/旋转 → `interpolate(frame, [inFrame, outFrame], [from, to])`
- 自然「弹跳」动效 → `spring({ frame, fps, config: { damping, stiffness } })`
- 词级字幕高亮 → 遍历 transcript，按 `frame / fps` 过滤

若可以，用 Remotion 原语；若不行，再升级到 GSAP 插件。

GSAP 是强力逃生舱，不是默认。每个插件都会增加 bundle 体积、注册样板，以及另一份要读的技能。

## 在 Remotion 内确定性运行 GSAP

标准 GSAP 依赖 `requestAnimationFrame` — 非确定性，开箱不兼容 Remotion。以下三种模式 Remotion 安全：

```jsx
// Pattern 1: paused timeline, seek by progress
const tl = useRef(gsap.timeline({ paused: true })).current;
useEffect(() => {
  tl.to('.x', { x: 500 }).to('.y', { opacity: 0 });
}, []);
tl.progress(frame / durationInFrames);

// Pattern 2: paused timeline, seek by time
tl.seek(frame / fps);

// Pattern 3: GSAP as value calculator only
const easeFn = gsap.parseEase('power2.out');
const t = frame / durationInFrames;
const easedValue = easeFn(t);
```

完整说明见 `.agents/skills/gsap-react/SKILL.md`。

## 对照流水线的阶段导演

每个流水线的 asset-director 都有动效相关指引。若你处于：
- **animated-explainer** → 读 `skills/pipelines/explainer/asset-director.md` — 含 kinetic typography 的 text/SVG 选项
- **animation** → 读 `skills/pipelines/animation/asset-director.md` — 含 logo/motion-graphics 的 MorphSVG 与 MotionPath
- **cinematic** → 读 `skills/pipelines/cinematic/asset-director.md` — 含电影感相机运动的 MotionPath

asset-director 告诉你在该流水线语境下*做什么*；本选择器告诉*怎么做*。

## 禁止事项

- ❌ 仅需淡入淡出/滑动的场景却引入 GSAP — 用 Remotion 原语。
- ❌ 在 Remotion 内用 `requestAnimationFrame` 跑 GSAP — 渲染将非确定性。
- ❌ 已指明插件却跳过对应 Layer 3 技能 — 各插件的 prompting 指引很重要。
- ❌ 在组件函数体内注册 GSAP 插件 — 在模块作用域或应用入口注册一次即可。
