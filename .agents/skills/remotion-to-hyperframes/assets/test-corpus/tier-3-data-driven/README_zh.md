# Tier 3 — stargazed-data-driven

## 测试内容

专为数据驱动场景构建的 fixture，在不使用 PR #214 中 runtime adapter 的前提下，复现生产级 Remotion composition 的典型形态。若某次翻译能通过 T3，则说明该 skill 能正确处理：

- 带 `z.object` schema 与类型化 `defaultProps` 的 `<Composition>`
- 在不同 scene 中以不同 props 复用的自定义 React 子组件
- 嵌套数据结构（`stats[]`）展开为重复 HTML，并带逐实例属性
- 由帧驱动的数字递增动画（`AnimatedNumber` → GSAP `onUpdate`）
- 两种不同 `spring` 配置分别映射为两种不同 `back.out`  overshoot
- 通过组件 props 实现的逐实例延迟（`delayInFrames` → GSAP timeline 偏移）

## Composition 结构

```
Stargazed (10 s @ 30 fps, 1280×720)
├── Sequence 0–3 s   TitleScene
│                    ├── title  ← spring scale
│                    └── subtitle ← linear fade
├── Sequence 3–7 s   StatsScene
│                    ├── StatCard "Stars" 1247 #fbbf24 (delay 0 frames)
│                    ├── StatCard "Forks" 312 #60a5fa  (delay 12 frames)
│                    └── StatCard "Issues" 48 #f87171  (delay 24 frames)
└── Sequence 7–10 s  OutroScene
                     └── UnderlinedText "thanks for watching" ← scale-in underline
```

每个 `StatCard` 为自定义子组件，内部使用 `AnimatedNumber` 从 0 计数到目标值。`AnimatedNumber` 本身通过 `useCurrentFrame()` 与手写的 `1 - (1 - t)^3` ease 推导显示数值。

## 有损部分（以及为何 threshold = 0.90）

1. **`spring → back.out(N)`**：本 composition 中有两种 spring 配置。
   - `{ damping: 12, stiffness: 100, mass: 1 }`（title）→ `back.out(1.4)`
   - `{ damping: 14, stiffness: 90, mass: 1 }`（stat card）→ `back.out(1.2)`

   Overshoot 比例（1.4 与 1.2）近似 damping 差异。GSAP 的 back ease 尾段曲线与 Remotion 的 spring 并不完全一致——每个 spring 实例约损失 ~0.03 平均 SSIM。

2. **Count-up easing**：`AnimatedNumber` 使用 `1 - (1 - t)^3`（cubic ease-out），在组件内手动计算。GSAP 的 `power3.out` 为相同曲线形状——应高度接近。两路渲染器每帧都会对显示整数取整；在亚帧 timing 差异下，取整值在相邻两数之间切换时会出现轻微不一致。

3. **Font rendering**：与 T1/T2 相同 caveat。系统 Helvetica/Arial 回退字体在两路渲染器间产生轻微抗锯齿差异，对 stat card 数字（大号 weight 800）影响最大。

T3 中平均 SSIM 低于 0.90 表示**结构性**不匹配（scene 时长错误、stagger timing 错误、props 连线缺失），而非近似漂移——这才是我们关心的失败信号。针对 Remotion @ 4.0 与 PNG/BT.709 输出的标定均值为 0.953。

## 翻译对照（skill 速查）

| Remotion                                                                    | HyperFrames                                                                           |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `<Composition schema={z.object({...})} defaultProps={...} />`               | 根 `#stage` div 上的 data-* 属性                                                      |
| 嵌套数组 prop（`stats[]`）                                                  | 带逐实例 `data-*` 属性的重复 HTML 标记                                                |
| 自定义 React 子组件                                                         | 以内联重复 HTML 实现，以组件 prop 接口为模板                                          |
| `<AnimatedNumber from={0} to={value} dur={45} />`（cubic ease-out count-up） | 对 `{ v: 0 }` 对象做 tween，`onUpdate` 重写 `textContent`，ease 为 `power3.out`       |
| `spring({damping:12, stiffness:100})`                                       | `back.out(1.4)`，时长约 ~0.7 s                                                        |
| `spring({damping:14, stiffness:90})`                                        | `back.out(1.2)`，时长约 ~0.7 s                                                        |
| `delayInFrames={i * 12}`（逐实例）                                          | GSAP timeline 偏移 `(i * 0.4)` s                                                      |
| `useVideoConfig()` 获取 `fps`                                               | 省略——composition fps 在 `#stage` 的 `data-fps` 上                                    |

## 如何渲染与评估

```bash
# Render Remotion baseline (no setup.sh — no binary assets in this fixture)
cd remotion-src && npm install && npm run render

# Render HyperFrames translation
cd ../hf-src && npx hyperframes render --output ../hf.mp4

# Compare
../../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```
