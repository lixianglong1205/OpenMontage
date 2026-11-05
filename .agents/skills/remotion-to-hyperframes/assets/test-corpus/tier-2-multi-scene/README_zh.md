# Tier 2 — title-image-outro

## 测试内容

三场景合成。每个场景练习一种不同的 Remotion 惯用法：

1. **场景 1（0–2 s）** — TitleScene，使用 `spring({damping:12, stiffness:100, mass:1})`
   驱动文字上的 `transform: scale()`。测试有损的 `spring → GSAP ease` 转换。
2. **场景 2（2–4 s）** — ImageScene，淡入通过 `staticFile` 加载的图片，并
   以线性方式将其从 0.8 缩放到 1.0。测试资源路径 + 线性 `interpolate`。
3. **场景 3（4–6 s）** — OutroScene，1 秒线性淡入。在
   较难场景之后做健全性检查。

全程播放静音 6 秒 WAV，`volume={0.5}`。测试 `<Audio>` 的转换。

若某次转换通过 T2，则技能已正确处理 `<Sequence>` 边界、
`<Audio>` / `<Img>` / `staticFile`，以及 Remotion `spring → GSAP ease` 启发式。

## 转换对照

| Remotion                                                            | HyperFrames                                                                                              |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `<Sequence from={0} durationInFrames={60}>`                         | `<div data-start="0" data-duration="2" data-track-index="0">`                                            |
| `spring({frame, fps, config: {damping:12, stiffness:100, mass:1}})` | `gsap.to(target, { scale: 1, duration: 0.7, ease: "back.out(1.4)" })`                                    |
| `<Audio src={staticFile("music.wav")} volume={0.5} />`              | `<audio src="assets/music.wav" data-start="0" data-duration="6" data-volume="0.5" data-track-index="1">` |
| `<Img src={staticFile("square.png")} />`                            | `<img src="assets/square.png">`（setup.sh 会复制到两棵目录树）                                  |
| `interpolate(frame, [0, 15], [0, 1])` at 30 fps                     | `gsap.to(target, { opacity: 1, duration: 0.5, ease: "none" })`                                           |

场景交叉淡入是 HyperFrames 的惯用法，而非 Remotion：在场景边界处
我们 `gsap.set(scene, { opacity: 0 })`，使上一场景在
正确时刻消失。Remotion 则通过 `<Sequence>` 的 durationInFrames 隐式完成这一点。

## 如何渲染与评估

```bash
# 1. Generate the binary assets (PNG + WAV) via ffmpeg
./setup.sh

# 2. Render Remotion baseline
cd remotion-src && npm install && npm run render

# 3. Render HyperFrames translation
cd ../hf-src && npx hyperframes render --output ../hf.mp4

# 4. Compare
../../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```

## 为何阈值是 0.95？

与 T1 相同（`expected.json` 为编排器编码该阈值）。在校准期间，spring → `back.out(1.4)`
比预期更干净——相对 0.95 门槛，验证均值为 0.985。若转换在其他方面出错（spring 过冲不对、交错错位、
资源路径漂移），平均 SSIM 会远低于 0.95——那就是失败信号。
