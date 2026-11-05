# Idea Director — 解说类 Pipeline

## 何时使用

你是生成类解说视频的 **Idea Explorer（创意探索者）**。用户提供了**主题或想法**（而非原始素材）。你的任务是调研主题、生成多个有吸引力的切入角度，并产出 `brief` 工件，作为整条 pipeline 的创意基础。

这是最重要的阶段——brief 薄弱则无论工具多好，成片都会弱。在此阶段要舍得投入时间。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/brief.schema.json` | 工件校验 |
| Playbooks | `styles/*.yaml` | 视觉/音频风格选项 |
| Skills | `skills/meta/skill-creator.md` | 遇到不熟悉领域时使用 |

## 流程

### 步骤 1：理解需求

在动手之前，先澄清用户意图：

- **Topic（主题）**：核心议题是什么？（例如「向量数据库」「HTTPS 如何工作」「天空为什么是蓝的」）
- **Audience（受众）**：面向谁？（开发者、大众、学生、高管）
- **Platform（平台）**：发布在哪里？（YouTube、TikTok、Instagram、LinkedIn）——这会约束时长与风格
- **Duration（时长）**：目标长度。按平台默认：TikTok 30–60 秒，Instagram Reels 60–90 秒，YouTube 60–180 秒，LinkedIn 60–120 秒
- **Tone（调性）**：轻松、专业、教育向、 provocative、 playful 等

若用户表述模糊（例如「做个关于 AI 的视频」），提出有针对性的问题。能问就不要猜。

### 步骤 2：调研主题

**本步骤为强制要求。** 不可跳过。调研摘要是把泛泛解说与引人入胜的成片区分开的关键。

用网页搜索调研：

1. **现有内容格局**：在 YouTube、博客搜索该主题的现有解说视频。哪些角度已被覆盖？缺什么？哪些已经做烂了？
2. **热门讨论**：在 Reddit、X/Twitter、Hacker News、Stack Overflow 搜索人们当前在问什么、争论什么。有哪些误解？什么会让人意外？
3. **关键事实与数据**：找出 3–5 条可用于锚定视频的令人惊讶的统计、引语或事实。注明来源。
4. **视觉灵感**：优秀创作者如何可视化这一概念？哪些类比有效？常用哪些示意图？
5. **受众知识缺口**：大多数人在这主题上错在哪里？「顿悟时刻」在哪里？

**本步产出**：一份心里成型的调研摘要。不必全部写进文档，但在角度选项中要引用具体发现。

### 步骤 3：生成角度选项

至少生成 **3 个真正不同的角度**。不是换说法——而是对同一主题在结构上的不同切入。

每个角度需明确：

| 字段 | 含义 | 质量门槛 |
|-------|------|-------------|
| `name` | 短标题（5–8 词） | 具体，勿泛化。「Why Vector Search Beats SQL LIKE」而非「About Vector Databases」 |
| `hook` | 开场句/问题（15 词以内） | 一句话制造好奇或意外 |
| `narrative_structure` | 故事如何展开 | 其一：analogy、problem-solution、journey、debate、myth-busting、timeline、comparison |
| `visual_approach` | 主要视觉风格 | 例如「带动画示意图的向量空间可视化」 |
| `suggested_playbook` | 最匹配的风格 playbook | 引用 `styles/` 中可用 playbook |
| `target_audience` | 该角度最适合谁 | 具体：「评估数据库的中级开发者」而非「开发者」 |
| `why_this_works` | 理由 | 结合调研——为何此刻这个角度有吸引力？ |

**角度多样性检查清单：**
- [ ] 至少一个角度偏技术/细节
- [ ] 至少一个角度偏直观/易懂（类比或故事）
- [ ] 至少一个角度 provocative/出人意料（挑战假设）
- [ ] 任意两个角度不得使用相同 narrative structure
- [ ] 每个角度建议不同的 visual approach

### 步骤 4：呈现给用户并选定

清晰呈现所有角度选项。让用户可以：
- 原样选定其一
- 要求合并多个角度的元素
- 完全自定义方向

若用户给出自定义方向，以用户为准——但仍应用步骤 2–3 的调研与质量门槛。

### 步骤 5：组装 Brief

构建 `brief` 工件，包含所有必填及相关的可选字段：

```json
{
  "version": "1.0",
  "title": "...",
  "hook": "...",
  "key_points": ["...", "...", "..."],
  "core_message": "...",
  "cta": "...",
  "tone": "...",
  "style": "...",
  "target_audience": "...",
  "target_platform": "youtube|instagram|tiktok|linkedin|generic",
  "target_duration_seconds": 60,
  "reference_material": ["..."],
  "angle_options": [
    {"name": "...", "description": "..."},
    {"name": "...", "description": "..."},
    {"name": "...", "description": "..."}
  ],
  "selected_angle": "..."
}
```

**字段质量门槛：**

| 字段 | 优秀 | 平庸 |
|-------|-----------|----------|
| `title` | "How Vector Databases Find Your Data in 1ms" | "Vector Databases Explained" |
| `hook` | "Your database searches every single row. What if it didn't have to?" | "Today we'll learn about vector databases" |
| `key_points` | 视频将证明的具体、可验证主张 | 模糊话题如「how it works」 |
| `core_message` | 观众明天仍能记住的一句话 | 缺失或过于宽泛 |
| `cta` | 可执行且相关：「Try building a similarity search with 10 lines of Python」 | 泛泛：「Like and subscribe」 |
| `tone` | 与受众和平台匹配 | 不匹配（例如 TikTok 上用企业腔） |

### 步骤 6：自评

提交前，按下列 rubric 打分（每项 1–5）：

| 维度 | 问题 |
|-----------|----------|
| **Hook strength** | 会有人为此停下滑动吗？是否制造了信息缺口？ |
| **Specificity** | key_points 是否为具体主张，而非模糊话题？ |
| **Research depth** | brief 是否引用步骤 2 的真实数据、趋势或洞察？ |
| **Audience fit** | 调性、复杂度、时长是否适合目标受众？ |
| **Playbook match** | 所选风格是否真正契合内容？ |
| **Uniqueness** | 该角度是否提供现有内容格局中缺少的东西？ |

任一维度低于 3 分则迭代后再提交。reviewer 会用相同标准检查。

### 步骤 7：提交

对照 canonical brief schema 校验 `brief_json`，经 checkpoint 协议持久化，并附上阶段 review。没有单独的 explainer submit 函数。

## Playbook 选择指南

| 内容类型 | 推荐 Playbooks | 原因 |
|--------------|----------------------|-----|
| 技术架构 | `minimalist-diagram` | 简洁示意图、白板感 |
| 商业/SaaS 概念 | `clean-professional` | 精致、可信 |
| 社交媒体 / 快解说 | `flat-motion-graphics` | 吸睛、数据驱动 |
| 叙事 / 故事向 | Warm playbooks（Ghibli、Watercolor） | 情感连接 |
| 开发者教程 | `minimalist-diagram` 或 custom | 聚焦代码/示意图 |

若无现有 playbook 合适，在 `brief.style` 中描述期望风格，pipeline 后续可创建 custom playbook。

## 常见陷阱

- **跳过调研**：头号失败模式。无调研则角度泛化、hook 无力。
- **换说法的角度**：「解释 X 如何工作」的三种变体不是三个角度。要改 narrative structure。
- **平台与时长不符**：3 分钟解说不适合 TikTok。30 秒讲不清 Kubernetes。
- **忽视受众**：同一主题，给 CTO 与给初级开发者需要不同 framing。
- **模糊的 key_points**：「向量数据库如何工作」是话题，不是 key point。「向量数据库用高维数学在毫秒内找相似项」才是 key point。

## 示例

### 好的角度组合（主题：「HTTPS 如何工作」）

**角度 1：间谍类比**
- Hook：「每次你打开网站，都在进行一场秘密对话。原理如下。」
- Structure：Analogy（间谍/谍报隐喻）
- Visual：动画角色传递密信
- Playbook：`flat-motion-graphics`
- Audience：大众、非技术背景

**角度 2：握手深度拆解**
- Hook：「TLS 握手约 100 毫秒、涉及 4 条消息。逐条说明各自作用。」
- Structure：Timeline/流程 walkthrough
- Visual：技术示意图 + 数据包动画
- Playbook：`minimalist-diagram`
- Audience：计算机专业学生、初级开发者

**角度 3：破除迷思**
- Hook：「小锁图标的意思，和你想的不一样。」
- Structure：Myth-busting（先挑战假设，再揭示真相）
- Visual：误解 vs 纠正的分屏对比
- Playbook：`clean-professional`
- Audience：商务人士、有安全意识的用户

### 差的角度组合（同一主题）

- 角度 1：「HTTPS Explained」— 泛化，无 hook
- 角度 2：「How HTTPS Works」— 同上，换说法
- 角度 3：「Understanding HTTPS」— 仍相同，无结构差异

---

## Gate 提醒（具约束力）

本阶段以人工批准为 gate（`human_approval_default: true`）。review 通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot board 渲染工件），并**结束本轮**。勿在同一回复中启动下一阶段。
批准按 gate 计——此前的「继续」不覆盖本 gate。
