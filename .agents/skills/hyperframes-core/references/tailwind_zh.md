# HyperFrames Tailwind

HyperFrames 的 `init --tailwind` 使用脚手架固定的 Tailwind 浏览器运行时。应将其视为 Tailwind v4，而非 Studio 的 Tailwind v3 配置。

## 何时使用

- 项目通过 `npx hyperframes init --tailwind` 脚手架创建。
- `index.html` 中包含 `window.__tailwindReady`。
- 任务涉及 Tailwind 工具类、`@theme`、自定义 utility，或 composition 中的 v3 到 v4 迁移修复。
- 渲染帧出现 Tailwind 样式缺失或第 0 帧闪烁。

## 版本约定

- **固定版本：`@tailwindcss/browser@4.2.4`**（权威来源：`packages/cli/src/commands/init.ts` 中的 `TAILWIND_BROWSER_VERSION`）。
- 不要用 `cdn.tailwindcss.com` 替换脚手架运行时（未固定版本，破坏可复现性）。
- 保持 readiness shim 行为确定；HyperFrames 在第 0 帧捕获前会等待 `window.__tailwindReady`。
- 离线、受限网络或需要生产稳定渲染时，将 Tailwind 编译为 CSS 并发布样式表，而非使用浏览器运行时。

## v4 浏览器运行时规则

Tailwind v4 以 CSS 为先：

```html
<style type="text/tailwindcss">
  @theme {
    --color-brand: oklch(0.68 0.2 252);
    --font-display: "Inter", sans-serif;
  }

  @utility headline-balance {
    text-wrap: balance;
    letter-spacing: 0;
  }
</style>
```

在浏览器运行时 composition 中避免仅 v3 的模式：

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

不要仅为 composition 的颜色、字体、间距或 utility 添加 `tailwind.config.js`。请使用 `@theme` 和 `@utility`。

**从 v3 迁移？** 显式加载现有 JS 配置：在 `text/tailwindcss` 块内写入 `@config "./tailwind.config.js";`。v4 **不会**自动检测 v3 配置文件。

## Composition 模式

用 Tailwind 处理静态布局与样式。与渲染时序相关的逻辑放在 GSAP 或其他可 seek 的 HyperFrames 适配器中。

```html
<section
  id="hero"
  class="clip absolute inset-0 grid place-items-center bg-zinc-950 text-white"
  data-start="0"
  data-duration="5"
  data-track-index="1"
>
  <div class="w-[1280px] max-w-[82vw] text-center">
    <h1 class="text-7xl font-black leading-none text-balance">Render-ready Tailwind</h1>
  </div>
</section>
```

重复项请**通过 CSS 变量参数化**——保持 class 列表静态，以便运行时能看到每个 utility：

```html
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 0"></span>
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 1"></span>
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 2"></span>
```

## 动态 Class 安全

浏览器运行时扫描它能看到的 class。不要在 seek 时才拼装渲染关键 class 名：

```js
// Risky: the runtime may never see every generated class.
element.className = `bg-${color}-500`;
```

优先在 HTML、data 变体或显式 CSS 中使用完整 class token：

```html
<div data-tone="blue" class="bg-blue-500 data-[tone=rose]:bg-rose-500"></div>
```

若无法避免生成 class，确保完整 class token 在验证前已出现在 `text/tailwindcss` 块中。

## 视频专用约束

v4 与渲染模式下的常见陷阱。以下每条均为硬性规则：

- **仅使用稳定尺寸** — 使用 `w-[…]` / `h-[…]` / `aspect-video` / grid / flex。**不要使用 `md:` / `lg:` 断点**（渲染器为固定视口）。
- **通过 transform / opacity 动画** — `translate-*`、`scale-*`、`opacity-*` 适合 seek；动画化 Tailwind 尺寸类 utility 则不适合。
- **渲染关键动效不要用 `transition-*`** — 可 seek 的运行时（GSAP）必须掌控状态。
- **不要使用交互变体** — `hover:` / `focus:` / `active:` / `group-*:` / `peer-*:` / scroll / pointer 变体在渲染期间不会触发。
- **裸 `border` 在 v4 有问题** — v4 默认为 `currentColor`（v3 为 `gray-200`）。务必写清颜色：`border border-white/20`。
- **v4 utility 重命名** — `shadow-sm` → `shadow-xs`，`rounded-sm` → `rounded-xs`，`outline-none` → `outline-hidden`，`flex-shrink-*` → `shrink-*`，`flex-grow-*` → `grow-*`。
- **现代 CSS 可用** — `color-mix()`、容器查询、逻辑属性均可；渲染器为当前版 Chrome。

## 验证

```bash
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect

# Render proof — frame 0 must NOT flash unstyled content. Preview alone can hide this.
npx hyperframes render . --workers 1 --quality draft --output tailwind-proof.mp4
```

## 快速调试清单

渲染中 Tailwind 样式未生效时，按顺序检查：

1. 项目是否通过 `npx hyperframes init --tailwind` 脚手架创建？
2. `index.html` 的 `<head>` 是否包含 `<script src="…@tailwindcss/browser@4.2.4…">`（而非 `cdn.tailwindcss.com`）？
3. `<head>` 中是否存在 `window.__tailwindReady` Promise？
4. 文件中是否没有 v3 指令（`@tailwind base/components/utilities`）？
5. 是否已将 token 从 `tailwind.config.js` 迁到 `@theme`（或 v3 迁移时使用 `@config` 引用）？
6. 每个渲染关键 class 是否以完整静态 token 出现（避免 `bg-${color}-500` 式拼装）？
7. 重新运行 `npx hyperframes validate`，再执行上述渲染验证。
