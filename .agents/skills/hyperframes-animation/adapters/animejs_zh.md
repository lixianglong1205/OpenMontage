---
name: hyperframes-animejs
description: HyperFrames 的 Anime.js 适配器模式。在 HyperFrames 合成内编写 Anime.js 动画或时间轴、在 window.__hfAnime 上注册动画、使 Anime.js 由 seek 驱动且可确定、或将 Anime.js 示例翻译为适合渲染的 HyperFrames HTML 时使用。
---

# HyperFrames 中的 Anime.js

HyperFrames 可通过 `animejs` 运行时适配器对 Anime.js 实例进行 seek。合成拥有动画对象；HyperFrames 拥有时钟。

## 约定

- 在合成初始化期间同步创建动画或时间轴。
- 设置 `autoplay: false`，使 Anime.js 不会按自身时钟推进。
- 将每个返回的动画或时间轴注册到 `window.__hfAnime`。
- 使用有限时长与循环次数。
- 避免基于挂钟时间、网络状态或未设种随机数而变更 DOM 的回调。

适配器通过 `instance.seek(timeMs)` 对所有已注册实例进行 seek，其中 `timeMs` 为 HyperFrames 时间（毫秒）。

## 基本模式

```html
<script src="https://cdn.jsdelivr.net/npm/animejs@4.0.2/lib/anime.iife.min.js"></script>
<script>
  const anim = anime({
    targets: ".mark",
    translateX: 280,
    rotate: "1turn",
    opacity: [0, 1],
    duration: 1200,
    easing: "easeOutExpo",
    autoplay: false,
  });

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(anim);
</script>
```

## 时间轴模式

```html
<script>
  const tl = anime.timeline({
    autoplay: false,
    easing: "easeOutCubic",
  });

  tl.add({
    targets: ".title",
    translateY: [40, 0],
    opacity: [0, 1],
    duration: 650,
  }).add(
    {
      targets: ".accent",
      scaleX: [0, 1],
      duration: 450,
    },
    250,
  );

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(tl);
</script>
```

## 模块构建

若使用 ES 模块构建，适配器不关心实例如何创建。它只要求返回的对象暴露 `seek()`、`pause()`，最好还有 `play()`：

```html
<script type="module">
  import { animate } from "https://cdn.jsdelivr.net/npm/animejs/+esm";

  const anim = animate(".chip", {
    x: "18rem",
    duration: 900,
    autoplay: false,
  });

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(anim);
</script>
```

## 适用场景

- Anime.js 语法紧凑的小型 SVG 与 DOM 点缀动画。
- 可改为 seek 驱动的导入 Anime.js 示例。
- 多个独立微动画推入同一注册表。

除非用户明确要求 Anime.js，复杂场景编排请用 GSAP。GSAP 仍是 HyperFrames 的主要创作路径。

## 避免

- 保留 Anime.js 默认的 `autoplay`。
- 依赖 `anime.running` 自动发现，而非显式 `window.__hfAnime.push(...)`。
- 无限循环。根据合成时长计算有限重复次数。
- 在定时器、Promise、事件处理器中构建动画，或在异步资源加载之后构建。

## 校验

编辑使用 Anime.js 的合成后：

```bash
npx hyperframes lint
npx hyperframes validate
```

## 致谢与参考

- HyperFrames 适配器源码：`packages/core/src/runtime/adapters/animejs.ts`。
- Anime.js 关于 `autoplay`、`pause()` 与 `seek()` 的文档：https://animejs.com/documentation/
