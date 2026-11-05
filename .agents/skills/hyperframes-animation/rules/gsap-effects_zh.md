# 适用于 HyperFrames 的 GSAP 效果

即插即用的动画模式。每种效果都是自包含的（HTML + CSS + JS），并遵循 HyperFrames 的 seek 驱动约定 —— 确定性、无随机性，时间轴注册在 `window.__timelines` 上。

## 目录

- [打字机](#typewriter) — 逐字显示文本，可选光标 / 退格 / 词语轮播
- [音频可视化](#audio-visualizer) — 预提取音频数据，由时间轴驱动 Canvas/DOM 渲染

---

## Typewriter

使用 GSAP 的 TextPlugin 逐字显示文本。

### 必需插件

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/TextPlugin.min.js"></script>
<script>
  gsap.registerPlugin(TextPlugin);
</script>
```

### 基础打字机

```js
const text = "Hello, world!";
const cps = 10; // chars per second: 3-5 dramatic, 8-12 conversational, 15-20 energetic
tl.to(
  "#typed-text",
  { text: { value: text }, duration: text.length / cps, ease: "none" },
  startTime,
);
```

### 带闪烁光标

三条规则：

1. **同一时刻只显示一个光标** — 显示下一个之前先隐藏上一个。
2. **空闲时光标必须闪烁** — 打字结束后、暂停期间。
3. **文本与光标之间无间隙** — HTML 中元素必须紧挨排列。

```html
<span id="typed-text"></span><span id="cursor" class="cursor-blink">|</span>
```

```css
@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}
.cursor-blink {
  animation: blink 0.8s step-end infinite;
}
.cursor-solid {
  animation: none;
  opacity: 1;
}
.cursor-hide {
  animation: none;
  opacity: 0;
}
```

模式：闪烁 → 常亮（开始打字）→ 打字 → 常亮 → 闪烁（打字结束）。

```js
tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], startTime);
tl.to("#typed-text", { text: { value: text }, duration: dur, ease: "none" }, startTime);
tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], startTime + dur);
```

### 退格

TextPlugin 从前面删除 —— 不适合退格效果。用手动截断子串：

```js
function backspace(tl, selector, word, startTime, cps) {
  const el = document.querySelector(selector);
  const interval = 1 / cps;
  for (let i = word.length - 1; i >= 0; i--) {
    tl.call(
      () => {
        el.textContent = word.slice(0, i);
      },
      [],
      startTime + (word.length - i) * interval,
    );
  }
  return word.length * interval;
}
```

### 与静态文本的间距

当打字机词语紧挨静态文本时，在包裹用的 `span` 上使用 `margin-left`。不要用 flex 的 `gap`（会把光标与文本拉开），也不要在静态文本末尾加空格（动态 `span` 为空时会被折叠）。

```html
<div style="display:flex; align-items:baseline;">
  <span style="font-size:40px; color:#555;">Ship something</span>
  <span style="margin-left:14px;"><span id="word"></span><span id="cursor">|</span></span>
</div>
```

### 词语轮播

打字 → 保持 → 退格 → 下一个词。在每次空闲时刻（保持、退格后）光标都要闪烁。

```js
let offset = 0;
words.forEach((word, i) => {
  const typeDur = word.length / 10;
  tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], offset);
  tl.to("#typed-text", { text: { value: word }, duration: typeDur, ease: "none" }, offset);
  tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], offset + typeDur);
  offset += typeDur + 1.5; // hold

  if (i < words.length - 1) {
    tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], offset);
    const clearDur = backspace(tl, "#typed-text", word, offset, 20);
    tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], offset + clearDur);
    offset += clearDur + 0.3;
  }
});
```

### 逐词追加

在同一元素中逐词拼成完整句子：

```js
let accumulated = "";
let offset = 0;
words.forEach((word) => {
  const target = accumulated + (accumulated ? " " : "") + word;
  const newChars = target.length - accumulated.length;
  tl.to("#typed-text", { text: { value: target }, duration: newChars / 10, ease: "none" }, offset);
  accumulated = target;
  offset += newChars / 10 + 0.3;
});
```

### 多行光标交接

在打字机行之间交接：隐藏上一行 → 下一行闪烁 → 暂停 → 开始打字时变为常亮。不要 `hidden → solid`（会跳过空闲闪烁）。

```js
tl.call(
  () => {
    prevCursor.classList.replace("cursor-blink", "cursor-hide");
    nextCursor.classList.replace("cursor-hide", "cursor-blink");
  },
  [],
  handoffTime,
);

const typeStart = handoffTime + 0.5; // brief blink pause
tl.call(() => nextCursor.classList.replace("cursor-blink", "cursor-solid"), [], typeStart);
tl.to("#next-text", { text: { value: text }, duration: dur, ease: "none" }, typeStart);
tl.call(() => nextCursor.classList.replace("cursor-solid", "cursor-blink"), [], typeStart + dur);
```

### 节奏参考

| CPS   | 感受             | 适用场景                   |
| ----- | ---------------- | -------------------------- |
| 3-5   | 慢、刻意         | 戏剧性揭示、悬疑           |
| 8-12  | 自然打字         | 对话、旁白                 |
| 15-20 | 快、有劲         | 技术演示、代码             |
| 30+   | 近乎即时         | 填充长文本块               |

---

## Audio Visualizer

预提取音频数据，每帧用一次 `tl.call(...)` 驱动 Canvas / DOM 渲染。**不要**在渲染时使用 Web Audio API —— seek 期间没有实际播放。

### 提取音频数据

使用捆绑的提取脚本（需要 `ffmpeg` 和 Python `numpy`）：

```bash
python skills/hyperframes-creative/scripts/extract-audio-data.py audio.mp3 -o audio-data.json
python skills/hyperframes-creative/scripts/extract-audio-data.py video.mp4 --fps 30 --bands 16 -o audio-data.json
```

### 数据格式

```json
{
  "fps": 30,
  "totalFrames": 5415,
  "frames": [{ "time": 0.0, "rms": 0.42, "bands": [0.8, 0.6, 0.3] }]
}
```

- **`rms`** (0-1) — 整体响度，在整轨上归一化。
- **`bands[]`** (0-1) — 频段幅度。索引 0 = 低音，索引越高 = 高音。各频段独立归一化。

### 加载数据（同步）

```js
// Option A — inline (small files, under ~500 KB)
var AUDIO_DATA = {
  /* paste audio-data.json contents */
};

// Option B — sync XHR (large files; must be synchronous for deterministic timeline construction)
var xhr = new XMLHttpRequest();
xhr.open("GET", "audio-data.json", false);
xhr.send();
var AUDIO_DATA = JSON.parse(xhr.responseText);
```

**不要使用异步 `fetch()`。** HyperFrames 在页面加载后同步读取 `window.__timelines` —— 在 `.then()` 里构建时间轴会导致开始捕获时时间轴尚未就绪。

### 驱动时间轴

**Canvas 2D** — 最常见（柱状图、波形、圆、渐变）：

```js
const canvas = document.getElementById("viz");
const ctx = canvas.getContext("2d");

for (let f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    () => {
      const frame = AUDIO_DATA.frames[f];
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // draw using frame.rms and frame.bands
    },
    [],
    f / AUDIO_DATA.fps,
  );
}
```

**WebGL / Three.js** — HyperFrames 会 patch `THREE.Clock` 以实现确定性时间。每帧根据音频数据更新 uniform。

**DOM 元素** — 元素少于约 20 个时可行，元素很多时比 Canvas 慢。

### 平滑

```js
let prev = null;
const smoothing = 0.25; // 0.1-0.2 snappy, 0.3-0.5 flowing
function smooth(f) {
  const raw = AUDIO_DATA.frames[f];
  if (!prev) {
    prev = { rms: raw.rms, bands: [...raw.bands] };
    return prev;
  }
  prev = {
    rms: prev.rms * smoothing + raw.rms * (1 - smoothing),
    bands: raw.bands.map((b, i) => prev.bands[i] * smoothing + b * (1 - smoothing)),
  };
  return prev;
}
```

### 空间映射

- **水平**：低音在左，高音在右（从左到右遍历 bands）
- **垂直**：低音在下，高音在上
- **环形**：低音在 12 点方向，顺时针展开；镜像可成完整圆

### 运动原则

- **低音驱动大动作** — 缩放、发光、位移。
- **高音驱动细节** — 闪烁、边缘效果。
- **RMS 驱动全局** — 背景亮度、整体能量。
- 选 2–3 个属性做动画，过多会显得杂乱。
- 最小值保持在零以上 —— 安静段落仍要有动感。

### 频段数量

| 频段数 | 细节程度 | 适用场景                   |
| ----- | --------- | -------------------------- |
| 4     | 低        | 背景发光、脉冲             |
| 8     | 中        | 柱状图、基础频谱           |
| 16    | 高        | 精细 EQ（默认）            |
| 32    | 很高      | 密集径向布局               |

### 分层

用 CSS `z-index` 叠多层 canvas 营造纵深 —— 背景层由低音/rms 驱动，前景层由各频段驱动，无需逐元素复杂度也能有层次。

```html
<canvas id="bg-layer" style="position:absolute;top:0;left:0;z-index:1;"></canvas>
<canvas id="main-layer" style="position:absolute;top:0;left:0;z-index:2;"></canvas>
```
