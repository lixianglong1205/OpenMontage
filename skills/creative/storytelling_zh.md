# 解说类视频的叙事与结构

> 来源：YouTube Creator Academy、Derek Muller 博士论文（悉尼大学，2008）、Kurzgesagt 制作
> 方法论（Philipp Dettmer）、3Blue1Brown（Grant Sanderson）、Richard Mayer《多媒体学习》
>（Cambridge UP，2001/2020）

## 解说弧模板

适用于 **3 分钟解说视频**（其他时长按比例缩放）：

```
[0:00 - 0:08]  HOOK
               Pattern interrupt or counterintuitive claim. 1-2 sentences max.
               Visual: striking image or animation that creates curiosity.

[0:08 - 0:30]  TENSION / INFORMATION GAP
               "Here's what most people think... but that's not quite right."
               Establish stakes: why should I care?
               Visual: show the misconception or the puzzle.

[0:30 - 0:50]  CONCEPT 1 (Foundation)
               Simplest building block needed. ONE idea, ONE visual.
               End with a "but" or "therefore" transition.

[0:50 - 1:15]  CONCEPT 2 (Complication)
               Build on Concept 1. Introduce the wrinkle.
               Visual: transform/evolve the previous visual.

[1:15 - 1:20]  PALETTE CLEANSER
               Brief pause, visual gag, or "let that sink in" moment.
               Gives working memory a beat to consolidate.

[1:20 - 1:50]  CONCEPT 3 (Key Insight)
               The "aha" moment. Core of the video.
               1-3 seconds of deliberate silence after the reveal.
               Visual: the most polished animation in the video.

[1:50 - 2:20]  PROOF / EXAMPLE
               Concrete demonstration: "Watch what happens when..."
               Visual: show the insight working in a specific case.

[2:20 - 2:45]  IMPLICATIONS / "SO WHAT?"
               Connect back to the real world. "This means that..."
               Scale from specific back to general.

[2:45 - 3:00]  REFRAME + CLOSE
               Callback to the hook. Restate the core insight in one sentence.
               Optional: open a new curiosity gap.
```

## 按时长缩放

| 时长 | 概念数 | Hook | Tension | Core | Proof | Close |
|--------|----------|------|---------|------|-------|-------|
| 1 分钟 | 1-2 | 5s | 10s | 30s | 10s | 5s |
| 2 分钟 | 2-3 | 8s | 15s | 60s | 25s | 12s |
| 3 分钟 | 3-5 | 8s | 22s | 100s | 30s | 15s |
| 5 分钟 | 5-8 | 10s | 30s | 180s | 50s | 20s |

## 反主观规则

> OpenMontage 脚本中的 Hook、节拍与段落描述必须说明情绪的**视觉成因**，而不是情绪本身。CMU/Harvard CHAI 研究表明，主观措辞在标注者与模型解读之间差异极大——因此它无法约束像素，也无法可靠地指导下游生成工具。
>
> | 避免 | 改用 |
> |---|---|
> | "epic reveal" | "wide aerial pull-back; subject silhouetted against rising sun" |
> | "inspiring moment" | "low angle on the subject's face; light catches the edge of a tear" |
> | "moody atmosphere" | "low-key key light, lifted shadows by 2 stops, fog volumetrics" |
> | "powerful music swell" | "music drops out at 0:42, holds 1.5s of silence, returns with low taiko at half tempo" |
>
> 该规则适用于脚本旁白以及 scene-director 所消费的元数据字段。命名这些视觉原语的通用词汇表见 `skills/creative/video-gen-prompting.md`。

## 脚本中的主体过渡

当脚本节拍引入新主体、移除旧主体，或将焦点从一方交给另一方时，**明确写出过渡类型**，以免 scene-director 需要自行推断。CMU/Harvard 分类法使用四种标签：

| 标签 | 含义 |
|---|---|
| **revealing** | 新主体进入画面或被揭示（门打开、镜头摇到发现、雾散开）。 |
| **disappearing** | 既有主体离开画面或被移除（走出、淡出、被遮挡）。 |
| **switching** | 焦点从主体 A 跳到主体 B（切镜、跟焦、甩镜）。 |
| **complex-alternating** | 同一节拍内多个主体反复交替焦点（辩论交叉剪辑、群戏动作）。 |

在节拍中用 1–2 句描述机制（切镜、摇镜、光线揭示等）。这会作为过渡原语写入 scene_plan。

## Hook 类型

| 类型 | 模式 | 最适合 |
|------|---------|----------|
| **Contrarian** | "Everything you've been told about X is wrong." | Veritasium 式科学/辟谣 |
| **Outcome** | "By the end of this video, you'll understand X." | 3Blue1Brown 式数学/概念 |
| **Mystery** | "In 1987, something impossible happened..." | Kurzgesagt 式故事驱动 |
| **Stakes** | "This one mistake costs people X every year." | 实用/操作类内容 |

## 30 秒规则

YouTube 数据显示 **50% 的观众流失发生在前 30 秒**。Hook 与张力铺垫必须在第 30 秒前完成。能撑过 30 秒悬崖的留存曲线，通常可保留 40–60% 观众看完整支视频。

## 「But-Therefore」方法

段落之间不要用「and then（然后）」连接，始终用 **「but（但是）」** 或 **「therefore（因此）」**。

**差：** "Atoms have electrons, AND THEN those electrons have energy levels, AND THEN..."

**好：** "Atoms have electrons, BUT they don't behave like tiny planets, THEREFORE we need a
completely new model..."

应用结构：
```
SETUP:     Here's what you think you know about X.
BUT:       Here's why that's wrong / incomplete / surprising.
THEREFORE: We need to understand Y (the real mechanism).
BUT:       Y creates a new puzzle...
THEREFORE: The actual answer is Z.
THEREFORE: This changes how you should think about X.
```

## 误区优先法（有研究支撑）

Derek Muller 的博士研究（悉尼大学，2008）表明：**先呈现常见误区再驳斥的视频，学习效果显著优于**只呈现正确信息的视频。观看「误区优先」视频的受试者在后测中得分更高，并报告更高的参与度。

应用方式：在揭示真相之前，先考虑从观众*以为*正确的内容开场。

## 引导式发现（3Blue1Brown 方法）

不要直接给出答案。**重建推理路径**，让观众感觉是自己发现的。

1. **The Question** — 提出一个具体、可感知的问题
2. **The Naive Attempt** — 展示显然的做法；让它部分成立，再让它失效
3. **The Key Insight** — 引入一个新想法。视觉上暂停 2–3 秒静音。
4. **The Build** — 逐步应用该洞见。每一步都应显得顺理成章。
5. **The Generalization** — 「注意这个模式不只适用于我们的具体例子……」

**渐进揭示：** 不要一次展示全貌。逐层构建画面，每一层在旁白提到它时才出现。

## 每个节拍的镜头意图

写节拍时附一行镜头意图，以免 scene-director 从空白开始臆造。使用 `skills/creative/video-gen-prompting.md` 中的通用词汇（Subject / Subject Motion / Scene / Spatial Framing / Camera）。一行即可——scene-director 会展开成完整规格。

示例节拍：

```
[0:30] Concept 1 — atoms aren't tiny planets
Narration: "We grew up imagining electrons as tiny planets orbiting the nucleus..."
Camera intent: medium shot of stylized atom; slow rotation; deep focus.
```

镜头意图行会被 scene-director 的五维规格原样消费——保持具体，不用情绪形容词。

## 节奏规则

| 规则 | 数值 | 来源 |
|------|-------|--------|
| 旁白语速 | 150-160 wpm | Kurzgesagt 标准（日常对话约 170-190） |
| 新视觉元素 | 每 3-5 秒 | Kurzgesagt 制作规范 |
| 概念密度 | 每 30-45 秒最多 1 个新概念 | Mayer 分段原则（Segmenting Principle） |
| 模式打断 | 每 45-90 秒 | YouTube 留存数据 |
| 刻意静音 | 关键洞见后 1-3 秒 | 3Blue1Brown 手法 |
| 调色板重置 | 每 45-60 秒 | Kurzgesagt 制作规范 |

## Mayer 多媒体学习原则（应用版）

以下是认知科学中最相关、有研究支撑的规则：

1. **Segmenting（分段）** — 每 30–45 秒最多 1 个新概念。3 分钟视频 = 4–6 个概念段。
2. **Signaling（信号）** — 每 30–45 秒使用口头路标（「有趣的地方来了」）。
3. **Temporal Contiguity（时间邻近）** — 旁白与画面必须同步。即使错开几秒，学习效果也会下降约 30%。
4. **Coherence（连贯）** — 去掉有趣但无关的内容。「诱人细节」会使迁移测试学习效果降低 20–30%。
5. **Modality（模态）** — 使用旁白（音频）+ 画面（动画），而非屏幕文字 + 画面。口语 + 图优于文字 + 图。

## 在 OpenMontage 中的应用

为动画解说流水线编写 **script artifact** 时：

1. 根据主题从上表选择 Hook 类型
2. 用解说弧模板组织段落
3. 段落之间使用「but-therefore」连接
4. 科学/技术类主题考虑误区优先法
5. 在脚本中设置 `narration_wpm: 155` 以计算准确时长
6. 在 scene_plan 中规划每 3–5 秒一次视觉变化
7. 在脚本中标记关键洞见的「silence」节拍
8. 校验：总概念数不应超过上表缩放上限
