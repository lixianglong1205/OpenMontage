# 转场翻译：@remotion/transitions → HF 交叉淡入淡出 / shader-transitions

`@remotion/transitions` 包是 Remotion 预置的场景间转场库。HF 有两种迁移路径：

1. **手动 GSAP 交叉淡入淡出** — 适用于简单的透明度/变换转场。免费，无需额外包。
2. **HF shader-transitions 包** — 适用于与 @remotion/transitions 预设视觉一致的丰富转场。

## 模式：`<TransitionSeries>` 即带重叠的 `<Series>`

```tsx
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

可翻译为按转场时长重叠的场景：

- SceneA: [0, 60] = `data-start="0" data-duration="2"`
- SceneB: [60-15, 60-15+60] = `data-start="1.5" data-duration="2"`（转场窗口与 A 的末尾和 B 的开头重叠）

然后用 GSAP 驱动转场：

```js
// Manual fade (presentation={fade()})
tl.to(sceneA, { opacity: 0, duration: 0.5, ease: "none" }, 1.5);
tl.fromTo(sceneB, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "none" }, 1.5);
```

## Presentation 对照表

| Remotion `presentation`            | HF 迁移方式                                                                            |
| ---------------------------------- | ----------------------------------------------------------------------------------------- |
| `fade()`                           | 手动 `gsap.to(opacity)` 交叉淡入淡出                                                       |
| `slide({direction: "from-right"})` | 入场 `gsap.fromTo(translateX: "100%" → 0)` + 出场 `to(translateX: "-100%")` |
| `wipe({direction: "from-left"})`   | 入场 `gsap.fromTo(clip-path: inset(0 100% 0 0) → inset(0 0 0 0))`                  |
| `clockWipe()`                      | 使用 HF 的 `sdf-iris` shader-transition（`npx hyperframes add sdf-iris`）                    |
| `flip()`                           | 两场景间各承担 180° 的 `gsap.to(rotateY)`                                              |
| `cube()`                           | 使用 HF 的 `cinematic-zoom`，或手动用 `rotateY` + `transform-origin` 构建           |
| `iris()`                           | 使用 HF 的 `sdf-iris` shader-transition                                                     |
| `none()`                           | 无转场；在边界处硬切                                                   |

## Timing 迁移

```tsx
linearTiming({durationInFrames: 15})              → ease: "none"
linearTiming({durationInFrames: 15, easing: ...}) → 按 timing.md 中的 easing 对照表设置 ease
springTiming({config: {damping: 12}})             → ease: "back.out(1.4)"（约 0.7 s）
```

将 `durationInFrames` 换算为秒（`/fps`）。

## 何时使用 HF shader-transitions

对于 Remotion 预设中有对应 GLSL 实现的丰富转场
（iris、ripple、zoom、glitch），请使用 HF 的 [shader-transitions](https://hyperframes.heygen.com/catalog/blocks)
包。其效果比手动 GSAP 变换更丰富。

```bash
npx hyperframes add sdf-iris
```

在 composition 中：

```html
<div id="iris-transition" class="hf-shader-transition" data-start="1.5" data-duration="0.5">
  <!-- bound scenes via the shader-transition's data-from / data-to -->
</div>
```

每种 shader-transition 有各自的数据属性；具体见 catalog 页面
中对应 block 的说明。

## 当源项目使用自定义 Presentation 时

Remotion 支持自定义 `presentation` 实现：

```tsx
const customPresentation: PresentationComponent = ({
  children,
  presentationProgress,
  presentationDirection,
}) => {
  return (
    <div
      style={
        {
          /* compute transform from progress */
        }
      }
    >
      {children}
    </div>
  );
};
```

迁移方式：从 `style={...}` 块中提取数学公式，并输出等价的 GSAP tween。具体而言，变换公式可直接映射为按 `progress` 参数化的 `gsap.to(target, { transform: ... })`。

若自定义 presentation 在内部使用 `useCurrentFrame()` 来动画化
超出简单 progress 曲线之外的内容，则视源为不可翻译，改走运行时互操作模式（见
[escape-hatch.md](escape-hatch.md)）。
