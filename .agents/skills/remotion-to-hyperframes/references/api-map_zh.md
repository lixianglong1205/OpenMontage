# Remotion → HyperFrames API 对照表

权威翻译对照表。开始翻译时加载本参考，了解高层映射；涉及易错细节（时序、转场等）时再加载各主题参考文档。

## 如何阅读本表

- **`drop`** = 从输出中完全移除。HF 运行时自行处理。
- **`see references/X.md`** = 映射非平凡；请阅读链接文件。
- **`refuse + interop`** = 技能退出并推荐 [PR #214](https://github.com/heygen-com/hyperframes/pull/214) 中的运行时适配器模式。

## 合成根（Composition root）

| Remotion                                             | HyperFrames                                                                                                          |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `<Composition id durationInFrames fps width height>` | root `<div id="stage" data-composition-id data-start="0" data-duration="<dur/fps>" data-fps data-width data-height>` |
| `defaultProps={...}`                                 | `#stage` 上的 `data-*` 属性（每个标量 prop 一个）。嵌套对象/数组 — 见 [parameters.md](parameters.md)    |
| `schema={z.object(...)}`                             | HTML 中不表示；schema 仅存在于 agent 的翻译步骤中                                       |
| `calculateMetadata`（同步）                           | 在翻译时解析，将具体值写入 `data-*`                                                     |
| `calculateMetadata`（异步）                          | **refuse + interop** — 见 [escape-hatch.md](escape-hatch.md)                                                        |
| `registerRoot(RemotionRoot)`                         | drop                                                                                                                 |
| `<AbsoluteFill style>`                               | `<div style="position:absolute;inset:0;{style}">`                                                                    |

## 序列（Sequencing）

嵌套与交错细节见 [sequencing.md](sequencing.md)。

| Remotion                                   | HyperFrames                                                                                               |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `<Sequence from={F} durationInFrames={D}>` | `<div data-start="<F/fps>" data-duration="<D/fps>" data-track-index="N">`                                 |
| `<Series>` + `<Series.Sequence>`           | 兄弟节点，使用顺序递增的 `data-start` 值                                                              |
| `<Loop durationInFrames={D}>`              | 非原语 — 输出自定义 GSAP `repeat: -1` 循环并手动计算偏移                            |
| `<Freeze frame={F}>`                       | 移除包装器；HF 在 seek 驱动的时间线外没有运行动画，因此 freeze 为无操作 |

## 时序（Timing）

见 [timing.md](timing.md) — 本节杠杆最高。

| Remotion                                                   | HyperFrames                                                                                                        |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `useCurrentFrame()`                                        | drop — HF 对时间线 seek。由 `frame` 推导的数学变为暂停 GSAP tween 的可动画属性。 |
| `useVideoConfig()` 的 `fps` / `durationInFrames`          | drop — 从 `#stage` 的 `data-fps` / `data-duration` 读取                                                          |
| `interpolate(frame, [a,b], [x,y])`（线性）                | 在偏移 `a/fps` 处：`gsap.fromTo(t, {p:x}, {p:y, duration:(b-a)/fps, ease:"none"})`                                  |
| `interpolate(frame, [a,b,c,d], [x,y,y,z])`（多段） | 在偏移 `a/fps`、`b/fps`、`c/fps` 处三次 `gsap.to` 调用                                                         |
| `interpolate(..., {easing: Easing.bezier})`                | GSAP `CustomEase.create("c", "M0,0 C${a},${b} ${c},${d} 1,1")`                                                     |
| `spring({frame, fps, config: {damping, stiffness, mass}})` | GSAP `back.out(N)` — damping → 过冲对照表见 [timing.md](timing.md)                                      |
| `interpolateColors(frame, range, colors)`                  | `gsap.to({...}, { backgroundColor, color, duration, ease })` — GSAP 原生处理颜色补间                  |
| `Easing.in / .out / .inOut(power)`                         | GSAP `power<N>.in` / `power<N>.out` / `power<N>.inOut`                                                             |

## 媒体（Media）

裁剪、音量渐变与解码器说明见 [media.md](media.md)。

| Remotion                               | HyperFrames                                                                 |
| -------------------------------------- | --------------------------------------------------------------------------- |
| `<Audio src volume>`                   | `<audio data-start data-duration data-track-index data-volume src>`         |
| `<Audio playbackRate startFrom endAt>` | `data-playback-rate`、`data-trim-start`、`data-trim-end`                    |
| `<Video src>`                          | `<video muted playsinline data-start data-duration data-track-index src>`   |
| `<OffthreadVideo>`                     | `<video>` — HF 不需要离线程变体（使用 headless Chrome）   |
| `<Img src>`                            | `<img>`                                                                     |
| `<IFrame src>`                         | `<iframe>` — HF 对嵌套 iframe 自动回退为截图模式       |
| `staticFile("x.png")`                  | `"assets/x.png"` — 将文件复制到 `index.html` 旁的 `hf-src/assets/` |
| `delayRender()` / `continueRender()`   | drop — HF 通过 Frame Adapter 模式等待资源就绪            |

## 转场（Transitions）

见 [transitions.md](transitions.md)。

| Remotion                                                                       | HyperFrames                                                                                               |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `<TransitionSeries>` + `<TransitionSeries.Transition presentation={fade()} />` | 在边界处手动 `gsap.to(scene, {opacity: 0/1, duration})` 交叉淡入淡出                               |
| `slide()`、`wipe()`、`clockWipe()`、`fade()`                                   | HF [shader-transitions](https://hyperframes.heygen.com/catalog/blocks) 包预设 — 选最接近的 |
| `linearTiming({durationInFrames})`                                             | 时长为秒（`/fps`）                                                                              |
| `springTiming({config})`                                                       | 时长为秒，ease 为 `back.out` — 见 [timing.md](timing.md)                                         |

## Lottie

见 [lottie.md](lottie.md)。

| Remotion                        | HyperFrames                                                                                                       |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `<Lottie animationData={data}>` | `<div id="lottie-N">` + `<script>const anim = lottie.loadAnimation({...}); window.__hfLottie.push(anim)</script>` |
| `loop` / `playbackRate` props   | 仅在确认播放器 seek 行为后再翻译；HF 适配器通过 `goToAndStop` 按绝对时间 seek              |
| `@remotion/lottie` runtime      | 从 CDN 加载 `lottie-web` — 移除 React 包装                                                                    |

## 字体（Fonts）

见 [fonts.md](fonts.md)。

| Remotion                                            | HyperFrames                                                                                 |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `@remotion/google-fonts/<Family>` 的 `loadFont()` | `@font-face` 规则引用 Google Fonts CSS，或在 `<head>` 中 `<link>` Google Fonts |
| 通过 `@font-face` 的本地字体                         | 相同 — 将规则粘贴到 `<style>`                                                        |
| 系统字体回退                                | 记录字体回退差异成本（见 [eval.md](eval.md)）                         |

## 参数（Parameters）

见 [parameters.md](parameters.md)。

| Remotion                      | HyperFrames                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------------- |
| `z.object({foo: z.string()})` | `#stage` 上的 `data-foo`（schema 隐含于 HTML 结构）                             |
| 嵌套数组 prop（`stats[]`） | 重复 HTML 标记，每项带独立 `data-*` 属性                                         |
| Zod 默认值            | 直接将默认值写入 HTML                                                          |
| Zod 运行时校验        | 不表示；若校验重要，在发出 HTML 前的翻译步骤中校验 |

## React 模式

| Remotion                                           | HyperFrames                                                      |
| -------------------------------------------------- | ---------------------------------------------------------------- |
| 自定义 React 子组件（纯、由 prop 驱动）      | 以内联重复 HTML 实现，以 prop 接口为模板 |
| `useState` 驱动动画                       | **refuse + interop**                                             |
| `useReducer` 驱动动画                     | **refuse + interop**                                             |
| `useEffect(fn, [deps])`（非空 deps）           | **refuse + interop**                                             |
| `useEffect(fn, [])`（仅挂载副作用）       | 移除 effect；若需启动时工作可用 `queueMicrotask`  |
| `useCallback`、`useMemo`                           | drop 包装 — 仅为装饰                                   |
| 自定义 hook（纯 `useCurrentFrame` 推导） | 内联函数体                                                  |
| 带 state/effect 的自定义 hook                     | refuse + interop                                                 |

## 分布式渲染

`@remotion/lambda` 与 `@remotion/cloudrun` 属于部署配置 —
与渲染的合成本身正交。技能将其作为**警告**（非阻塞）输出，并在第 3 步（Generate）中 drop，在
`TRANSLATION_NOTES.md` 中注明。HF 目前为单机；记录该差距。

| Remotion                   | HyperFrames                                            |
| -------------------------- | ------------------------------------------------------ |
| `@remotion/lambda` import  | drop 该 import（警告 `r2hf/lambda-import`）         |
| `renderMediaOnLambda(...)` | drop 该调用；在 `TRANSLATION_NOTES.md` 中注明          |
| `@remotion/cloudrun`       | drop import 与调用；在 `TRANSLATION_NOTES.md` 中注明 |

## 何时完全退出

若存在任何阻塞模式，应推荐 [PR #214](https://github.com/heygen-com/hyperframes/pull/214) 中的运行时 interop 模式，
而非尝试翻译。见 [escape-hatch.md](escape-hatch.md)。

阻塞项记录在 [`scripts/lint_source.py`](../scripts/lint_source.py)，
并由 [tier-4-escape-hatch](../assets/test-corpus/tier-4-escape-hatch/) 测试。
