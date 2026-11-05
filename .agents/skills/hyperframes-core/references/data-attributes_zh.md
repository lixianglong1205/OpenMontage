# 数据属性参考

每个 HyperFrames 合成（composition）都使用 `data-*` 属性向框架声明时序与结构。本文是完整的属性表——请与 `tracks-and-clips.md` 配合阅读，以了解 `data-track-index` 背后的规则。

## 合成根节点

每个可渲染的合成都需要一个根元素：

| 属性                         | 是否必填 | 含义                                                                             |
| ---------------------------- | -------- | -------------------------------------------------------------------------------- |
| `data-composition-id`        | 是       | 唯一 ID。必须与 `window.__timelines` 上动画注册表键一致。                        |
| `data-width` / `data-height` | 是       | 像素画幅尺寸。常见值：`1920x1080`、`1080x1920`、`1080x1080`。                    |
| `data-duration`              | 是       | 时长（秒）。这是渲染时长，而非 GSAP 时间轴长度。                                 |
| `data-fps`                   | 否       | 可选帧率提示。CLI 渲染标志可覆盖输出 fps。                                       |
| `data-composition-variables` | 否       | 变量声明的 JSON 数组（写在 `<html>` 上）。见 `variables-and-media.md`。        |

根节点应为 `position: relative`，具有明确的像素尺寸，并隐藏溢出（overflow），除非有意在画幅外进行合成。

## 片段（Clip）属性

带时序的子元素即为片段。**可见的时序元素（`<div>`、`<img>` 等）必须带有 `class="clip"`**——否则运行时会令该元素在整个合成期间始终可见，并忽略 `data-start` / `data-duration`。`<video>` 可省略（框架直接管理可见性）；`<audio>` 无视觉，也可省略。

**片段必须是合成根节点的直接子元素。** 嵌套在包装用 `<div>` 内的片段不会被注册——最明显的是，包装层内的 `<video>` 不会被 seek/解码，渲染结果为黑屏。若要包装/变换片段，应将包装层放在片段_内部_，或直接对片段元素做动画；不要用包装层包住片段。（`<video>`/`<audio>` 还必须位于**宿主**根节点，绝不能放在子合成 `<template>` 中——见 `variables-and-media.md`。）

| 属性               | 是否必填                                        | 含义                                                                                                                              |
| ------------------ | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `id`               | 是                                              | 稳定的 DOM ID，用于 lint、时间轴目标与调试。                                                                                       |
| `data-start`       | 是                                              | 开始时间（秒），或受支持的片段时间引用。                                                                                          |
| `data-duration`    | 对 `div`、`img` 及子合成必填                    | 时长（秒）。视频/音频在已知时可默认为媒体时长。                                                                                    |
| `data-track-index` | 是                                              | 时间轴轨道。同一轨道上的片段不得重叠。                                                                                            |
| `data-media-start` | 否                                              | 媒体源内的偏移（秒）。                                                                                                            |
| `data-volume`      | 否                                              | 静态音频音量，`0` 到 `1`，默认 `1`。若要淡入淡出，请在时间轴上动画 `volume`（见 `variables-and-media.md`）。                      |
| `data-has-audio`   | 否（仅 `<video>`）                              | 设为 `"true"` 以声明视频带有音轨，当自动检测会漏判时使用。                                                                        |

**可见时间窗两端均包含。** 片段在 `start ≤ t ≤ start + duration` 期间显示——在恰好 `t = start + duration` 时仍会渲染，因此最后一帧保持动画的结束状态（运行不会提前一帧隐藏）。在 `data-duration` 上完成的 reveal/入场动画会在最后一帧可见；你不必为了保证结束状态被渲染而刻意在 `data-duration` _之前_ 结束。（`/hyperframes-animation` 中的 climax-dwell 指引关乎节奏，与此边界无关。）

## 子合成宿主属性

当片段作为子合成宿主（加载另一份合成文件）时：

| 属性                         | 是否必填 | 含义                                                                   |
| ---------------------------- | -------- | ---------------------------------------------------------------------- |
| `data-composition-id`        | 是       | 被加载文件内部的合成 ID。                                              |
| `data-composition-src`       | 是       | 子合成 HTML 文件路径。                                                 |
| `data-width` / `data-height` | 是       | 该子合成实例的渲染尺寸。                                               |
| `data-variable-values`       | 否       | 按实例的变量覆盖，JSON 格式。见 `variables-and-media.md`。           |

完整接线模式见 `sub-compositions.md`。

## 编写提示

- `id="root"` — 脚手架与转场目录使用的模板约定，便于 CSS 用 `#root` 定位合成根，而不用 `[data-composition-id="main"]`。运行时非必需，但与生态其余部分一致。
- `class="clip"` — 可见时序元素（`<div>`、`<img>` 等）所需的运行时可见性标记。见上文「片段属性」。
- `data-layout-allow-overflow` — 告知 `hyperframes inspect`：该元素（或其子树）上的溢出是有意的。说明：
  - `inspect` 在采样时间戳测量 `getBoundingClientRect`，而非渲染像素——`overflow: hidden` 会裁剪视觉，但**不会**消除 `inspect` 的溢出发现。本属性是逃生口；仅靠 CSS overflow 不够。
  - 可设在合成**根**或任意子元素上。当被指出的违规者是 `div.<comp>-root inside div.<comp>-root`（根节点将其子元素的并集报告为溢出）时，修复应加在根上，而非逐个缩小文字字号——后者无法收敛。
  - 在多场景 `group_wN.html`（continue 运行）中，每个场景局部元素在其他场景的时间窗内仍留在 DOM 中；布局盒并集在 morph 接缝处几乎总会超出画布。在**构建时**就给根以及每个场景局部主/辅元素打上本属性，而不是等 `inspect` 报错后再加。
  - **影响范围——它静默的不只是 `inspect`。** 该属性会沿子树继承（感知探测会向上遍历祖先），因此也会为所有后代关闭渲染感知检查 `text-clipping`、`content-cramped-container` 与 `foreground-over-panel`。若把它放在同时承载真实前景内容的持久面板上，会在面板整个生命周期内对该内容禁用碰撞检查。优先用最窄的 opt-out：作用域限于最小的装饰性包装层，或对单一有意的主文字裁剪使用逐元素 `data-layout-bleed="true"`。两项画布/边缘检查 `primary-offscreen` 与 `foreground-over-panel` 在 allow-overflow 下**仍会**运行，因此无法隐藏被画幅切掉的字标或 bleed 到面板边缘的文字。
- `data-layout-ignore` — 从布局审计中完全排除该元素。

## 遗留 / 已移除属性

这些名称出现在旧项目与示例中。编写或编辑时请使用当前名称：

| 旧名称       | 改用               |
| ------------ | ------------------ |
| `data-layer` | `data-track-index` |
| `data-end`   | `data-duration`    |
