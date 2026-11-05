# Tier 1 — title-card-fade

## 测试内容

最简单的非平凡 Remotion → HyperFrames 翻译。单个文本元素在前 0.5 s 内淡入，保持 2.0 s，在最后 0.5 s 内淡出。无音频、无媒体、无自定义组件。

若某次翻译无法通过 T1，说明它在基础能力上就有问题：
`AbsoluteFill`、`useCurrentFrame`、多段输入的 `interpolate`，以及 Remotion 基于帧的驱动与 HF 的 paused-GSAP 驱动之间的时序偏移。

## 翻译对照说明

| Remotion                                                      | HyperFrames                                                                                             |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `<AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>`       | `<body style="background: #0a0a0a">` + 一个定位的根 div                                                    |
| `useCurrentFrame()`                                           | 省略 — HF 会定位时间轴                                                                                  |
| `interpolate(frame, [0, 15, 75, 90], [0, 1, 1, 0])` at fps=30 | `gsap.timeline({ paused: true })`，三个 `.to()` 调用，偏移 0s/0.5s/2.5s，均 `ease: "none"`              |
| `<div style={{ opacity }}>HELLO</div>`                        | 静态 markup；opacity 由时间轴驱动动画                                                                   |

Remotion→HF 的时间换算为 `time = frame / fps`。因此 30 fps 下的
`[0, 15, 75, 90]` 对应 `[0, 0.5, 2.5, 3.0]` 秒。

## 如何渲染与评估

```bash
# Render Remotion baseline
cd remotion-src && npm install && npm run render
# Renders to remotion-src/out/baseline.mp4

# Render HyperFrames translation
cd ../hf-src && npx hyperframes render --output ../hf.mp4

# Compare with the eval harness (from skill scripts/)
../../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```

`expected.json` 记录了该 fixture 的 SSIM 阈值（0.95）；
针对 Remotion @ 4.0 且 PNG/BT.709 输出的标定均值为 0.974。
