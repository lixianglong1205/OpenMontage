## 模糊

所有模糊转场均随 energy 缩放。完整对照表见 SKILL.md 中的「Blur Intensity by Energy」。

### 穿透模糊

内容在清晰呈现前会完全抽象化。这是最重的模糊转场。

**平静（Calm）（此类型的默认——本身就很重）：**

```js
tl.to(old, { filter: "blur(30px)", scale: 1.08, duration: 0.5, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.3, ease: "power1.in" }, T + 0.3);
// Hold: both scenes in abstract blur state
tl.fromTo(new,
  { filter: "blur(30px)", scale: 0.92, opacity: 0 },
  { filter: "blur(30px)", scale: 0.92, opacity: 1, duration: 0.2, ease: "none" }, T + 0.5);
// Slow resolve
tl.to(new, { filter: "blur(0px)", scale: 1, duration: 0.7, ease: "power1.out" }, T + 0.7);
```

**中等（Medium）：**

```js
tl.to(old, { filter: "blur(15px)", scale: 1.05, opacity: 0, duration: 0.4, ease: "power2.in" }, T);
tl.fromTo(new,
  { filter: "blur(15px)", scale: 0.95, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.4, ease: "power2.out" }, T + 0.2);
```

### 方向模糊

模糊 + skew，模拟单一方向上的运动。模糊与 skew 随 energy 缩放。

**中等（Medium）（默认）：**

```js
tl.to(old, { filter: "blur(12px)", skewX: -8, x: -200, opacity: 0, duration: 0.4, ease: "power3.in" }, T);
tl.fromTo(new,
  { filter: "blur(12px)", skewX: 8, x: 200, opacity: 0 },
  { filter: "blur(0px)", skewX: 0, x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, T + 0.15);
```

**平静（Calm）（更重模糊、更柔和的运动）：**

```js
tl.to(old, { filter: "blur(20px)", skewX: -4, x: -100, opacity: 0, duration: 0.6, ease: "power1.in" }, T);
tl.fromTo(new,
  { filter: "blur(20px)", skewX: 4, x: 100, opacity: 0 },
  { filter: "blur(0px)", skewX: 0, x: 0, opacity: 1, duration: 0.6, ease: "power1.out" }, T + 0.3);
```
