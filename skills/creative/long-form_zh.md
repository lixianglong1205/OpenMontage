# 长视频制作流程（10 分钟以上）

> 来源：YouTube Creator Academy、VidIQ 数据分析研究、Think Media 制作指南、
> Paddy Galloway 留存分析、Retention Rabbit 2025 基准报告、AIR Media-Tech
> 留存剪辑指南、Epidemic Sound 混音指南、Sweetwater YouTube 母带处理

## 速查卡

```
DURATION:         8-15 min (sweet spot for most topics)
HOOK:             Complete by 0:30 — survive the 30-second cliff
PATTERN INTERRUPT: Every 45-90 seconds
RETENTION TARGET:  40-60% average view duration
CHAPTER LENGTH:    2-4 minutes per chapter
NARRATION:        150-160 WPM
MUSIC BED:        Continuous, ducked 18-20 dB below speech
TARGET LUFS:      -14 LUFS integrated
END SCREEN:       Last 20 seconds (YouTube end screen cards)
```

## 留存基准（2025–2026 数据）

| 视频时长 | 良好留存 | 优秀留存 |
|---------------|---------------|-------------------|
| 1-3 min | 60%+ | 75%+ |
| 3-5 min | 50%+ | 65%+ |
| 5-10 min | 45%+ | 60%+ |
| **10-20 min** | **40%+** | **55%+** |
| 20-60 min | 35%+ | 50%+ |

- 平台平均：所有 YouTube 视频 **23.7%**
- 仅 **16.8%** 的视频留存超过 50%
- 仅 **16%** 的观众能看到最后 10 秒
- **留存率每提高 10 个百分点**，与展示量 **25%+** 的增长相关

### AI 生成内容警示

- AI 生成视频相较真人出镜内容的留存 **低 70%**
- AI 旁白相较真人旁白，前 45 秒内 **35%** 观众流失
- **对 OpenMontage 的启示：** 优先选用听感自然的 TTS（ElevenLabs 优于 Piper），并避免可识别的 AI 视觉瑕疵。`sound-design.md` 中的处理链必不可少。

## 留存曲线管理

### 关键节点

| 时间戳 | 发生什么 | 如何撑住 |
|-----------|-------------|----------------|
| 0:00-0:03 | 缩略图与视频是否一致 | 首帧必须兑现缩略图承诺 |
| 0:00-0:30 | **前 60 秒内 55%+ 离开** | 钩子 + 张力须在 0:30 前完成。此处须留住 70%+。 |
| 2:00-3:00 | **留存低谷** — 初始好奇已消耗 | 在 2:00 前交付第一个主要回报，1:45 处做模式打断 |
| 55-65% 进度 | 长视频的 **二次流失** | 用 burst 序列 + 开放环闭合重新拉回 |
| 最后 20s | 片尾画面机会 | CTA + 片尾卡片 |

### 撑过 2–3 分钟低谷的战术

1. **前 60 秒埋开放环** — 早提问题，答案留到后面
2. **2:00 前第一个主要回报** — 钩子承诺须有「首付」
3. **1:45–2:00 模式打断** — 机位变化、B-roll 爆发、音乐切换
4. **低谷处的「burst 序列」** — 5–10 个快切持续 10–15 秒，再回到平静
5. **预告线索** — 「但真正让人惊讶的部分，一分钟后就到」

### 模式打断（Pattern Interrupts）

每 **60–90 秒** 部署 **大打断**，每 **20–30 秒** **小打断**：

| 手法 | 类型 | 使用时机 |
|-----------|------|-------------|
| B-roll 切镜 | 小 | 每 30–60 秒口播 |
| 视觉风格变化 | 大 | 新章节、新概念 |
| 屏幕文字/图形 | 小 | 关键数据、定义、强调 |
| 音乐能量变化 | 大 | 章节过渡 |
| 直接对镜头 | 小 | 「有意思的是……」 |
| Burst 序列（5–10 快切） | 大 | 每 2–3 分钟 |
| 音效 | 小 | 转场 whoosh、文字 pop |

**影响：** 前 5 秒使用模式打断的视频，平均留存 **高 23%**。

### 再钩子（Re-Engagement Hooks）

在 **2 分钟** 处及之后每 **3–4 分钟** 放置 **再钩子**：

```
"But that's not even the interesting part..."
"Now here's where it gets weird..."
"Most people stop here, but if you keep watching..."
"This next part changes everything..."
```

这些口头路标给观众理由看完下一段。

## 内容结构

### 章节模板

```
[INTRO]        0:00 - 0:30    Hook + stakes + preview
[CHAPTER 1]    0:30 - 3:00    Foundation concept
[RE-HOOK]      3:00 - 3:15    Curiosity gap for next section
[CHAPTER 2]    3:15 - 6:00    Complication / deeper layer
[PALETTE CLEANSER]  6:00 - 6:15    Visual break, humor, or "let that sink in"
[CHAPTER 3]    6:15 - 9:00    Key insight / "aha" moment
[PROOF]        9:00 - 10:30   Demonstration / example
[CONCLUSION]   10:30 - 11:30  Implications + reframe
[OUTRO]        11:30 - 12:00  CTA + end screen
```

### 章节长度规则

| 章节内容 | 理想时长 | 说明 |
|----------------|-------------|-------|
| 简单概念 | 2-3 minutes | 一个想法、一套视觉 |
| 复杂概念 | 3-4 minutes | 多步骤，需要示例 |
| 演示 | 2-3 minutes | 展示，而非只讲 |
| 故事/叙事 | 3-5 minutes | 需要铺垫 + 回报 |

10–15 分钟视频 **最多 5–6 章**。章节过多 = 过于碎片化。

### YouTube 章节（时间戳）

在描述中加入章节标记：
```
0:00 Introduction
0:30 Why This Matters
3:15 The Key Mechanism
6:15 The Breakthrough
9:00 Real-World Example
10:30 What This Means For You
```

章节改善导航，让观众跳到相关段落，可提升留存。

## 音频一致性

### 音乐床（Music Bed）管理

| 规则 | 数值 |
|------|-------|
| 音乐存在 | 全程连续（无静音空档） |
| 口播时 duck | 比旁白低 -18 至 -20 dB |
| 音乐过渡 | 章节间 2–3 秒交叉淡化 |
| 能量匹配 | 章节边界切换音乐能量 |
| BPM 一致 | 全片 ±10 BPM 内 |

### 长时长的 LUFS

- 目标：**-14 LUFS integrated**（YouTube 标准）
- 动态范围：口播为主内容 **6–12 dB**
- 按章节检查 LUFS — 章节间差异应 **< 2 LUFS**
- 终混使用 **-1.5 dBTP** 限制器

### 旁白节奏

| 段落 | WPM | 能量 |
|---------|-----|--------|
| Hook | 160-170 | 高能量、紧迫 |
| 讲解 | 150-160 | 稳定、清晰 |
| 关键洞见 | 140-150 | 更慢、刻意 |
| 揭示后静音 | 0 WPM（暂停 1–3s） | 让信息落地 |
| 结论 | 155-165 | 有力、收束 |

## 视觉节奏

### 各阶段切镜频率

| 阶段 | 时间 | 切镜间隔 | 说明 |
|-------|--------|-------------|-------|
| Hook | 0:00-0:30 | 每 3–5s | 快变传递动势 |
| 前段主体 | 0:30-3:00 | 每 10–15s | 高能量、频繁 B-roll |
| 中段主体 | 3:00-7:00 | 每 15–25s | 稳定；切镜少，情境 B-roll 多 |
| 后段主体 | 8:00+ | 15–25s 平静 + burst 序列 | 平静与每 2–3 分钟 5–10 快切 burst 交替 |

### B-Roll 策略

- **单条 B-roll 时长：** 5–8 秒
- **B-roll 占全片比例：** 教育类 **35–50%**
- **观看时长影响：** 35–50% 策略性 B-roll 使观看时长 **+15–25%**
- **镜头吸收时间：** 观众约需 3 秒；超过 5 秒无变化，注意力下降

### 「必须有变化」规则

| 规则 | 数值 |
|------|-------|
| 视/听变化 | 每 3–5 秒 |
| 实质性画面变化 | 每 20–30 秒 |
| 无任何变化上限 | 15 秒（超过预期流失） |

## 片尾画面与卡片

### 片尾画面（最后 20 秒）

- YouTube 允许在 **最后 5–20 秒** 放置片尾元素
- 包含：订阅按钮、下一条推荐、播放列表链接
- **勿在最后 20 秒放关键内容** — 会被遮挡
- 口头 CTA：「若觉得有用，可以看下这条关于……的下一支视频」

### 信息卡片

- 在提到相关话题时放置
- 每 2 分钟最多 1 张 — 过多显得骚扰
- 最佳时机：引用另一支视频已讲过的概念时

## 在 OpenMontage 中的应用

制作长视频时：

1. **按章节结构** — 每章 2–4 分钟，最多 5–6 章
2. **0:30 前完成 hook** — 遵循 `storytelling.md` 的 Explainer Arc 模板
3. **2:00–3:00 再钩子** — 留存低谷区
4. **每 45–90 秒模式打断** — B-roll、文字叠加、视觉变化
5. **连续音乐床** — 用 `music_gen` 生成全长轨，duck 18–20 dB
6. **旁白 150–160 WPM** — 比短视频慢，利于学习理解
7. **按章节查 LUFS** — 应一致（变化 < 2 LUFS）
8. **预留最后 20 秒** 给片尾 — 不放必要内容
9. **加章节时间戳** — 发布阶段元数据
10. **目标平均观看时长 40–60%** — 任一点留存低于 30%，该段需模式打断

## 时间备忘（12 分钟视频）

```
0:00-0:03   Visual hook (most compelling shot)
0:03-0:08   Verbal hook (promise/question)
0:08-0:15   Stakes ("here's why this matters")
0:15-0:30   Value preview + open loop planted
0:30-0:35   Branded intro (5 sec max)
0:35-1:45   Body segment 1 (high energy, cuts every 10-15s)
1:45-2:00   Pattern interrupt to bridge retention valley
2:00-3:00   First major payoff delivered
3:00-3:05   Chapter 2 mini-hook + bridging sentence
3:00-5:30   Body segment 2 (stabilized pacing, 15-25s cuts)
~5:00       Mid-roll CTA (subscribe ask, after earning value)
5:30-8:00   Body segment 3 (B-roll heavy, callbacks)
7:00-7:15   Burst sequence (5-10 quick cuts to re-engage)
8:00-10:00  Body segment 4 (mix calm + energy bursts)
9:30        Open loop resolution / major callback payoff
10:00-11:20 Final segment + main reveal
11:00       Card placement (last 20% of video)
11:20-11:40 Outro: tease next content, do NOT say goodbye
11:40-12:00 End screen (last 20 seconds), 1-2 elements
```
