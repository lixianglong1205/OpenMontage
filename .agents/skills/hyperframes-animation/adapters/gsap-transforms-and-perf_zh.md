# 变换与性能

## 变换别名

优先使用 GSAP 的变换别名，而非原始 `transform` 字符串：

| GSAP 属性                   | 等价项                |
| --------------------------- | --------------------- |
| `x`, `y`, `z`               | `translateX/Y/Z` (px) |
| `xPercent`, `yPercent`      | `translateX/Y` in `%` |
| `scale`, `scaleX`, `scaleY` | `scale`               |
| `rotation`                  | `rotate` (deg)        |
| `rotationX`, `rotationY`    | 3D 旋转               |
| `skewX`, `skewY`            | `skew`                |
| `transformOrigin`           | `transform-origin`    |

别名让 GSAP 独立追踪并插值各轴，避免对同一元素的多个补间之间发生意外覆盖。

## autoAlpha

显示/隐藏时优先使用 `autoAlpha`，而非 `opacity`：

```javascript
gsap.to(".panel", { autoAlpha: 0, duration: 0.4 });
```

`autoAlpha: 0` 会同时设置 `opacity: 0` 和 `visibility: hidden`，在 alpha 为零时会让元素退出命中测试与无障碍树——比普通 `opacity: 0` 更接近「真正消失」。

## clearProps

补间完成时移除 GSAP 设置的内联样式：

```javascript
gsap.to(".item", { x: 100, rotation: 45, clearProps: "all" });
gsap.to(".item", { x: 100, rotation: 45, clearProps: "rotation,x" });
```

适用于动画段落结束时，将元素交还给 CSS 控制。

## CSS 变量

```javascript
gsap.to(".chart", { "--hue": 180, duration: 1 });
```

可动画化任意自定义属性。适用于颜色、长度、数值——凡是 CSS 能够插值的属性均可。

## 相对值与方向值

- 相对值：`"+=20"`、`"-=10"`、`"*=2"`。
- 方向旋转：`"360_cw"`、`"-170_short"`、`"90_ccw"` — 控制在两个值之间插值时旋转走哪条路径。

## SVG 要点

- `svgOrigin` 在 SVG 的全局坐标空间中设置变换原点（而非元素本地盒）。**不要**在同一元素上同时使用 `svgOrigin` 与 `transformOrigin`——二选一。
- 通过相同的别名（`x`、`y`、`rotation`）动画 SVG 变换属性——GSAP 会处理 SVG 特有的细节。

## 性能规则

### 优先使用变换与 opacity

动画 `x`、`y`、`scale`、`rotation`、`opacity` 会留在 GPU 合成层。若变换能达到同样效果，避免动画 `width`、`height`、`top`、`left`、`margin`、`padding`。

### will-change（慎用）

```css
.title {
  will-change: transform;
}
```

仅用于**确实**会动画的元素。到处滥用会失效并浪费内存。

### gsap.quickTo 用于高频更新（仅预览）

对于由**事件**驱动的高频更新——指针移动、滚动、音频 scrub——`quickTo` 复用同一补间，而不是每帧新建：

```javascript
const xTo = gsap.quickTo("#cursor", "x", { duration: 0.4, ease: "power3" });
const yTo = gsap.quickTo("#cursor", "y", { duration: 0.4, ease: "power3" });

container.addEventListener("mousemove", (e) => {
  xTo(e.pageX);
  yTo(e.pageY);
});
```

> **注意：** 渲染模式没有输入事件。渲染器按帧 seek；`mousemove`、`scroll` 等永远不会触发。`quickTo` 的主要用途仅限浏览器中的**实时预览**。要在渲染里做音频驱动动画，需预先提取音频数据并以声明式驱动时间轴（见 `../rules/gsap-effects.md`）。

### stagger 优于 N 个补间

一个带 `stagger` 的补间在可读性与运行时开销上都优于带手动 delay 的 N 个补间。

### 清理

在实时预览中，暂停或对屏外动画执行 `kill()`。渲染模式不受影响（渲染器直接驱动时间）。
