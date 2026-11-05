# 实战示例：添加组件

## 场景

用户希望为标题文字添加 shimmer 扫光效果。

## 步骤

### 1. 安装组件

```bash
hyperframes add shimmer-sweep
```

### 2. 阅读代码片段

打开 `compositions/components/shimmer-sweep.html` 并阅读注释头部说明。

### 3. 接入到你的 composition

**HTML** — 包裹目标元素：

```html
<div class="shimmer-sweep-target" style="--shimmer-color: rgba(255, 255, 255, 0.5)">
  <h1 class="title">AI-Powered Video</h1>
</div>
```

**CSS** — 从代码片段中粘贴 `.shimmer-sweep-target` 与 `.shimmer-mask` 规则。

**JS** — 粘贴自动注入脚本（放在 timeline 代码之前）：

```js
document.querySelectorAll(".shimmer-sweep-target").forEach((el) => {
  if (!el.querySelector(".shimmer-mask")) {
    const mask = document.createElement("div");
    mask.className = "shimmer-mask";
    el.appendChild(mask);
  }
});
```

**Timeline** — 添加扫光动画：

```js
tl.fromTo(
  ".shimmer-sweep-target",
  {
    "--shimmer-pos": "-20%",
  },
  {
    "--shimmer-pos": "120%",
    duration: 1.2,
    ease: "power2.inOut",
    stagger: 0.15,
  },
  1.5,
);
```

### 4. Lint 与预览

```bash
hyperframes lint
hyperframes preview
```

### 5. 自定义

- `--shimmer-color`：每个元素的高亮色
- `--shimmer-width`：光带宽度（默认 20%）
- `--shimmer-angle`：扫光方向（默认 120deg）
- Timeline 的 `duration`、`ease`、`stagger`：控制速度与观感
