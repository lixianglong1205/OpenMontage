---
name: asr-keyword-glow
description: 关键词在「被说出」时发光并放大——attack/sustain/release 包络与逐词时间戳同步。即使没有真实音频，硬编码时间也能营造「旁白强调」效果。
metadata:
  tags: asr, audio-sync, highlight, glow, keyword, text, speech, emphasis
---

# ASR 关键词发光

短语中的每个词在「被说出」时会视觉激活（发光模糊 + 缩放），遵循 attack-sustain-release（类 ASR）包络。在真实 ASR 流水线中，这些时间来自词级转写数据；在宣传片中，可硬编码时间以控制强调节奏。包络在词结束后仍保留 subtle 的「余辉」，形成近期强调的 breadcrumb。

## 工作原理

每个词有 `{ start, end }` 时间戳。在每一帧计算该词的包络值：

- **开始前** → 0（尚未开始）
- **开始 → 峰值** → attack（线性 0 → 1）
- **峰值 → 结束** → sustain（保持 1）
- **结束 → 结束+release** → decay（1 → restLevel，通常 0.25）
- **release 之后** → restLevel（保持 subtle 高亮）

包络同时驱动 `textShadow` 模糊半径与 `scale`。模糊越大、缩放越大 = 「正在说」的强调感。

## HTML

```html
<div
  class="scene"
  id="asr-scene"
  data-composition-id="asr-scene"
  data-start="0"
  data-duration="6"
  data-track-index="0"
>
  <div class="phrase">
    <!-- One <span class="word"> per word in {phrase}. data-word is a
         stable key used to look up the word's ASR timing in JS. The
         final word may be a {brandWord}, which gets longer emphasis
         and the .brand modifier. -->
    <span class="word" data-word="{w1Key}">{w1}</span>
    <span class="word" data-word="{w2Key}">{w2}</span>
    <!-- … -->
    <span class="word brand" data-word="{brandKey}">{brandWord}</span>
  </div>
</div>
```

## CSS

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: {sceneBackgroundColor};
  font-family: {font};
}
.phrase {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  justify-content: center;
  max-width: 1700px;
  font-size: 120px;
  font-weight: 900;
  letter-spacing: 2px;
  color: {restColor};
  text-align: center;
  line-height: 1.2;
}
.word {
  display: inline-block;
  transform-origin: 50% 50%;
  /* Initial subtle rest glow */
  text-shadow: 0 0 0 {glowColorTransparent};
  will-change: transform, text-shadow;
}
.word.brand {
  color: {brandAccentColor};
  letter-spacing: 12px;
  text-transform: uppercase;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Per-word "spoken" times — author these to control narrator pacing.
  // Shape: { [wordKey]: { start, end } } in local seconds. One entry
  // per <span class="word" data-word="…">. The brand word's window is
  // typically 1.5-2× as long as a normal word.
  const TIMINGS = {
    // {w1Key}: { start: …, end: … },
    // {w2Key}: { start: …, end: … },
    // …
    // {brandKey}: { start: …, end: … },
  };

  function envelope(time, start, end) {
    const releaseEnd = end + RELEASE;
    if (time < start) return 0;
    if (time < end) {
      // attack — linear ramp over ATTACK_DUR then sustain
      const attack = Math.min((time - start) / ATTACK_DUR, 1);
      return attack;
    }
    if (time < releaseEnd) {
      // decay to rest level
      const decay = (time - end) / RELEASE;
      return 1 - decay * (1 - REST_LEVEL);
    }
    return REST_LEVEL;
  }

  const words = document.querySelectorAll(".word");

  // Single driver — 0 → composition duration
  const driver = { t: 0 };
  tl.to(
    driver,
    {
      t: SCENE_DURATION,
      duration: SCENE_DURATION,
      ease: "none",
      onUpdate: () => {
        words.forEach((el) => {
          const word = el.dataset.word;
          const timing = TIMINGS[word];
          if (!timing) return;
          const env = envelope(driver.t, timing.start, timing.end);
          const blur = MAX_BLUR * env;
          const scale = 1 + MAX_SCALE_BOOST * env;
          el.style.textShadow = `0 0 ${blur}px ${glowColorRgba(env)}`;
          el.style.transform = `scale(${scale})`;
        });
      },
    },
    0,
  );

  window.__timelines["asr-scene"] = tl;
</script>
```

`glowColorRgba(env)` 返回品牌发光色，alpha 随 `env` 调制（例如 `rgba({glowR}, {glowG}, {glowB}, ${GLOW_ALPHA_BASE + env * GLOW_ALPHA_RANGE})`）。

## 变体

### 多倍频发光（峰值更 dramatic）

在 sustain 阶段将包络驱动的模糊与 sin 脉冲叠加——高强调词在峰值处「呼吸」。正弦频率 `PULSE_HZ` 控制 sustain 窗口内呼吸次数；振幅 `PULSE_AMPLITUDE` 控制呼吸可见度。

```js
const sustain = env * (1 + Math.sin(driver.t * PULSE_HZ) * PULSE_AMPLITUDE);
const blur = MAX_BLUR * sustain;
```

### 峰值颜色过渡

活跃词随 `env` 上升从 `restColor` 线性插值到 `peakColor`，回到 rest 时 settle 回 `restColor`：

```js
function lerpChannel(a, b, t) {
  return Math.round(a + (b - a) * t);
}
el.style.color = `rgb(${lerpChannel(REST_RGB.r, PEAK_RGB.r, env)}, ${lerpChannel(REST_RGB.g, PEAK_RGB.g, env)}, ${lerpChannel(REST_RGB.b, PEAK_RGB.b, env)})`;
```

### 卡拉 OK 风格（暗 rest + 亮 active，视频旁白推荐）

默认幅度（小 MAX_BLUR、小 MAX_SCALE_BOOST、rest 文本全白）在视频中显得过 subtle——未激活词仍占主导。卡拉 OK 风格修正这一点：**未激活词渲染为 DIM**，激活词 **向亮白 + 更大 scale 插值**：

```js
// Tunable constants — see How to Choose Values
// REST_RGB    — dim color for inactive words
// ACTIVE_RGB  — bright color at peak (non-brand)
// BRAND_RGB   — bright color at peak (brand word)
// MAX_BLUR, MAX_SCALE_BOOST, REST_LEVEL all pushed higher than default

function lerpChannel(a, b, t) {
  return Math.round(a + (b - a) * t);
}
function colorAt(env, isBrand) {
  const target = isBrand ? BRAND_RGB : ACTIVE_RGB;
  return `rgb(${lerpChannel(REST_RGB.r, target.r, env)}, ${lerpChannel(REST_RGB.g, target.g, env)}, ${lerpChannel(REST_RGB.b, target.b, env)})`;
}

// In onUpdate:
el.style.color = colorAt(env, el.classList.contains("brand"));
```

视觉效果：任意时刻 1–2 个词亮且发光（正在说的词 + 刚说完词的 lingering rest），短语其余部分 dim。这比 subtle 的「人人半发光」基线更接近真实卡拉 OK / 歌词视频美学。

何时用卡拉 OK vs 默认：短旁白短语（5–10 词）且需逐词清晰 POP → 卡拉 OK。长 dense 文本、多词 subtle 强调 → 默认 subtle。卡拉 OK 会推高 MAX_BLUR、MAX_SCALE_BOOST 以及 REST_RGB 与 ACTIVE_RGB 的对比；其余逻辑相同。

### 3D 弹出

包络与 `translateZ` 组合，使词在「说」时向镜头「前倾」：

```js
const popZ = env * MAX_POP_Z;
el.style.transform = `translateZ(${popZ}px) scale(${scale})`;
```

父元素需设置 `perspective`。

### 来自真实 ASR 转写

真实 ASR 场景下，用转写 JSON 替换硬编码 TIMINGS（每项含 `word`、`start_ms`、`end_ms`）。转为秒后以相同方式喂入。形状 `{ [wordKey]: { start, end } }` 在手写或从 `hyperframes transcribe` 派生时一致。

## 如何选取数值

- **TIMINGS** — 逐词 `{ start, end }` 映射。每个 `.word` span 写一条。
  - 形状：`{ wordKey: { start: number, end: number } }`，均为场景本地秒。
  - 约束：单调不重叠——每条 `end < 下一条 start`（重叠窗口会使包络歧义）。
  - 品牌词窗口：通常为非品牌词平均窗口的 1.5–2×，使品牌 sustain 更长。
- **ATTACK_DUR** — 词开始后包络 0 → 1 的秒数。
  - 范围：0.1–0.25 s
  - 效果：更短更 punchy、类 ASR；更长更平滑。
  - 约束：须 <（最短词的 end - start），否则词达不到 1。
- **RELEASE** — 词结束后包络 1 → REST_LEVEL 的秒数。
  - 范围：0.2–0.5 s
- **REST_LEVEL** — RELEASE 后保持的包络值。
  - 范围：0.15–0.4（默认风格）；0.05–0.2（卡拉 OK——更 dim 的 rest）。
  - 效果：更低 = 更 quiet 的 breadcrumb；更高 = 刚说过的词保持更亮。
  - 约束：须 < 1；应 > 0 以保留 breadcrumb。
- **MAX_BLUR** — 峰值 `text-shadow` 模糊半径（px）。
  - 范围：15–25 px（默认）；30–45 px（卡拉 OK）。
  - 效果：更大像「喊」；更小像「中性旁白」。
- **MAX_SCALE_BOOST** — 峰值附加 scale（如 0.08 ⇒ 1.0 → 1.08）。
  - 范围：0.03–0.10（默认）；0.15–0.25（卡拉 OK）。
  - 效果：更大更「弹」；更小「仅发光」。
- **SCENE_DURATION** — 单一 driver tween 的总秒数。
  - 约束：须等于场景 `data-duration`，使 driver `t` 与 HF seek 同步到达 TIMINGS 末尾。
- **REST_RGB / ACTIVE_RGB / BRAND_RGB**（卡拉 OK）— 离散颜色，非数值。
  - REST_RGB：品牌调色板中性 dim 色；应读作 off-white-ish dim，非黑。
  - ACTIVE_RGB：峰值时品牌文本色，全可读。
  - BRAND_RGB：品牌 accent（常与 glow 同色）。
- **PULSE_HZ / PULSE_AMPLITUDE**（多倍频变体）— 正弦呼吸频率/深度。
  - PULSE_HZ：4–10 rad/s；PULSE_AMPLITUDE：0.1–0.3。
- **MAX_POP_Z**（3D 弹出变体）— 峰值最大 Z 平移（px）。
  - 范围：20–60 px；父级需 `perspective`。

Ease 族——离散选择：

- 单一线性 driver（`ease: "none"`），使 `t` 与场景时间 1:1。其他 ease 会扭曲逐词包络形状——勿改。

## 关键原则

- **包络形状：attack-sustain-decay-rest** — 词结束后勿归零。rest level（REST_LEVEL > 0）使刚说过的词保持 subtle 高亮，形成注意力 breadcrumb。
- **品牌词强调更长（1.5–2× 普通词）** — 品牌是 headline；让其 sustain。
- **每个词 `display: inline-block`** — `<span>` 上 `transform` 生效所需。
- **除非采用卡拉 OK，MAX_BLUR 与 MAX_SCALE_BOOST 保持在默认范围** — 介于默认与卡拉 OK 之间的值会得到 awkward 的「半大声」强调。
- **逐词 `text-shadow`（非 `box-shadow`）** — text-shadow 是 GLYPH 周围的发光，才读作「说话强调」。box-shadow 会照 inline-block 包围盒（矩形）发光。
- **单一 driver、多词 onUpdate** — 一个 tween 遍历所有词。勿每词一个 tween——60+ 词时时间线难维护。
- **❗ 高潮停留 ≥1s** — 最后一词强调后，composition 继续 ≥1s。最后一词即 headline beat。

## 关键约束

- **Timeline 须 paused**：`gsap.timeline({ paused: true })`
- **Registry key = `data-composition-id`**
- **词元素上无 CSS animation**
- **每个 `.word` 上 `display: inline-block`**
- **每个 `.word` 上 `will-change: transform, text-shadow`**
- **时间单调**（后 start > 前 end）——重叠词会破坏包络

## 组合

- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 活跃词在峰值获得 depth 分层强调
- [sine-wave-loop.md](sine-wave-loop.md) — 非活跃词在强调间隙 subtle 呼吸
- [context-sensitive-cursor.md](context-sensitive-cursor.md) — 打字机按 ASR 节奏逐词打出

## 搭配的 HF skills

- `/hyperframes-animation` — 单一 driver、多元素包络
- `/hyperframes-media` — `hyperframes transcribe` 输出真实 ASR 数据
- `/hyperframes-media` — 与字幕渲染搭配
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
