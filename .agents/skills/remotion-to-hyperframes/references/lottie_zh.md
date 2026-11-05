# Lottie 迁移：@remotion/lottie → HF lottie 适配器

Lottie 动画是较清晰的迁移场景 — HF 内置
[Lottie 适配器](https://github.com/heygen-com/hyperframes/blob/main/packages/core/src/runtime/adapters/lottie.ts)，
同时支持 `lottie-web` 与 `@lottiefiles/dotlottie-web`。该
适配器会自动发现注册在 `window.__hfLottie` 上的动画，
并通过 `goToAndStop` 逐帧定位。

## 模式

```tsx
import { Lottie } from "@remotion/lottie";
import animationData from "./hello.json";

export const MyComp = () => (
  <AbsoluteFill>
    <Lottie animationData={animationData} loop={false} />
  </AbsoluteFill>
);
```

对应迁移为：

```html
<div id="stage" ...>
  <div id="lottie-anim" style="width:100%;height:100%"></div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
  <script>
    const anim = lottie.loadAnimation({
      container: document.getElementById("lottie-anim"),
      renderer: "svg",
      loop: false,
      autoplay: false,
      path: "assets/hello.json",
    });
    window.__hfLottie = window.__hfLottie || [];
    window.__hfLottie.push(anim);
  </script>
</div>
```

与典型 Lottie 嵌入相比的主要差异：

- `autoplay: false` — HF 通过 seek 驱动播放
- 通常 `loop: false`（除非 Remotion 中 `loop={true}`）
- `window.__hfLottie.push(anim)` 将动画挂接到 HF 的
  逐帧 seek

## 资源处理

Remotion 通过 webpack import 打包动画 JSON。HF 需要 JSON
文件位于磁盘上的 `assets/`，并通过路径引用：

1. 将 `hello.json` 从 Remotion 项目复制到 `hf-src/assets/`。
2. 在 `loadAnimation` 中使用 `path: "assets/hello.json"` 引用。

对于 dotlottie（二进制）格式，改用 `@lottiefiles/dotlottie-web`：

```html
<script src="https://unpkg.com/@lottiefiles/dotlottie-web"></script>
<canvas id="anim" style="width:100%;height:100%"></canvas>
<script>
  const player = new DotLottie({
    canvas: document.getElementById("anim"),
    src: "assets/hello.lottie",
    autoplay: false,
  });
  window.__hfLottie = window.__hfLottie || [];
  window.__hfLottie.push(player);
</script>
```

HF 适配器同时处理两种播放器 API（对 `goToAndStop`
与 `setCurrentRawFrameValue` / `seek` 做鸭子类型兼容）。

## 多个 Lottie 动画

同一 composition 中的多个 `<Lottie>` 实例均可工作 — 将每个实例
推入 `window.__hfLottie`，适配器会同步 seek 全部动画：

```js
window.__hfLottie.push(anim1);
window.__hfLottie.push(anim2);
window.__hfLottie.push(anim3);
```

## Lottie 源文件本身并不阻碍迁移

Lottie 动画自带确定性时间轴，是 Remotion composition 中
_最容易_ 迁移的部分，因为动画逻辑已自包含 — Remotion 与 HF
都不会对其做“动画”，二者仅 seek。迁移成本接近零。

## After Effects → Lottie 限制

Lottie 仅支持 After Effects 功能子集。表达式、多数
效果（投影、颜色叠加）、除 Normal/Add/
Multiply 外的混合模式、亮度遮罩及多数 3D 参数均不支持。若 Remotion composition 使用的 Lottie 文件依赖这些能力，
动画在 Remotion 与 HF 中都会失效 — 这不是迁移
问题，而是 Lottie 固有限制。完整支持特性列表见
[airbnb/lottie/after-effects.md](https://github.com/airbnb/lottie/blob/master/after-effects.md)。

## 循环行为

Remotion 的 `loop={true}` 会连续播放动画。迁移为播放器选项前，
请先检查生成的帧。HF
适配器按 composition 绝对时间 seek；不会在播放器之上额外做取模循环
或播放速率缩放。若要精确重复
周期或非默认播放速率，请将时序烘焙进 Lottie
资源，或在 Lottie 图层外编写显式时间轴并验证
渲染输出。

## 性能说明

据 [Lottie 适配器](https://github.com/heygen-com/hyperframes/blob/main/packages/core/src/runtime/adapters/lottie.ts)
文档：lottie-web 的 `goToAndStop(time, isFrame=false)` 以毫秒计时间；
适配器传入 `time * 1000` 以提高精度。这比
传入帧号更准确（尤其当动画内部
fps 与 HF 渲染 fps 不一致时）。
