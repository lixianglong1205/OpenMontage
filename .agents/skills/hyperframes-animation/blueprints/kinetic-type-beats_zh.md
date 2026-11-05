# kinetic-type-beats — 动感字体节拍

**意图**：扁平、居中、粗体排版的镜头，动效即词语/短句的变化——同一行通过硬切就地替换 token，或跨全屏节拍（每拍自带动作）逐句构建陈述，最终以 spring-pop  payoff 落地。

**适用角色**

- Hook（来自 `hook-kinetic-type-flash`）：当一条静止台词以有力的修辞问句或「你一直在做 X」式点名收尾，且就地 token 互换本身就是笑点时。
- Hook（来自 `hook-kinetic-type-escalation`）：当同一句陈述应跨多个独立全屏节拍递进（每拍不同动作），并在 spring-pop payoff 元素上收束——强度递增 /「把 X 变成 Y」式开场。
- Problem（来自 `problem-kinetic-type-beats`）：当脚本为 3–5 条短痛点陈述（或「要是……？」式 framing），每条应单独落在空白画布上，再被下一条替换——此时尚无产品画面。
- Product_Intro（来自 `product-intro-kinetic-type-namedrop`）：当 hook 就是文字——硬切穿过「Introducing…」/ tagline / 价值节拍，并在品牌名或 logo 上收束。
- Benefits（来自 `benefits-kinetic-type`）：当「你得到什么」是快速 staccato 蒙太奇——8–12 条短价值语，每条闪现后清空，再进入下一条，节奏极快。
- CTA（来自 `cta-kinetic-type`）：当收束语是一条有力的收尾句（或短叠的价值行），逐拍 snap/fade 进入并落在品牌 lockup 或 URL 上——无空间布景、无点击按钮。
- Brand_Outro（来自 `brand-outro-kinetic-type-resolve`）：当结尾是居中通道内一连串单词动词的快速连发，强调广度，并收束于品牌的那一个定义性词语（动效即信息，无 logo lockup）。

**时长**：3.4–12s（Benefits 最快约 3.5–4s，8–12 个亚 0.5s 节拍；Brand_Outro 约 3.6s；Problem 最长 7–12s；CTA 跨度 3.6–11.7s，视节拍数而定）

**镜头结构**（扁平、固定居中锚点；纯色 `[bg color]` 上的粗体 sans-serif 文字；字形/token 为唯一主体；除非注明 modifier，否则机位锁定；两种折叠子形态——**(A) 固定行 token 互换** 与 **(B) 多节拍陈述构建**）

- **Scene 1（0.0–~1.0s）— 第一拍落地。** 纯色 `[bg color]` 场。粗体 `[type color]` 文字经一种入场方式到达正中心：逐字 type-on 并带尾随闪烁 caret，或硬切 FLASH-in（无 fade/slide），或逐词 stagger 的 fade/blur，或 oversized 词平滑 SCALES DOWN 为居中小号词。可选在关键词上播放 `[accent color]` 动作：自左向右绘制的 underline / strike-through、文字背后的小型 particle/dot burst，或 `[accent color]` selection-box 框选该词。
  - _变体 — Hook (flash)_：固定 `[hook line]`（或其首词）居中停驻；无递进动作。
  - _变体 — Hook (escalation)_：`[beat 1 text]` 大号入场并 scale-down 至居中，或置于发光 `[motif]` 之上并慢速 camera push-in（见 camera modifier）；以硬切结束。
  - _变体 — Problem_：居中 `[pain line 1]` 以块为单位在一或两行内 reveal，并带 `[accent]` underline / particle burst。
  - _变体 — Product_Intro_：粗体 `[hook word, e.g. "Introducing"]` 入场并带 typography accent（split-and-slide apart、drawn underline，或 `[accent]` selection-box）。
  - _变体 — Brand_Outro_：可选单帧 `[product UI / hero asset]` 闪过后进入动词通道，随后 `[verb 1]` 硬切入居中。

- **Scene 2..N — 节拍就地替换（引擎）。** 居中锚点逐拍前进；上一拍无任何残留。按子形态选择互换机制：
  - **子形态 A（固定行 token 互换）**：行固定，仅可变槽位以 instant hard CUT 变化（无 roll/scroll/blur）——`[token A]` → `[token B]` → `[token C]`——或末词 backspace 后重打（`[word A]` → `[word B]`）。其余行保持不变。
  - **子形态 B（多节拍陈述构建）**：每拍全屏 hard-cut 至新背景/新行，每拍自带 distinct entrance/exit MOVE——springy scale-in/scale-out overshoot、3D letter-tumble（字形散入旋转深度云再重组为下一句）、motion-blur fly-in 在中心锐化落定、前句加速/zoom 穿过镜头并 fade、letter-spacing collapse，或 bottom-up masked slide。背景可在选定节拍 hard-flip `[bg A]`↔`[bg B]`，并 invert `[type color]` 以保持可读。
  - _变体 — Hook (escalation)_：beat 2 `[beat 2 text]`（更强调）snap 入；beat 3 `[beat 3 text]`（高潮）hold，再在字形本身做 transition-out——沿 Z 向前 dolly 穿过 oversized glyph，或 per-word karaoke highlight sweep 自左向右点亮词语。
  - _变体 — Problem_：每条 `[pain line k]` 以 chunk-reveal 或 motion-blur fly-in 入场，前一条 blur/zoom 离场；可选 `[accent color]` 过渡词（「[what-if hook]」）自中心 scale up、hold，再 zoom 穿过镜头并 fade。
  - _变体 — Product_Intro_：每条 `[tagline phrase]` 为 hard-cut/push-through inverted-text 节拍，并带一次性 accent（strike-through、slider/toggle 形状滑入，或 bg-invert 循环 white→`[accent]`→black 翻转 fg/bg）。
  - _变体 — Benefits_：高 tempo（~0.4s/beat）——每条 `[benefit phrase]` 以 springy scale-in/out 或 3D letter-tumble pop；整段多次 bg light↔dark flip 并 invert 文字色。
  - _变体 — CTA_：每条 `[value line]` → `[value line]` → `[CTA verb line]` 以 hard cut / zoom-blur cut through near-black / fade-out 清空，下一条 pop/fade/slide 入。可选 `[accent motif]` 在后方绘制（rising line-graph trim-path、细 wireframe guides、gutter geometry tiles）。
  - _变体 — Brand_Outro_：居中单个 `[verb / keyword]` 以稳定 ~0.2s cadence HARD-CUT 至下一个（无 fade/scale），叠在 continuous moving field 上（见 camera modifier）。

- **Scene N（最后一拍 → 结束）— resolve 并 HOLD。** 最后一拍落地并 hold 至结束（仅 settle，不再 scale-out）。按角色分 resolve：
  - _变体 — Hook (flash)_：末次 token swap 落地并 hold；可选 tiny punctuation/emphasis snap（`?` → `?!`，或 fill snap 至 `[accent color]`）。
  - _变体 — Hook (escalation)_：resolve 于 `[payoff bg]`——`[payoff element]`（彩色方块 / heart-eyes reaction emoji）SPRING-POPS 居中；小 `[accent motes]` 向外漂移；轻微 settle。
  - _变体 — Problem_：末条 `[pain line]` reveal（自左向右 swipe 并 leading-edge blur，或字母 radial explode 后 resolving line fade up）；hold 痛点于屏。
  - _变体 — Product_Intro_：resolve 于品牌——`[logo mark]` / `[wordmark]` 居中 pop in（可选 sting：liquid/ink splash、blob backing），或末个价值词 hold 于 expanding-iris `[accent]` 圆内，圆 scale 填满画幅并 hard-cut Closing word 穿过。
  - _变体 — Benefits_：末条 `[benefit phrase]` 入场（可选在 inverted bg 上）并 SETTLE——不再 scale/tumble 退出。
  - _变体 — CTA_：落在 lockup——`[logo mark]` SCALES UP small→full 并 hold，或 `[logo]`/`[url]` 在 icon 旁 segment-by-segment 构建。End-card 完全 static hold。
  - _变体 — Brand_Outro_：hard cut 至 `[resolve word / brand keyword]`（最长，仍居中）；HOLDS ~0.5s，背景场持续运动。

**动效词汇**：hard-cut / flash word swaps；in-place token cycle（instant cut，无 roll/scroll/blur）；type-on 并带尾随 blinking caret；backspace-and-retype；per-word staggered fade/blur reveal；big→small scale-down；springy scale-in/scale-out overshoot；3D letter-tumble scatter-and-reassemble；motion-blur fly-in / blur-off；prior text zoom-through-camera；letter-spacing collapse；bottom-up masked slide；绘制的 `[accent]` underline / strike-through；particle/dot burst from text；`[accent]` selection-box frame；bg-invert hard-flip 并 text-color invert；karaoke per-word highlight sweep；radial letter-explode；expanding-iris circle wipe-to-next；final spring-pop payoff element（square / emoji / logo mark）；drifting `[accent]` motes / ambient shapes；segment-by-segment URL/wordmark build；final-token punctuation snap；settle-and-hold。

**规则映射**

- hard-cut / flash word swaps、in-place token cycle、整行 state swap at time thresholds → `discrete-text-sequence`
- type-on character-by-character + blinking trailing caret → `discrete-text-sequence`（text/typing state progression）+ `context-sensitive-cursor`（caret blink/color-switch）
- backspace-and-retype final word(s) → `discrete-text-sequence`（typos/holds/backspace explicitly in-scope）
- one short distinct phrase per beat / script-driven phrase windows / word-by-word tagline assembly → `dynamic-content-sequencing`
- percussive per-beat phrase entrances on a shared beat array（distinct entrance per phrase，steady cadence）→ `kinetic-beat-slam`（最贴合 multi-beat statement-build 引擎与 ~0.2s Brand_Outro verb march）
- per-word staggered fade/blur reveal → `kinetic-beat-slam`（per-phrase/per-word distinct entrances）；soft-focus blur 组件 → `depth-of-field-blur`（off-focus words 上的 selective-focus blur）
- big→small scale-down on a word；springy scale-in/scale-out overshoot → `spring-pop-entrance`（spring pop/settle），plain scale tween 由 `gsap-effects` 支撑
- 3D letter-tumble scatter-into-depth-cloud then reassemble → `depth-scatter-assemble`（字形散入 3D depth cloud 并重组为下一句；可与 `3d-text-depth-layers` 组合做 extruded read，或 `hacker-flip-3d` 做 in-place per-char flip）
- karaoke per-word highlight sweep synced across words → `asr-keyword-glow`（keyword glow+scale on synced rail）OR `css-marker-patterns`（highlight sweep）——选 ASR-driven 或 static-timeline sweep
- drawn-on `[accent]` underline / strike-through / loop / scribble under key word → `css-marker-patterns`（highlight sweep / circle / burst / scribble / sketchout）
- particle/dot burst from behind text → `css-marker-patterns`（burst），由 `gsap-effects` 支撑
- `[accent]` selection-box frame around a word → `css-marker-patterns`（circle/box marker）+ `gsap-effects`
- bg-invert hard-flip（light↔dark / white→accent→black）并 text-color invert → `discrete-text-sequence`（whole-text/state swap 覆盖 synchronized fg/bg state change）
- letter-spacing collapse；bottom-up masked slide → `gsap-effects`（tween letter-spacing / masked translate）+ techniques：per-word kinetic typography / clip-path reveal
- expanding-iris circle wipe，在同一中心将当前词 morph 为下一词 → `scale-swap-transition`（morph two elements at same center）
- final spring-pop payoff element（colored square / reaction emoji / logo mark）→ `spring-pop-entrance`（或 `physics-press-reaction` 做更重 pop）
- drifting `[accent]` motes / ambient shapes / soft drifting gradient field beneath the type → `sine-wave-loop`（idle drift loop）
- segment-by-segment URL / wordmark build beside its icon → `discrete-text-sequence`（segment-by-segment state reveal）或 `dynamic-content-sequencing`
- final-token punctuation / emphasis snap（`?`→`?!`，fill→accent）→ `discrete-text-sequence`
- settle-and-hold final frame → `spring-pop-entrance`（settle phase）/ static hold（无需 rule）
- motion-blur fly-in / blur-off / zoom-through-camera streak on type → `motion-blur-streak`（fast fly-in / zoom-through 上的 directional velocity blur；重 motion-blur smear 在中心锐化 resolve）
- radial letter-explode（glyphs explode outward radially then resolve）→ `depth-scatter-assemble`（radial per-letter explode-and-resolve 与 depth-cloud scatter 同属 scope）
- 3D letter-tumble depth-cloud scatter-and-reassemble → `depth-scatter-assemble`（free tumbling depth-cloud 飞出并 snap 回下一句）

**camera modifier**（可选，叠在 flat shot 上；多数变体机位锁定）

- Slow continuous global zoom-in / uniform push-in 贯穿整段（Problem、Brand_Outro）→ `multi-phase-camera`（push phase）——固定文字与 moving background field 之间产生 parallax。
- Camera dolly/zoom forward THROUGH oversized glyph along Z 作为 beat transition-out（Hook escalation、Product_Intro push-through）→ `coordinate-target-zoom`（target glyph center）或 `multi-phase-camera`（push）。
- Scene 1 在 glowing `[motif]` 上 slow push-in（Hook escalation）→ `multi-phase-camera`（push）或 `coordinate-target-zoom`。
- 注意：in-place token swap（子形态 A）及多数 Benefits/Hook-flash/CTA 变体完全 camera-static——互换即唯一动效。
