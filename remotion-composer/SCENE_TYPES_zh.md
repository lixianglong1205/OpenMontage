# Remotion Composer — 场景与叠加层速查表

`Explainer` 组合可接受的 `cut.type` 与 `overlay.type` 值的权威列表。每一行对应 `src/Explainer.tsx` 中的一条分发分支。

新增组件时，请在此文件与 `src/components/index.ts` 中一并登记。

---

## Cut 类型（`cut.type`）

| `type` | Component | Required fields | Common fields | Purpose |
|---|---|---|---|---|
| *(none — video)* | `OffthreadVideo` | `source`（mp4 路径） | `source_in_seconds`, `animation`（zoom-in, ken-burns）, `in_seconds`, `out_seconds` | 直接播放 MP4 片段 |
| *(none — image)* | `Img` | `source`（png/jpg 路径） | `animation`, `in_seconds`, `out_seconds` | 以 Ken Burns 效果播放静图 |
| `text_card` | `TextCard` | `text` | `fontSize`, `backgroundVideo`, `backgroundOverlay`, `color` | 大字号排版节拍 |
| `hero_title` | `HeroTitle` | `text` | `heroSubtitle`, `backgroundVideo`, `backgroundOverlay` | 标题/片尾卡 |
| `stat_card` | `StatCard` | `stat` | `subtitle`, `accentColor`, `backgroundVideo` | 单个醒目数字 |
| `callout` | `CalloutBox` | `text` | `callout_type`（info/warning/tip/quote）, `title`, `backgroundVideo` | 带要点的框式信息 |
| `comparison` | `ComparisonCard` | `leftLabel`, `leftValue`, `rightLabel`, `rightValue` | `title`, `backgroundColor` | 左右对比 |
| `bar_chart` | `BarChart` | `chartData` | `chartAnimation`, `showValues`, `showGrid`, `backgroundVideo` | 动画柱状图 |
| `line_chart` | `LineChart` | `chartSeries` | `chartAnimation`, `xLabel`, `yLabel`, `showMarkers` | 动画折线图 |
| `pie_chart` | `PieChart` | `chartData` | `donut`, `centerLabel`, `centerValue`, `showLegend` | 饼图 / 环形图 |
| `kpi_grid` | `KPIGrid` | `chartData` | `title`, `columns`, `chartAnimation` | 2–4 列 KPI 网格 |
| `progress_bar` | `ProgressBar` | `progress` | `progressLabel`, `progressColor`, `progressSegments` | 动画进度条 |
| `anime_scene` | `AnimeScene` | `images`（列表） | `particles`, `lightingFrom`, `lightingTo`, `vignette` | 静图动漫场景，含粒子与镜头运动 |
| **`terminal_scene`** | **`TerminalScene`** | **`steps`**（cmd/out/pause/pill 列表） | **`terminalTitle`, `prompt`, `accentColor`** | **合成终端动画 — 无需真实录屏。参见 [`.agents/skills/synthetic-screen-recording/SKILL.md`](../.agents/skills/synthetic-screen-recording/SKILL.md)** |
| **`screenshot_scene`** | **`ScreenshotScene`** | **`backgroundImage`**（`public/` 内路径）, **`screenshotSteps`**（叠加层列表） | **`screenshotSize`（自然像素宽/高）, `cursorStartAt`, `accentColor`** | **方案一合成 UI — 放入任意截图，在其上播放脚本化叠加（cursor, click_pulse, type_into, bubble_append, typing_dots, highlight_box, callout_balloon）。15–30 秒聚焦演示可与真实录屏难以区分。坐标相对于 contain-fit 矩形归一化（0–1）。参见 [`.agents/skills/synthetic-ui-recording/SKILL.md`](../.agents/skills/synthetic-ui-recording/SKILL.md)（规划中）。** |

---

## Overlay 类型（`overlay.type`）

| `type` | Component | Required fields | Common fields | Purpose |
|---|---|---|---|---|
| `section_title` | `SectionTitle` | `text` | `accentColor`, `position`（top-left 等） | 小节标签 |
| `stat_reveal` | `StatReveal` | `text` | `subtitle`, `accentColor`, `position` | 角落统计徽章 |
| `hero_title` | `HeroTitle`（作为 overlay） | `text` | `subtitle` | 全画幅标题叠加 |
| **`provider_chip`** | **`ProviderChip`** | **`providers`**（字符串列表） | **`cycleSeconds`, `position`, `accentColor`, `label`** | **轮播徽章，循环展示 provider 名称 — 用于 AI 生成动态场景，标明片段由哪个模型产出** |

---

## 新增场景类型

1. 在 `src/components/MyScene.tsx` 中创建 React 组件。使用 `interpolate(frame, [inFrame, outFrame], [from, to])` 与 `spring(...)` 实现动效。读取 `useCurrentFrame()` 与 `useVideoConfig()`。
2. 在 `src/components/index.ts` 中导出。
3. 在 `src/Explainer.tsx` 的 `Cut` 接口中增加对应 `type`（及新 prop 字段）。
4. 在 `SceneRenderer` 中增加分发分支：
   ```tsx
   if (cut.type === "my_scene" && cut.mySceneData) {
     return maybeWrapWithBg(<MyScene ... />);
   }
   ```
5. 在本文件中记录。这样后续 agent 才能发现该类型。

## 现有合成 UI 组件

目前仅有 `TerminalScene`。该模式可推广 — 若流水线需要，可考虑后续增加：

- `ChatTranscript` — Claude/Cursor/GPT 聊天气泡时间线，含打字动画
- `EditorScene` — VS Code 风格编辑器，语法高亮与光标移动
- `PrReview` — GitHub PR diff 视图，行内评论渐显
- `SlackThread` — Slack 线程，头像与反应弹出
- `TicketBoard` — Jira / Linear 卡片跨列移动

模式：参照 `TerminalScene.tsx` — `steps` 时间线原语列表、光标推进时长、基于 spring 的渐显，以及可选的非阻塞 pill/徽章。
