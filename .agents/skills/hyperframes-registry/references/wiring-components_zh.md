# 组件接入

组件是效果片段——可直接合并进现有 composition 的 HTML、CSS，以及可选的 JS。与 block 不同，组件没有独立时间轴；它们参与宿主 composition 的时间轴。

## 一般流程

1. 运行 `hyperframes add <component-name>`
2. 打开安装后的文件（例如 `compositions/components/grain-overlay.html`）
3. 阅读注释头中的用法说明
4. 将各部分复制到你的宿主 composition：
   - **HTML 元素** — 放在你的 `<div data-composition-id="...">` 内
   - **CSS 样式** — 放入 composition 的 `<style>` 块
   - **JS 设置** — 放入 composition 的 `<script>`，且位于你的时间轴代码之前
   - **Timeline 调用** — 放入你的 GSAP 时间轴（若组件暴露了此类调用）

## 示例：grain-overlay（仅 CSS，无需时间轴集成）

```html
<!-- Paste the overlay div into your composition -->
<div
  id="grain-overlay"
  style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 100;"
>
  <div class="grain-texture"></div>
</div>
```

然后将 CSS keyframes 与 `.grain-texture` 规则粘贴到你的样式中。无需 GSAP 时间轴调用——颗粒效果通过 CSS `@keyframes` 动画实现。

## 示例：shimmer-sweep（需要时间轴集成）

完整的 shimmer-sweep 接入说明（HTML 包裹、CSS、JS 设置与时间轴调用）见 `examples/add-component.md`。

## 关键原则

- 组件继承宿主 composition 的尺寸与时长
- 将组件 HTML 放在相对内容的合适 z-index 层级
- 阅读各片段注释头中的可定制参数
- 接入完成后运行 `hyperframes lint`，以发现结构问题
