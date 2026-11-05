# 缓动、交错与基于函数的值

## 缓动（Easing）

内置缓动：`power1`、`power2`、`power3`、`power4`、`back`、`bounce`、`circ`、`elastic`、`expo`、`sine`、`none`。

每种均有 `.in`、`.out`、`.inOut` 变体。

| 缓动                       | 适用场景                                                                 |
| -------------------------- | ----------------------------------------------------------------------- |
| `power1.out`, `power2.out` | 常规 UI 动效。多数入场动画的默认选择。                         |
| `power3.out`, `power4.out` | 更有冲击力的减速。标题卡、主视觉揭示。                       |
| `sine.inOut`               | 漫长、缓慢、平静的动效。交叉淡入淡出、环境漂移动画。                     |
| `back.out(1.7)`            | 轻微 overshoot（过冲）。活泼的入场。参数控制过冲幅度。 |
| `elastic.out(1, 0.3)`      | 弹簧式弹跳。第一个参数 = 振幅，第二个 = 周期。                 |
| `expo.inOut`               | 干脆、戏剧化。主视觉场景之间的快速切换。                |
| `none` (linear)            | 与计时对位配合的镜头运动、机械感动效。                |

入场选 `.out`，退场选 `.in`，对称移动与持续动效选 `.inOut`。

## 缓动词汇（角色与情绪）

缓动是「语气」：全程只有低语的视频很无聊；在耳语、正常与重击之间变化的视频才吸引人。每个合成至少应使用 3 种不同缓动——全部用 `power2.out` 会产生扁平、单调的动效。

按角色划分的完整调色板（每个系列均有 `.in`、`.out`、`.inOut` 变体）：

| 系列               | 角色                                                                    | 典型用途                                                                                        |
| -------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `power1`–`power4`    | 从温和（1）到激进（4）的加速曲线                             | 通用。power2 是主力，power4 用于戏剧化快切                                |
| `back(N)`            | 过冲后回稳。N 控制越过目标多远（1=轻微，4=夸张） | Logo 揭示、徽章弹出、卡片入场。`back.out(2.5)` 偏活泼，`back.out(1.2)` 偏优雅 |
| `elastic(amp, freq)` | 弹簧弹跳。amp=幅度，freq=振荡速度                         | 面板散开、充满能量的下落、趣味揭示                                                        |
| `bounce`             | 球落地式弹跳                                                           | 物理交互、图标落地、计分器                                               |
| `expo`               | 极端加速曲线（比 power4 陡得多）                        | 高端/奢华揭示、戏剧化入场                                                         |
| `sine`               | 平滑、有机、无硬边                                               | 环境漂浮、呼吸感、Ken Burns、任何循环动效。`.inOut` 用于 yoyo 往复                 |
| `circ`               | 圆形加速（起初极快、末尾极柔，或相反）     | 镜头运动、场景转场、轨道运动                                                    |
| `steps(N)`           | 离散的 N 步跳跃，无插值                                      | 打字效果、光标闪烁、计数 tick、复古/数字美学                              |

**情绪映射：** 让缓动角色与节拍的情绪内容一致。平滑/有机缓动（`sine`、`power1`）显得沉思、漂移。激进减速（`power4.out`、`expo.out`）显得干脆、自信。弹簧过冲（`back.out`）显得弹跳、有物理感。应以 storyboard 的情绪描述指导选用哪种角色——而非套用公式。

## 默认值

```javascript
const tl = gsap.timeline({
  paused: true,
  defaults: { duration: 0.6, ease: "power2.out" },
});
```

或全局设置：

```javascript
gsap.defaults({ duration: 0.6, ease: "power2.out" });
```

更推荐在 timeline 作用域设置默认值——可在同一处记录该合成的动效语言。

## 交错（Stagger）

```javascript
gsap.fromTo(".item", { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, stagger: 0.08 });
```

对象形式：

```javascript
gsap.fromTo(
  ".item",
  { y: 24, opacity: 0 },
  {
    y: 0,
    opacity: 1,
    stagger: {
      each: 0.08, // delay between each
      from: "center", // "start" | "end" | "center" | "edges" | "random" | index
      amount: 0.6, // total stagger time (overrides each if both set)
      grid: "auto", // for 2D stagger
      axis: "x" | "y",
    },
  },
);
```

优先使用 `stagger`，而非 N 个带手动 delay 的独立 tween——目标数量或顺序变化时仍能保持正确。使用 `fromTo()` 而非 `from()`，以便起始状态明确（见 `gsap-timeline-and-labels.md` → 子合成入场）。

## 基于函数的值

任意变量均可为函数 `(index, target, targets) => value`：

```javascript
gsap.to(".item", {
  x: (i, target, targets) => i * 50,
  rotation: (i) => (i % 2 === 0 ? 5 : -5),
  stagger: 0.1,
});
```

当各元素取值依赖 index、属性或测量尺寸时使用。比在循环里逐个创建 tween 更省、也更惯用。

## gsap.matchMedia（仅预览）

`matchMedia` 仅在媒体查询匹配时运行 setup，不匹配时自动 revert。适用于浏览器中**预览**不同视口尺寸，以及 `prefers-reduced-motion`。它**不能**替代按合成实际 `data-width`/`data-height` 渲染——HyperFrames 在固定视口下渲染。

```javascript
let mm = gsap.matchMedia();
mm.add(
  {
    isDesktop: "(min-width: 800px)",
    reduceMotion: "(prefers-reduced-motion: reduce)",
  },
  (context) => {
    const { isDesktop, reduceMotion } = context.conditions;
    gsap.to(".box", {
      rotation: isDesktop ? 360 : 180,
      duration: reduceMotion ? 0 : 2,
    });
  },
);
```
