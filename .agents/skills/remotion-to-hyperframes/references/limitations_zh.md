# 翻译限制

本技能明确无法翻译的内容，与 blocker 列表（由 `lint_source.py` 强制执行）分开说明。以下为**已知**缺口——在翻译周围 composition 时，应作为翻译说明向用户披露。

## 技能拒绝的 React 模式

见 [escape-hatch.md](escape-hatch.md)。以下任一情况会触发放弃翻译：

- 用 `useState`、`useReducer` 驱动动画
- 带非空 deps 的 `useEffect` / `useLayoutEffect`（副作用）
- 异步 `calculateMetadata`
- 第三方 React UI 库（MUI、Chakra、Mantine、antd、shadcn、Radix、NextUI）

`@remotion/lambda` 已不在此列表中——现为警告而非 blocker，因为 Lambda 配置与 composition 渲染正交。技能会移除相关 import 与 `renderMediaOnLambda(...)` 调用，并写入 `TRANSLATION_NOTES.md` 条目。见 [escape-hatch.md](escape-hatch.md)。

## 可用但需注意的模式

### `<Audio>` 上的音量渐变

Remotion 的 `volume` 可接受函数：

```tsx
<Audio src={...} volume={(f) => interpolate(f, [0, 30], [0, 1])} />
```

HF 仅支持静态 `data-volume`。翻译时：在翻译阶段用 `ffmpeg afade` 将渐变烘焙进音频文件，**或**去掉渐变并附说明。去掉渐变时听感不同但画面一致，SSIM 可通过——只需标注。

### 带子组件有状态的 `<Loop>`

```tsx
<Loop durationInFrames={30}>
  <CounterThatIncrementsViaUseRef />
</Loop>
```

`repeat: -1` 的 Loop 适用于**视觉**重复。若循环子组件在迭代间持有状态（计数器、随机种子等），HF 无法在每次迭代中完全一致复现。除非子组件在每次迭代内完全确定，否则应放弃翻译。

### 带 crossOrigin 的 Remotion `<Img>`

```tsx
<Img src="https://other-domain.com/x.png" crossOrigin="anonymous" />
```

HF 渲染器对 CORS 的处理与 Remotion 不同。多数公开图片可用；带认证头的私有图片不行。若源使用 `crossOrigin="use-credentials"`，需在翻译时下载并内联该资源。

### `<TransitionSeries>` 中的自定义 `presentation`

```tsx
const customPresentation: PresentationComponent = ({ children, presentationProgress }) => {
  return <div style={{ filter: `blur(${(1 - presentationProgress) * 20}px)` }}>{children}</div>;
};
```

纯 presentation（由 progress 计算 transform/filter/opacity）可干净地译为 GSAP tween。内部读取 `useCurrentFrame()` 或带子组件有状态的 presentation 不行——应放弃翻译。

### 代码分割组件（`React.lazy`）

```tsx
const HeavyChart = React.lazy(() => import("./HeavyChart"));
```

`React.lazy` 是异步的，不符合确定性渲染模型。译为普通 import；得到的 HF composition 会 upfront 包含全部代码。

## 始终可用的模式

- `<AbsoluteFill>` 与 `<Sequence>`（任意嵌套）
- `useCurrentFrame()` 派生：`interpolate`、`spring`、`Easing`、`interpolateColors`、手动计算
- 简单 props 的 `<Audio>`、`<Video>`、`<Img>`、`<IFrame>`
- `staticFile()` 引用
- 仅为 props 纯函数的自定义 React 子组件
- 仅为 `useCurrentFrame` 纯派生的自定义 hook
- `@remotion/lottie`（译为 HF 的 Lottie 适配器）
- `@remotion/google-fonts/<Family>`（译为 `<link>` 或 `@font-face`）
- 同步 `calculateMetadata`（在翻译时解析）
- 内置 presentation 的 `<TransitionSeries>`（`fade`、`slide`、`wipe`、`clockWipe`、`flip`、`iris`）

## 技能刻意不尝试翻译的内容

设计上超出范围：

- **HDR 渲染** — HF 支持 HDR 但 Remotion 不支持，故无源可译。
- **可变帧率** — 两者均假设恒定 fps。
- **多 composition 的 `<Composition>` 列表** — 一次译一个。技能会提示用户选择 composition。
- **Remotion Studio 属性面板** — HF Studio 中的可视化属性编辑需要不同基础设施；超出范围。

## 向用户报告缺口

当翻译**有产出**但存在缺口时，在输出旁写入 `TRANSLATION_NOTES.md`：

```markdown
# Translation notes

The following Remotion patterns were translated with caveats:

- `<Audio volume={(f) => ...}>` (line 15): volume ramp dropped — added
  static `data-volume="0.5"`. To preserve the ramp, run
  `ffmpeg -i music.wav -af "afade=t=in:st=0:d=1" music.faded.wav` and
  swap the source file.
- `<HeavyChart>` (line 30): translated as inline HTML. The original
  React.lazy boundary was dropped — bundle size unchanged because HF
  serves a single HTML file.

If any of these caveats matter, consider the runtime interop pattern
instead.
```

该文件由技能与 HF 输出一并生成，不存放在语料库中。
