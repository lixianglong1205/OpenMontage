---
name: hyperframes-css-animations
description: HyperFrames 的 CSS 动画适配器模式。在编写 CSS 关键帧、基于 animation-delay 的时序、animation-fill-mode、animation-play-state，或 HyperFrames 必须在预览与渲染期间可确定性 seek 的纯 CSS 动效时使用。
---

# HyperFrames 的 CSS 动画

HyperFrames 可通过 `css` 运行时适配器对 CSS 关键帧动画进行 seek。适用于简单重复图案、背景动效、 shimmer、发光、遮罩以及非序列化装饰。

场景编排通常用 GSAP 更清晰。CSS 动画最适合动效属于单个元素且时长固定的场景。

## 约定

- 在运行时初始化完成前，将待动画元素放入 DOM。
- 为带时序的元素设置 `data-start`，使局部动画时间与片段对齐。
- 使用有限的 `animation-duration` 与 `animation-iteration-count`，因为在没有 WAAPI 支持的 CSS 动画环境中，负 delay 回退无法表示无界时长。
- 优先使用 `animation-fill-mode: both`，以便 seek 后的状态在动效前后都能保持。
- 避免依赖墙钟时间的 JavaScript、由 hover 触发的状态，以及依赖用户事件的 class 切换。

适配器会查找具有计算后 `animation-name` 的元素，在可用时 seek 其浏览器 `Animation` 句柄，否则回退为通过负 `animation-delay` 暂停。

## 基础模式

```html
<div
  id="pulse-ring"
  class="clip pulse-ring"
  data-start="0"
  data-duration="4"
  data-track-index="2"
></div>

<style>
  .pulse-ring {
    width: 280px;
    height: 280px;
    border: 4px solid rgba(255, 255, 255, 0.7);
    border-radius: 50%;
    animation-name: pulse-ring;
    animation-duration: 1200ms;
    animation-timing-function: cubic-bezier(0.2, 0, 0, 1);
    animation-iteration-count: 3;
    animation-fill-mode: both;
  }

  @keyframes pulse-ring {
    from {
      opacity: 0;
      transform: scale(0.82);
    }
    35% {
      opacity: 1;
    }
    to {
      opacity: 0;
      transform: scale(1.18);
    }
  }
</style>
```

## 交错模式

使用 CSS 自定义属性，避免重复关键帧：

```html
<div class="clip dots" data-start="1" data-duration="3" data-track-index="3">
  <span style="--i: 0"></span>
  <span style="--i: 1"></span>
  <span style="--i: 2"></span>
</div>

<style>
  .dots span {
    display: inline-block;
    width: 18px;
    height: 18px;
    margin-right: 10px;
    border-radius: 50%;
    background: currentColor;
    animation: dot-pop 900ms ease-out both;
    animation-delay: calc(var(--i) * 120ms);
  }

  @keyframes dot-pop {
    from {
      opacity: 0;
      transform: translateY(18px) scale(0.75);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }
</style>
```

## 适用场景

- 已知重复次数的装饰性循环。
- 遮罩、发光、 shimmer、颗粒与 subtle 视差层。
- 简单单元素入场，完整 JS 时间轴会显得过重时。

## 避免

- 无限循环 CSS 动画，除非已确认浏览器暴露可 seek 的 WAAPI 支持的 CSS 动画句柄。更宜使用覆盖可见时长的有限迭代次数。
- 在 transform 可行时仍动画化 `top`、`left`、`width` 或 `height` 等布局属性。
- 依赖 hover、focus、滚动或媒体查询触发渲染关键动效。
- 启动后更改动画 class，除非另有确定性时间轴控制该变更。

## 校验

编辑 CSS 动画合成后：

```bash
npx hyperframes lint
npx hyperframes validate
```

## 致谢与参考

- HyperFrames 适配器源码：`packages/core/src/runtime/adapters/css.ts`。
- MDN CSS animation 文档：https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation
- MDN `animation-fill-mode`：https://developer.mozilla.org/en-US/docs/Web/CSS/animation-fill-mode
