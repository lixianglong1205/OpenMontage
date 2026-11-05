# 时序翻译：interpolate、spring、easing

这是杠杆最高的参考文档。缓动与时序是读者最能感知到的部分；翻译选错时，对 SSIM 的伤害比任何其他翻译决策都大。已在 T1–T3 档位上经实证验证。

## 转换：帧 → 秒

HF 的时间轴以秒为单位。Remotion 以帧为单位。始终使用：

```
time_seconds = frame / fps
```

因此在 fps=30 时：

- frame 15 → 0.5 s
- frame 30 → 1.0 s
- frame 90 → 3.0 s

在翻译阶段做一次换算即可，不要在运行时换算。

## interpolate — 线性

```tsx
const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
```

译为：

```js
gsap.to(target, { opacity: 1, duration: 1.0, ease: "none" }, 0);
// 若属性从 0 起始且 CSS 未预先设置，则用 fromTo
gsap.fromTo(target, { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "none" }, 0);
```

`ease: "none"` 对应 Remotion 默认的线性插值。若初始状态在 CSS 中，CSS 会设定起始值；否则使用 `fromTo`。

Remotion 中 `extrapolateLeft`/`extrapolateRight` 默认为 `"extend"`，但代理最常见的是 `"clamp"`。GSAP 不会外推——补间起止处数值保持。因此对 `clamp`，GSAP 行为一致；对 `extend`，需在生成代码前手动扩展输入范围。

## interpolate — 多段

```tsx
const opacity = interpolate(frame, [0, 15, 75, 90], [0, 1, 1, 0]);
```

在偏移 `[0]/fps`、`[1]/fps`、`[2]/fps` 处三段关键帧补间：

```js
const tl = gsap.timeline({ paused: true });
tl.to(target, { opacity: 1, duration: 0.5, ease: "none" }, 0);
tl.to(target, { opacity: 1, duration: 2.0, ease: "none" }, 0.5);
tl.to(target, { opacity: 0, duration: 0.5, ease: "none" }, 2.5);
```

已在 T1 验证——相对 Remotion 基线平均 SSIM 0.974。

## spring → GSAP back.out

Remotion 的 `spring()` 是损耗最大的翻译项。映射是近似的，但足够接近，真实合成中 SSIM 通常 ≥ 0.92（T2: 0.985，T3: 0.953）。

| Remotion `spring` 配置                          | GSAP 等价                                              | 验证场景                         |
| ------------------------------------------------- | ---------------------------------------------------- | -------------------------------- |
| `{damping: 12, stiffness: 100, mass: 1}` (snappy) | `back.out(1.4)`，时长约 0.7 s                          | T2、T3（TitleScene）              |
| `{damping: 14, stiffness: 90, mass: 1}` (calmer)  | `back.out(1.2)`，时长约 0.7 s                          | T3（StatCard）                    |
| `{damping: 8, stiffness: 200}` (very bouncy)      | `back.out(2.0)` 或 `elastic.out(1, 0.5)`，时长约 0.6 s | 未验证；预算约 0.05 SSIM |
| `{overshootClamping: true}`                       | `power3.out`，时长约 0.6 s（无 overshoot）              | 未验证                    |

**经验法则**：`back.out(N)` 的过冲比例 ≈ `(stiffness / damping^2) * 1.4`。对
`damping:12, stiffness:100` 得 `1.4 * 100/144 = 0.97`，接近已验证的 1.4（公式较粗，需目视微调）。典型配置的默认时长约 0.7 s。

当 spring 的 `delay`/`from`/`to` 非默认时，按比例缩放 duration。

## 带自定义 easing 的 interpolate

```tsx
import { Easing } from "remotion";
interpolate(frame, [0, 30], [0, 1], { easing: Easing.out(Easing.cubic) });
```

| Remotion                     | GSAP                                                                                   |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| `Easing.in(Easing.linear)`   | `ease: "none"`                                                                         |
| `Easing.out(Easing.cubic)`   | `ease: "power3.out"`                                                                   |
| `Easing.inOut(Easing.cubic)` | `ease: "power3.inOut"`                                                                 |
| `Easing.out(Easing.poly(N))` | `ease: "power<N>.out"` (N=2 quad, 3 cubic, 4 quart, 5 quint)                           |
| `Easing.bezier(a,b,c,d)`     | `CustomEase.create("c", "M0,0 C${a},${b} ${c},${d} 1,1")` (requires CustomEase plugin) |
| `Easing.elastic(bounciness)` | `ease: "elastic.out(${bounciness}, 0.3)"`                                              |
| `Easing.bounce`              | `ease: "bounce.out"`                                                                   |
| `Easing.back(overshoot)`     | `ease: "back.out(${overshoot * 1.7})"` (Remotion's overshoot scale differs)            |

## interpolate 驱动非数值属性

```tsx
const color = interpolateColors(frame, [0, 30], ["#ff0000", "#0000ff"]);
```

GSAP 原生支持颜色补间：

```js
gsap.to(target, { color: "#0000ff", duration: 1.0, ease: "none" }, 0);
```

`backgroundColor`、`borderColor` 同理。起始值从 CSS 或内联样式读取。

## 自定义计数 / 数字补间

当 Remotion 用帧驱动的数字 ramp（`Math.round(value * eased)`）时：

```tsx
const t = interpolate(frame, [0, 45], [0, 1]);
const eased = 1 - (1 - t) ** 3; // cubic ease-out
const value = Math.round(target * eased);
return <div>{value.toLocaleString()}</div>;
```

GSAP 等价——补间计数对象，在 `onUpdate` 中写入 `textContent`：

```js
const counter = { v: 0 };
tl.to(
  counter,
  {
    v: target,
    duration: 1.5,
    ease: "power3.out",
    onUpdate: () => {
      el.textContent = Math.round(counter.v).toLocaleString();
    },
  },
  0,
);
```

`power3.out` 与 `1 - (1-t)^3` 完全一致。已在 T3 验证（平均 SSIM 0.953）。
亚帧时间偏移可能导致逐帧数字不一致，但终值收敛——对 SSIM 的影响在噪声底之上可忽略。

## 通过 per-instance 属性的 stagger

当自定义子组件接受 `delayInFrames` 属性时：

```tsx
<StatCard delayInFrames={i * 12} value={...} />
```

译为 GSAP 时间轴偏移：

```js
cards.forEach((card, i) => {
  const start = base + i * (12 / fps); // fps=30 时 i * 0.4s
  tl.to(card, { ... }, start);
});
```

已在 T3 验证——三张 StatCard 分别在 0.0/0.4/0.8 s 错开。
