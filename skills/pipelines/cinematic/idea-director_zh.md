# Idea Director - 电影感流水线

## 何时使用

当项目需要预告片、品牌片、戏剧性蒙太奇或情绪驱动的短片，且节奏、氛围与情绪递进比直接说明更重要时，使用本流水线。

不要仅仅因为用户说「做得电影感一点」就选用本流水线。若项目实质上是屏幕演示、讲解片或素材再利用任务，应改走对应流水线。

## 参考输入

- `docs/cinematic-best-practices.md`
- `skills/creative/cinematic.md`
- `skills/creative/storytelling.md`

## 流程

### 1. 归类源素材现实

记录源素材模式：

- `footage_only`
- `footage_plus_stills`
- `still_led`
- `generated_support`
- `mixed_montage`

同时判断交付物是否必须以运动画面为核心。在 `brief.metadata.motion_required` 中以布尔值保存。

当视频承诺依赖运动镜头或动画化构图而非静态帧时，设 `motion_required = true`。例如：

- 科幻预告片，
- 电影感 teaser，
- 动作或 hype 剪辑，
- agent/avatar 类输出，
- 任何质量取决于生成视频片段的概念。

除非用户已提供素材，或当前环境确实能制作，否则不要假定已有库存、生成 B-roll 或音乐。

### 2. 定义情绪弧线

用平实语言选定弧线：

- tension -> reveal（张力 → 揭示）
- wonder -> scale（惊奇 → 规模）
- intimacy -> payoff（亲密 → 回报）
- urgency -> resolution（紧迫 → 解决）
- mystery -> CTA（神秘 → 行动号召）

brief 应告诉后续阶段要让观众**感受**什么，而不仅是讲**关于**什么。

### 3. 选定交付形态

常见输出形态：

- `teaser`
- `trailer`
- `hero_brand_film`
- `mood_cut`
- `social_cutdown`

将更长的规划细节写入 `brief.metadata`。

建议的 metadata 键：

- `source_mode`
- `motion_required`
- `delivery_shape`
- `emotional_arc`
- `anchor_assets`
- `music_strategy`
- `generated_support_level`
- `aspect_ratio_plan`
- `rights_constraints`

### 4. 对照现实检验方案

若用户源素材薄弱且没有生成路径，应明确说明。电影感结果仍需要足够视听素材来承载情绪。

若 `motion_required = true`，须明确运动实现路径：

- 确认计划使用的片段生成 provider，
- 确认目标构图是否必须使用 Remotion，
- 若任一项不可用或不稳定，应将方案标记为 blocked，而非静默改写成以静帧为主的 teaser。

### 5. 音乐计划（必填）

电影感视频成败在音频。**在用户批准 brief 之前，必须把音乐情况摆到台面上。**

按以下顺序检查可用性：

1. **用户音乐库：** 调用 `registry.get_by_capability("music_library")` 并查看 `music_library/`。列出可用曲目及其时长与情绪标签。
2. **免版税搜索：** 调用 `registry.get_by_capability("music_search")`。报告可用 provider、授权约束及密钥要求。
3. **音乐生成 API：** 调用 `registry.get_by_capability("music_generation")`。报告状态、配额、成本与质量权衡。
4. **自带音轨：** 用户可将其他已授权来源的曲目放入 `music_library/`。

以明确选项呈现：

```
MUSIC PLAN
├── Your music library: [N tracks / empty]
├── Royalty-free search: [providers / unavailable]
├── AI generation: [provider] — [AVAILABLE/UNAVAILABLE] [cost]
└── Bring your own: Drop a track in music_library/ before asset stage

Options:
  (a) Use a library track (which one?)
  (b) Search a royalty-free provider
  (c) Provide your own track
  (d) Generate via API (if available)
  (e) Proceed without music (not recommended for cinematic)
```

将决定记入 `brief.metadata.music_strategy`，包含所选来源及路径/提示词。

### 6. 质量门

- 源素材事实已写清，
- brief 标明 motion 是否为硬性要求，
- 情绪弧线具体可感，
- 输出形态与可用素材匹配，
- 音乐计划已落定（已选来源或明确延后），
- 方案确有电影感理由，而非仅贴标签。

## 常见陷阱

- 把普通剪辑加黑边就称作电影感。
- 未检查工具就假定可用生成插入镜头。
- 悄悄把以运动为核心的 brief 改成以静帧为主的 teaser。
- 规划 trailer 形态却没有 reveal 或 payoff。

---

## 门控提醒（具约束力）

本阶段需人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染 artifact），并**结束本轮回复**。不要在同一轮回复中启动下一阶段。
批准按门控逐项生效——此前说的「继续」不覆盖本门控。
