# 字体迁移

字体是迁移过程中最主要的「非翻译」噪声来源。在未安装真实字体时，同样的 `font-weight: 800` 在 HF 的 `chrome-headless-shell` 上渲染出的粗细，会明显比 Remotion 捆绑的 Chromium 更粗。验证表明，这会在噪声底线上造成约 0.025 的平均 SSIM 损失。

## 模式：`@remotion/google-fonts/<Family>`

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";
loadFont("normal", { weights: ["400", "800"] });
```

翻译为 `<head>` 中的 `<link>` 标签：

```html
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap"
    rel="stylesheet"
  />
  <style>
    body {
      font-family: Inter, sans-serif;
    }
  </style>
</head>
```

从 import 路径和 `loadFont` 参数中提取字体族名与字重。HF 的编译器会在渲染时内联 Google Fonts 的 CSS，因此每次渲染不会额外产生网络往返。

## 模式：通过 `@font-face` 加载本地字体

```tsx
import { Font } from "remotion";

Font.loadFont("/MyFont.woff2", "MyFont");
```

翻译为 `@font-face` 规则：

```html
<style>
  @font-face {
    font-family: "MyFont";
    src: url("assets/MyFont.woff2") format("woff2");
    font-weight: 400;
    font-style: normal;
  }
</style>
```

将字体文件复制到 HTML 旁的 `hf-src/assets/` 目录。

## 模式：系统字体回退（不加载字体）

```tsx
<div style={{ fontFamily: "Helvetica, Arial, sans-serif" }}>...</div>
```

在 HF 中使用相同字符串即可——但要注意：在 Linux 上若未安装真正的 Helvetica（CI 环境常见），Remotion 与 HF 会回退到**不同**的无衬线系统字体，因为它们捆绑的 Chromium 版本不同。这就是噪声底线：约 0.025 的平均 SSIM 代价，在大字重（800+）下表现为笔画宽度差异。

若某个特定 fixture 需要与 Remotion 渲染完全一致，请显式加载相同字体——不要依赖系统回退。

## 拿不准时：使用 Inter

Inter 在不同 Chromium 版本间渲染一致，且免费。当需要在验证 harness 中最小化字体漂移时，将 Remotion 中任何「系统无衬线」组合迁移为 Inter。

## 字体加载与 `delayRender`

Remotion 使用 `delayRender()` 推迟首帧，直到字体加载完成。HF 的编译器在编译时内联 Google Fonts，并通过 Frame Adapter 模式等待 `@font-face` 就绪——翻译时 `delayRender` 调用可以去掉。详见 [media.md](media.md)。

## 多字重加载

当 Remotion 加载多个字重时：

```tsx
loadFont("normal", { weights: ["400", "500", "700", "800"] });
```

在 Google Fonts URL 中内联全部字重：

```
?family=Inter:wght@400;500;700;800&display=swap
```

翻译规则：枚举组合 CSS 中出现的每一个不同的 `font-weight` 值（例如 `font-weight: 800` → 必须加载字重 800）。若 Remotion 源码加载了实际未使用的字重，可省略。

## 字体子集化

Remotion 的 `loadFont` 不做子集化；HF 的编译器目前也不做。翻译时不要在此优化——与 Remotion 源码保持相同字重集合是无损的。
