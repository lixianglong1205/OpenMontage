# 背景移除

生成透明叠加层（典型场景：在任意画面上叠加说话人头像）。使用 `u2net_human_seg`（MIT）。

```bash
npx hyperframes remove-background subject.mp4 -o transparent.webm          # default: VP9 + alpha
npx hyperframes remove-background subject.mp4 -o transparent.mov           # ProRes 4444 (editing)
npx hyperframes remove-background portrait.jpg -o cutout.png               # single-image cutout
npx hyperframes remove-background subject.mp4 -o subject.webm \
  --background-output plate.webm                                           # both layers, one pass
npx hyperframes remove-background subject.mp4 -o transparent.webm --device cpu
npx hyperframes remove-background --info                                   # detected providers
```

## 输出格式

- **`.webm`（VP9 alpha）** — 默认。可直接放入 `<video>`，在 Chrome 中原生透明播放（约 1 MB / 4 秒 @ 1080p）。
- **`.mov`（ProRes 4444）** — 可在剪辑软件中往返（Premiere / Resolve / DaVinci）。约 50 MB / 4 秒。
- **`.png`** — 单张图像抠图。

## 质量（`--quality`）

仅控制 VP9 编码器的 CRF — 分割质量是固定的。质量越高，抠图的 RGB 越接近源 MP4（在将抠图叠在自身源画面上时很重要）。

| 预设       | CRF | 适用场景                                      |
| ---------- | --- | --------------------------------------------- |
| `fast`     | 30  | 快速迭代、更小文件、颜色匹配要求较松          |
| `balanced` | 18  | **默认**；多数用途下视觉无差异                |
| `best`     | 12  | 母版 / 最终交付，颜色匹配最紧                 |

## 设备（`--device`）

`auto`（默认）在 Apple Silicon 上选 CoreML，有 CUDA 时用 CUDA，否则 CPU。可用 `--device cpu | coreml | cuda` 强制指定。CUDA 需要 `HYPERFRAMES_CUDA=1` 以及 GPU 版 `onnxruntime-node`。用 `--info` 可在不渲染的情况下查看检测到的 provider。

## 合成模式 — 选对用法

抠图 WebM 是源 MP4 RGB 的**重编码副本**。其背后的内容会影响观感。

| 模式                                                     | 抠图背后                                | 效果                                                                                                            |
| -------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **抠图叠在不同场景上**（最常见）                         | 静态图、渐变、无关视频                  | 效果很好。主体只有单一 RGB 源。                                                                                 |
| **抠图叠在自身源 mp4 上**（文字在主体后）                | 与抠图来源相同的 mp4                    | `balanced` 下重影几乎不可见；`fast` 会出现色偏 / 边缘光晕。母版请用 `best`。                                    |
| **抠图叠在同一人另一段素材上**                           | 同一主体的其他镜头                      | **两个主体叠在一起。不要这样做。**                                                                              |

## 文字在主体后模式（两条易忽略的规则）

在 presenter 抠图后面放标题：

```html
<video
  src="presenter.mp4"
  id="bg"
  data-start="0"
  data-duration="6"
  data-track-index="0"
  muted
  playsinline
></video>

<h1 id="headline" style="z-index:2; ...">MAKE IT IN HYPERFRAMES</h1>

<div class="cutout-wrap" style="position:absolute; inset:0; z-index:3; opacity:0">
  <video
    src="presenter.webm"
    data-start="0"
    data-duration="6"
    data-track-index="1"
    muted
    playsinline
  ></video>
</div>
```

```js
// Flip the wrapper's opacity at the cut, NOT the video's
tl.set(".cutout-wrap", { opacity: 1 }, 3.3);
```

两条容易忽略的规则：

1. **用不带时间轴的 `<div>` 包住抠图 `<video>`，动画作用在 wrapper 的 opacity 上，而不是 video 元素本身。** 框架会对活跃片段（任何带 `data-start` / `data-duration` 的元素）强制 `opacity: 1`，直接动画 video 的 opacity 会被静默覆盖。wrapper 没有 `data-*` 属性，因此由你的 CSS / GSAP 控制。
2. **两个 video 都使用 `data-start="0"` 和 `data-media-start="0"`**，以便框架从 t=0 同步解码。若晚挂载抠图（`data-start=3.3`），会引入 seek + 预热，相对底 mp4 差一帧 — 在切换点会看到一帧错位。

## 图层分离（`--background-output`）

除抠图外再输出**第二个**透明视频：同源 RGB，alpha 为 `255 - mask` 而非 `mask`。抠图主体不透明；plate 背景不透明（主体位置为透明洞）。当文字 / 图形需要落在**两层之间**时使用。

| 文件                             | Alpha 含义…                                             | 用途                                                             |
| -------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------- |
| `-o subject.webm`                | mask — 主体不透明，背景透明                             | 前景层（顶层）                                                   |
| `--background-output plate.webm` | 反 mask — 环境不透明，主体透明                          | 底层；在此与主体之间放置文字 / 图形                              |

两者共用同一 `--quality`，且单次推理 — 仅编码成本约翻倍。仅适用于视频输入且输出为 `.webm` / `.mov`。

**挖洞式 plate，非 inpainting。** `plate.webm` 中主体区域完全透明 — 在其下合成不透明内容以填洞。

**判断 `--background-output` 是否合适的一条标准：** _是否会有任何内容透过主体轮廓、出现在原先主体所在位置？_ 若否，不需要 plate — 仅 `subject.webm` 叠在不同背景上即可。

### 用例 → 正确工具

| 用例                                                                                | 正确工具                                                                           |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 文字/图形在抠图与 plate 之间（本命令存在的理由）                                    | **挖洞 plate**（`--background-output`）                                            |
| 主体叠到无关场景上                                                                  | 只要 `subject.webm`；忽略 plate                                                    |
| 单独展示**没有人物**的房间、且不叠其他内容                                          | **干净 plate** — 需要 inpainter（LaMa、ProPainter、E2FGVI）。不是本命令。         |
| 用另一主体替换当前主体                                                              | **干净 plate** — 同上                                                              |

### 标准三层模板（plate + 内容 + 抠图）

只交付两个透明层，中间可放任意内容 — 无需原始 mp4：

```html
<!-- z=1 plate: 环境不透明，主体轮廓透明 -->
<video
  src="plate.webm"
  data-start="0"
  data-duration="6"
  data-track-index="0"
  muted
  playsinline
></video>

<!-- z=2 你的内容在两层之间 -->
<h1 id="headline" style="z-index:2; ...">MAKE IT IN HYPERFRAMES</h1>

<!-- z=3 抠图把主体浮回顶层 -->
<div class="cutout-wrap" style="position:absolute; inset:0; z-index:3">
  <video
    src="subject.webm"
    data-start="0"
    data-duration="6"
    data-track-index="1"
    muted
    playsinline
  ></video>
</div>
```

功能上与上文「文字在主体后」模式等价，但不必交付原始 mp4 — plate 替代它。适合只交付两个透明层作为可复用资产时使用。

## 何时不应使用 `remove-background`

若用户要的是「**没有人物**的房间、单独展示」（任何地方都没有主体、也不在其上合成），`--background-output` 不对 — 其 plate 是透明洞，不是填好的干净 plate。他们需要 **inpainter**：LaMa、ProPainter 或 E2FGVI。应告知本命令做不到这一点。
