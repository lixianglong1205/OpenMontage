# 媒体迁移：Audio、Video、Img、IFrame、staticFile

## 资源路径

Remotion 的 `staticFile("x.png")` 解析到项目的 `public/` 目录。
HF 使用相对于 composition 的 `index.html` 的相对路径，惯例为
`assets/`：

```tsx
<Img src={staticFile("logo.png")} />
```

```html
<img src="assets/logo.png" />
```

翻译时，将资源从 `remotion-src/public/x` 复制到
`hf-src/assets/x`。多个文件可通过 setup 脚本批量处理；
示例模式见 T2 的 `setup.sh`。

## `<Audio>`

```tsx
<Audio src={staticFile("music.wav")} volume={0.5} />
```

```html
<audio
  data-start="0"
  data-duration="6"
  data-track-index="2"
  data-volume="0.5"
  src="assets/music.wav"
></audio>
```

`data-start` 与 `data-duration` 为必填项 — 运行时依赖它们来
调度音频。若 Remotion 未指定裁剪，默认使用 composition 的完整时长。

### 音量渐变

```tsx
<Audio src={staticFile("music.wav")} volume={(f) => interpolate(f, [0, 30], [0, 1])} />
```

HF 目前仅支持静态 `data-volume`。音量渐变需在翻译阶段
作用于音频文件（例如用 ffmpeg 的 `afade`），否则
丢弃渐变并附翻译说明。

### 裁剪 / playbackRate

```tsx
<Audio src={staticFile("music.wav")} startFrom={60} endAt={180} playbackRate={1.5} />
```

```html
<audio
  data-start="0"
  data-duration="<resolved from trim>"
  data-trim-start="2"
  data-trim-end="6"
  data-playback-rate="1.5"
  src="assets/music.wav"
></audio>
```

`startFrom` / `endAt` 为帧索引；需转换为秒。

## `<Video>` 与 `<OffthreadVideo>`

```tsx
<Video src={staticFile("intro.mp4")} muted playsInline />
<OffthreadVideo src={staticFile("intro.mp4")} muted />
```

```html
<video
  muted
  playsinline
  data-start="0"
  data-duration="5"
  data-track-index="0"
  src="assets/intro.mp4"
></video>
```

`<OffthreadVideo>` 是 Remotion 在无头渲染场景下的专用优化。
HF 已在无头 Chrome 中运行，因此 off-thread 变体
合并为普通 `<video>`。

`muted` 与 `playsinline` 为运行时自动播放所必需
（浏览器策略）。生成 HTML 时务必保留。

## `<Img>`

```tsx
<Img src={staticFile("logo.png")} style={{ width: 200, height: 200 }} />
```

```html
<img src="assets/logo.png" style="width: 200px; height: 200px;" />
```

宽/高会四舍五入为整数 px。若原始 style 含
动画尺寸，由 GSAP tween 驱动 — 见 [timing.md](timing.md)。

## `<IFrame>`

```tsx
<IFrame src="https://example.com" />
```

```html
<iframe src="https://example.com"></iframe>
```

当 HF 在 composition 中检测到嵌套 iframe 时，会自动回退到
**截图模式**，而非确定性的 BeginFrame 模式。这会
牺牲渲染性能，但输出在视觉上正确。详见
[hyperframes-vs-remotion.mdx](https://github.com/heygen-com/hyperframes/blob/main/docs/guides/hyperframes-vs-remotion.mdx)。

## `delayRender()` / `continueRender()`

```tsx
const handle = delayRender();
useEffect(() => {
  loadAsset().then(() => continueRender(handle));
}, []);
```

丢弃。HF 通过 [Frame Adapter 模式](https://hyperframes.heygen.com/concepts/frame-adapters)
等待资源就绪 — 图片、视频、字体与 Lottie 动画均原生
上报加载完成。应用层无需额外处理。

## 当资源不是文件时

若 Remotion 的媒体源为 Buffer、dataURL 或 URL.createObjectURL，
资源不在磁盘上，无法通过 setup.sh 复制。两种做法：

1. 在翻译阶段物化资源 — 将 buffer 写入
   `hf-src/assets/` 中的文件。
2. 对小资源（< 100 KB）直接在 HTML 中嵌入 data URL（`src="data:image/png;base64,..."`）。

对音视频 Buffer，优先选方案 1 — base64 编码的媒体
会撑大 HTML 并拖慢渲染器。
