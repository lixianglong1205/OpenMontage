# 连接 Blocks

Block 是独立的 composition，各自拥有 `data-composition-id`、尺寸、时长以及 GSAP 时间轴。在宿主 composition 中，通过 `<div>` 上的 `data-composition-src` 引入它们。

## 基本连接

执行 `hyperframes add data-chart` 之后，在 `index.html` 中将其接入：

```html
<div id="stage" data-composition-id="main" data-width="1920" data-height="1080" data-duration="20">
  <video id="a-roll" src="video.mp4" data-start="0" data-duration="20" data-track-index="0"></video>

  <!-- Block: appears at 2s, plays for 15s, on layer 1 -->
  <div
    data-composition-id="data-chart"
    data-composition-src="compositions/data-chart.html"
    data-start="2"
    data-duration="15"
    data-track-index="1"
    data-width="1920"
    data-height="1080"
  ></div>
</div>
```

## 必需属性

| 属性                   | 说明                                                                 |
| ---------------------- | -------------------------------------------------------------------- |
| `data-composition-src` | Block HTML 文件路径（相对于 index.html）                             |
| `data-composition-id`  | 与 block 内部 composition ID 一致的唯一 ID                           |
| `data-start`           | block 在宿主时间轴上出现的时间（秒）                                 |
| `data-duration`        | block 播放时长（秒，最多不超过 block 自身时长）                      |
| `data-track-index`     | 图层顺序 — 数值越大越靠前渲染                                      |
| `data-width`           | block 画布宽度（与 block 的尺寸一致）                                |
| `data-height`          | block 画布高度（与 block 的尺寸一致）                                |

## 时间轴协调

block 内部的 GSAP 时间轴与宿主时间轴独立运行。HyperFrames 运行时会加载子 composition，找到其 `window.__timelines` 注册，并按 `data-start` 偏移量与宿主同步 seek block。你**无需**在宿主的 GSAP 代码中引用 block 的时间轴。

## 定位 block

若要将 block 放在画面中的特定区域，可添加 CSS：

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
  style="position: absolute; right: 0; top: 0; width: 40%; height: 100%;"
></div>
```

## 多个 block

可添加更多 `<div data-composition-src="...">` 兄弟节点，`data-start` 可重叠或不重叠 — 每个 block 的时间轴相互独立，由运行时同步 seek。
