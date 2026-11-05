---
name: hacker-flip-3d
description: 字符级 3D 旋转配合随机字形替换，实现解密揭晓效果。
metadata:
  tags: text, 3d, reveal, decode, hacker, randomization, perspective
---

# Hacker Flip 3D 揭晓

字符从 90° 在 3D 中向下翻转，同时循环显示随机字形，最后定格为目标字符。营造「解密」或机场翻页显示牌（flap-display）式的揭晓感。

## 工作原理

每个字符各自从 `rotateX: 90deg`（隐藏） tween 到 `rotateX: 0deg`（已显示），整词按字符错开。翻转过程中：

1. **阶段 A（0 → 约 `REVEAL_THRESHOLD` 进度）**：字符显示随机替换的字形，并闪烁（每 `FLICKER_RATE` 帧更换一次）
2. **阶段 B（`REVEAL_THRESHOLD` → 1.0 进度）**：字符显示**真实**目标字符，并落到最终直立位置

`REVEAL_THRESHOLD` 区分「乱码」与「揭晓」——当翻转接近完成时，观众会看到正确字母「咔」地就位。

## HTML

```html
<div
  class="scene"
  id="hacker-flip-scene"
  data-composition-id="hacker-flip-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="hacker-text-wrap" id="hacker-text" data-target="{phrase}">
    <!-- Per-char spans get injected by setup script below.
         Ghost placeholder (data-ghost) is rendered identically to reserve width. -->
  </div>
</div>
```

`{phrase}` 是翻转最终解析到的目标词（通常是品牌名或短标签）。

## CSS

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: {bgColor};
  perspective: 1500px; /* REQUIRED — without this rotateX renders flat */
}

.hacker-text-wrap {
  font-family: {monoFont};      /* monospace recommended so flicker glyphs hold width */
  font-weight: 900;
  font-size: HACKER_FONT_SIZE;
  color: {textColor};
  letter-spacing: 4px;
  display: flex;
  /* Ghost / live chars are absolutely stacked; container reserves layout width */
  position: relative;
}

.hacker-char {
  display: inline-block;
  /* Hinge at the bottom edge — flap-display look */
  transform-origin: bottom;
  transform-style: preserve-3d;
  /* Will-change improves render perf */
  will-change: transform, opacity;
}

/* Ghost placeholder is hidden but reserves width for variable-glyph fonts.
   Without this, narrow target glyphs collapse width when displayed and
   characters shift horizontally during flicker. */
.hacker-ghost {
  opacity: 0;
  pointer-events: none;
}
```

## GSAP 时间轴与随机字形逻辑

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};

  const wrap = document.getElementById("hacker-text");
  const targetWord = wrap.dataset.target;
  const GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*";

  // Build live chars + ghost placeholders (ghost keeps layout width stable)
  wrap.innerHTML = "";
  const ghostRow = document.createElement("div");
  ghostRow.className = "hacker-ghost";
  ghostRow.style.display = "inline-flex";
  ghostRow.style.position = "absolute";
  ghostRow.style.left = "0";
  ghostRow.style.top = "0";
  ghostRow.textContent = targetWord;
  wrap.appendChild(ghostRow);

  const charEls = [];
  const liveRow = document.createElement("div");
  liveRow.style.display = "inline-flex";
  liveRow.style.position = "relative";
  for (const ch of targetWord) {
    const span = document.createElement("span");
    span.className = "hacker-char";
    span.textContent = ch === " " ? " " : ch;
    span.dataset.target = ch;
    liveRow.appendChild(span);
    charEls.push(span);
  }
  wrap.appendChild(liveRow);

  // Deterministic "random" — seeded by char index + frame group so the same
  // frame always yields the same glyph (HF seek determinism).
  function pseudoGlyph(seed) {
    const h = ((seed * 9301 + 49297) % 233280) / 233280;
    return GLYPHS[Math.floor(h * GLYPHS.length)];
  }

  const tl = gsap.timeline({ paused: true });

  // Per-char flip — stagger across the word
  charEls.forEach((el, i) => {
    const state = { p: 0 };
    tl.to(
      state,
      {
        p: 1,
        duration: FLIP_DURATION,
        ease: "power3.out",
        onUpdate: () => {
          // Phase A: random glyph flickering. Phase B: real character.
          const progress = state.p;
          if (progress < REVEAL_THRESHOLD) {
            // Update glyph every FLICKER_RATE worth of progress
            const flickerSeed = i * 1000 + Math.floor(progress * 100);
            el.textContent = pseudoGlyph(flickerSeed);
          } else {
            el.textContent = el.dataset.target === " " ? " " : el.dataset.target;
          }
          // Flip rotateX from 90 (down) to 0 (upright)
          const rotateX = 90 - progress * 90;
          const opacity = Math.min(1, progress * 2);
          el.style.transform = `rotateX(${rotateX}deg)`;
          el.style.opacity = opacity;
        },
      },
      i * CHAR_STAGGER,
    );
  });

  window.__timelines["hacker-flip-scene"] = tl;
</script>
```

## 如何选取参数

- **HACKER_FONT_SIZE** — 翻转文字的字号（px）。
  - 范围：视口较小边的 6–10%；翻转文字是视觉焦点，按此比例缩放
  - 约束：ghost 行必须使用相同字号，闪烁过程中布局宽度才稳定
  - 参考：../../examples/proof-logo-chain.html 在 1920×1080 下使用 `163px`
- **FLIP_DURATION** — 单字符翻转 tween 时长。
  - 范围：0.4–1.0s；低于 0.4s 随机字形阶段来不及闪烁，高于 1.0s 显得拖沓
  - 效果：更短更利落、偏现代；更长更机械、偏打字机
  - 参考：../../examples/proof-logo-chain.html 使用 `0.55s`
- **CHAR_STAGGER** — 相邻字符开始翻转的间隔（秒）。
  - 范围：0.03–0.08s；过快字符视觉上重叠，过慢显得费力
  - 约束：总解码时间 = `CHAR_STAGGER × (charCount − 1) + FLIP_DURATION`；须落在阶段时长预算内
  - 参考：../../examples/proof-logo-chain.html 使用 `0.033s`（60fps 下约 2 帧）
- **REVEAL_THRESHOLD** — 字形从随机切换为真实字符的进度点。
  - 范围：0.5–0.7；过低过早揭晓（缺少解密张力），过高像在最后硬切
  - 效果：离散调节观众何时「锁定」真实字母
  - 参考：../../examples/proof-logo-chain.html 使用 `0.6`
- **FLICKER_RATE** — 随机阶段两次字形重排之间的帧数。
  - 范围：3–6；低于 3 像噪声，高于 6 像离散打字而非闪烁
  - 约束：须 ≥ 约 3 帧（见关键约束）
  - 参考：../../examples/proof-logo-chain.html 等价于 `3`（内部时钟每 3 帧洗牌一次）
- **{bgColor} / {textColor}** — 舞台背景与活字符颜色 token。
- **{monoFont}** — 优先等宽字体，避免每次换字形宽度变化；若必须用比例字体，ghost 占位可弥补。
- **{phrase}** — 翻转解析到的目标词。长度通过 `CHAR_STAGGER` 影响总解码时长。

## 变体

- **自上而下铰链** — 将 `transform-origin: bottom` 改为 `top`，呈现下落翻页感。
- **中心旋转** — `transform-origin: center` 读作桶滚，而非翻页。
- **仅数字池** — 将 `GLYPHS` 限制为数字，用于价格/倒计时解码。
- **两段解码** — 串联两个不同字形池的 `FLIP_DURATION` tween（如符号 → 字母 → 真实字符），延长揭晓。

## 核心原则

- **在约 `REVEAL_THRESHOLD` 处**从随机字形切换为真实字形——足够接近落定，让观众 eye 捕捉到正确字母
- **铰链在 `transform-origin: bottom`** 才有翻页显示牌感（`top` 为自上而下，`center` 为旋转）
- **确定性随机**通过 seeded hash——HF 运行时逐帧 seek，同一帧必须显示同一字形（勿用 `Math.random()`）
- **Ghost 占位**与活字符内容相同、字体相同，叠在后方预留宽度——否则窄字形会在闪烁中挤动布局
- **每字符错开 0.04–0.08s**——过快重叠，过慢费力
- **用 `display: grid; place-items: center;` 将翻转置于场景正中**——勿加装饰性页眉/页脚（时间戳行、「// AUTH」标签、小状态点）。翻转文字即焦点；周围杂讯会稀释。若需次要标签，在同一堆叠布局中用大号字（56–72px 大写 + tracking），而非角落小注。

## 关键约束

- **场景根节点必须有 `perspective`**——无父级 perspective 时 `rotateX` 像 2D 缩放，而非 3D 翻转
- **每个字符上 `transform-style: preserve-3d`**——字符自有 transform 时保持 3D 上下文
- **时间轴须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **确定性随机**：勿用 `Math.random()`。用字符索引 + 帧组衍生的 seed，保证 seek 确定性
- **`onUpdate` 写 DOM**：HF 每帧 seek，调用频繁——保持每字符每帧 O(1)
- **闪烁速率 ≥ 约 3 帧/次字形切换**：更快像噪声，更慢像离散打字

## 组合

- [card-morph-anchor.md](card-morph-anchor.md) — 搭配：hacker-flip 揭晓短语后，卡片 morph 到下一场
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 数字揭晓的对应方案（文字 vs 数字）

## 与 HF 技能搭配

- `/hyperframes-animation` — 时间轴 + 逐字符 stagger + `onUpdate`
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
