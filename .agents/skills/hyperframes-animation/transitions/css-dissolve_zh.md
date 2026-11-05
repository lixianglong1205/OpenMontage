## 溶解（Dissolve）

### 交叉淡入淡出（Crossfade）

简单的透明度切换。基线方案。

```js
tl.to(old, { opacity: 0, duration: 0.5, ease: "power2.inOut" }, T);
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.inOut" }, T);
```

### 模糊交叉淡入淡出（Blur Crossfade）

带模糊与缩放变化的溶解效果。**按画面能量缩放模糊强度** — 参见 SKILL.md 中的「Blur Intensity by Energy」章节。下方示例为中等（默认）版本。节奏舒缓的构图可将模糊增至 20–30px，并在峰值模糊处保持 0.3–0.5s；高能量场景可降至 3–6px 且不保持。

**中等（默认）：**

```js
tl.to(old, { filter: "blur(10px)", scale: 1.03, opacity: 0, duration: 0.5, ease: "power2.inOut" }, T);
tl.fromTo(new,
  { filter: "blur(10px)", scale: 0.97, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.5, ease: "power2.inOut" }, T + 0.1);
```

**舒缓（wellness、奢华）— 强模糊，在抽象色块上保持：**

```js
tl.to(old, { filter: "blur(25px)", scale: 1.05, duration: 0.6, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.4, ease: "power1.in" }, T + 0.4);
tl.fromTo(new,
  { filter: "blur(25px)", scale: 0.95, opacity: 0 },
  { filter: "blur(25px)", scale: 0.95, opacity: 1, duration: 0.3, ease: "power1.inOut" }, T + 0.5);
tl.to(new, { filter: "blur(0px)", scale: 1, duration: 0.6, ease: "power1.out" }, T + 0.8);
```

### 焦点切换（Focus Pull）

离场画面缓慢变模糊，入场画面清晰淡入。景深感。**按能量缩放模糊量与保持时长。**

**中等：**

```js
tl.to(old, { filter: "blur(15px)", duration: 0.5, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.3, ease: "power2.in" }, T + 0.25);
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, T + 0.25);
```

**舒缓 — 慢速移焦，在最大离焦处长时间保持：**

```js
tl.to(old, { filter: "blur(30px)", duration: 0.8, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.5, ease: "power1.in" }, T + 0.6);
tl.fromTo(new, { opacity: 0, filter: "blur(20px)" },
  { opacity: 1, filter: "blur(20px)", duration: 0.3, ease: "power1.inOut" }, T + 0.7);
tl.to(new, { filter: "blur(0px)", duration: 0.6, ease: "power1.out" }, T + 1.0);
```

### 色块过渡（Color Dip）

先淡入纯色，保持，再淡出新场景。

```js
tl.to(old, { opacity: 0, duration: 0.2, ease: "power2.in" }, T);
// Background color shows through
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, T + 0.25);
```
