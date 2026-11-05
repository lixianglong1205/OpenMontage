# 合成模式

## 目录

- 画中画
- 主体后文字
- 带淡入淡出的标题卡
- 带章节标题的幻灯片
- 顶层合成示例

## 画中画（Video in a Frame）

对包裹层 div 做位置/尺寸动画。视频填满包裹层。包裹层**不要**加任何 `data-*` 属性。

```html
<div
  id="pip-frame"
  style="position:absolute;top:0;left:0;width:1920px;height:1080px;z-index:50;overflow:hidden;"
>
  <video
    id="el-video"
    data-start="0"
    data-duration="60"
    data-track-index="0"
    src="talking-head.mp4"
    muted
    playsinline
  ></video>
</div>
```

```js
tl.to(
  "#pip-frame",
  { top: 700, left: 1360, width: 500, height: 280, borderRadius: 16, duration: 1 },
  10,
);
tl.to("#pip-frame", { left: 40, duration: 0.6 }, 30);
```

## 主体后文字（透明 webm 叠加）

将标题 headline 放在主讲人 _后面_，使其轮廓遮挡文字。需要先用 `npx hyperframes remove-background presenter.mp4 -o presenter.webm` 生成透明抠像。

三层结构，外加一条关键规则：

```html
<!-- z=1 底层 — 完整不透明 mp4（场景 + 主讲人），始终可见 -->
<video
  id="cf-base"
  data-start="0"
  data-duration="6"
  data-media-start="0"
  data-track-index="0"
  src="presenter.mp4"
  muted
  playsinline
></video>

<!-- z=2 标题 — 全程可见 -->
<h1
  id="cf-headline"
  style="position:absolute;top:50%;left:50%;
     transform:translate(-50%,-50%); z-index:2; font-size:220px; font-weight:900;
     color:#fff; text-shadow:0 6px 32px rgba(0,0,0,.55); clip-path:inset(0 0 100% 0);"
>
  MAKE IT IN HYPERFRAMES
</h1>

<!-- z=3 抠像 — 同源、主讲人周围带 alpha，切换前隐藏 -->
<!-- 透明度加在 WRAPPER 上，不要加在 video 本身（见下方规则）。 -->
<div class="cutout-wrap" style="position:absolute;inset:0;z-index:3;opacity:0">
  <video
    id="cf-cutout"
    data-start="0"
    data-duration="6"
    data-media-start="0"
    data-track-index="1"
    src="presenter.webm"
    muted
    playsinline
  ></video>
</div>
```

```js
const tl = gsap.timeline({ paused: true });
const CUT = 3.3;

// 尽早露出标题
tl.to("#cf-headline", { clipPath: "inset(0 0 0% 0)", duration: 0.6, ease: "expo.out" }, 0.25);

// 在切换点让抠像包裹层可见 — 主讲人轮廓
// 从标题中「穿」出来。
tl.set(".cutout-wrap", { opacity: 1 }, CUT);

// 哨兵：将时间轴延伸到合成的完整时长，避免
// 渲染器在最后一个有意义 tween 之后提前结束。
tl.set({}, {}, 6);

window.__timelines["cover-flip"] = tl;
```

**为什么用 wrapper div，而不是直接给 video 设 opacity？**

框架在带 `data-start`/`data-duration` 的元素处于「激活」状态时会强制 `opacity: 1` — 这是它管理片段生命周期的方式。写在 video 元素上的 CSS `opacity: 0` 会被静默覆盖。把 video 包在一个没有 `data-*` 属性的 div 里；包裹层由你的 CSS/GSAP 控制。

**为什么两个 video 都是 `data-start="0"`？**

这样两者从 t=0 起同步解码。若抠像晚挂载（`data-start=3.3`），Chrome 会在挂载时 seek + 预热解码器，可能与底层 mp4 差一帧 — 切换处会出现单帧抖动。

**色彩匹配：** `remove-background` 默认 `--quality balanced`（crf 18），抠像的 RGB 与源 mp4 几乎一致 — 叠加时边缘光晕或色偏最小。英雄镜头可用 `--quality best`（crf 12）；仅当抠像叠在 _不同_ 背景上且体积敏感时，再降到 `--quality fast`（crf 30）。

## 带淡入淡出的标题卡

```html
<div
  id="title-card"
  data-start="0"
  data-duration="5"
  data-track-index="5"
  style="display:flex;align-items:center;justify-content:center;background:#111;z-index:60;"
>
  <h1 style="font-size:64px;color:#fff;opacity:0;">My Video Title</h1>
</div>
```

```js
tl.to("#title-card h1", { opacity: 1, duration: 0.6 }, 0.3);
tl.to("#title-card", { opacity: 0, duration: 0.5 }, 4);
```

## 带章节标题的幻灯片

在同一轨道上使用多个独立元素，各自拥有时间范围。幻灯片根据 `data-start`/`data-duration` 自动挂载/卸载。

```html
<div class="slide" data-start="0" data-duration="30" data-track-index="3">...</div>
<div class="slide" data-start="30" data-duration="25" data-track-index="3">...</div>
<div class="slide" data-start="55" data-duration="20" data-track-index="3">...</div>
```

## 顶层合成示例

```html
<div
  id="comp-1"
  data-composition-id="my-video"
  data-start="0"
  data-duration="60"
  data-width="1920"
  data-height="1080"
>
  <!-- Primitive clips -->
  <video
    id="el-1"
    data-start="0"
    data-duration="10"
    data-track-index="0"
    src="..."
    muted
    playsinline
  ></video>
  <video
    id="el-2"
    data-start="el-1"
    data-duration="8"
    data-track-index="0"
    src="..."
    muted
    playsinline
  ></video>
  <img id="el-3" data-start="5" data-duration="4" data-track-index="1" src="..." />
  <audio id="el-4" data-start="0" data-duration="30" data-track-index="2" src="..." />

  <!-- Sub-compositions loaded from files -->
  <div
    id="el-5"
    data-composition-id="intro-anim"
    data-composition-src="compositions/intro-anim.html"
    data-start="0"
    data-track-index="3"
  ></div>

  <div
    id="el-6"
    data-composition-id="captions"
    data-composition-src="compositions/caption-overlay.html"
    data-start="0"
    data-track-index="4"
  ></div>

  <script>
    // Just register the timeline — framework auto-nests sub-compositions
    const tl = gsap.timeline({ paused: true });
    window.__timelines["my-video"] = tl;
  </script>
</div>
```
