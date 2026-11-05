# 字幕

在编写字幕之前：确认转录文本来自正确的 Whisper 模型。CLI 默认的 `small.en` 会静默将非英语音频翻译为英语 — 参见 [`../transcribe.md`](../transcribe.md) →「Language Rule」，以及 [`transcript-handling.md`](transcript-handling.md) 中的强制质量检查。

分析口播内容以确定字幕风格。若用户指定了风格，则采用该风格；否则根据转录文本检测语气。

## 转录来源

```json
[
  { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 },
  { "id": "w1", "text": "world.", "start": 0.6, "end": 1.2 }
]
```

`id`（`w0`、`w1` …）是逐词覆盖的稳定引用，由 `hyperframes transcribe` 添加。为兼容手写转录，该字段可选。生成方式见 [`../transcribe.md`](../transcribe.md) →「Output Shape」；消费前清理见 [`transcript-handling.md`](transcript-handling.md)。

## 风格检测（未指定风格时）

选定风格前先通读完整转录。四个维度：

**1. 视觉感受** — 企业风→简洁；高能量→醒目；叙事→优雅；技术→精确；社交→活泼。

**2. 配色** — 深色底+亮色用于活力；低饱和用于专业；高对比用于清晰；单一强调色。

**3. 字体气质** — 粗体/窄体用于冲击；干净无衬线用于现代；圆角用于友好；衬线用于优雅。

**4. 动画特征** — scale-pop 用于有力；柔和淡入用于平静；逐词用于强调；打字机用于技术感。

## 逐词样式

扫描值得单独处理的词：

- **品牌/产品名** — 更大字号、独特色
- **全大写** — 缩放增强、闪动、强调色
- **数字/统计** — 粗字重、强调色
- **情绪关键词** — 夸张动画（过冲、弹跳）
- **行动号召** — 高亮、下划线、色块突出
- **标记高亮** — 超出纯色的强调（高亮扫过、圈选、爆发、涂鸦、sketchout）见 `hyperframes-animation/rules/css-marker-patterns.md`。

## 脚本到风格映射

| 语气         | 字体气质                | 动画                          | 颜色                       | 字号    |
| ------------ | ------------------------ | ---------------------------------- | --------------------------- | ------- |
| Hype/发布  | 粗窄体，800-900 | Scale-pop、back.out(1.7)、0.1-0.2s | 深色底上的亮色              | 72-96px |
| 企业         | 干净无衬线，600-700      | 淡入+滑动，power3.out，0.3s       | 白/中性，低饱和强调色 | 56-72px |
| 教程         | 等宽/干净无衬线，500-600 | 打字机/淡入，0.4-0.5s          | 高对比、极简      | 48-64px |
| 叙事         | 衬线/优雅，400-500   | 慢淡入，power2.out，0.5-0.6s    | 暖色低饱和            | 44-56px |
| 社交         | 圆角无衬线，700-800    | 弹跳，elastic.out，逐词  | 活泼、彩色胶囊      | 56-80px |

## 词组划分

- **高能量：** 2-3 词。快速切换。
- **对话：** 3-5 词。自然短语。
- **沉稳/平静：** 4-6 词。较长词组。

在句界、150ms 以上停顿或达到最大词数时断组。

## 定位

- **横屏 (1920x1080)：** 距底 80-120px，居中
- **竖屏 (1080x1920)：** 偏下中部，距底约 600-700px，居中
- 切勿遮挡主体面部
- `position: absolute` — 勿用 relative
- 同一时刻仅显示一组字幕

## 防止文字溢出

使用 `window.__hyperframes.fitTextFontSize()`：

```js
var result = window.__hyperframes.fitTextFontSize(group.text.toUpperCase(), {
  fontFamily: "Outfit",
  fontWeight: 900,
  maxWidth: 1600,
});
el.style.fontSize = result.fontSize + "px";
```

选项：`maxWidth`（横屏 1600，竖屏 900）、`baseFontSize`（78）、`minFontSize`（42）、`fontWeight`、`fontFamily`、`step`（2）。

CSS 兜底：容器设 `max-width`，`overflow: visible`（**勿**用 `hidden` — hidden 会裁切放大强调词与发光效果），`position: absolute`，显式 `height`。逐词样式使用 `scale > 1.0` 时，计算 `maxWidth = safeWidth / maxScale` 以留余量。

**容器模式：** 全宽绝对定位容器、居中。**勿**使用 `left: 50%; transform: translateX(-50%)` — 会在合成边缘造成裁切。

## 字幕退出保证

每组在退出动画后**必须**硬清除：

```js
tl.to(groupEl, { opacity: 0, scale: 0.95, duration: 0.12, ease: "power2.in" }, group.end - 0.12);
// `tl.set` 是瞬时切换，不是补间 — 此处可安全设置 `visibility`（core 的「勿对 visibility 做动画」针对补间；非数值本身也无法平滑插值）。
tl.set(groupEl, { opacity: 0, visibility: "hidden" }, group.end);
```

构建时间轴后自检 — 放在 `window.__timelines[id] = tl` **之前**，以便在合成初始化时运行：

```js
GROUPS.forEach(function (group, gi) {
  var el = document.getElementById("cg-" + gi);
  if (!el) return;
  tl.seek(group.end + 0.01);
  var computed = window.getComputedStyle(el);
  if (computed.opacity !== "0" && computed.visibility !== "hidden") {
    console.warn(
      "[caption-lint] group " + gi + " still visible at t=" + (group.end + 0.01).toFixed(2) + "s",
    );
  }
});
tl.seek(0);
```

## 预置字幕组件

从零搭建字幕样式前，先查 registry — 15 个即用字幕组件覆盖常见风格。用 `npx hyperframes add <name>` 安装，并通过 `data-composition-src` 作为子合成接入（见 `hyperframes-registry`）。

```bash
npx hyperframes catalog --tag caption-style   # list all caption components
npx hyperframes add caption-highlight         # install a specific one
```

| 风格                     | 组件                    | 适用场景                     |
| ------------------------- | ---------------------------- | ---------------------------- |
| TikTok 式高亮    | `caption-highlight`          | 社交、高能量          |
| 卡拉 OK 胶囊              | `caption-pill-karaoke`       | 音乐、歌词视频          |
| 电影感编辑       | `caption-editorial-emphasis` | 纪录片、叙事    |
| 故障 / 赛博            | `caption-glitch-rgb`         | 科技、游戏                 |
| 全屏 slam          | `caption-kinetic-slam`       | hype、公告          |
| 霓虹发光                 | `caption-neon-glow`          | 夜景、俱乐部、霓虹美学 |
| 霓虹强调（多色） | `caption-neon-accent`        | 多彩、活泼            |
| 擦除揭示               | `caption-clip-wipe`          | 简洁、现代                |
| 渐变填充             | `caption-gradient-fill`      | 鲜艳、吸睛        |
| 矩阵解码             | `caption-matrix-decode`      | 科幻、科技揭示         |
| 表情弹出                 | `caption-emoji-pop`          | 社交、轻松               |
| 视差层           | `caption-parallax-layers`    | 景深、电影感             |
| 粒子爆发             | `caption-particle-burst`     | 庆祝、冲击关键词 |
| 熔岩纹理              | `caption-texture`            | 醒目、戏剧化               |
| 字重变化              | `caption-weight-shift`       | 优雅、排版         |

相关：`caption-blend-difference`（标签为 `text` / `blend-mode`，非 `caption-style`，故不会出现在上述筛选结果中）通过 `mix-blend-mode: difference` 让文字相对任意背景自动反色 — 背景杂乱或不可预测时有用。

带预览浏览全部：[hyperframes.heygen.com/catalog](https://hyperframes.heygen.com/catalog)

字幕组件自带透明背景 — 纯叠加层。若底层视频过亮或杂乱，在宿主合成中于字幕子合成**下方**加对比层（如半透明深色 div），而非写在组件内部。

## 延伸阅读

- [`motion.md`](motion.md) — 卡拉 OK、标记效果、音频驱动调制、scatter 退出。
- [`transcript-handling.md`](transcript-handling.md) — 输入格式、质量检查、清理、外部 API 回退。
- `hyperframes-animation/rules/css-marker-patterns.md` — 标记高亮（确定性、完全可 seek）。

## 约束

- 确定性。禁止 `Math.random()`、`Date.now()`。
- 与转录时间戳同步。
- 同一时刻仅一组可见。
- 每组必须在 `group.end` 处有硬 `tl.set` 清除。
- 字体：编译器仅自动嵌入**内置映射集**（Inter、Roboto、Montserrat …）— 对这些字体只需在 CSS 中声明 `font-family`。**其他**字体（品牌/自定义如 `TT Norms Pro`，或非拉丁 CJK/天城文族）**不会**自动提供：需 `@font-face` 指向项目内真实 `.woff2`，否则渲染会静默回退到通用字体。勿假设本地能看到的 `font-family` 在渲染端同样可用 — 渲染机是干净的无头 Chrome，未安装系统字体。
