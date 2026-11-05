# 全屏动效模式

对于全帧动效（连续背景、色块过渡、跨多个片段的全出血视觉状态），优先采用 **共享背景层 + 透明定时内容层**，而不是堆叠不透明的场景背景。

## 原因

堆叠不透明的场景 `div` 意味着每次场景切换都要重绘整帧，跨场景的视觉连续性只能「伪造」，而每一种「全局」状态（色相偏移、暗角、胶片颗粒）都必须在每个场景上重复实现。由可 seek 的时间轴驱动的共享背景层提供一块连续视觉表面，使场景本身变得轻量且透明。

## 模式

```html
<div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="20">
  <!-- Shared background — NOT a clip. Always visible. Driven by the timeline. -->
  <div id="bg" class="full-bleed"></div>

  <!-- Timed content layers — transparent backgrounds. -->
  <section
    id="scene1"
    class="clip transparent"
    data-start="0"
    data-duration="6"
    data-track-index="1"
  >
    <!-- content -->
  </section>
  <section
    id="scene2"
    class="clip transparent"
    data-start="6"
    data-duration="14"
    data-track-index="1"
  >
    <!-- content -->
  </section>
</div>

<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Drive the shared background from the seekable timeline.
  tl.to("#bg", { backgroundColor: "#0a1530", duration: 6, ease: "sine.inOut" }, 0);
  tl.to("#bg", { backgroundColor: "#1a0a30", duration: 14, ease: "sine.inOut" }, 6);

  // Scene-local animations stay transparent on top.
  tl.from("#scene1 h1", { y: 48, opacity: 0, duration: 0.6 }, 0.2);

  window.__timelines["main"] = tl;
</script>
```

## 规则

- **背景不是 clip。** 不要设置 `data-start` / `data-duration` / `data-track-index`。它在整个 composition 期间始终存在。
- **内容场景使用透明背景。** 共享 `#bg` 上的任何内容都会透过来。
- **在共享层上驱动全局状态。** 色相偏移、暗角、颗粒、胶片风格滤镜 — 在共享层上动画一次即可，不要按场景重复。
- **不要对 `.clip` 元素动画 visibility。** HyperFrames 已根据 `data-start` 和 `data-duration` 显示/隐藏 clip。在 clip 本身上动画 `display` / `visibility` 会与框架自带的显隐逻辑冲突。改为动画 clip 内部的 _子包装元素_。
- **用 snapshot 验证有意溢出。** 在添加 `data-layout-allow-overflow` 以消除 inspect 警告之前，运行 `npx hyperframes snapshot` 并确认溢出符合预期。

## 何时不使用此模式

若场景在视觉上确实彼此独立 — 不同色域之间的硬切、无需连续性 — 堆叠不透明背景的模式即可。共享背景模式适用于背景 **本身就是动效语言的一部分**，而不仅仅是背板的情况。
