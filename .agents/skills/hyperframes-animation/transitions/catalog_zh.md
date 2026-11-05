# 转场目录

硬性规则、场景模板，以及指向实现代码的路由说明。按需阅读你所需转场类型的参考文件——不要一次性加载全部。

## 目录

- CSS 转场的硬性规则
- Shader 转场
- 场景模板
- CSS 转场示例
- Shader 转场路由

## 硬性规则（CSS）

违反以下规则会导致真实 bug。

**场景可见性：** 场景 1 默认可见（不要设 `opacity: 0`）。场景 2 及之后在**容器** div 上设 `opacity: 0`。由 GSAP 揭示它们。不要使用可见性垫片（`timedEls`）。

**字体：** 直接写你想要的 `font-family`——编译器会通过 `@font-face` 与内联 data URI 自动嵌入支持的字体。无需 `<link>` 或 `@import`。在包括沙箱 iframe 在内的所有上下文中均可用。

**元素结构：** 在独立 composition 中，场景 div 不要加 `class="clip"`。只有根 div 设置 `data-composition-id` / `data-start` / `data-duration`。

**叠加层元素：** 交错块 = 全屏 1920×1080，不是细条。故障 RGB 叠加层 = 正常混合、35% 不透明度，不要用 `mix-blend-mode: multiply`（在深色背景上不可见）。漏光叠加层 = 大于画幅（2400px+），不要出现可见形状。过曝 = 对场景使用 `filter: brightness()`，不要只靠白色叠加层。

**VHS 磁带：** 用 `cloneNode(true)` 克隆真实场景内容，不要用色条。每条：宽于画幅（2020px，`left:-50px`）。红/蓝色差副本 z-index 高于主条带。用带种子的 PRNG 做确定性随机偏移。

**Z-index：** 重力下落、缩小、对角分割需要**离场**场景在上层（`zIndex: 10`），以便其退出时露出后方新场景（`zIndex: 1`）。

**页面燃烧：** 内容与页面一起燃烧——没有下落碎屑。在燃烧结束时用 `tl.set` 隐藏 scene1，**永远不要**用 `onComplete`（不可逆）。`onUpdate` 在 `wp <= 0` 时必须恢复 `clipPath: "none"` 以支持倒放。入场场景在燃烧进度 90% 时从黑场淡入。

**时钟擦除：** 9 点 polygon，含中间边缘位置。分 4 个象限用独立 tween 逐步推进。

**网格溶解：** 每个单元格循环 5 种调色板颜色，不要单色。

**百叶数量按能量：** 平静：4 横 / 6 竖。中等：6–8 横 / 8 竖。高：12–16 横 / 16 竖。

**不要使用：** 星形 iris（polygon 插值损坏）、移轴（无选择性 CSS 模糊）、镜头光晕（可见形状，非光学效果）、铰链/门（扭曲过快）。

## Shader 转场

Shader 设置、WebGL 初始化、捕获与 fragment shader 由 `@hyperframes/shader-transitions`（`packages/shader-transitions/`）处理。API 细节请阅读包源码。使用 shader 的 composition 须遵循本目录 `overview.md` 中的 shader 兼容 CSS 规则。

## 场景模板

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #000;
        font-family: "YOUR FONT", sans-serif; /* compiler embeds supported fonts automatically */
      }
      .scene {
        position: absolute;
        top: 0;
        left: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
      }
      #scene1 {
        z-index: 1;
        background: #color;
      }
      #scene2 {
        z-index: 2;
        background: #color;
        opacity: 0;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-width="1920"
      data-height="1080"
      data-start="0"
      data-duration="TOTAL"
    >
      <div id="scene1" class="scene"><!-- visible --></div>
      <div id="scene2" class="scene"><!-- hidden --></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      var tl = gsap.timeline({ paused: true });
      // Transition code here
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

每个转场遵循：定位新场景 → 动画离场 → 交换 → 动画入场 → 清理叠加层。

## CSS 转场

所有代码示例中，`old` 表示离场场景内层选择器，`new` 表示入场，`T` 为转场开始时间。按需阅读对应类型的参考文件。

| 类型           | 转场效果                                             | 参考                             |
| -------------- | ---------------------------------------------------- | -------------------------------- |
| Push           | 推滑、垂直推、弹性推、挤压                           | `transitions/css-push.md`        |
| Radial / Shape | 圆形 iris、菱形 iris、对角分割                       | `transitions/css-radial.md`      |
| 3D             | 3D 卡片翻转                                          | `transitions/css-3d.md`          |
| Scale / Zoom   | 穿 zoom、缩小                                        | `transitions/css-scale.md`       |
| Dissolve       | 交叉淡入淡出、模糊交叉、焦点拉、色 dip               | `transitions/css-dissolve.md`    |
| Cover          | 交错块、水平百叶、垂直百叶                           | `transitions/css-cover.md`       |
| Light          | 漏光、过曝 burn、胶片 burn                           | `transitions/css-light.md`       |
| Distortion     | 故障、色差、波纹、VHS 磁带                           | `transitions/css-distortion.md`  |
| Mechanical     | 快门、时钟擦除                                       | `transitions/css-mechanical.md`  |
| Grid           | 网格溶解                                             | `transitions/css-grid.md`        |
| Other          | 重力下落、变形圆                                     | `transitions/css-other.md`       |
| Blur           | 模糊穿过、方向模糊                                   | `transitions/css-blur.md`        |
| Destruction    | 页面燃烧                                             | `transitions/css-destruction.md` |

## Shader 转场

WebGL shader 转场由 `@hyperframes/shader-transitions`（`packages/shader-transitions/`）提供。该包负责设置、捕获、WebGL 初始化、渲染循环与 GSAP 集成。可用 shader 与 API 请阅读包源码——不要手动复制原始 GLSL。

内置效果不是上限。若没有内置覆盖的效果，你可以从零编写自定义 GLSL、改编网上找到的 shader 代码（ShaderToy、GLSL Sandbox、GitHub），或构建不属于现有类别的自定义 CSS 转场——以新方式组合 clip-path、transform 与 filter。若分镜需要尚不存在的效果，就实现它；框架能渲染浏览器能运行的任何内容。
