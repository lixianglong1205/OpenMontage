## 失真

### Glitch

RGB 色调叠加层（不要使用 multiply 混合——以 35% 不透明度采用 normal 混合）会以较大偏移量抖动。场景本身也会抖动。

```js
tl.set("#glitch-r", { opacity: 1, x: 40, y: -8 }, T);
tl.set("#glitch-g", { opacity: 1, x: -30, y: 12 }, T);
tl.set("#glitch-b", { opacity: 1, x: 15, y: -20 }, T);
tl.set(old, { x: -15 }, T);
// 6 jitter frames at 0.03s intervals with big offsets (±30-60px)
// ... swap and clear at T + 0.2
```

### 色差（Chromatic Aberration）

RGB 叠加层起始对齐，随后分开（±80px），场景淡出，再汇聚到新场景。

```js
tl.set("#glitch-r", { opacity: 0.6, x: 0 }, T);
tl.set("#glitch-g", { opacity: 0.6, x: 0 }, T);
tl.set("#glitch-b", { opacity: 0.6, x: 0 }, T);
tl.to("#glitch-r", { x: -80, opacity: 0.8, duration: 0.3, ease: "power2.in" }, T);
tl.to("#glitch-b", { x: 80, opacity: 0.8, duration: 0.3, ease: "power2.in" }, T);
tl.to("#glitch-g", { y: 30, duration: 0.3, ease: "power2.in" }, T);
// Swap at T + 0.3, converge back at T + 0.3
```

### 波纹（Ripple）

快速振荡（±30px）+ 缩放失真（0.97–1.03）+ 渐强模糊。在失真峰值处切换。

```js
tl.to(old, { x: 30, scale: 1.02, duration: 0.04, ease: "none" }, T);
tl.to(old, { x: -25, scale: 0.98, filter: "blur(4px)", duration: 0.04, ease: "none" }, T + 0.04);
// ... more oscillations with increasing blur
// Swap at peak, incoming stabilizes with decreasing wobble
```

### VHS 磁带

将场景克隆为 20 条水平条带（每条 54px，clip-path 裁切）。各条带在 per-bar 随机间隔上以种子伪随机偏移独立移动 x。在每条带上添加红+蓝色差偏移副本（z-index 高于主层，35% 不透明度）。条带宽度大于画面（2020px，left:-50px），以免边缘露出。

克隆实现模式见 SKILL.md。
