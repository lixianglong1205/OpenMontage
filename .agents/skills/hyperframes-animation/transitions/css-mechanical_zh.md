## 机械式

### 快门

两扇全屏遮罩分别从顶部和底部向中间闭合，在中间相遇。在完全闭合时切换画面，再重新打开。

```js
tl.to("#shutter-top", { y: 0, duration: 0.25, ease: "power3.in" }, T);
tl.to("#shutter-bot", { y: 0, duration: 0.25, ease: "power3.in" }, T);
tl.set(old, { opacity: 0 }, T + 0.25);
tl.set(new, { opacity: 1 }, T + 0.25);
tl.to("#shutter-top", { y: -540, duration: 0.25, ease: "power3.out" }, T + 0.3);
tl.to("#shutter-bot", { y: 540, duration: 0.25, ease: "power3.out" }, T + 0.3);
```

### 时钟擦除

径向多边形扫过，逐步穿越各象限。使用 9 点多边形，并在边缘设置中间顶点位置，以实现平滑扫过。

```js
tl.set(new, { opacity: 1, zIndex: 10 }, T);
var d = 0.1; // duration per quadrant
tl.set(new, { clipPath: "polygon(50% 50%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%)" }, T);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 50%, 100% 50%, 100% 50%, 100% 50%, 100% 50%)", duration: d, ease: "none" }, T);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 50% 100%, 50% 100%, 50% 100%)", duration: d, ease: "none" }, T + d);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 0% 100%, 0% 50%, 0% 50%)", duration: d, ease: "none" }, T + d*2);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 0% 100%, 0% 50%, 0% 0%)", duration: d, ease: "none" }, T + d*3);
tl.set(new, { clipPath: "none", zIndex: "auto" }, T + d*4 + 0.02);
tl.set(old, { opacity: 0, zIndex: "auto" }, T + d*4 + 0.02);
```
