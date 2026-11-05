# 文本效果 — 参考

对于确定性的文本动画规格（例如 `typewriter` 在精确的 `240ms / 46ms stagger / steps(1, end) easing` 下），本技能将转交给 Pixel Point 在 [github.com/pixel-point/animate-text](https://github.com/pixel-point/animate-text) 维护的独立 **`animate-text`** 技能。该技能提供 24 种命名文本效果的目录，以及可移植的契约与各库实现配方（GSAP、Anime.js、WAAPI）。

**我们不会在仓库内内置该目录。** Pixel Point 的 `animate-text` 是唯一权威来源；在此 vendoring 其文件会违反上游许可（截至撰写时上游未声明明确许可证）。单独加载该技能可在法律上保持清晰，同时仍能获得相同目录。

## 如何使用

当某个 beat 需要确定性文本动画时，请与本技能一并加载上游技能：

```bash
# In your project root, install the upstream skill into .agents/skills/
npx skills add pixel-point/animate-text
```

或在支持技能的 agent 运行时，可按名称调用该技能：

```
/animate-text
```

安装后，规格位于：

```
.agents/skills/animate-text/assets/effects/<id>.json   # per-library implementation recipe
.agents/skills/animate-text/assets/specs/<id>.json     # portable motion contract
```

读取这些文件的子 agent 可获得精确的 GSAP 时序、easing 字符串、DOM 拆分规则与 stagger 算法 — 无需自行发挥创意。

## 何时不需要上游技能

若某个 beat 的文本动画简单到可用散文描述（「标题逐词向上淡入，80ms stagger」），可直接用本技能包中已有的 GSAP 知识内联实现（`hyperframes-creative` → `references/motion-principles.md` 与 `references/beat-direction.md`；`hyperframes-animation` → `techniques.md`，条目 #4「Per-Word Kinetic Typography」）。上游目录在以下情况最有价值：

- 你希望在多个 beat 间使用同一**命名**效果（使整体像一套设计系统，而非一次性方案）
- 你在若干相似效果间选择（typewriter vs per-character-rise vs bottom-up-letters），并想在一处看到全部 24 种
- 你需要布局感知类效果（`kinetic-center-build`、`short-slide-right`、`short-slide-down`），仅靠参数不够 — 这些附带自定义布局算法

## 效果名称 — 词汇表（请勿将此当作实现来源）

为方便撰写 storyboard：上游技能提供 24 种效果。此处列出其 ID，以便在加载上游技能之前即可在 `STORYBOARD.md` 中命名。**实现规格在上游技能中，不在此处。**

- **Per-character (7):** soft-blur-in, per-character-rise, typewriter, bottom-up-letters, top-down-letters, stagger-from-center, stagger-from-edges
- **Per-word (8):** per-word-crossfade, spring-scale-in, shared-axis-y, blur-out-up, kinetic-center-build, short-slide-right, short-slide-down, depth-parallax-words
- **Per-line (2):** mask-reveal-up, line-by-line-slide
- **Whole element (7):** micro-scale-fade, shimmer-sweep, fade-through, shared-axis-z, scale-down-fade, focus-blur-resolve, shared-axis-x

描述、时长、easing 曲线及各库配方：加载 `/animate-text` 并阅读其目录页。

## 在 storyboard 中

每个 beat 中的每个文本元素均可按 ID 命名效果，例如：

```markdown
**Text Animations:**

- Main headline: `kinetic-center-build`
- Eyebrow label: `soft-blur-in`
- Body copy 3 lines: `mask-reveal-up`
```

实现该 beat 的子 agent 若尚未加载 `/animate-text`，会先加载它，再从上游技能文件中读取每个命名效果的规格。

若上游技能不可用（离线构建、网络限制、不支持技能加载的 agent 运行时），子 agent 会退而仅根据描述实现效果 — 结合 GSAP 知识与效果 ID 所表达的意图（例如「typewriter」= 逐字符阶梯式显现、无插值）。
