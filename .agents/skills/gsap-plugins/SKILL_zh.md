---
name: gsap-plugins
description: GSAP 官方技能：GSAP 插件 — 注册、ScrollToPlugin、ScrollSmoother、Flip、Draggable、Inertia、Observer、SplitText、ScrambleText、SVG 与物理插件、CustomEase、EasePack、CustomWiggle、CustomBounce、GSDevTools。在用户询问 GSAP 插件、滚动定位、flip 动画、可拖拽、SVG 绘制或插件注册时使用。
license: MIT
---

# GSAP 插件

## 何时使用本技能

在编写或审查使用 GSAP 插件的代码时应用本技能：注册插件、滚动定位、flip/FLIP 动画、可拖拽元素、SVG（DrawSVG、MorphSVG、MotionPath）、文本（SplitText、ScrambleText）、物理、缓动插件（CustomEase、EasePack、CustomWiggle、CustomBounce）或 GSDevTools。ScrollTrigger 有独立技能（gsap-scrolltrigger）。

**相关技能：** 核心补间请用 **gsap-core**；ScrollTrigger 请用 **gsap-scrolltrigger**；React 请用 **gsap-react**。

## 注册插件

每个插件只需注册一次，以便 GSAP（及打包工具）知道要包含它。对项目中使用的每个插件调用 **gsap.registerPlugin()**：

```javascript
import gsap from "gsap";
import { ScrollToPlugin } from "gsap/ScrollToPlugin";
import { Flip } from "gsap/Flip";
import { Draggable } from "gsap/Draggable";

gsap.registerPlugin(ScrollToPlugin, Flip, Draggable);
```

- ✅ 在任何补间或 API 调用中使用插件之前先注册。
- ✅ 在 React 中，在顶层或应用中注册一次（例如在首次 useGSAP 之前）；不要在会重复渲染的组件内注册。useGSAP 本身也是插件，使用前需要先注册。

## 滚动

### ScrollToPlugin

动画化滚动位置（窗口或可滚动元素）。用于「滚动到元素」或「滚动到位置」，无需 ScrollTrigger。

```javascript
gsap.registerPlugin(ScrollToPlugin);

gsap.to(window, { duration: 1, scrollTo: { y: 500 } });
gsap.to(window, { duration: 1, scrollTo: { y: "#section", offsetY: 50 } });
gsap.to(scrollContainer, { duration: 1, scrollTo: { x: "max" } });
```

**ScrollToPlugin — 主要配置（scrollTo 对象）：**

| 选项 | 说明 |
|--------|-------------|
| `x`, `y` | 目标滚动位置（数字），或 `"max"` 表示最大滚动 |
| `element` | 要滚动到的选择器或元素（用于 scroll-into-view） |
| `offsetX`, `offsetY` | 相对目标位置的像素偏移 |

### ScrollSmoother

平滑滚动包装器（平滑原生滚动）。需要 ScrollTrigger 和特定 DOM 结构（内容包装 + smooth 包装）。需要平滑、带惯性的滚动时使用。设置详见 GSAP 文档；在 ScrollTrigger 之后注册。DOM 结构示例：

```html
<body>
	<div id="smooth-wrapper">
		<div id="smooth-content">
			<!--- ALL YOUR CONTENT HERE --->
		</div>
	</div>
	<!-- position: fixed elements can go outside --->
</body>
```

## DOM / UI

### Flip

用 `Flip.getState()` 捕获状态，再应用变更（如布局或 class 变更），然后用 `Flip.from()` 从先前状态动画到新状态（FLIP：First、Last、Invert、Play）。在两种布局状态之间动画（列表、网格、展开/折叠）时使用。

```javascript
gsap.registerPlugin(Flip);

const state = Flip.getState(".item");
// change DOM (reorder, add/remove, change classes)
Flip.from(state, { duration: 0.5, ease: "power2.inOut" });
```

**Flip — 主要配置（Flip.from vars）：**

| 选项 | 说明 |
|--------|-------------|
| `absolute` | flip 期间使用 `position: absolute`（默认：`false`） |
| `nested` | 为 `true` 时只测量第一层子元素（更适合嵌套 transform） |
| `scale` | 为 `true` 时缩放元素以适配（避免拉伸）；默认 `true` |
| `simple` | 为 `true` 时只动画 position/scale（更快，精度较低） |
| `duration`, `ease` | 标准补间选项 |

#### 更多信息

https://gsap.com/docs/v3/Plugins/Flip

### Draggable

使元素可用鼠标/触摸拖拽、旋转或抛出。用于滑块、卡片、可重排列表或任意拖拽交互。

```javascript
gsap.registerPlugin(Draggable, InertiaPlugin);

Draggable.create(".box", { type: "x,y", bounds: "#container", inertia: true });
Draggable.create(".knob", { type: "rotation" });
```

**Draggable — 主要配置选项：**

| 选项 | 说明 |
|--------|-------------|
| `type` | `"x"`、`"y"`、`"x,y"`、`"rotation"`、`"scroll"` |
| `bounds` | 元素、选择器或 `{ minX, maxX, minY, maxY }` 以限制拖拽范围 |
| `inertia` | `true` 启用抛出/惯性（需要 InertiaPlugin） |
| `edgeResistance` | 0–1；拖过边界时的阻力 |
| `cursor` | 拖拽时的 CSS 光标 |
| `onDragStart`, `onDrag`, `onDragEnd` | 回调；接收 event 与 target |
| `onThrowUpdate`, `onThrowComplete` | 启用 inertia 时的回调 |

### Inertia (InertiaPlugin)

与 Draggable 配合实现松手后的惯性，或跟踪任意对象任意属性的惯性/速度，再用简单补间平滑停住。使用 `inertia: true` 时与 Draggable 一起注册：

```javascript
gsap.registerPlugin(Draggable, InertiaPlugin);
Draggable.create(".box", { type: "x,y", inertia: true });
```

或跟踪某属性的速度：
```javascript
InertiaPlugin.track(".box", "x");
```

然后用 `"auto"` 延续当前速度并滑到停止：

```javascript
gsap.to(obj, { inertia: { x: "auto" } });
```

### Observer

跨设备规范化指针与滚动输入。用于滑动、滚动方向或自定义手势逻辑，而不像 ScrollTrigger 那样直接绑定滚动位置。

```javascript
gsap.registerPlugin(Observer);

Observer.create({
  target: "#area",
  onUp: () => {},
  onDown: () => {},
  onLeft: () => {},
  onRight: () => {},
  tolerance: 10
});
```

**Observer — 主要配置选项：**

| 选项 | 说明 |
|--------|-------------|
| `target` | 要观察的元素或选择器 |
| `onUp`, `onDown`, `onLeft`, `onRight` | 在该方向超过 tolerance 时的回调 |
| `tolerance` | 判定方向前的像素阈值；默认 10 |
| `type` | `"touch"`、`"pointer"` 或 `"wheel"`（默认：`"touch,pointer"`） |

## 文本

### SplitText

将元素文本拆分为字符、词和/或行（各自独立元素），以便交错或逐单位动画。需要逐字、逐词或逐行动画文本时使用。返回实例含 **chars**、**words**、**lines**（设置 `mask` 时还有 **masks**）。用 **revert()** 恢复原始 markup，或交给 **gsap.context()** 还原。与 **gsap.context()**、**matchMedia()**、**useGSAP()** 集成。API：**SplitText.create(target, vars)**（target = 选择器、元素或数组）。

```javascript
gsap.registerPlugin(SplitText);

const split = SplitText.create(".heading", { type: "words, chars" });
gsap.from(split.chars, { opacity: 0, y: 20, stagger: 0.03, duration: 0.4 });
// later: split.revert() or let gsap.context() cleanup revert
```

**onSplit()**（v3.13.0+）在每次拆分及 **autoSplit** 重新拆分时运行动画；从 **onSplit()** 返回补间/时间线时，SplitText 会在重新拆分时清理并同步进度：

```javascript
SplitText.create(".split", {
  type: "lines",
  autoSplit: true,
  onSplit(self) {
    return gsap.from(self.lines, { y: 100, opacity: 0, stagger: 0.05, duration: 0.5 });
  }
});
```

**SplitText — 主要配置（SplitText.create vars）：**

| 选项 | 说明 |
|--------|-------------|
| **type** | 逗号分隔：`"chars"`、`"words"`、`"lines"`。默认 `"chars,words,lines"`。只拆需要的部分（如不用行则 `"words, chars"`）以提升性能。避免仅 chars 且无 words/lines，或使用 **smartWrap: true** 防止奇怪换行。 |
| **charsClass**, **wordsClass**, **linesClass** | 各拆分元素的 CSS class。追加 `"++"` 可添加递增 class（如 `linesClass: "line++"` → `line1`、`line2`…）。 |
| **aria** | `"auto"`（默认）、`"hidden"` 或 `"none"`。无障碍：`"auto"` 在拆分元素上加 `aria-label`，在行/词/字元素上加 `aria-hidden`，屏幕阅读器读 label；`"hidden"` 对阅读器全部隐藏；`"none"` 不改 aria。若需暴露嵌套链接/语义，用 `"none"` 并加仅屏幕阅读器可见的副本。 |
| **autoSplit** | 为 `true` 时，字体加载完成或元素宽度变化（且拆分行）会 revert 并重新拆分，避免错误换行。**动画必须在 onSplit() 内创建**以指向新拆分元素；从 **onSplit()** **return** 动画以便重新拆分时自动清理与时间同步。 |
| **onSplit(self)** | 拆分完成时回调（**autoSplit** 为 `true` 时每次重新拆分也会调用）。接收 SplitText 实例。返回 GSAP 补间或时间线可在重新拆分时自动 revert/同步该动画。 |
| **mask** | `"lines"`、`"words"` 或 `"chars"`。为各单位包一层 `overflow: clip` 元素做遮罩/揭示。仅一种类型；包装器在实例 **masks** 数组（或设 class 时用 `-mask`）。 |
| **tag** | 包装元素标签；默认 `"div"`。行内用 `"span"`（注意：部分浏览器行内元素上 rotation/scale 等 transform 可能不渲染）。 |
| **deepSlice** | 为 `true`（默认）时，跨多行的嵌套元素（如 `<strong>`）会再细分，避免行在垂直方向被拉长。仅拆分行时生效。 |
| **ignore** | 不拆分的选择器或元素（如 `ignore: "sup"`）。 |
| **smartWrap** | 仅拆 **chars** 时，用词包在 `white-space: nowrap` 的 span 里，避免词中间换行。若已拆 words 或 lines 则忽略。默认 `false`。 |
| **wordDelimiter** | 词边界：字符串（默认 `" "`）、RegExp，或 `{ delimiter: RegExp, replaceWith: string }` 自定义拆分（如 hashtag 的零宽连接符或非拉丁语）。 |
| **prepareText(text, parent)** | 接收原始文本与父元素的函数；返回修改后的文本再拆分（如为无空格语言插入断行标记）。 |
| **propIndex** | 为 `true` 时在各拆分元素上加带索引的 CSS 变量（如 `--word: 1`、`--char: 2`）。 |
| **reduceWhiteSpace** | 合并连续空格；默认 `true`。v3.13.0 起还尊重换行，并可为 `<pre>` 插入 `<br>`。 |
| **onRevert** | 实例 revert 时的回调。 |

**提示：** 只拆要动画的部分（例如只动画词则跳过 chars）。自定义字体在加载后再拆（如 `document.fonts.ready.then(...)`）或使用 **autoSplit: true** 与 **onSplit()**。拆 chars 时为避免字距变化，可用 CSS `font-kerning: none; text-rendering: optimizeSpeed;`。避免 `text-wrap: balance`；可能干扰拆分。SplitText 不支持 SVG `<text>`。

**延伸阅读：** [SplitText](https://gsap.com/docs/v3/Plugins/SplitText/)

### ScrambleText

用 scramble/故障效果动画文本。揭示或过渡文本且带 scramble 效果时使用。

```javascript
gsap.registerPlugin(ScrambleTextPlugin);

gsap.to(".text", {
  duration: 1,
  scrambleText: { text: "New message", chars: "01", revealDelay: 0.5 }
});
```

## SVG

### DrawSVG (DrawSVGPlugin)

通过动画 `stroke-dashoffset` / `stroke-dasharray` 显示或隐藏 SVG 描边。适用于 `<path>`、`<line>`、`<polyline>`、`<polygon>`、`<rect>`、`<ellipse>`。用于「绘制」或「擦除」描边时。

**drawSVG 值：** 描述路径上描边的**可见段**（起止位置），不是「随时间从 A 动画到 B」。格式：百分或长度的 `"start end"`。例：`"0% 100%"` = 整段描边；`"20% 80%"` = 仅 20%–80% 可见（两端留空）。补间从元素**当前**段动画到**目标**段 — 如 `gsap.to("#path", { drawSVG: "0% 100%" })` 从当前状态到整段描边。单值（如 `0`、`"100%"`）表示起点为 0：`"100%"` 等价于 `"0% 100%"`。

**必需：** 元素须有可见描边 — 在 CSS 或 SVG 属性中设置 `stroke` 与 `stroke-width`；否则无可见效果。

```javascript
gsap.registerPlugin(DrawSVGPlugin);

// draw from nothing to full stroke
gsap.from("#path", { duration: 1, drawSVG: 0 });
// or explicit segment: from 0–0 to 0–100%
gsap.fromTo("#path", { drawSVG: "0% 0%" }, { drawSVG: "0% 100%", duration: 1 });
// stroke only in the middle (gaps at ends)
gsap.to("#path", { duration: 1, drawSVG: "20% 80%" });
```

**注意：** 仅影响描边（非填充）。优先单段 `<path>`；多段路径在部分浏览器可能渲染异常。`<use>` 内容无法视觉修改。**DrawSVGPlugin.getLength(element)** 与 **DrawSVGPlugin.getPosition(element)** 返回描边长度与当前位置。

**延伸阅读：** [DrawSVG](https://gsap.com/docs/v3/Plugins/DrawSVGPlugin)

### MorphSVG (MorphSVGPlugin)

通过动画 `d` 属性（路径数据）将一种 SVG 形状 morph 到另一种。起止形状点数不必相同 — MorphSVG 转为 cubic bezier 并按需加点。用于图标互 morph、形状过渡或基于路径的动画。适用于 `<path>`、`<polyline>`、`<polygon>`；`<circle>`、`<rect>`、`<ellipse>`、`<line>` 内部转换或通过 **MorphSVGPlugin.convertToPath(selector | element)**（DOM 中替换为 `<path>`）。

**morphSVG 值：** 可为**选择器**（如 `"#lightning"`）、**元素**、**原始路径数据**（如 `"M47.1,0.8 73.3,0.8..."`），或对 polygon/polyline 为 **points 字符串**（如 `"240,220 240,70 70,70 70,220"`）。完整配置用**对象形式**，**shape** 为唯一必填。

```javascript
gsap.registerPlugin(MorphSVGPlugin);

// convert primitives to path first if needed:
MorphSVGPlugin.convertToPath("circle, rect, ellipse, line");

gsap.to("#diamond", { duration: 1, morphSVG: "#lightning", ease: "power2.inOut" });
// object form:
gsap.to("#diamond", {
  duration: 1,
  morphSVG: { shape: "#lightning", type: "rotational", shapeIndex: 2 }
});

```

**MorphSVG — 主要配置（morphSVG 对象）：**

| 选项 | 说明 |
|--------|-------------|
| **shape** | _（必填。）_ 目标形状：选择器、元素或原始路径字符串。 |
| **type** | `"linear"`（默认）或 `"rotational"`。Rotational 用角度/长度插值，可减少 morph 中段扭结；linear 不对时可试 rotational。 |
| **map** | 段如何匹配：`"size"`（默认）、`"position"` 或 `"complexity"`。起止段对不齐时用；都不行则拆成多 path 分别 morph。 |
| **shapeIndex** | 偏移起点路径中哪一点对应终点第一点（避免形状「交叉」或翻转）。单段 path 用数字；**多段**用**数组**（如 `[5, 1, -8]`）。负值反转该段。用 **shapeIndex: "log"** 一次记录自动计算值，再粘贴到补间。**findShapeIndex(start, end)**（独立工具）提供交互 UI 找合适值。仅闭合路径。 |
| **smooth** | (v3.14+)。添加平滑点。数字（如 `80`）、`"auto"` 或对象：`{ points: 40 \| "auto", redraw: true \| false, persist: true \| false }`。`redraw: false` 保留原锚点（保真高、间距可能不均）。`persist: false` 补间结束移除加点。默认 morph 锯齿或不自然时用。 |
| **curveMode** | 布尔 (v3.14+)。插值控制柄角度/长度而非 raw x/y，减少曲线中段扭结。morph 中段有扭结时可试。 |
| **origin** | **type: "rotational"** 的旋转原点。字符串：`"50% 50%"`（默认）或 `"20% 60%, 35% 90%"` 区分起止原点。 |
| **precision** | 输出路径数据小数位；默认 `2`。 |
| **precompile** | 预计算路径字符串数组（或 **precompile: "log"** 一次，从控制台复制）。跳过昂贵启动计算；极复杂 morph 用。仅 `<path>`（先 convert polygon/polyline）。 |
| **render** | 每次更新调用的 Function(rawPath, target) — 如画到 canvas。RawPath 为段数组（每段 = 交替 x,y cubic bezier 坐标数组）。 |
| **updateTarget** | 使用 **render**（如仅 canvas）时设 **updateTarget: false**，不更新原 `<path>`。**MorphSVGPlugin.defaultUpdateTarget** 设默认。 |

**工具：** **MorphSVGPlugin.convertToPath(selector | element)** 将 circle/rect/ellipse/line/polygon/polyline 转为 DOM 中的 `<path>`。**MorphSVGPlugin.rawPathToString(rawPath)** 与 **stringToRawPath(d)** 在路径字符串与 raw 数组间转换。插件在 target 上存原始 `d`（如 tween 回去：`morphSVG: "#originalId"` 或同一元素）。

**提示：** morph 扭曲或翻转时设 **shapeIndex**（用 `"log"` 或 findShapeIndex()）。多段 path 时 **shapeIndex** 为数组（每段一个值）。仅在首帧慢时 precompile；不能修复 tween 中卡顿（需简化 SVG 或缩小尺寸）。**延伸阅读：** [MorphSVG](https://gsap.com/docs/v3/Plugins/MorphSVGPlugin)

### MotionPath (MotionPathPlugin)

沿 SVG 路径动画元素。沿路径移动对象（如曲线或自定义路线）时使用。

```javascript
gsap.registerPlugin(MotionPathPlugin);

gsap.to(".dot", {
  duration: 2,
  motionPath: { path: "#path", align: "#path", alignOrigin: [0.5, 0.5] }
});
```

**MotionPath — 主要配置（motionPath 对象）：**

| 选项 | 说明 |
|--------|-------------|
| `path` | SVG path 元素、选择器或路径数据字符串 |
| `align` | 对齐 target 的 path 元素或选择器 |
| `alignOrigin` | `[x, y]` 原点 (0–1)；默认 `[0.5, 0.5]` |
| `autoRotate` | 旋转元素以跟随路径切线 |
| `curviness` | 0–2；路径平滑 |

### MotionPathHelper

MotionPath 的可视编辑器（对齐、偏移）。开发阶段调 path 对齐时使用。

```javascript
gsap.registerPlugin(MotionPathPlugin, MotionPathHelperPlugin);

const helper = MotionPathHelper.create(".dot", "#path", { end: 0.5 });
// adjust in UI, then use helper.path or helper.getProgress() in your animation
```

## 缓动

### CustomEase

自定义缓动曲线（cubic-bezier 或 SVG path）。内置 ease 不够用时使用。基础用法在 gsap-core；使用时注册：

```javascript
gsap.registerPlugin(CustomEase);
const ease = CustomEase.create("name", ".17,.67,.83,.67");
gsap.to(".el", { x: 100, ease: ease, duration: 1 });
```

### EasePack

更多命名 ease（如 SlowMo、RoughEase、ExpoScaleEase）。注册后在补间中使用 ease 名称。

### CustomWiggle

Wiggle/抖动缓动。值需要「摆动」（多次振荡）时使用。

### CustomBounce

可配置强度的 bounce 式缓动。

## 物理

### Physics2D (Physics2DPlugin)

2D 物理（速度、角度、重力）。简单物理动画（如抛射、弹跳）时使用。

```javascript
gsap.registerPlugin(Physics2DPlugin);

gsap.to(".ball", {
  duration: 2,
  physics2D: {
    velocity: 250,
    angle: 80,
    gravity: 500
  }
});
```

### PhysicsProps (PhysicsPropsPlugin)

对属性值应用物理。物理驱动的属性动画时使用。

```javascript
gsap.registerPlugin(PhysicsPropsPlugin);

gsap.to(".obj", {
  duration: 2,
  physicsProps: {
    x: { velocity: 100, end: 300 },
    y: { velocity: -50, acceleration: 200 }
  }
});
```

## 开发

### GSDevTools

用于 scrub 时间线、切换动画与调试的 UI。仅开发使用；勿发布。注册并用时间线引用创建实例。

```javascript
gsap.registerPlugin(GSDevTools);
GSDevTools.create({ animation: tl });
```

## 其他

### Pixi (PixiPlugin)

GSAP 与 PixiJS 集成，动画 Pixi 显示对象。用 GSAP 动画 Pixi 对象时注册。

```javascript
gsap.registerPlugin(PixiPlugin);

const sprite = new PIXI.Sprite(texture);
gsap.to(sprite, { pixi: { x: 200, y: 100, scale: 1.5 }, duration: 1 });
```

## 最佳实践

- ✅ 首次使用前用 **gsap.registerPlugin()** 注册每个使用的插件。
- ✅ 布局过渡用 **Flip.getState()** → 改 DOM → **Flip.from()**；带惯性的拖拽用 **Draggable** + **InertiaPlugin**。
- ✅ 组件卸载或元素移除时 revert 插件实例（如 `SplitTextInstance.revert()`）。

## 禁止

- ❌ 未先 **gsap.registerPlugin()** 就在补间或 API 中使用插件。
- ❌ 将 GSDevTools 或仅开发用插件发布到生产环境。

### 延伸阅读

https://gsap.com/docs/v3/Plugins/
