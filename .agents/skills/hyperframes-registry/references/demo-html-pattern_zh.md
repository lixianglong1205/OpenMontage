# demo.html 约定

## 为何组件附带 demo.html

注册表中的每个组件都会在 snippet 旁附带一个 `demo.html` 文件。demo 有两个用途：

1. **预览夹具（Preview fixture）** — CI 预览流水线渲染 demo，为目录文档页生成缩略图与预览视频。

2. **用法示例** — demo 将组件效果应用于代表性内容，作为可运行的参考。

## Demo 结构

demo 是一份完整、可独立运行的 HTML 组合：

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Component Name — Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      /* reset + canvas size */
    </style>
  </head>
  <body>
    <div data-composition-id="<name>-demo" data-width="1920" data-height="1080" data-duration="N">
      <!-- Demo content showing the effect -->
      <!-- Component snippet inlined here -->
    </div>
    <script>
      // GSAP timeline demonstrating the effect
      window.__timelines = window.__timelines || {};
      window.__timelines["<name>-demo"] = tl;
    </script>
  </body>
</html>
```

关键约定：

- `data-composition-id` 为 `<component-name>-demo`，以避免冲突
- demo 自包含 — snippet 中的全部 CSS 与 JS 均内联
- GSAP 时间轴注册在 `window.__timelines` 上
- 时长应足够展示效果（通常 5–8 秒）

## Block 不需要 demo.html

Block 本身已是可独立渲染的组合，只有 component 需要 demo 包装。

## Demo 不会被安装

`demo.html` **不会**由 `hyperframes add` 安装 — 它仅存在于注册表中，用于预览生成与参考。
