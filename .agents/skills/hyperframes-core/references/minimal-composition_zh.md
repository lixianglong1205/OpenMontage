# 最小组合

可渲染的最小 HyperFrames 组合 —— 一个独立（顶层）根节点、一个 clip 和一个 tween：

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Minimal HyperFrames Composition</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        background: #0b0f14;
        color: white;
        font-family: Inter, system-ui, sans-serif;
      }
      #root {
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
      }
      .clip {
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
      }
      h1 {
        margin: 0;
        font-size: 96px;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-width="1920"
      data-height="1080"
      data-duration="5"
    >
      <section id="title-card" class="clip" data-start="0" data-duration="5" data-track-index="1">
        <h1 id="title">Hello HyperFrames</h1>
      </section>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      tl.from("#title", { y: 48, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.2);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

必需元素：

- 根 `<div>` 带有 `data-composition-id`、`data-width`、`data-height`、`data-duration`
- 至少一个 clip（任意带有 `data-start`、`data-duration`、`data-track-index` 的元素）
- 以 paused 状态创建的 GSAP 时间轴，注册在 `window.__timelines["<composition-id>"]` 上

此模式为**独立**（顶层 `index.html`）——根节点外围没有 `<template>` 包装。关于子组合（由 `data-composition-src` 加载的文件），见 `sub-compositions.md`。
