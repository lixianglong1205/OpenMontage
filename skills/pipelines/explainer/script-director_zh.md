# Script Director — 解说类 Pipeline

## 何时使用

你是生成式解说视频的脚本撰写者。你手头有来自 Idea Explorer 的 `brief` 产物。你的任务是从零撰写旁白脚本——没有现成素材可转录。

脚本是视频的骨架。每一个画面、每一个场景、每一条音频提示都源于你在此写下的内容。平庸的脚本无法靠出色的视觉补救。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | 产物校验 |
| 前置产物 | `proposal_packet` | 已选概念：标题、hook、key_points、core_message、tone、narrative_structure、duration |
| 前置产物 | `research_brief`（可选但价值高） | 数据点、受众洞察、专家引语——用真实事实支撑脚本 |
| Playbook | 来自 `proposal_packet.selected_concept.suggested_playbook` 的活跃风格 playbook | 嗓音风格、节奏规则 |
| Meta skill | `skills/meta/voice-performance-director.md` | 结构化 TTS 演绎提示，实现自然、有表现力的旁白 |
| Layer 3 | TTS 提供商技能（查看所选 TTS 工具的 `agent_skills`） | TTS 能力与说话人指导 |

## 流程

### 步骤 1：吸收提案与研究

仔细阅读 `proposal_packet.selected_concept`。提取：
- **目标时长** — 这是你的字数预算（见下方节奏表）
- **Hook** — 开场必须兑现这一承诺
- **Key points** — 脚本中必须全部覆盖
- **Core message** — 观众应记住的唯一要点
- **Tone** — 影响用词、句长、正式程度
- **Target audience** — 影响复杂度与默认知识假设
- **Narrative structure** — 结构方式（myth_busting、journey、data_narrative 等）

然后阅读 `research_brief` 获取 grounding 素材：
- **`data_points`** — 可编入脚本的具体统计与事实。将 `surprise_factor: "surprising"` 或 `"counterintuitive"` 的 claim 用作留存锚点。
- **`audience_insights.misconceptions`** — 若叙事结构为 `myth_busting`，这些即你的 myth/reality 对。
- **`audience_insights.common_questions`** — 在脚本中自然合适处直接回应。
- **`expert_voices`** — 可引用的专家增加权威。少用——每篇脚本一至两处即可。
- **`trending.recent_developments`** — 若有时效性，可引用以使内容显得及时。

**`research_brief` 是你的速查表。** 每条事实、每个惊人数据、每个误解都已预先核实并有来源。要用起来。引用「73% 的开发者……」（来自研究）的脚本，比说「许多开发者……」更有说服力。

### 步骤 2：按需深化研究

Research Director 已完成主要工作——你已有充满有据事实的 `research_brief`。此处的任务是定向补充：

1. **核实与更新**：若 research_brief 中任一点数据显得过时或不确定，重新检索确认。
2. **填补脚本级缺口**：研究提供宏观事实。你可能需要特定类比、精确技术细节，或某段更好的例子。
3. **找最佳讲解方式**：顶尖教育者（3Blue1Brown、Kurzgesagt、Fireship、Veritasium）如何讲解该概念？哪些类比有效？
4. **寻找可引用时刻**：若 research_brief 的 expert_voices 有可用引语，使用之。否则检索一条有力引语锚定关键段落。

**不要重复 Research Director 的工作。** 若 research_brief 已有 6 个数据点，无需再找 6 个。聚焦脚本层需求：对的词、对的类比、对的顺序。

### 步骤 3：规划叙事弧线

写正文前先规划结构。每篇解说脚本遵循戏剧弧线：

```
HOOK (0-5s)     → 抓住注意力。问题、大胆主张或惊人事实。
                   绝不：「在本视频中，我们将学习……」
                   绝不：「Hey guys, welcome back……」

SETUP (5-15s)   → 观众为何要在意？制造知识缺口。
                   呈现问题或疑问。让他们需要答案。

BUILD (15-Xs)   → 递进揭示。每段建立在前一段之上。
                   用「因此 / 但是」过渡，而非「然后」。
                   South Park 规则：「发生了这个，因此那个发生了，
                   但是随后出现了这个转折……」

CLIMAX（结束前约 5s）→ 「啊哈」时刻。一切豁然开朗。
                            这是对开场知识缺口准备的回报。

LANDING（最后 5s）→ 快速回顾 core message + CTA。
                     此处不要引入新信息。
```

将 brief 的每个 `key_points` 映射到 BUILD 阶段的特定小节。

### 步骤 4：撰写脚本

写各 section 前，用 `skills/meta/voice-performance-director.md` 创建顶层 `voice_performance` 计划。计划须描述嗓音意图、节奏轮廓、能量曲线、停顿策略，以及哪一 section 用于 TTS 样片审批。不要写成模糊的「自然嗓音」备注。

按下列字段撰写每个小节：

```json
{
  "id": "s1",
  "label": "Hook",
  "text": "Your database searches every single row. Every. Single. One. What if it didn't have to?",
  "start_seconds": 0,
  "end_seconds": 5,
  "speaker_directions": "Emphasize 'every single row' with measured pacing. Brief pause before the question.",
  "delivery_cues": {
    "pace": "measured",
    "energy": "curious",
    "emphasis_words": ["every", "single"],
    "pause_after_seconds": 0.6,
    "delivery_note": "Let the repetition feel intentional, then soften into the question.",
    "provider_text": "Your database searches every single row. Every. Single. One. <break time=\"0.6s\"/> What if it didn't have to?"
  },
  "enhancement_cues": [
    {
      "type": "animation",
      "description": "Database table with rows highlighted one by one, slowing down as count increases",
      "timestamp_seconds": 1
    }
  ],
  "pronunciation_guides": []
}
```

#### 时长估算

| 节奏 | 词/分钟 | 适用场景 |
|------|-------------|----------|
| Conversational | ~150 wpm | 多数解说默认 |
| Contemplative | ~120 wpm | 复杂主题，需消化时间 |
| Energetic | ~180 wpm | 短视频、高能量、TikTok/Reels |
| Technical | ~130 wpm | 代码走读、架构深潜 |

**按时长的字数预算：**
- 30s 视频 → 约 65–75 词
- 60s 视频 → 约 130–150 词
- 90s 视频 → 约 195–225 词
- 120s 视频 → 约 260–300 词

统计词数。若超出预算 20%+，TTS 要么赶工要么超时长。务必毫不留情地删减。

#### Speaker Directions

撰写 TTS 能实际执行的指导。优先结构化 `delivery_cues`，而非仅散文式 `speaker_directions`：

| 指导 | TTS 实现 |
|-----------|-------------------|
| "Speak slowly, with emphasis" | 降低 speed、提升 stability |
| "Excited, picking up pace" | 提高 speed、提高 style |
| "Pause for 1 second" | SSML `<break time="1s"/>` |
| "Whisper" | SSML whisper 标签（依模型） |
| "Emphasize THIS word" | 后处理备注或 SSML emphasis |

避免 TTS 无法执行的指导：「smile while speaking」「gesture toward screen」「look at camera」。

**表现力旁白规则：** 每个以旁白为主导的小节须在 `pace`、`energy`、`emphasis_words`、`pause_before_seconds`、`pause_after_seconds`、`delivery_note` 或 `provider_text` 中至少包含两条具体提示。当需要标点或 SSML 停顿标签使朗读更自然时，使用 `provider_text`。

#### Enhancement Cues

每个小节应至少有一条 enhancement cue。这些告诉 Scene Planner 与 Asset Generator 要生成何种视觉。

| Cue 类型 | 何时使用 | 示例 |
|----------|-------------|---------|
| `overlay` | 关键术语、定义、标签 | "Show 'embedding' definition overlay" |
| `diagram` | 流程、架构、流向 | "Mermaid flowchart: query → encode → search → rank" |
| `stat_card` | 惊人数字或对比 | "Display: 1ms vs 500ms search time" |
| `animation` | 需动态才能理解的概念 | "Animate vectors moving through high-dimensional space" |
| `code_snippet` | 代码示例 | "Show Python: `results = collection.query(embedding)`" |
| `broll` | 现实语境 | "Show examples of apps using vector search" |

**密度规则**：至少每 8–10 秒一条 enhancement cue。60 秒视频至少 6–8 条提示。视觉不变，观众会流失。

#### Pronunciation Guides

针对技术术语、缩写与非英文词：

```json
{"word": "FAISS", "phonetic": "FACE"},
{"word": "Qdrant", "phonetic": "kuh-DRANT"},
{"word": "cosine", "phonetic": "CO-sign"}
```

### 步骤 5：对照 Playbook 校验

阅读活跃风格 playbook 并核实：

| Playbook 字段 | 对脚本的影响 |
|----------------|---------------|
| `identity.pace` | 匹配词密度。`contemplative` = 更少词、更长停顿 |
| `audio.voice_style` | 塑造 speaker directions 的语气 |
| `voice_performance` | 确认节奏、停顿、能量曲线对 TTS 足够明确 |
| `motion.pacing_rules` | 如「定场镜头至少保持 2s」影响小节时长 |
| `identity.mood` | 用词：`warm` 偏口语；`professional` 偏精确 |

### 步骤 6：自评

为脚本打分（1–5）：

| 标准 | 问题 |
|-----------|----------|
| **Hook power** | 前 3 秒能否让人停下滑动？ |
| **Word count accuracy** | 是否在目标时长的 ±10% 内？ |
| **Narrative flow** | 每段是否建立在前段之上？「因此/但是」而非「然后」？ |
| **Enhancement density** | 是否至少每 8–10 秒一条 cue？ |
| **Voice performance** | 停顿、重音、节奏、样片小节是否明确？ |
| **Jargon management** | 术语是否解释或有发音指南？ |
| **Climax payoff** | 「啊哈」时刻是否兑现 hook 的承诺？ |
| **CTA relevance** | 行动号召是否具体、可执行？ |

任一维度低于 3 分，提交前修订。

### 步骤 7：提交

将 `script_json` 按 canonical script schema 校验，经 checkpoint 协议持久化，并附上 stage review。没有单独的 explainer submit 函数。

### 制作中的事实核查

脚本撰写中若遇不确定：
- 用 `web_search` 在写入脚本前核实事实性陈述
- 用 `web_search` 查找参考图以保证视觉准确
- 在 decision log 中记录：`category="visual_accuracy_check"`

脚本中每条事实性陈述应可追溯到 `research_brief`。
若陈述不在研究中，须补充研究并添加来源。不要编造统计、日期或出处。

## 常见陷阱

- **字数过多**：头号失败原因。TTS 节奏固定。60 秒视频写 250 词，音频要么赶要么变成 100 秒。数词。
- **信息前置**：hook 应制造好奇，而非倾倒信息。「HTTPS 使用 TLS 1.3 与 AEAD ciphers」是糟糕开场。「那把锁图标的意思并非你想的那样」才更有吸引力。
- **缺少 enhancement cues**：无视觉方向的脚本是播客脚本。每小节至少一条提示告诉视觉团队展示什么。
- **泛化的 speaker directions**：「Read naturally」无用。「Start measured and precise, then accelerate through the list to convey scale」才可执行。
- **忘记受众**：给 CTO 的脚本与给高中生的用词应不同，即便讲同一概念。
- **小节间无过渡**：每小节应有逻辑衔接到下一段。观众不应想「等等，为什么突然讲这个？」

## 示例：撰写良好的 Section

```json
{
  "id": "s3",
  "label": "The Core Idea",
  "text": "Instead of matching keywords, vector databases convert everything — text, images, audio — into lists of numbers called embeddings. Similar things get similar numbers. So finding related content becomes a math problem: which numbers are closest?",
  "start_seconds": 15,
  "end_seconds": 28,
  "speaker_directions": "Measured pace through 'text, images, audio' with slight pause between each. Speed up slightly on 'similar things get similar numbers' — it should feel like a revelation. Brief pause before the final question.",
  "enhancement_cues": [
    {
      "type": "animation",
      "description": "Show text/image/audio icons transforming into number arrays (embeddings). Arrays cluster by similarity in a 2D space.",
      "timestamp_seconds": 16
    },
    {
      "type": "stat_card",
      "description": "Display: 'Everything becomes numbers. Similar things → similar numbers.'",
      "timestamp_seconds": 22
    }
  ],
  "pronunciation_guides": [
    {"word": "embeddings", "phonetic": "em-BED-ings"}
  ]
}
```

---

## 关卡提醒（具约束力）

本阶段需人工审批（`human_approval_default: true`）。review 通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot board 渲染产物），**结束本轮**。勿在同一回复中启动下一阶段。
审批按关卡进行——较早的「继续」不覆盖本关卡。
