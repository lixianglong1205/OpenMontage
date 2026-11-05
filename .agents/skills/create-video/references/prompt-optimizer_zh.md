---
name: prompt-optimizer
description: 为 HeyGen Video Agent 撰写生产级提示词——从基础创意到完整艺术指导的分镜脚本
---

# Video Agent 提示词优化器

为 HeyGen Video Agent API 撰写有效提示词。基于 40+ 条已制作视频的模式总结。

**核心洞察：Video Agent 是 HTML 解释器。** 它原生渲染版式、字体与结构化内容。将 B-roll 描述为带动作动词的叠层文字动态图形（如「slams in」「types on」「counts up」）——而非版式规格（如「upper-left, 48pt」）。

## 参考文件

| 文件 | 何时加载… |
|------|-------------|
| [visual-styles.md](visual-styles.md) | 选择视觉风格（20 种风格及完整规格） |
| [prompt-examples.md](prompt-examples.md) | 从零撰写提示词（完整制作示例 + 模板） |

## 工作流：从简报到提示词

1. **收集数据** — 调研主题：网页搜索、API、内部文档。收集真实引语、数据、账号 handle
2. **提炼论点** — 不是清单，而是故事。*「X 正在发生，因为 Y——证据如下。」* 归纳为 3–5 个主题并构成叙事弧
3. **选择风格** — 情绪优先，内容其次。自问：*「观众应该感受到什么？」* 见 [visual-styles.md](visual-styles.md)
4. **撰写虚拟人** — 与内容情绪语境匹配的 thematic 着装。布景中加入品牌 logo 与内容相关道具（见下方虚拟人指南）
5. **提取关键文案** — 列出必须逐字出现的每个数字、引语、handle 与标签
6. **拆分为场景** — 一场景一概念。轮换场景类型。同一类型不可连续 3 场以上。至少 2 场纯 B-roll
7. **撰写旁白** — 旁白中数字拼写（如「one-point-eight-five million」），画面上用数字（如「1.85M」）。每场含 B-roll 在内都要有旁白
8. **为每场 B-roll 分层** — L1 背景、L2 主视觉、L3 辅助、L4 信息条、L5 特效。每个元素必须动起来
9. **添加音乐方向** — 参考艺人，描述能量曲线
10. **添加旁白风格** — 如何演绎：快/慢、何处停顿、各段情绪 register

## 提示词结构

每条生产级提示词遵循以下结构：

```
FORMAT:    What kind of video, how long, what energy
TONE:      Emotional register, references
AVATAR:    Detailed physical + environment description (60-100 words)
STYLE:     Named aesthetic with colors, typography, motion rules, transitions
CRITICAL ON-SCREEN TEXT:  Exact strings that must appear
SCENE-BY-SCENE:  Individual scene breakdowns with VO and layered visuals
MUSIC:     Genre, reference artists, energy arc
NARRATION STYLE:  How to deliver the voiceover
```

### FORMAT

```
FORMAT: 75-second high-energy tech daily briefing. Think: a creator who just got amazing news.
FORMAT: Bloomberg-style strategy briefing. 100-120 seconds. CEO-delivered.
```

### TONE

```
TONE: Confident, direct, data-backed. Highlights hit hard. Lowlights are honest — no spin.
TONE: Edgy, punk tech commentary. Vice News meets The Face magazine — raw, confrontational.
```

### CRITICAL ON-SCREEN TEXT

列出屏幕上必须出现的每条精确字符串。缺少此项时，Agent 可能概括、四舍五入数字或改写引语。

```
CRITICAL ON-SCREEN TEXT (display literally):
- "$141M ARR — All-Time High"
- "1.85M Signups — +28% MoM"
- Quote: "Use technology to serve the message, not distract from it." — Shalev Hani
- "@username" — exact social handle
```

### MUSIC & NARRATION

```
MUSIC: Driving electronic, heavy bass drops on key numbers. Run the Jewels meets
a tech keynote. Builds relentlessly, only softens for customer stories.

NARRATION STYLE: High energy throughout. Let numbers PUNCH — pause before big ones,
then deliver hard. Customer stories get warmth. The close should feel like a mic drop.
```

## 虚拟人描述指南

**虚拟人不是固定头像** — 像电影角色一样为每条视频设计。以服装设计师 + 布景设计师的视角思考。

### 主题着装规则

虚拟人的着装与环境必须与内容的情绪/文化语境一致：

| 内容类型 | 虚拟人设计 | 不要这样 |
|---|---|---|
| 春节 | 金绣红色旗袍，灯笼点亮的庭院 | 「穿西装的记者」 |
| 突发科技新闻 | 外勤记者，风吹头发，耳麦，城市天际线 | 「桌播主播」 |
| 睡眠科学 | 超大奶油色针织，盘腿坐在床上，暖色台灯 | 「实验室分析师」 |
| Reddit 社区 | 凌乱书桌，显示器上的 Reddit  alien，墙上 upvote 箭头 | 「棚内研究员」 |

### 应指定什么

| 元素 | 弱 | 强 |
|---------|------|--------|
| 服装 | "Business casual" | "Black ribbed merino turtleneck, high collar framing jaw" |
| 环境 | "An office" | "Glass-walled conference room. Whiteboard with hand-drawn tier pyramid" |
| 显示器内容 | "Computer screens" | "Monitor shows scrolling green terminal text and red security alerts" |
| 灯光 | "Well lit" | "Cool blue monitor glow from left, warm amber desk lamp from right" |

### 模板

```
AVATAR: [Clothing — fabric, color, fit, accessories, posture].
[Setting — specific props, brand logos, what's on the walls].
[Monitors/desk — content visible on screens, items on desk].
[Lighting — direction, color temperature]. [Mood of the space].
60-100 words. 3+ content-specific props. Brand elements visible.
```

## 场景类型

| 类型 | 格式 | 何时使用 |
|------|--------|-------------|
| **A-ROLL** | 虚拟人对着镜头说话 | 开场、核心洞察、CTA、情绪高点 |
| **FULL SCREEN B-ROLL** | 无虚拟人——仅动态图形 | 数据可视化、信息密度高的内容 |
| **A-ROLL + OVERLAY** | 分屏：虚拟人 + 内容 | 展示数据同时保持人物连接 |

**轮换是硬性要求。** 同一类型不可连续 3 场以上。每条提示词至少 2 场纯 B-roll。

**每场都有旁白。** 每场 B-roll 必须包含 `VOICEOVER:` 行。无声 B-roll = 成片缺陷。

### 场景结构

**A-ROLL:**
```
SCENE 1 — A-ROLL (10s)
[Avatar center-frame, excited, hands gesturing]
VOICEOVER: "The exact script for this scene."
Lower-third: "TITLE TEXT" white on blue bar.
```

**带分层的 B-ROLL：**
```
SCENE 2 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — motion graphic only]
VOICEOVER: "The exact script for this scene."
LAYER 1: Dark #1a1a1a background with subtle grid lines pulsing.
LAYER 2: "HEADLINE" SLAMS in from left in white Bold 100pt at -5 degrees.
LAYER 3: Three data cards CASCADE from right, staggered 0.3s.
LAYER 4: Bottom ticker SLIDES in: "supporting text scrolling continuously."
LAYER 5: Grid lines RIPPLE outward from impact point.
Hard cut.
```

**A-ROLL + OVERLAY：**
```
SCENE 3 — A-ROLL + OVERLAY (10s)
[SPLIT — Avatar LEFT 35%. Content RIGHT 65%. NO overlap.]
Avatar gestures toward content side.
VOICEOVER: "The exact script for this scene."
RIGHT SIDE: "HEADLINE" in cyan 60pt. Three stats COUNT UP below.
```

叠加场景中，虚拟人左右侧应交替出现。

## 视觉分层系统

将 B-roll 拆成 5 个叠层。这是动态图形场景最有效的手法。

| 层 | 用途 | 示例 |
|-------|---------|---------|
| **L1** | 背景 | 纹理表面、网格、渐变、色块 |
| **L2** | 主视觉 | 占据画面的主标题/数字 |
| **L3** | 辅助数据 | 卡片、统计、要点、次要信息 |
| **L4** | 信息条 | 滚动条、标签、来源、引语 |
| **L5** | 特效 | 粒子、故障、网格动画、环境动效 |

每场 B-roll：4 层以上。每个 overlay 内容侧：3 层以上。**每个元素必须动起来。**

## 动效词汇

### 高能量
| 动词 | 示例 |
|------|---------|
| **SLAMS** | `"$95M" SLAMS in from left at -5 degrees` |
| **CRASHES** | `Title CRASHES in from right, screen-shake on impact` |
| **PUNCHES** | `Quote card PUNCHES up from bottom` |
| **STAMPS** | `Data blocks STAMP in staggered 0.4s` |
| **SHATTERS** | `Text SHATTERS after 1.5s, revealing number underneath` |

### 中等能量
| 动词 | 示例 |
|------|---------|
| **CASCADE** | `Three cards CASCADE from top, staggered 0.3s` |
| **SLIDES** | `Ticker SLIDES in from right — continuous scroll` |
| **DROPS** | `"TIER 1" DROPS in with white flash` |
| **FILLS** | `Progress bar FILLS 0 to 90% in orange` |
| **DRAWS** | `Chart line DRAWS itself left to right` |

### 低能量
| 动词 | 示例 |
|------|---------|
| **types on** | `Quote types on word by word in italic white` |
| **fades in** | `Logo fades in at center, held for 3 seconds` |
| **FLOATS** | `Bokeh orbs FLOAT across frame at different speeds` |
| **morphs** | `Number morphs from 17 to 18.9` |
| **COUNTS UP** | `"1.85M" COUNTS UP from 0 in amber 96pt` |

## 转场类型

| 转场 | 能量 | 适合的风格 |
|------------|--------|---------------|
| Smash cut | 激进 | Deconstructed, Maximalist, Carnival Surge |
| White flash frame | 有力 | Deconstructed, Maximalist |
| Grid wipe | 系统化 | Swiss Pulse, Digital Grid |
| Hard cut | 干净 | Swiss Pulse, Shadow Cut |
| Liquid dissolve | 优雅 | Data Drift, Dream State |
| Slow cross-dissolve | 精致 | Velvet Standard |
| Pop cut / bounce | 趣味 | Play Mode, Carnival Surge |
| Snap cut | 紧迫 | Red Wire, Contact Sheet |
| Soft dissolve | 温暖 | Soft Signal, Warm Grain, Quiet Drama |
| Iris wipe | 怀旧 | Heritage Reel |

## 时长指南

| 内容类型 | 时长 |
|--------------|----------|
| 钩子/开场（A-roll） | 6–10 秒 |
| 数据密集的 B-roll | 10–15 秒（切勿 ≤5s——会导致黑场） |
| A-roll + Overlay | 8–12 秒 |
| CTA / 结尾（A-roll） | 6–8 秒 |

**常见成片长度：** 社交短片：30–45s（5–7 场）| 简报：60–75s（7–9 场）| 深度：90–120s（10–13 场）

**语速：** 约 150 词/分钟。计算：`words / 150 * 60 = seconds`

## 无效做法

以下模式往往效果很差：

**版式语言** — 屏幕坐标会导致 B-roll 空白/黑屏：
```
❌ "UPPER-LEFT: headline in 48pt Helvetica"
❌ "CENTER-SCREEN: display at coordinates (400, 300)"
✅ "135K" SLAMS in from left, white Impact 120pt, fills 40% of frame.
```

**只提艺术家名而无规格** — 「Ikko Tanaka style」对 Video Agent 无意义。应译为具体规则：
```
❌ "Use an Ikko Tanaka style"
✅ "Flat color blocks, maximum 3 colors per frame, 60% negative space, typography as primary element"
```

**把风格示例整段塞进提示词** — 风格库里的完整示例场景会干扰 Agent。用风格的 **规则**，不要用示例场景。

**强行缩短 B-roll（≤5 秒）** — 渲染时间不够。所有测过 5s B-roll 的视频都出现空白/黑屏。用 10–15s。

**内容是清单而非故事** — 「这里有 5 条推文」成片很平。始终综合成：*「X 正在发生，因为 Y——证据如下。」*

## 制作经验

### 风格表现（40+ 条视频）

| 排名 | 风格 | 优势 |
|------|-------|----------|
| 1 | Deconstructed (Brody) | 各主题最稳 |
| 2 | Swiss Pulse (Müller-Brockmann) | 数据密集内容最佳 |
| 3 | Digital Grid (Crouwel) | 科技主题强 |
| 4 | Geometric Bold (Tanaka) | 优雅通用 |
| 5 | Maximalist Type (Scher) | 高能量，慎用 |

### 按方法的时长

| 方法 | 平均时长 | 质量 |
|----------|-------------|---------|
| 自然分镜 + 定制虚拟人 | ~106s | 最佳 |
| 自然分镜，无定制虚拟人 | ~69s | 良好 |
| 强行短场景 + 定制虚拟人 | ~71s | 参差 |
| 版式语言提示词 | ~48s | 差 |

## 质量检查清单

- [ ] 论点驱动——是故事，不是 bullet points
- [ ] 风格具名，含颜色、字体、动效、转场（见 [visual-styles.md](visual-styles.md)）
- [ ] 虚拟人有主题着装 + 品牌环境（60–100 词）
- [ ] 列出关键文案——每条数据、引语、标签
- [ ] 场景类型轮换——同一类型不可连续 3 场。至少 2 场 B-roll
- [ ] 每场有 VOICEOVER——含 B-roll
- [ ] B-roll 4 层以上，每个元素有动效动词
- [ ] B-roll 10–15 秒（切勿 ≤5s）
- [ ] 谈到公司时出现品牌 logo
- [ ] 每个元素都在动——无静态帧
