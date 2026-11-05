# 场景转场

转场告诉观众两个场景之间是什么关系。交叉淡入淡出表示「延续」；推入滑动表示「下一点」；模糊交叉淡入淡出表示「跟我一起飘」。选择转场时要匹配内容在情绪上正在做什么，而不仅是技术上的效果。

## 目录

- 多场景合成的动画规则
- 能量与情绪下的转场选择
- 叙事位置
- 模糊强度
- 预设
- 实现
- CSS 与 shader 指引
- 与 shader 兼容的 CSS 规则
- 视觉模式警告

## 多场景合成的动画规则

以下规则对每一个多场景合成都是不可妥协的：

1. **每个合成都使用转场。** 没有例外。没有转场的场景会像硬切（jump cut）。
2. **每个场景都使用入场动画。** 元素要「动进来」——透明度、位置、缩放等。任何场景都不应完整弹出到屏幕上。使用 `gsap.fromTo()`（不要用 `gsap.from()`），以便起始状态明确：`from()` 是向当前 CSS 动画，若与 CSS `opacity: 0` 搭配会变成 0→0 空操作，元素永远不会出现（见 `/hyperframes-core` → sub-compositions）。
3. **禁止出场动画**，最后一幕除外。不要在转场触发前用 `gsap.to()` 把元素动画移出。转场本身就是出场。转场开始时，即将离场的场景内容必须完全可见——由转场负责视觉交接。
4. **最后一幕例外：** 最后一幕可以把元素淡出（例如合成结尾淡入黑场）。这是唯一允许出场动画的场景。

```js
// ❌ BANNED — fading the outgoing scene out, then the next scene just runs its entrance.
//    This is a jump cut with a dip, not a transition.
tl.to("#s1", { opacity: 0, duration: 0.4 }, 4.0);
tl.from("#s2 .headline", { y: 40, opacity: 0 }, 4.4);

// ✅ CORRECT — outgoing and incoming animate AT THE SAME TIME T; the motion IS the handoff.
const T = 4.0;
tl.to("#s1", { yPercent: -100, filter: "blur(8px)", duration: 0.5, ease: "power3.in" }, T);
tl.fromTo("#s2", { yPercent: 100 }, { yPercent: 0, duration: 0.5, ease: "power3.out" }, T);
```

> **读完本文件还不算完成。** 本概览告诉你选**哪种**转场以及**何时**用。在写任何转场之前，你必须打开本目录下的 **`catalog.md`**，查看 GSAP 代码以及每条转场都必须遵守的硬性规则——*定位新场景 → 动画出场 → 交换 → 动画入场 → 清理 overlay*——并查阅各类别的 `css-*.md` 了解细节。只凭本概览编写转场，就会做出上面 ❌ 那种模式。

## 能量 → 主转场

| 能量                                   | CSS 主选                     | Shader 主选                          | 点缀                           | 时长      | 缓动                   |
| ---------------------------------------- | ---------------------------- | ------------------------------------ | ------------------------------ | --------- | ---------------------- |
| **平静**（ wellness、品牌故事、奢华） | 模糊交叉淡入淡出、焦点拉焦   | Cross-warp morph、thermal distortion | Light leak、circle iris        | 0.5-0.8s  | `sine.inOut`, `power1` |
| **中等**（企业、SaaS、讲解类）  | Push slide、staggered blocks | Whip pan、cinematic zoom             | Squeeze、vertical push         | 0.3-0.5s  | `power2`, `power3`     |
| **高**（促销、体育、音乐、发布） | Zoom through、overexposure   | Ridged burn、glitch、chromatic split | Staggered blocks、gravity drop | 0.15-0.3s | `power4`, `expo`       |

选**一种**主转场（约占场景切换的 60–70%）+ 1–2 种点缀。不要每个场景都用不同转场。

## 情绪 → 转场类型

思考转场在**传达**什么，而不只是长什么样。

| 情绪                     | 转场                                                                                                                          | 为何有效                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| **温暖 / 亲切**      | Light leak、blur crossfade、focus pull、film burn · **Shader:** thermal distortion、light leak、cross-warp morph                     | 边缘柔和、暖色 wash。不要尖锐或机械感。                                 |
| **冷 / 临床**      | Squeeze、zoom out、blinds、shutter、grid dissolve · **Shader:** gravitational lens                                                   | 内容被机械地变换——压缩、缩小、切片、网格化。                      |
| **编辑 / 杂志风** | Push slide、vertical push、diagonal split、shutter · **Shader:** whip pan                                                            | 像翻页或切分版式。干净的方向性运动。                        |
| **科技 / 未来感**    | Grid dissolve、staggered blocks、blinds、chromatic aberration · **Shader:** glitch、chromatic split                                  | Grid dissolve 是核心「数据感」转场。Shader glitch 增加 posterization 与 scan lines。 |
| **紧张 / 尖锐**         | Glitch、VHS、chromatic aberration、ripple · **Shader:** ridged burn、glitch、domain warp                                             | 不稳定、扭曲、数字崩坏。Ridged burn 增加闪电裂纹般锐边。   |
| **活泼 / 趣味**        | Elastic push、3D flip、circle iris、morph circle、clock wipe · **Shader:** ripple waves、swirl vortex                                | Overshoot、弹跳、旋转、扩张。Swirl vortex 增加有机螺旋扭曲。        |
| **戏剧 / 电影感** | Zoom through、zoom out、gravity drop、overexposure、color dip to black · **Shader:** cinematic zoom、gravitational lens、domain warp | 尺度、重量、光效极端。Shader 转场增加逐像素深度。                      |
| **高端 / 奢华**     | Focus pull、blur crossfade、color dip to black · **Shader:** cross-warp morph、thermal distortion                                    | 克制。Cross-warp morph 让两幕有机地流入彼此。                  |
| **复古 / 模拟**       | Film burn、light leak、VHS、clock wipe · **Shader:** light leak                                                                      | 有机的不完美。暖色 bleed、scan line 位移。                            |

## 叙事位置

| 位置                   | 用法                                                                        | 原因                                                   |
| -------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------- |
| **开场**                | 最有辨识度的转场。匹配情绪。0.4–0.6s                 | 为整片设定视觉语言。        |
| **相关要点之间** | 你的主转场。保持一致。0.3s                                  | 不要分散注意力——内容在延续。           |
| **话题切换**           | 与主转场不同。Staggered blocks、shutter、squeeze。 | 暗示「新段落」——观众大脑会重置。    |
| **高潮 / 英雄揭示**   | 最大胆的点缀。最快或最戏剧化。                             | 这是回报——把最好的转场用在这里。 |
| **收束**              | 回到柔和。Blur crossfade、crossfade。0.5–0.7s                      | 高潮后让观众「呼气」。               |
| **片尾**                  | 最慢、最简单。Crossfade、color dip to black。0.6–1.0s                 | 收尾。结尾不要引入新能量。       |

## 按能量划分的模糊强度

| 能量     | 模糊    | 时长 | 峰值保持 |
| ---------- | ------- | -------- | ------------ |
| **平静**   | 20-30px | 0.8-1.2s | 0.3-0.5s     |
| **中等** | 8-15px  | 0.4-0.6s | 0.1-0.2s     |
| **高**   | 3-6px   | 0.2-0.3s | 0s           |

## 预设

| 预设     | 时长 | 缓动            |
| ---------- | -------- | ----------------- |
| `snappy`   | 0.2s     | `power4.inOut`    |
| `smooth`   | 0.4s     | `power2.inOut`    |
| `gentle`   | 0.6s     | `sine.inOut`      |
| `dramatic` | 0.5s     | `power3.in` → out |
| `instant`  | 0.15s    | `expo.inOut`      |
| `luxe`     | 0.7s     | `power1.inOut`    |

## 实现

阅读本目录下的 `catalog.md` 获取各类转场的 GSAP 代码与硬性规则，并阅读 `css-*.md` 了解各类别的实现细节。

| 类别    | CSS                                                            | Shader (WebGL)                                                            |
| ----------- | -------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Push/slide  | Push slide、vertical push、elastic push、squeeze               | Whip pan                                                                  |
| Scale/zoom  | Zoom through、zoom out、gravity drop、3D flip                  | Cinematic zoom、gravitational lens                                        |
| Reveal/mask | Circle iris、diamond iris、diagonal split、clock wipe、shutter | SDF iris                                                                  |
| Dissolve    | Crossfade、blur crossfade、focus pull、color dip               | Cross-warp morph、domain warp                                             |
| Cover       | Staggered blocks、horizontal blinds、vertical blinds           | —                                                                         |
| Light       | Light leak、overexposure burn、film burn                       | Light leak (shader)、thermal distortion                                   |
| Distortion  | Glitch、chromatic aberration、ripple、VHS tape                 | Glitch (shader)、chromatic split、ridged burn、ripple waves、swirl vortex |
| Pattern     | Grid dissolve、morph circle                                    | —                                                                         |

## CSS 无法实现的转场

避免：star iris、tilt-shift、lens flare、hinge/door。原因见 catalog.md。

## CSS 与 Shader

CSS 转场用 opacity、transform、clip-path 和 filter 动画场景容器。Shader 转场在 WebGL 画布上逐像素合成两幕纹理——可以 warp、dissolve、morph，这是 CSS 做不到的。

**两者都是一等选项。** Shader 由 `@hyperframes/shader-transitions` 包提供——从包中 import，不要手写原始 GLSL。CSS 转场搭建更简单。按你想要的效果选择，而不是按哪种更省事。

**可以混用。** 同一合成里可以部分转场用 WebGL shader，部分用 CSS crossfade。在任意 `TransitionConfig` 条目省略 `shader` 字段即可得到平滑 opacity crossfade，而不是 WebGL 效果：

```js
var tl = HyperShader.init({
  bgColor: "#000",
  accentColor: "#6366f1",
  scenes: ["s1", "s2", "s3", "s4"],
  transitions: [
    { time: 4.0, shader: "sdf-iris", duration: 0.7 }, // WebGL shader
    { time: 8.5, duration: 0.8 }, // no shader → CSS crossfade
    { time: 13.0, shader: "domain-warp", duration: 0.6 }, // WebGL shader
  ],
});
```

无论转场类型如何，HyperShader 都会管理所有场景可见性。让它创建时间轴（不要向 `init()` 传入 `timeline:`），在调用之后把节拍动画加到返回的 `tl` 上。

## 与 Shader 兼容的 CSS 规则

Shader 转场通过 html2canvas 将 DOM 场景捕获为 WebGL 纹理。Canvas 2D 渲染管线与 CSS 并不完全一致。遵循以下规则，避免转场边界出现可见瑕疵：

1. **渐变中不要用 `transparent` 关键字。** Canvas 会把 `transparent` 插值为 `rgba(0,0,0,0)`（零 alpha 的黑色），产生暗边。始终用目标色在零 alpha：`rgba(200,117,51,0)`，不要用 `transparent`。
2. **厚度小于 4px 的元素不要用渐变背景。** Canvas 无法在 1–2px 元素上匹配 CSS 渐变渲染。细 accent 线用纯色 `background-color`。
3. **捕获期间可见的元素不要用 CSS 变量（`var()`）。** html2canvas 不能可靠解析自定义属性。内联样式使用字面量颜色值。
4. **用 `data-no-capture` 标记无法捕获的装饰元素。** 捕获函数会跳过它们。它们在 live DOM 上存在，但不在 shader 纹理里。用于无法遵守上述规则的元素。
5. **渐变 opacity 不要低于 0.15。** 低于 10% opacity 的渐变元素在 canvas 与 CSS 中渲染不同。提高到 0.15+，或用等亮度的纯色。
6. **每个 `.scene` div 必须有显式 `background-color`，并在 `init()` 配置里传入相同的 `bgColor`。** 包通过 html2canvas 捕获场景元素。`.scene` 上的 CSS `background-color` 与 `bgColor` 配置必须一致。缺任一都会导致纹理渲染为黑色。

这些规则仅适用于 shader 转场合成。纯 CSS 合成无此限制。

## 视觉模式警告

避免产生可见重复几何图案的转场——瓷砖网格、六边形单元、均匀点阵、等距 blob 圆。无论背后数学多复杂，都会显得廉价、人工。有机噪声（FBM、domain warping）是好的，因为不规则。几何重复是坏的，因为眼睛会立刻看出网格。
