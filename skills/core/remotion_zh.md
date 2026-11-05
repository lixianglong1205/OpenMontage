# Remotion 技能

## 何时使用

从 Phase 3 起，凡需高级视频合成——React 场景组装、参数化模板、动画叠加、转场或数据驱动批量渲染——请使用 Remotion。简单剪切、烧录与编码优先直接用 FFmpeg。

## 与 Remotion Agent Skills 的关系

**已安装的 agent skills**（`.agents/skills/remotion-best-practices/`）教授正确的 Remotion API 用法——导入、时序、动画约束与代码模式。
**本文件**说明 OpenMontage 如何使用 Remotion——哪些 composition 对应 pipeline 阶段、产物如何流入，以及如何触发渲染。

## Remotion 优先路由

**在可用时，Remotion 是所有最终渲染的默认合成引擎。**
它通过 `<OffthreadVideo>` 处理视频片段、静帧、动画场景、组件类型、转场与混合内容——均在单次基于 React 的渲染 pass 中完成。

FFmpeg 为**回退方案**——仅在 Remotion 不可用时使用，或用于不受益于 React 渲染的简单独立操作。

| 用例 | 后端 | 原因 |
|----------|---------|-----|
| 最终视频渲染（任意内容类型） | **Remotion** | 所有 composition 的默认选择 |
| 视频片段 + 动画静帧 + 文字卡片 | **Remotion** | 混合内容一次 pass |
| 仅视频剪切与转场 | **Remotion** | 原生 `<OffthreadVideo>` + 转场 |
| 动画图表/文字卡片 | **Remotion** | 逐帧控制 |
| 数据驱动批量视频 | **Remotion** | Zod props + 参数化渲染 |
| 词级字幕（在 composition 内） | **Remotion** | CaptionOverlay 词高亮——优于 SRT |
| 音频嵌入（旁白 + 音乐） | **Remotion** | 原生 `<Audio>` 组件，支持音量/淡入淡出 |
| 简单 trim、concat（无 composition） | FFmpeg | 即时，无 Node 依赖 |
| 字幕烧录（独立、事后） | FFmpeg | 仅用于向已渲染视频追加字幕而不重渲 |
| 人脸增强、调色 | FFmpeg | 基于滤镜、确定性 |
| Remotion 不可用 | FFmpeg | 自动回退 |

**注意：** `render` 操作默认自动路由到 Remotion。仅当未安装 Remotion 或 agent 显式调用 `operation='compose'` 做独立操作时才选 FFmpeg。agent 也可在 capability-extension 协议下即时编写自定义 Remotion composition，当现有 composition 无法覆盖布局时（例如自定义 PiP、分屏）。

## 支持的场景类型（Cut Types）

Explainer composition 支持以下 cut 类型：

| 类型 | 所需 Props | 最适合 |
|------|---------------|----------|
| `text_card` | `text` | 陈述、标题、收尾信息 |
| `stat_card` | `stat`，可选 `subtitle`、`accentColor` | 大数字、 impactful 指标 |
| `hero_title` | `text`，可选 `heroSubtitle` | 开场标题、 dramatic 揭示 |
| `callout` | `text`，可选 `title`、`callout_type`（info/warning/tip/quote） | 提示、引用、重要说明 |
| `comparison` | `leftLabel`、`rightLabel`、`leftValue`、`rightValue` | 前后对比、A/B、对决 |
| `bar_chart` | `chartData` [{label, value}]，可选 `title`、`chartAnimation` | 类别对比、排名 |
| `line_chart` | `chartSeries` [{label, data: [{x,y}]}]，可选 `title` | 趋势、时间序列、增长 |
| `pie_chart` | `chartData` [{label, value}]，可选 `donut`、`centerLabel` | 占比、构成 |
| `kpi_grid` | `chartData` [{label, value, prefix, suffix, change, icon}] | 仪表盘、 traction 指标 |
| `progress_bar` | `progress`（0-100），可选 `progressSegments` | 旅程可视化、完成度、堆叠指标 |
| `anime_scene` | `images`（1-4 路径），可选 `animation`、`particles`、`particleColor`、`particleCount`、`particleIntensity`、`vignette`、`lightingFrom`、`lightingTo` | 动漫/吉卜力风格场景：多图交叉淡入、镜头运动、粒子叠加 |

**图表动画：** `grow-up`、`slide-in`、`pop`（bar），`draw`、`fade-in`（line），`spin`、`expand`、`sequential`（pie），`count-up`、`pop`、`cascade`（kpi）

### Anime Scene — 多图交叉淡入 + 粒子

`anime_scene` 类型渲染 1–4 张图像，带平滑交叉淡入、电影感镜头运动与动画粒子叠加，从静帧营造动画感。

**镜头运动类型：** `zoom-in`、`zoom-out`、`pan-left`、`pan-right`、`ken-burns`、`drift-up`、`drift-down`、`parallax`、`static`

**粒子类型：** `fireflies`（漂浮金色光点）、`petals`（飘落樱花）、`sparkles`（闪烁星点）、`mist`（漂移雾层）、`light-rays`（丁达尔光）

**关键 prop：** `sceneDurationSeconds` 由 `SceneRenderer` 自动传入——这修复了 Remotion 常见陷阱：`useVideoConfig().durationInFrames` 返回的是整个 composition 时长，而非该场景 `<Sequence>` 的时长。

**多图交叉淡入数学：** 每张图均分时间段。图 N 的淡出与图 N+1 的淡入在 `crossfadeDur`（约 1.2s）内**重叠**，避免空帧。同一场景从同一视觉体系生成 2–3 张图，但按 beat 变化镜头、主体与光照。相近 seed 有助于 subtle 运动，又避免整段重复同一 prompt。

**参考 composition：** `remotion-composer/public/demo-props/mori-no-seishin.json` — 6 个 anime 场景、30 秒，含粒子、光照、叠加与环境音乐。

**风格 playbook：** `styles/anime-ghibli.yaml` — 吉卜力启发美学：色板、 typography、运动参数与 FLUX prompt 前缀。

**零 API Key 视频策略：** 当无图像或视频生成能力时，可完全用上述组件类型构建视频。精心编排的 hero_title → kpi_grid → bar_chart → comparison → stat_card → text_card 序列可产出 polished、专业视频，零外部依赖。

### 零 API Key 视频的验证公式

以下规则来自系统化渲染测试，可产出电影感结果：

**1. 每个视频坚持一种背景家族。** 使用与 playbook 或自定义 identity 一致的背景处理，而非强迫每条序列同一深色 dashboard 外观。
这可避免白↔深色的刺眼闪切，并让图表色更突出。
目标是视觉统一，而非强制深色主题。

**2. 扁平 props 格式。** 所有场景属性放在 cut 对象**顶层**（如 `cut.text`、`cut.chartData`），**不要**嵌套在 `props` 键下。

**3. KPI Grid 数据规则：**
- `value` 须为小而可读的数。组件自动格式化 ≥1M→「XM」、≥1K→「XK」。
  「81 亿」用 `value: 8.1, suffix: " Billion"`。勿用巨大原始数加 suffix。
- `change` 须为**数字**（如 `3.2`），不是字符串（**不要** `"+3.2%"`）。

**4. Comparison 与 Callout 主题：**
- `comparison` 接受 `backgroundColor`、`color`（文字色）以适配深色主题。
- `callout` 接受 `backgroundColor`，同时设置容器与卡片背景。

**5. 叠加层提升 polish。**
- `section_title` 叠加在叙事上分组场景（如「THE CRISIS」「THE DATA」）。
- `stat_reveal` 叠加在图表场景上浮动 dramatic 数字（如角落「10x」）。

**6. 场景节奏：** 每场景 4–6 秒，45–50 秒视频约 8–10 场景。图表动画至少留 4 秒完成。Hero title 仅需约 4 秒。

**7. 色板统一。** 选 4–5 种与主题相关的 accent 色，在图表、叠加与 accent 中一致使用。bar/pie/line 场景共用同一 `chartColors` 数组以保持视觉统一。

**参考 composition：** 见 `remotion-composer/public/demo-props/climate-dashboard.json` 作为金标准，及其他 demo 文件中的模式。

### 渲染前验证（强制）

**渲染前务必运行 `composition_validator`。** 可捕获：
- 缺失资源文件（图像、音频）导致渲染失败
- 旁白音频长于视频时长（音频被截断）
- 音乐短于视频（结尾静音）
- 无效 cut 时序（out ≤ in）

```python
from tools.analysis.composition_validator import CompositionValidator
result = CompositionValidator().execute({
    "composition_path": "path/to/composition.json",
    "assets_root": "remotion-composer/public",
})
# result.data["valid"] must be True before rendering
```

**音频时长对齐：**
- 生成 TTS 旁白后，工具返回 `audio_duration_seconds`。
- 若旁白超过视频时长：缩短脚本并重生成，或延长最后一场景。
- 用 `tools.analysis.audio_probe.probe_duration(path)` 检查任意音频时长。
- 音乐应 ≥ 视频时长；播放器通过 `fadeOutSeconds` 处理淡出。

## 架构

```
remotion-composer/
├── src/
│   ├── Root.tsx              # Composition 注册表
│   ├── compositions/         # 每个 pipeline 类型一个文件
│   │   ├── Explainer.tsx     # 生成的 explainer composition
│   │   ├── AnimatedScene.tsx # 单个动画场景
│   │   └── TitleCard.tsx     # 独立标题卡
│   ├── components/           # 可复用视觉积木
│   │   ├── Caption.tsx       # 字幕/ caption 渲染器
│   │   ├── DiagramOverlay.tsx
│   │   ├── ProgressBar.tsx
│   │   └── TransitionWrapper.tsx
│   └── styles/               # Tailwind + playbook 衍生样式
├── public/                   # 静态资源（字体、LUT）
├── package.json
├── remotion.config.ts
└── tsconfig.json
```

## Pipeline 集成

### 产物如何映射到 Remotion Props

| OpenMontage 产物 | Remotion Prop | 映射到 |
|---------------------|---------------|---------|
| `scene_plan.json` → `scenes[]` | `scenes` prop | `<TransitionSeries>` 子节点 |
| `scene.type` | 组件选择器 | `talking_head` → `<Video>`，`diagram` → `<DiagramOverlay>` 等 |
| `scene.start_seconds` / `end_seconds` | `from` / `durationInFrames` | `fps * seconds` 换算 |
| `scene.transition_in` / `transition_out` | `<TransitionSeries.Transition>` | `fade`、`slide`、`wipe` |
| `asset_manifest.json` → assets | `assets` prop | `staticFile()` 或绝对路径 |
| `style_playbook` | `theme` prop | 颜色、字体、动画曲线 |
| `edit_decisions.json` → cuts | `cuts` prop | 带 trim 的 `<Series>` + `<Video>` 片段 |
| `media_profile` | Composition 尺寸 | 来自 profile 的 `width`、`height`、`fps` |

### 渲染调用

编排器通过 CLI 调用 Remotion 渲染：

```bash
# Standard render (composition name is "Explainer", no entry point needed)
npx remotion render Explainer \
  --props="public/demo-props/my-video.json" \
  --output=output/final.mp4 \
  --codec=h264 --crf=18

# With specific media profile
npx remotion render Explainer \
  --width=1080 --height=1920 --fps=30 \
  --props="public/demo-props/my-video.json" \
  --output=output.mp4
```

**注意：** 不要指定 `src/index.ts` 作为入口——Remotion 自动发现 composition。composition 名称为 `Explainer`（不是 `ExplainerVideo`）。

在 Python 中，当 `backend="remotion"` 时通过 `subprocess` 从 `video_compose.py` 调用。

### 媒体 Profile 映射

| OpenMontage Profile | Remotion 配置 |
|--------------------|-----------------|
| `youtube_landscape` | `width: 1920, height: 1080, fps: 30` |
| `youtube_shorts` | `width: 1080, height: 1920, fps: 30` |
| `tiktok_vertical` | `width: 1080, height: 1920, fps: 30` |
| `instagram_reels` | `width: 1080, height: 1920, fps: 30` |
| `instagram_square` | `width: 1080, height: 1080, fps: 30` |
| `cinematic_wide` | `width: 2560, height: 1080, fps: 24` |

## 关键模式

### 场景计划到 Composition

`scene_plan.json` 中每个场景成为 `<TransitionSeries>` 的子节点：

```tsx
// Pseudocode — actual component in remotion-composer/src/compositions/Explainer.tsx
const Explainer: React.FC<ExplainerProps> = ({ scenes, theme, assets }) => {
  return (
    <TransitionSeries>
      {scenes.map((scene, i) => (
        <React.Fragment key={scene.id}>
          {scene.transition_in && (
            <TransitionSeries.Transition
              presentation={mapTransition(scene.transition_in)}
              timing={timing({ durationInFrames: 15 })}
            />
          )}
          <TransitionSeries.Sequence durationInFrames={secondsToFrames(scene)}>
            <SceneRenderer scene={scene} theme={theme} assets={assets} />
          </TransitionSeries.Sequence>
        </React.Fragment>
      ))}
    </TransitionSeries>
  );
};
```

### 用 calculateMetadata 动态时长

当 TTS 音频决定视频长度（生成的 explainer）时，使用 `calculateMetadata`：

```tsx
export const ExplainerVideo = {
  component: Explainer,
  calculateMetadata: async ({ props }) => {
    const totalDuration = props.scenes.reduce(
      (sum, s) => sum + (s.end_seconds - s.start_seconds), 0
    );
    return {
      durationInFrames: Math.ceil(totalDuration * props.fps),
      fps: props.fps,
      width: props.width,
      height: props.height,
    };
  },
};
```

### Style Playbook 到 Theme

Style playbook（`skills/styles/`）定义视觉参数。映射到 Remotion theme：

```tsx
// Derived from the style playbook YAML
const cleanProfessional = {
  background: "#FFFFFF",
  text: "#1A1A1A",
  accent: "#2563EB",
  fontFamily: "Inter",
  headingWeight: 600,
  transitionType: "fade",
  transitionDuration: 15, // frames
  animationEasing: "easeInOutCubic",
};
```

### 音频分层

旁白 + 背景音乐 + SFX 作为并行的 `<Audio>` 组件。

**音乐 offset 与循环：** `audio.music` 配置支持：
- `offsetSeconds` — 跳过安静前奏，从曲目高能段开始。可用 `tools/analysis/audio_energy.py` 自动找最优 offset。
- `loop` — 若音乐短于视频则循环。Remotion 原生支持。
- `fadeInSeconds` / `fadeOutSeconds` — 起止平滑音量 ramp。

```json
"audio": {
  "music": {
    "src": "project/music.mp3",
    "volume": 0.15,
    "offsetSeconds": 55,
    "loop": false,
    "fadeInSeconds": 2,
    "fadeOutSeconds": 3
  }
}
```

```tsx
<AbsoluteFill>
  <Audio src={narrationUrl} />
  <Audio src={musicUrl} volume={0.06} startFrom={offsetFrames} loop />
  {sfxCues.map(cue => (
    <Sequence key={cue.id} from={secondsToFrames(cue.time)}>
      <Audio src={cue.url} volume={cue.volume} />
    </Sequence>
  ))}
  {/* Visual layers */}
</AbsoluteFill>
```

### 成本追踪

Remotion 渲染 CPU 密集但 API 成本为 $0。通过 cost_tracker 追踪：
- `estimate`：基于 composition 时长 × 分辨率档位
- `reserve`：0（无 API 支出）
- `reconcile`：墙钟渲染时间，用于基准对比

## 关键约束

- **禁止 CSS 动画或 transition** — 无法正确渲染。所有运动用 `useCurrentFrame()` + `interpolate()`。
- **禁止 Tailwind 动画类** — `animate-*` 类会破坏基于帧的渲染。静态 Tailwind 工具类可用。
- **始终 clamp interpolate()** — 使用 `extrapolateLeft: 'clamp', extrapolateRight: 'clamp'`，防止值越过端点。
- **`useVideoConfig().durationInFrames` 返回的是 COMPOSITION 时长，不是 Sequence 时长** — 这是 Remotion 头号陷阱。若 composition 为 31s（930 帧）而场景的 `<Sequence>` 为 5s（150 帧），在该场景内 `durationInFrames` 仍返回 930。任何直接用 `durationInFrames` 的交叉淡入、镜头运动或时序逻辑都会严重错误。**修复：** 从父级传入 `sceneDurationSeconds` prop，在组件内计算 `effectiveDuration = Math.round(sceneDurationSeconds * fps)`。`AnimeScene` 组件实现了该模式。
- **需要 Node.js 18+** — 在最低系统要求中为可选，在推荐配置中为必需。
- **串行渲染，非并行** — 除非机器内存充足。每次渲染会 spawn 一个 Chromium 实例。

## 渲染后验证协议（所有 pipeline）

**每次 Remotion 渲染在向用户展示前必须验证。** 本协议适用于**所有** pipeline，不限 explainer。各 pipeline 的 compose-director 可扩展但**不得跳过任一步**。

**步骤 1：探测输出文件（门禁 — 阻塞后续步骤）：**
```bash
ffprobe -v quiet -print_format json -show_format -show_streams rendered_video.mp4
```
验证以下全部：
- [ ] 存在视频流，分辨率与 FPS 正确
- [ ] **存在音频流** — 若缺失，立即停止，修复音频配置并重渲
- [ ] 时长在目标 ±5% 内
- [ ] 文件大小合理（非 0 字节、非异常偏小）

**若缺少音频流，不要继续。** 表示旁白/音乐未嵌入。
最常见原因：音频源在外部混音但未传入 Remotion 的 `audio` prop。修复：在 composition props 中添加 `audio.narration` 与 `audio.music` 并重渲。

**步骤 2：** 在场景 midpoint 提取审阅帧并逐帧目视检查。

**步骤 3：** 用 WhisperX/transcriber 工具转写渲染视频的音频。
- 若返回 0 词 → 虽有流但无声 → 排查
- 若词数 < 脚本 80% → 音频被截断 → 排查
- 将最后转写词与脚本最后词对比

**步骤 4：** 向用户呈现结构化审阅：文件统计、音频验证结果、视觉发现与字幕状态，再宣告视频完成。

## 质量检查清单

- [ ] Composition 时长等于各场景时长之和减去转场重叠
- [ ] 所有 `staticFile()` 引用指向存在的资源
- [ ] 转场不截断内容（时序中计入重叠）
- [ ] **渲染输出含音频流**（ffprobe 确认 codec_type: "audio"）
- [ ] **旁白词经转写验证**（非仅假设 props 正确）
- [ ] 音频层与视觉场景同步
- [ ] 字幕/caption 渲染正确（优先 Remotion CaptionOverlay，而非 FFmpeg SRT）
- [ ] Theme 颜色与当前 style playbook 一致
- [ ] 输出分辨率与 FPS 符合目标 media profile
- [ ] 渲染无 Chromium 超时错误
- [ ] 最终输出在目标平台正常播放
- [ ] 含文字场景（CTA、标题）使用 Remotion text_card，**不要**用带文字的 AI 生成图
