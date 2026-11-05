# 参数翻译：Zod schema、defaultProps、calculateMetadata

带类型的 Remotion `<Composition schema={...} defaultProps={...} />`
如何转换为带参数的 HF 合成。

## 同步 calculateMetadata（可翻译）

```tsx
<Composition
  id="MyVideo"
  component={MyVideo}
  schema={z.object({ title: z.string(), duration: z.number() })}
  defaultProps={{ title: "Hello", duration: 90 }}
  calculateMetadata={({ props }) => ({
    durationInFrames: props.duration,
    fps: 30,
  })}
/>
```

当 `calculateMetadata` 为同步且仅使用 `props` 时，**在翻译时解析**
——用 `defaultProps`（或调用方指定的值）调用它，并将具体结果写入 HTML：

```html
<div
  id="stage"
  data-composition-id="MyVideo"
  data-start="0"
  data-duration="3"          <!-- 90/30 -->
  data-fps="30"
  data-title="Hello"
></div>
```

`data-title` 属性承载该值。原先读取 `props.title` 的代码，在 HF 中改为
`document.getElementById("stage").dataset.title`。

## 异步 calculateMetadata（不可翻译）

```tsx
<Composition
  calculateMetadata={async ({ props }) => {
    const res = await fetch(...);
    return { durationInFrames: res.duration };
  }}
/>
```

**拒绝并走互操作路径**。HF 需要预先获得合成元数据以填充 HTML。
在翻译时解析网络请求会违背动态元数据的初衷。参见 [escape-hatch.md](escape-hatch.md)。

Lint 规则 `r2hf/async-metadata` 会捕获此类用法。T4 用例 03 对其进行了测试。

## 默认 props（defaultProps）

```tsx
defaultProps={{
  title: "Hello",
  subtitle: "World",
  count: 42,
}}
```

翻译为根节点 `#stage` div 上的 `data-*` 属性：

```html
<div id="stage" data-title="Hello" data-subtitle="World" data-count="42">...</div>
```

约定：`propName` → `data-prop-name`（kebab-case）。在 GSAP
脚本内通过 `document.getElementById("stage").dataset.propName` 读取。

## 嵌套对象 / 数组 props

```tsx
defaultProps={{
  stats: [
    { label: "Stars", value: 1247, color: "#fbbf24" },
    { label: "Forks", value: 312, color: "#60a5fa" },
  ],
}}
```

不要尝试把数组编码为 JSON 形式的 `data-` 属性——HF 运行时
不会解析这类数据。应将数组**物化为重复的 HTML 标记**：

```html
<div id="scene-stats">
  <div class="stat-card" data-stat-index="0" data-stat-value="1247" style="--card-color:#fbbf24">
    <div class="number">0</div>
    <div class="label">Stars</div>
  </div>
  <div class="stat-card" data-stat-index="1" data-stat-value="312" style="--card-color:#60a5fa">
    <div class="number">0</div>
    <div class="label">Forks</div>
  </div>
</div>
```

组件模板（`StatCard.tsx`）成为标记模板；
每个实例将其标量 props 渲染为 `data-*` 与 CSS
自定义属性。

在 T3 中验证——三个 StatCard 以不同 props 复用，
平均 SSIM 0.953。

## 需要类型化解析的数值 props

`document.getElementById("stage").dataset.count` 是字符串。读取时转换：

```js
const count = Number(stage.dataset.count);
```

或在翻译时数据已确定、且无需随每次渲染变化时，
直接将值内联到 GSAP 脚本中。

## 布尔 props

```tsx
defaultProps={{ darkMode: true }}
```

两种约定：

- `data-dark-mode="true"` —— 按字符串读取，比较 `=== "true"`
- `data-dark-mode`（存在/缺失）—— 为 true 时用 `<div data-dark-mode>`，为 false 时省略

选定一种并保持一致。存在/缺失形式更符合 HTML 习惯，
且与 CSS 属性选择器配合良好：

```css
[data-dark-mode] .scene {
  background: #000;
}
```

## Zod 运行时校验

Remotion 的 `schema` 在合成加载时校验 props。HF 没有
等价机制——HTML 进入渲染器时，schema 已不存在。

改为在翻译时校验。若用户传入无效数据，
在输出 HTML 之前以翻译错误失败。这与 Zod
「大声失败」的意图一致，且无需运行时依赖。

## 当合成用 props 做派生 prop 计算时

```tsx
const Composition: React.FC<Props> = ({ stats }) => {
  const total = stats.reduce((acc, s) => acc + s.value, 0);
  return <div>{total}</div>;
};
```

在翻译时计算派生值，并写入 HTML
或某个 `data-` 属性。不要在 HF 合成里用 JS 表达该计算——
那会增加运行时开销，并使 HTML 状态化，
不利于人工编辑。

若派生逻辑非平凡（涉及数组本身，而不仅是标量），
将其物化为 HTML 中的静态文本。
