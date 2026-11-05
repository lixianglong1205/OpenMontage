---
name: dynamic-content-sequencing
description: 根据内容长度与每项时长配置自动计算时间轴起止时间——较长内容获得更多屏幕时间，无需硬编码数字。
metadata:
  tags: timeline, sequencing, dynamic, duration, content-aware, utility
---

# 动态内容序列

一种实用模式（本身不是动效规则），适用于展示一系列条目（卡片、短语、统计数字等）的场景。每项时长由其内容长度与每项配置共同计算；序列器自动分配绝对起止时间。与 [discrete-text-sequence](discrete-text-sequence.md)（单一文本元素切换状态）不同——本规则在彼此独立的内容块之间切换。

## 工作原理

1. 定义内容数组——每项包含 `{ text, speedFactor, hold }`（或任意字段）
2. 预计算绝对开始时间：`start[i] = sum of durations 0..i-1`
3. 在 onUpdate 中，找出当前活跃项（满足 `start ≤ time` 的最后一项）并渲染

「动态」之处：文本更长的项获得更多屏幕时间（公式：`baseDuration + textLength * msPerChar`）。无需为每项硬编码 `from` / `durationInFrames`。

## HTML

```html
<div
  class="scene"
  id="seq-scene"
  data-composition-id="seq-scene"
  data-start="0"
  data-duration="{DURATION}"
  data-track-index="0"
>
  <div class="display">
    <div class="eyebrow" id="eyebrow">{eyebrow}</div>
    <div class="title" id="title"></div>
    <div class="body" id="body"></div>
    <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
  </div>
  <div class="brand">— {Brand}</div>
</div>
```

## CSS

占位符：`{font}` 为项目无衬线字体栈；`{bgColor1}`/`{bgColor2}` 构成深色背景径向渐变；`{accentColor}` 用于眉标 / 品牌 / 进度条填充高亮；`{textColor}` 为主要可读前景色。

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: radial-gradient(ellipse at center, {bgColor1} 0%, {bgColor2} 70%);
  font-family: {font};
}
.display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  text-align: center;
  max-width: 1400px;
}
.eyebrow {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: 14px;
  color: {accentColor};
  text-transform: uppercase;
}
.title {
  font-size: 120px;
  font-weight: 900;
  letter-spacing: -2px;
  line-height: 1;
  color: {textColor};
}
.body {
  font-size: 48px;
  font-weight: 500;
  line-height: 1.4;
  color: {accentColor};
  opacity: 0.9;
  min-height: 160px; /* reserve space so layout doesn't jump */
}
.progress-bar {
  width: 600px;
  height: 4px;
  background: {accentColor}26; /* ~15% alpha */
  border-radius: 2px;
  margin-top: 16px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, {accentColor} 0%, {accentColor2} 100%);
  width: 0%;
}
.brand {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 32px;
  font-weight: 900;
  letter-spacing: 12px;
  color: {accentColor};
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Content array — N entries, each with its own pacing config.
  // Shape: short eyebrow label, short title, longer body sentence, plus per-entry pacing.
  // The final entry typically uses a larger `hold` (closing beat).
  const CONTENT = [
    {
      eyebrow: "{eyebrow1}",
      title: "{title1}",
      body: "{body1}",
      speedFactor: SPEED_FACTOR,
      hold: HOLD_MID,
    },
    {
      eyebrow: "{eyebrow2}",
      title: "{title2}",
      body: "{body2}",
      speedFactor: SPEED_FACTOR,
      hold: HOLD_MID,
    },
    // …
    {
      eyebrow: "{eyebrowN}",
      title: "{titleN}",
      body: "{bodyN}",
      speedFactor: SPEED_FACTOR,
      hold: HOLD_FINAL,
    },
  ];

  // Pre-compute absolute start times.
  // Duration per entry: BASE_DURATION + body.length * SEC_PER_CHAR + entry.hold seconds.
  // BASE_DURATION, SEC_PER_CHAR documented in How to Choose Values.
  let cumulative = 0;
  const TIMELINE = CONTENT.map((entry) => {
    const dur = BASE_DURATION + entry.body.length * SEC_PER_CHAR + entry.hold;
    const start = cumulative;
    cumulative += dur;
    return { ...entry, start, end: cumulative };
  });

  // Reverse-search current entry
  function entryAt(time) {
    for (let i = TIMELINE.length - 1; i >= 0; i--) {
      if (time >= TIMELINE[i].start) return TIMELINE[i];
    }
    return TIMELINE[0];
  }

  const eyebrowEl = document.getElementById("eyebrow");
  const titleEl = document.getElementById("title");
  const bodyEl = document.getElementById("body");
  const progressEl = document.getElementById("progress-fill");

  const TOTAL_DURATION = cumulative + TAIL_PAD;
  const driver = { t: 0 };
  let lastTitle = "";

  tl.to(
    driver,
    {
      t: TOTAL_DURATION,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        const entry = entryAt(driver.t);
        // Only swap content on transitions (avoid per-frame DOM thrash)
        if (entry.title !== lastTitle) {
          eyebrowEl.textContent = entry.eyebrow;
          titleEl.textContent = entry.title;
          bodyEl.textContent = entry.body;
          lastTitle = entry.title;
        }
        // Progress bar fills 0% → 100% as composition advances
        progressEl.style.width = `${(driver.t / TOTAL_DURATION) * 100}%`;
      },
    },
    0,
  );

  window.__timelines["seq-scene"] = tl;
</script>
```

## 变体

### 项间交叉淡入淡出（非硬切）

在查找函数中加入 `overlap`——在重叠窗口内同时返回前一项与下一项，以交叉淡入淡出透明度渲染：

```js
function activeEntries(time, overlap = 0.3) {
  const result = [];
  TIMELINE.forEach((e) => {
    if (time >= e.start - overlap && time <= e.end + overlap) result.push(e);
  });
  return result;
}
```

然后根据与边界的距离，为相邻两项计算不透明度并渲染。

### 每项动效差异

每项可有独立动效风格。将 `entry.style` 映射到现有规则之一：第 1 章用 [3d-text-depth-layers](3d-text-depth-layers.md)，第 2 章用 [hacker-flip-3d](hacker-flip-3d.md)，第 3 章用 [counting-dynamic-scale](counting-dynamic-scale.md)。序列器只编排时间；每项渲染采用对应规则。

### 自动延长合成时长

若事先不知道序列有多长（动态条目数量），将 `data-duration` 绑定到计算出的 `TOTAL_DURATION`。在时间轴注册**之前**于脚本中完成：

```js
document
  .querySelector("[data-composition-id]")
  .setAttribute("data-duration", String(Math.ceil(TOTAL_DURATION)));
```

（注意：HF 在合成加载时读取 `data-duration`；初始化后再设置可能无效——请根据粗略 TOTAL 计算手动编写 duration。）

## 核心原则

- **时间轴只预计算一次，而非每帧**——在脚本初始化时构建绝对 start/end，使 onUpdate 为 O(log n) 反向查找，而非 O(n²)。
- **每项时长公式：`BASE_DURATION + body.length × SEC_PER_CHAR + hold`**——更长文本需要更多阅读时间。该公式是本规则的核心教学点；各常量的取值范围见「如何选取数值」。
- **为 body 元素预留 `min-height`**——每项内容高度不同；不预留则布局跳动，下游元素（进度条、品牌）会抖动。
- **仅在切换项时更新 DOM，而非每帧**——跟踪 `lastTitle`（或任意键），仅在变化时调用 `textContent =`。每帧赋值 textContent 会在 HF 渲染中产生闪烁。
- **可选进度指示**——底部细条显示 0–100% 可强化「这是一段序列」的观感。
- **高潮停留长于序列中段**——片尾的 `hold`（HOLD_FINAL）应大于序列内的 `hold`（HOLD_MID），使最终品牌/CTA 有足够落点。

## 如何选取数值

- **BASE_DURATION** — 与内容长度无关时，每条目的最短可见时间
  - 范围：0.6–1.5 s
  - 效果：偏低时短条目闪过快，眼睛来不及读；偏高时短标题显得拖沓
  - 约束：保证即使一词条目也有可读时间
  - 参考：见 `../../examples/messaging-multi-phrase.html`（及采用本规则的任意 blueprint）

- **SEC_PER_CHAR** — 每个 body 字符额外增加的时间
  - 范围：0.03–0.06 s/char（视频阅读约 17–33 字/秒）
  - 效果：偏低时段落式 body 显得仓促；偏高时短 body 显得慢
  - 约束：整段序列应统一，使节奏像同一引擎；字符较宽的语言可取范围上沿
  - 参考：见 `../../examples/messaging-multi-phrase.html`（及采用本规则的任意 blueprint）

- **HOLD_MID** — 非最终条目「打字」完成后的停留
  - 范围：0.5–1.0 s
  - 效果：偏低显得赶；偏高显得懒
  - 约束：`HOLD_MID < HOLD_FINAL`
  - 参考：见 `../../examples/messaging-multi-phrase.html`（及采用本规则的任意 blueprint）

- **HOLD_FINAL** — 最后一条目的停留（片尾 / 高潮）
  - 范围：1.0–2.0 s
  - 效果：偏低截断收尾；偏高拖太久
  - 约束：须明显大于 HOLD_MID，使收尾读成一拍而非又一段中段停顿
  - 参考：见 `../../examples/messaging-multi-phrase.html`（及采用本规则的任意 blueprint）

- **SPEED_FACTOR** — 每项节奏倍率
  - 范围：0.5–2.0（默认 1.0）
  - 效果：<1 拉长由 body 驱动的时长（适合高密度段落）；>1 压缩
  - 约束：离散选择——除非某项需特殊节奏否则用 1.0；若每项相同，可并入 SEC_PER_CHAR
  - 参考：见 `../../examples/messaging-multi-phrase.html`（及采用本规则的任意 blueprint）

- **TAIL_PAD** — 最后一条目 `end` 之后加到 `TOTAL_DURATION` 的秒数
  - 范围：0.0–1.0 s
  - 效果：0 表示驱动器恰在最后 `hold` 结束；>0 留安静一拍（适合切到下一段合成前）
  - 约束：若下游还有合成，倾向用 0，在合成接缝处处理「呼吸」
  - 参考：见 `../../examples/messaging-multi-phrase.html`（及采用本规则的任意 blueprint）

- **CONTENT length (N)** — 序列中的条目数
  - 范围：3–6 条
  - 效果：<3 不算序列（用静态场景）；>6 拖长
  - 约束：每项 `title` 在所选 `.title` fontSize 下须单行放得下；body 换行后须落在 `min-height` 内
  - 参考：见 `../../examples/messaging-multi-phrase.html`（及采用本规则的任意 blueprint）

## 关键约束

- **时间轴必须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **预计算 TIMELINE 数组** — 不要在 onUpdate 中重算
- **body 上设置 `min-height`** 以保证布局稳定
- **仅在条目切换时交换 DOM** — 使用 lastTitle/lastKey 守卫
- **仅顺序播放** — 并行轨道需用其他归约方式（本规则面向顺序序列）

## 组合

- [discrete-text-sequence.md](discrete-text-sequence.md) — 每条 body 上的逐字机效果
- [context-sensitive-cursor.md](context-sensitive-cursor.md) — 各章段落的光标颜色
- [vertical-spring-ticker.md](vertical-spring-ticker.md) — 项间词语弹簧过渡（替代硬切）
- [scale-swap-transition.md](scale-swap-transition.md) — 条目间的视觉 morph

## 与 HF 技能搭配

- `/hyperframes-animation` — 单一 driver、反向查找分发
- `/hyperframes-core` — 合成接线
- `/hyperframes-cli` — `hyperframes lint`
