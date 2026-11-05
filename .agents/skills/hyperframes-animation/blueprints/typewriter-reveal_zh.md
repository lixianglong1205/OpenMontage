# typewriter-reveal — Typewriter Reveal

**意图**：实时光标像真人一样逐字输入（并编辑）一行文字，随后要么将其坍缩为一点并弹出品牌收束，要么在持久品牌标识下保持该行，同时副行逐字输入/切换为最终 CTA —— 以「有人在现场打字」作为本镜头的驱动力。

**适用角色**

- Hook（来自 hook-typed-line-to-reveal）：现场打出一条共鸣式问句/陈述，随后将其坍缩（COLLAPSE）并弹簧弹出（spring-pop）品牌 —— 可为 logo 组合锁，或产品 UI 时刻（「日常痛点在此，我们在此」）。
- Brand_Outro（来自 brand-outro-persistent-mark-cta-rail）：整镜保持 hero 标识于画面正中/顶部；其下副行切换或逐字输入至最终 CTA —— 在 logo 已确立后再落地行动号召。

**时长**：3.6–7s（Brand_Outro 3.6–6.0s · Hook 5.5–7s）

**镜头结构**（单一合并模板；`[slots]` 与具体产品无关）

- Scene 1（0.0–~2.0s）：在纯色 `[bg color]` 背景上，闪烁的文本输入光标 `|` 位于行首，随后 `[primary line]` 逐字符打出（TYPES），光标尾随其后。
  - _变体 — Hook_：画面上无其他元素；打出的 `[hook line]` 独占画面。（子变体：该行在 UI  chrome 内输入 —— 圆角 `[input/pill]` —— 且整组持续向左平移（TRANSLATES）并略缩放，使活动光标始终锚定在画面中心附近，较早文字向左滚出并在左缘被裁剪 —— 滚动推送（ticker push）。）
  - _变体 — Brand_Outro_：`[logo mark]`（+ 可选 `[wordmark]`）已居中/偏上且整镜保持（STAYS）完全可见；标识自身播放入场 flourish（例如 `[checkmark/icon]` 描边绘入标识，或细同心环自标识向外 ripple）；打出的 `[tagline / product label]` 为标识下方的副行（SUB-LINE）。

- Scene 2（~2.0–4.5s）：已打出行在原位修改（MODIFIED）—— 活动文本被编辑而非重拍。
  - _变体 — Hook_：末词退格（BACKSPACE）后新词重打（RETYPES）（`[word A]` → `[word B]`），或填充/光标在末词 snap 至 `[accent color]`。短暂 hold。
  - _变体 — Brand_Outro_：副行原位移除（REMOVED）—— 直接硬切/替换（hard CUT/replace，无 backspace）或移动遮罩擦除（mask-WIPE）；标识做小幅 idle move（轻旋 / sparkle  reposition）；标识从不离画。

- Scene 3 — 收束（resolve）：
  - _变体 — Hook（collapse，~0.3–0.7s）_：光标消失；整段文字/组件在中心坍缩（COLLAPSES）为一点（水平 X-collapse 或 scale-to-0 zoom-out）并消失，留下干净 `[bg]`。随后（剩余时长）居中 `[brand element]` 弹簧弹出（SPRING-POPS）：
    - _logo-lockup 子变体_：`[mark/icon]` 弹出，再侧滑让 `[wordmark]` 揭罩/自其后滑出（UNMASKS）；二者 settle 为居中 lockup。
    - _product-UI 子变体_：`[UI control]`（如按钮）弹出；`[cursor]` 自角落 sweep 并 homing 其上；接触时 ~150ms 状态翻转（state-FLIP）—— 底色 cross-fade 至 `[accent color]`，图标 invert，soft radial GLOW 向外 bloom 并持续。
  - _变体 — Brand_Outro（~4.5s–end）_：最终 `[CTA]` 在副行槽位收束 —— 以 caret 逐字打出和/或 plain text 旁 `[CTA in accent-color button]` 呈现；可选 `[accent color]` GLOW ring / halo 在持久标识周围 settle。hold 至结束。终帧：`[logo mark]` +（glow ring）+ `[CTA]`。

**运动词汇**：闪烁文本光标；逐字符 type-on；backspace-and-retype 或原位 hard-cut/mask-wipe 文本切换；可选向左 ticker push（组件平移以保持光标居中）；持久居中 hero 标识（从不消失）及入场 flourish（图标 stroke-draw、同心 ripple 环）与小幅 idle move（rotate / sparkle）；已打出行的 X-collapse / scale-to-0 zoom-out；spring-pop 品牌揭示；wordmark unmask-slide 成 lockup；cursor sweep + UI state-flip + radial glow bloom；accent glow/halo ring settle；pill/button CTA reveal；hold。

**规则映射**（各运动动词 → `rules/<id>.md`）

- blinking text caret → `context-sensitive-cursor`（caret color-switch + blink）
- character-by-character type-on → `discrete-text-sequence`（typing/typos/holds/backspace）；recipe `gsap-effects`（typewriter）
- backspace-and-retype → `discrete-text-sequence`
- in-place hard-cut / replace text swap → `discrete-text-sequence`（whole-text state swaps）
- mask-wipe erase of sub-line → `techniques.md` clip-path reveal（run in reverse）
- leftward ticker push (assembly translates to keep caret centered) → `camera-cursor-tracking`（viewport follows a moving caret）
- persistent hero mark hold → no motion rule needed（static anchor; intentional — it's the absence of motion）
- entry flourish: icon stroke-draw into mark → `svg-path-draw`
- entry flourish: concentric ripple rings from mark → `cursor-click-ripple`（ripple bloom）
- small idle mark move (rotate / sparkle reposition) → `sine-wave-loop`（idle）
- X-collapse / scale-to-0 zoom-out of typed line → `scale-swap-transition`（closest fit — it morphs/collapses elements at a shared center; approximation, since a standalone collapse-and-vanish without the paired same-center brand pop isn't its exact case）
- spring-pop brand reveal → `spring-pop-entrance`（alt `physics-press-reaction`）
- collapse-text → pop-brand as a same-center morph pair → `scale-swap-transition`（morph two elements at same center）
- wordmark unmask-slide into lockup → `techniques.md` clip-path reveal（unmask）；slide via `spring-pop-entrance`
- cursor sweep onto UI control + press → `cursor-click-ripple`（cursor→target press + ripple）
- UI state-flip (base/icon invert on contact) → `hacker-flip-3d`
- radial glow bloom / accent glow-halo ring settle → `asr-keyword-glow`（accent glow）；ring expansion via `center-outward-expansion`
- pill/button CTA reveal → `spring-pop-entrance`（alt `scale-swap-transition`）

**镜头修饰**：两种角色均无需 camera —— 镜头 static。Hook 的 ticker push 为 ELEMENT translate（已打出组件左滑以保持光标居中），非 camera move → 由 `camera-cursor-tracking` 建模，而非真实 camera 规则。
