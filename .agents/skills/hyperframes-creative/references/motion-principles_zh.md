# 动效原则

## 目录

- 护栏规则
- 未被明确要求时不要做的事
- 视觉构图
- 图像动效处理
- 关键 GSAP 规则

## 护栏规则

你懂这些规则，却总在违反。停下来。

- **不要给每个 tween 用同一种 ease。** 你习惯什么都默认 `power2.out`。像区分字重一样区分 ease——同一场景里，独立 tween 使用相同 ease 的不要超过 2 个。
- **不要给所有元素用同一速度。** 你习惯什么都用 0.4–0.5s。最慢的场景应比最快的慢 3 倍。刻意变化时长。
- **不要让所有元素从同一方向进入。** 你习惯每个元素都是 `y: 30, opacity: 0`。要变化：从左、从右、从缩放、仅透明度、字间距等。
- **不要每个场景用同一 stagger。** 每个场景需要自己的节奏。
- **不要每个场景都做环境 zoom。** 为每个场景选不同的环境动效：慢速平移、轻微旋转、缩放推进、色相变化，或什么都不做。动效之后的静止同样有力。
- **不要从 t=0 开始。** 第一个动画偏移 0.1–0.3s。零延迟会像跳切。

## 未被明确要求时不要做的事

### Easing 是情绪，不是技巧

过渡是动词。Easing 是副词。`expo.out` 的滑入 = 自信。`sine.inOut` = 梦幻。`elastic.out` = 俏皮。同一动作，不同含义。刻意选择副词。

**方向规则——没有商量余地：**

- `.out` 用于元素进入。先快后慢。感觉响应灵敏。这是你的默认。
- `.in` 用于元素离开。先慢后快，甩出去。
- `.inOut` 用于元素在位置之间移动。

你经常搞反。进入用 ease-in 会发闷。离开用 ease-out 会像拖泥带水。

### 速度传达重量感

- 快（0.15–0.3s）——能量、紧迫、自信
- 中（0.3–0.5s）——专业，多数内容
- 慢（0.5–0.8s）——厚重、奢华、沉思
- 很慢（0.8–2.0s）——电影感、情绪、氛围

### 场景结构：建立 / 呼吸 / 收束

每个场景有三个阶段。你把一切都堆在建立阶段，呼吸和收束什么都没有。

- **建立（0–30%）**——元素进入，stagger。不要一次全部堆上。
- **呼吸（30–70%）**——内容可见，靠**一种**环境动效保持生气。
- **收束（70–100%）**——退出或果断收束。退出比进入更快。

### 转场即含义

- **交叉淡入淡出** =「这还在延续」
- **硬切** =「醒醒」/ 打断
- **慢溶解** =「跟我一起飘」

你把什么都做交叉淡入淡出。打断与调性切换要用硬切。

### 编排即层级

先动的元素被认为最重要。按重要性 stagger，不要按 DOM 顺序。不要等完成——重叠进入。无论条目多少，整条 stagger 序列总时长控制在 500ms 以内。

### 不对称

进入要比退出更长。卡片出现 0.4s，消失 0.25s。

## 视觉构图

你是为 web 做，视频帧不是页面。

- **每个场景至少两个焦点。** 眼睛需要可移动的目标。绝不要单块文字漂在空白里。
- **填满画幅。** 主标题文字：宽度的 60–80%。你会想用 web 尺寸的元素。别这样。
- **每个场景至少三层。** 背景处理（光晕、超大号淡化字、色块）。前景内容。点缀元素（分隔线、标签、数据条）。
- **背景不是空的。** 径向光晕、超大号淡化字溢出画框、轻微边框面板、细线规则。纯 #000 会像「还没加载完」。
- **锚定到边缘。** 内容钉在左/上或右/下。居中漂浮是 web 模式。
- **分屏。** 左侧数据面板，右侧内容。顶部元数据条，下方全宽。分区布局，不要居中堆叠。
- **用结构元素。** 规则线、分隔线、边框面板。它们为眼睛造路径，且动效友好（scaleX 从 0）。

## 图像动效处理

永远不要嵌入未经处理的扁平原图。每张图都必须有动效处理：

- **透视倾斜**：用 `gsap.set(el, { transformPerspective: 1200, rotationY: -8 })` + `box-shadow`——制造深度。不要用 CSS `transform: perspective(...)`，GSAP 会覆盖它。
- **慢速 zoom（Ken Burns）**：GSAP `scale: 1` → `1.04`，持续 beat 时长——让照片有电影感
- **设备框**：用 CSS `border-radius` 和 `box-shadow` 包成笔记本/手机外形
- **漂浮 UI**：抽出关键元素，在不同 z 深度动画做视差
- **滚动揭示**：把图裁进视口窗口，动画 `y` 位置

## 关键 GSAP 规则

以下规则来自两次独立的网站 capture 构建（2026-04-20）：composition 通过 lint 却仍上线即坏——元素永不出现、环境动效无法 scrub、进入 tween 静默干掉目标。Linter 抓不到这些；作者必须遵守。

- **capture 内容不要用 iframe。** Iframe 无法与 timeline 确定性 seek——capture 引擎无法在内部 scrub，输出里会冻住（或空白）。若你要美化的是在线 Web 应用，用 `capture/` 的截图做堆叠面板或分层图，不要 live embed。

- **同一元素上不要叠两个 transform tween。** 常见失败：同一 `<img>` 上 `y` 进入 + `scale` Ken Burns。第二个 tween 的 `immediateRender: true` 在构造时写入初始状态，覆盖第一个 tween 设的值——元素不可见或跑到画外，且无 lint 警告。另一机制：`tl.from()` 在 playhead seek 过 timeline 末尾时会重置到声明的「from」状态，线性播放看起来对的元素在 capture 引擎非线性 seek 下会消失。两种修法：

  ```html
  <!-- BAD: two transforms on one element -->
  <img class="hero" src="..." />
  <script>
    tl.from(".hero", { y: 50, opacity: 0, duration: 0.6 }, 0);
    tl.to(".hero", { scale: 1.04, duration: beat }, 0); // kills the entrance
  </script>

  <!-- GOOD option A: combine into one tween -->
  <script>
    tl.fromTo(
      ".hero",
      { y: 50, opacity: 0, scale: 1.0 },
      { y: 0, opacity: 1, scale: 1.04, duration: beat, ease: "none" },
      0,
    );
  </script>

  <!-- GOOD option B: split across parent + child -->
  <div class="hero-wrap"><img class="hero" src="..." /></div>
  <script>
    tl.from(".hero-wrap", { y: 50, opacity: 0, duration: 0.6 }, 0); // entrance on parent
    tl.to(".hero", { scale: 1.04, duration: beat }, 0); // Ken Burns on child
  </script>
  ```

- **在 `.clip` 场景内优先 `tl.fromTo()` 而非 `tl.from()`。** `gsap.from()` 默认 `immediateRender: true`，在 timeline 构造时就写入「from」状态——早于 `.clip` 场景的 `data-start` 生效。非线性 seek 场景时（capture 引擎会这样做），元素可能闪一下、从错误位置开始，或完全跳过进入。显式 `fromTo` 让每个 timeline 位置的状态可确定：

  ```js
  // BRITTLE: immediateRender interacts badly with scene boundaries
  tl.from(el, { opacity: 0, y: 50, duration: 0.6 }, t);

  // DETERMINISTIC: state is defined at both ends, no immediateRender surprise
  tl.fromTo(el, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.6 }, t);
  ```

- **环境 pulse 必须挂在可 seek 的 `tl` 上，绝不用裸 `gsap.to()`。** 光晕、微光、轻微漂浮循环、logo 呼吸——都必须加进场景 timeline，不能单独启动。独立 tween 按墙钟时间跑，不随 capture 引擎 scrub，渲染视频里效果缺失，studio 预览却看起来对：

  ```js
  // BAD: lives outside the timeline, never renders in capture
  gsap.to(".aura", { scale: 1.08, yoyo: true, repeat: 5, duration: 1.2 });

  // GOOD: seekable, deterministic, renders
  tl.to(".aura", { scale: 1.08, yoyo: true, repeat: 5, duration: 1.2 }, 0);
  ```

- **每个场景边界都要 hard-kill，不只 caption。** 上面 caption hard-kill 规则可推广：任何在 beat 边界改变可见性的元素，淡出之后都需要确定性 `tl.set()` 硬关闭，因为同一元素上后续 tween（或兄弟 tween 的 `immediateRender`）可能把它「复活」。对所有有退出动画的元素适用：

  ```js
  tl.to(el, { opacity: 0, duration: 0.3 }, beatEnd);
  tl.set(el, { opacity: 0, visibility: "hidden" }, beatEnd + 0.3); // deterministic kill
  ```

这些就是带完整代码示例的精确规则——不要概括或缩短。它们存在，是因为 lint 干净的作品没有这些仍会坏着上线。
