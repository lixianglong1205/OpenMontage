# 子合成（Sub-Compositions）

子合成是嵌入宿主合成中的独立 HTML 文件。HyperFrames 会加载它、独立 seek，并在 `data-start` 处将结果合成到宿主中。

## 宿主接线

在宿主合成中，子合成以带有 `data-composition-src` 的 clip 形式出现：

```html
<div
  id="chart"
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="8"
  data-track-index="2"
  data-width="1920"
  data-height="1080"
></div>
```

- 宿主上的 `data-composition-id` 必须与 `data-composition-src` 所指文件内部的 `data-composition-id` 一致。
- 宿主 clip 还需要自己的 `data-start`、`data-duration`、`data-track-index`、`data-width`、`data-height`。

## 子合成文件结构

### 心智模型 — 运行时实际在做什么

当宿主通过 `data-composition-src` 加载子合成时，运行时：

1. `fetch` 该 HTML 文件。
2. 用 `DOMParser` 解析。
3. **找到 `<template>` 元素，并仅将其内容克隆到宿主插槽中。**
4. **`<template>` 之外的一切**（包括整个 `<head>`）**都会被丢弃**。

因此 `<template>` 不只是包装器 — 它是**传输容器**。若某节点需要在实际渲染中存在，它必须在 `<template>` 内。没有例外。

### 文件形态

```html
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <!-- head is metadata for the source file only; the runtime ignores it -->
  </head>
  <body>
    <template>
      <!-- EVERYTHING the runtime needs goes here: styles, markup, scripts -->
      <style>
        /* Root: style by #root, never a class. (At render the CSS is scoped to
           data-composition-id, so a class on the root stops matching — see Pitfall 3.) */
        #root {
          position: absolute;
          inset: 0;
          color: #fff;
        }
        /* .label, #bar, … — descendants, plain selectors */
      </style>

      <div id="root" data-composition-id="data-chart" data-width="1920" data-height="1080">
        <!-- sub-composition markup -->
      </div>

      <script>
        window.__timelines = window.__timelines || {};
        const tl = gsap.timeline({ paused: true });
        // ... build timeline ...
        window.__timelines["data-chart"] = tl;
      </script>
    </template>
  </body>
</html>
```

与**独立**合成对比：独立合成将根节点直接放在 `<body>` 中，没有 `<template>` 包装。

## 能通过静态检查但在渲染时仍会失败的常见陷阱

`lint`、`validate` 和 `inspect` 是逐文件单独评估的。以下两类失败属于**跨文件挂载契约**，只有在运行时真正尝试挂载子合成时才会暴露。创作时留意它们，并用下方的预渲染检查清单验证。

### 陷阱 1 — 把 `<style>` 放在 `<head>` 而非 `<template>` 内

```html
<!-- ❌ WRONG — looks normal, ships catastrophically broken -->
<head>
  <style>
    #root { font-size: 88px; ... }
  </style>
</head>
<body>
  <template>
    <div id="root" data-composition-id="data-chart" ...>...</div>
  </template>
</body>

<!-- ✅ RIGHT — styles are inside the template, root styled by #root (see Pitfall 3) -->
<head></head>
<body>
  <template>
    <style>
      #root { font-size: 88px; ... }
    </style>
    <div id="root" data-composition-id="data-chart" ...>...</div>
  </template>
</body>
```

**为何会这样：** 标准 HTML 惯例会把 `<style>` 放在 `<head>`。在独立 HTML 文件中这是对的。在 HyperFrames 子合成中**不是** — 运行时只克隆 `<template>` 的内容，因此 `<head><style>` 会被直接丢弃。

**症状：** 合成能通过 lint / validate / inspect，渲染也能完成，但所有文本都会以左上角 tiny 的未样式默认字体出现，SVG 会撑满画布尺寸，因为 CSS 从未进入 live DOM。同样适用于 `<script>` 块、`<link rel="stylesheet">`、自定义元素注册 — 任何需要在渲染中执行或生效的内容都必须放在 `<template>` 内。

### 陷阱 2 — 宿主 `data-composition-id` ≠ 内部 template 的 `data-composition-id`

```html
<!-- ❌ WRONG — host renames the slot; runtime can't find the timeline -->
<!-- host file (e.g. index.html) -->
<div data-composition-id="chart-mount" data-composition-src="compositions/chart.html" ...></div>

<!-- chart.html -->
<template>
  <div data-composition-id="data-chart" ...>...</div>
  <script>
    window.__timelines["data-chart"] = tl;
  </script>
</template>

<!-- ✅ RIGHT — both ids match, and the timeline key matches them too -->
<div data-composition-id="data-chart" data-composition-src="compositions/chart.html" ...></div>
<!-- chart.html template root: data-composition-id="data-chart" -->
<!-- timeline: window.__timelines["data-chart"] = tl; -->
```

**为何会这样：** 给宿主插槽起名 `chart-mount`（「挂载点」）而内部用 `data-chart`（「实际图表」）感觉很自然。HyperFrames 不是这样工作的 — **宿主的 `data-composition-id` 是框架用来查找已注册 timeline 的 lookup key**。Lint 会通过，因为每个文件内的 id 各自有效；跨文件不一致只会在渲染时爆雷。

**症状：** 渲染日志出现 `Sub-composition timelines not registered after 45000ms: <host-id>`（每个不匹配的插槽一条），每个场景等 45 秒，然后捕获静态初始帧（视频时长正常但没有动画）。

### 陷阱 3 — 用 class 而非 `#root` 给根节点设样式

```html
<!-- ❌ WRONG — class on the root, stylesheet keyed off it -->
<template>
  <style>
    .frame {
      position: absolute;
      inset: 0;
      background: #faf9f5;
    }
    .frame .title {
      font-size: 120px;
    }
  </style>
  <div id="root" class="frame" data-composition-id="03-scene" ...>
    <div class="title">…</div>
  </div>
</template>

<!-- ✅ RIGHT — root styled by #root, descendants by plain selectors -->
<template>
  <style>
    #root {
      position: absolute;
      inset: 0;
      background: #faf9f5;
    }
    .title {
      font-size: 120px;
    }
  </style>
  <div id="root" data-composition-id="03-scene" ...>
    <div class="title">…</div>
  </div>
</template>
```

**为何会这样：** 子合成内联到一次合成渲染时，编译器**将每个文件的 CSS 限定在其 `data-composition-id` 上**，避免场景互相泄漏样式 — 每条规则 `S` 会变成 `[data-composition-id="<id>"] S`（**后代**选择器）。若最左选择器是**根节点自身的 class**（`.frame`），则变成 `[data-composition-id="<id>"] .frame`，无法匹配根节点（根就是 scoped 元素本身，不是其后代），因此**所有 `.frame…` 规则会静默失效**。`#root` 被 scoper 特殊处理，仍能匹配根；普通后代选择器（`.title`）正常匹配。每场景的 class 命名空间也是多余的 — `data-composition-id` 作用域已经隔离各场景样式。

**症状：** 与陷阱 1 **完全相同** — 左上角 tiny 未样式文本、图片自然尺寸、仅内联样式（如卡片背景）幸存。陷阱在于：这能通过 `lint`/`validate`/`inspect`（它们孤立评估、未 scoped）**且在 `preview` 里看起来完美**（Studio 在各自 iframe 挂载各场景，也未 scoped） — 只在合成 MP4 渲染时失败。Lint 规则 `subcomposition_root_styled_by_class` 会标记；registry 阻塞（如 `apple-money-count`）示范 `#root` 模式。

### 渲染前验证清单

```bash
# For every sub-composition file in compositions/:
#   1) <style> + <script> + main markup all live INSIDE <template>
grep -n "<style\|<script\|<template" compositions/<scene>.html
#      → first <style>/<script>/<div data-composition-id> should be AFTER <template>, before </template>

#   2) host data-composition-id == internal data-composition-id == window.__timelines key
grep "data-composition-id" index.html
grep "data-composition-id\|__timelines\[" compositions/<scene>.html
#      → all three strings must match exactly per scene

#   3) the root is styled by #root, not by a class on the data-composition-id element
grep -n 'data-composition-id=' compositions/<scene>.html
#      → that element should NOT also carry a class="…" that the <style> keys off
#        (e.g. `.frame { … }`); scoping drops it. Style the root via #root. See Pitfall 3.
```

关于运行时端到端检查（快速 `snapshot` + 逐场景帧目检），见 `hyperframes-cli` 的 Minimum Completion Gate 中的 **Visual smoke test** 步骤 — 那是唯一能捕获上述三个陷阱的门禁。

## HyperFrames 对子合成的处理

- 加载文件，并在其内部 `data-composition-id` 下注册 timeline。
- 独立于宿主 playhead seek 子合成的 timeline。
- 从宿主 clip 的 `data-start` 起播放子合成内容，持续 `data-duration` 秒。

**不要**手动把子合成 timeline `master.add(child)` 嵌进宿主 timeline。HyperFrames 已独立驱动它们 — 在 GSAP 中嵌套会导致 double-seek。

### 宿主 clip 的 `data-duration` 即插槽可见窗口

宿主 clip 上的 `data-duration` 定义**插槽可见多久**，且优先于子合成内部 GSAP timeline 长度。两点后果：

- **内部 timeline 短于插槽 → 插槽保持。** 若子合成 GSAP timeline 在 `data-duration` 结束前结束，插槽会在剩余窗口内一直显示最后一帧。无需用空 tween 填充 timeline。
- **`data-duration` 短于宿主合成 → 插槽在自身 `data-duration` 结束时结束（并变空白）。** 这是预期行为：clip 是时间轴上的固定长度窗口，不是「填到合成结束」。若要让子合成全程可见，将其 `data-duration` 设为覆盖宿主窗口（或再加 clip 覆盖剩余时间）。单个全屏子合成短于整个合成几乎总是错误 — linter 会标记为 `subcomposition_blanks_before_host`。

## 子合成内的动画

入场 tween 优先用 `gsap.fromTo()` 而非 `gsap.from()`。宿主在 clip 每次变为可见时会 re-seek 子合成；`gsap.from()` 在注册时记录起始状态，seek-back 可能不同步，而 `gsap.fromTo()` 显式声明两端点，可干净重播。

## 每实例变量

若子合成在 `<html>` 元素上声明变量（`data-composition-variables`），宿主可按实例覆盖值：

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-variable-values='{"title":"Q4 Revenue","accent":"#66d9ef"}'
  data-start="2"
  data-duration="8"
  data-track-index="2"
  data-width="1920"
  data-height="1080"
></div>
```

宿主可用不同 `data-variable-values` 多次渲染同一子合成，产生每实例变体。变量声明语法见 `variables-and-media.md`。
