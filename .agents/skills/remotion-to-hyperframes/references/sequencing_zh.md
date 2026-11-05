# 时序翻译：Sequence、Series、Composition 根节点

Remotion 嵌套的 `<Sequence>` 树如何映射为 HF 扁平的 `data-start` /
`data-duration` 标记，以及单一 paused GSAP 时间线。

## 核心思路

Remotion 的 `<Sequence from={F} durationInFrames={D}>` 是一种坐标
变换：它将 `useCurrentFrame()` 偏移 `F`，并把子组件裁剪到窗口
`[F, F+D]`。HF 没有逐元素的「当前帧」——只有单一的 composition
seek 时间，运行时根据各元素的 `data-start` / `data-duration` 显示或隐藏。

结果：嵌套树被展平为同一父级下的一组兄弟节点，每个节点拥有自己的时间窗口。

## `<Composition>` → 根节点 `#stage`

```tsx
<Composition
  id="MyVideo"
  component={MyVideo}
  durationInFrames={300}
  fps={30}
  width={1280}
  height={720}
/>
```

```html
<div
  id="stage"
  data-composition-id="MyVideo"
  data-start="0"
  data-duration="10"      <!-- 300/30 -->
  data-fps="30"
  data-width="1280"
  data-height="720"
>
  <!-- composition content -->
</div>
```

`#stage` 上必须设置 `data-start="0"`（运行时需要它来锚定
播放；缺失会触发 lint 警告）。

## `<AbsoluteFill>` → 定位 div

```tsx
<AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>...children...</AbsoluteFill>
```

```html
<div style="position:absolute;inset:0;background-color:#0a0a0a;">...children...</div>
```

`AbsoluteFill` 在 Remotion 中只是一个带样式的 div。翻译为带
`position:absolute; inset:0` 的 div，并透传其他 style 属性。

## `<Sequence>` → 带时间窗口的 div

```tsx
<Sequence from={0} durationInFrames={90}>
  <TitleCard />
</Sequence>
```

```html
<div data-start="0" data-duration="3" data-track-index="0">
  <!-- TitleCard children inlined -->
</div>
```

帧转秒：`from/fps`、`durationInFrames/fps`。为每个并行渲染层选择
`data-track-index`（背景 = 0，叠层 = 1，音频 = 2 等）。顺序场景可共用同一 index。

## 嵌套 `<Sequence>` 的展平

Remotion 在序列嵌套时会累加偏移：

```tsx
<Sequence from={60} durationInFrames={120}>
  <Sequence from={30} durationInFrames={60}>
    <ImageScene />
  </Sequence>
</Sequence>
```

内层序列的有效窗口为 `[60+30, 60+30+60] = [90, 150]`。

翻译时求和后输出一个带解析后窗口的 HF div：

```html
<div data-start="3" data-duration="2" data-track-index="0">
  <!-- ImageScene children -->
</div>
```

## `<Series>` → 按顺序偏移的兄弟节点

```tsx
<Series>
  <Series.Sequence durationInFrames={60}>
    <A />
  </Series.Sequence>
  <Series.Sequence durationInFrames={120}>
    <B />
  </Series.Sequence>
  <Series.Sequence durationInFrames={90}>
    <C />
  </Series.Sequence>
</Series>
```

每个 `Series.Sequence` 占用下一个时间槽。输出兄弟节点，`data-start` 递增累加：

```html
<div data-start="0" data-duration="2" data-track-index="0">A</div>
<div data-start="2" data-duration="4" data-track-index="0">B</div>
<div data-start="6" data-duration="3" data-track-index="0">C</div>
```

## 场景边界的交叉淡入淡出

Remotion 的 `<Sequence>` 默认在边界处硬切显示/隐藏。HF 行为相同——若 composition 需要在场景间平滑淡入淡出，须在边界处用 GSAP 显式驱动 opacity：

```js
const tl = gsap.timeline({ paused: true });
tl.set(scene1, { opacity: 1 }, 0);
tl.set(scene1, { opacity: 0 }, 2); // hard cut at 2s
tl.set(scene2, { opacity: 1 }, 2);
```

0.5 秒交叉淡入淡出示例：

```js
tl.to(scene1, { opacity: 0, duration: 0.5 }, 1.5);
tl.to(scene2, { opacity: 1, duration: 0.5 }, 1.5);
```

Remotion `<TransitionSeries>` 的翻译见 [transitions.md](transitions.md)。

## `<Loop>`

```tsx
<Loop durationInFrames={30}>
  <Spinner />
</Loop>
```

HF 没有 `<Loop>` 原语。翻译为带 `repeat: -1` 的 GSAP 时间线：

```js
const spinTl = gsap.timeline({ paused: true, repeat: -1, repeatRefresh: false });
spinTl.to(spinner, { rotate: 360, duration: 1.0, ease: "none" });
// Embed in the main composition timeline at the right offset:
mainTl.add(spinTl, 3);
```

这种方式较脆弱——Remotion 的 `<Loop>` 每次迭代会重置内部状态，
GSAP 的 repeat 也会，但若被循环的子节点自身还有动画，需注意
`repeatRefresh` 按需开启或关闭。对大多数简单的「一直旋转」场景足够。

## `<Freeze>`

```tsx
<Freeze frame={30}>
  <Animated />
</Freeze>
```

去掉包装层。`<Freeze>` 将子节点的 `useCurrentFrame()` 固定在某一帧——
但在 HF 中，子节点动画已由显式 GSAP tween 驱动，因此 freeze 翻译为「不要对该元素做 tween」。

## 多条并行轨道

当背景视频、叠层文字与音频同时播放时，使用不同的 `data-track-index`：

```html
<div data-track-index="0">background video</div>
<div data-track-index="1">overlay text</div>
<audio data-track-index="2" ...></audio>
```

运行时按 index 决定轨道顺序。媒体相关轨道约定见 [media.md](media.md)。
