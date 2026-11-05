# 何时退出：运行时互操作模式

部分 Remotion 合成无法被干净地翻译。技能应事先识别这些情况，并推荐采用
[PR #214](https://github.com/heygen-com/hyperframes/pull/214) 中的 **运行时互操作模式（runtime interop pattern）**，
而不是产出有问题的 HTML。

## 何时推荐互操作

先运行 `scripts/lint_source.py`。若返回任何 blocker，则推荐互操作。blocker 包括：

| 规则                        | 检测内容                                                       |
| --------------------------- | -------------------------------------------------------------- |
| `r2hf/use-state`            | 用 useState 驱动动画                                           |
| `r2hf/use-reducer`          | 用 useReducer 驱动动画                                         |
| `r2hf/use-effect-deps`      | 带非空 deps 的 useEffect/useLayoutEffect（副作用）             |
| `r2hf/async-metadata`       | calculateMetadata 返回 Promise                                 |
| `r2hf/third-party-react-ui` | 从 MUI、Chakra、Mantine、antd、shadcn、Radix、NextUI 导入       |

以上任一项都会破坏 HF 所依赖的 seek 驱动、确定性帧模型。强行翻译会产生静默错误的输出。

## 互操作模式实际做了什么

根据 [PR #214](https://github.com/heygen-com/hyperframes/pull/214)，运行时适配器会：

1. 通过 esbuild 将用户的 Remotion 代码与 React、`@remotion/player` 打包。
2. 在 HF 合成的 HTML 内挂载 Remotion `<Player>`。
3. 在 mount 时暂停播放器。
4. 在 `window.__hfRemotion` 上注册播放器，提供 `seekTo(frame)`、
   `pause()`、`durationInFrames`、`fps`。
5. HF 的渲染循环通过 `seekTo(frame)` 逐帧 seek 播放器。

结果：Remotion 的 React 树在 HF 的确定性帧节拍上渲染。
自定义 hook、useState、useEffect、MUI 组件等均可工作，因为由 Remotion 的 React reconciler 负责渲染。

## 推荐话术

当技能检测到 blocker 时，输出类似：

> Remotion 源码使用了 `useState`（及其他），无法翻译为 HF 的 seek 驱动 HTML 模型。推荐路径是 **运行时互操作模式**：用 `@remotion/player` 打包 Remotion 代码，让 HF 逐帧驱动。
>
> 完整实现见 https://github.com/heygen-com/hyperframes/pull/214。简要步骤：
>
> 1. 用 esbuild 打包 `entry.tsx`：`npx esbuild entry.tsx --bundle --outfile=dist/bundle.js --format=iife --jsx=automatic`
> 2. 挂载 Player 并在 `window.__hfRemotion` 上注册：
>
>    ```tsx
>    const playerRef = useRef<PlayerRef>(null);
>    useEffect(() => {
>      playerRef.current?.pause();
>      window.__hfRemotion = window.__hfRemotion || [];
>      window.__hfRemotion.push({
>        seekTo: (f) => playerRef.current?.seekTo(f),
>        pause: () => playerRef.current?.pause(),
>        durationInFrames,
>        fps,
>      });
>    }, []);
>    ```
>
> 3. 在 HF 的 `index.html` 中引用 bundle 并正常渲染：
>    `<script src="dist/bundle.js"></script>`

## lint 输出已包含推荐

`lint_source.py` 会为每条 finding 输出 `recommendation` 字段。原样展示即可——它们按 blocker 规则调优：

```json
{
  "rule": "r2hf/use-state",
  "message": "useState detected — Remotion compositions that drive animation via React state are not deterministic frame-capture targets in HyperFrames",
  "recommendation": "Use the runtime interop pattern from PR #214 instead of attempting a translation"
}
```

## 何时不必退出：仅 warning

部分模式只产生 warning，不是 blocker——去掉包装后再翻译：

| 规则                      | 操作                                                                |
| ------------------------- | ------------------------------------------------------------------- |
| `r2hf/lambda-import`      | 去掉 `@remotion/lambda` 配置；HF 单机运行，记录差距                 |
| `r2hf/delay-render`       | 去掉调用；HF 处理资源就绪                                           |
| `r2hf/use-callback`       | 去掉包装，内联函数                                                  |
| `r2hf/use-memo`           | 去掉包装，内联计算                                                  |
| `r2hf/custom-hook` (pure) | 若 hook 体为 `useCurrentFrame` 的派生，则内联 hook 体              |
| `r2hf/static-file`        | 将 `staticFile("x")` 替换为 `"assets/x"`                            |
| `r2hf/interpolate-colors` | 翻译为 GSAP 颜色补间（见 [timing.md](timing.md)）                   |

这些在 T4 cases 05–07 中有文档说明。

`r2hf/lambda-import` 是 warning 而非 blocker，因为 Lambda
配置与渲染出的合成正交。作者即便配置了 AWS Lambda 做分布式渲染，否则干净的 Remotion 合成也不应因此翻译失败。技能会在第 3 步（Generate）去掉
`@remotion/lambda` 导入和 `renderMediaOnLambda(...)` 调用，并写入 `TRANSLATION_NOTES.md` 条目，以便用户单独配置 HF 渲染。

## 源码同时有 blocker 与 warning 时

退出。只要存在一条 blocker，技能就不应尝试翻译——即便合成其余部分很干净。
用户应对整段使用互操作，或先从 Remotion 源码中重构掉 blocker 模式。
