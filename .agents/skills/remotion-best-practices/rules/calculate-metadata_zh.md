---
name: calculate-metadata
description: 动态设置合成（composition）的时长、尺寸和 props
metadata:
  tags: calculateMetadata, duration, dimensions, props, dynamic
---

# 使用 calculateMetadata

在 `<Composition>` 上使用 `calculateMetadata`，可在渲染前动态设置时长、尺寸并转换 props。

```tsx
<Composition
  id="MyComp"
  component={MyComponent}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{ videoSrc: "https://remotion.media/video.mp4" }}
  calculateMetadata={calculateMetadata}
/>
```

## 根据视频设置时长

使用 [`getVideoDuration`](./get-video-duration.md) 和 [`getVideoDimensions`](./get-video-dimensions.md) 技能获取视频时长与尺寸：

```tsx
import { CalculateMetadataFunction } from "remotion";
import { getVideoDuration } from "./get-video-duration";

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const durationInSeconds = await getVideoDuration(props.videoSrc);

  return {
    durationInFrames: Math.ceil(durationInSeconds * 30),
  };
};
```

## 与视频尺寸对齐

使用 [`getVideoDimensions`](./get-video-dimensions.md) 技能获取视频尺寸：

```tsx
import { CalculateMetadataFunction } from "remotion";
import { getVideoDuration } from "./get-video-duration";
import { getVideoDimensions } from "./get-video-dimensions";

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const dimensions = await getVideoDimensions(props.videoSrc);

  return {
    width: dimensions.width,
    height: dimensions.height,
  };
};
```

## 根据多个视频设置时长

```tsx
const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const metadataPromises = props.videos.map((video) =>
    getVideoDuration(video.src),
  );
  const allMetadata = await Promise.all(metadataPromises);

  const totalDuration = allMetadata.reduce(
    (sum, durationInSeconds) => sum + durationInSeconds,
    0,
  );

  return {
    durationInFrames: Math.ceil(totalDuration * 30),
  };
};
```

## 设置默认 outName

根据 props 设置默认输出文件名：

```tsx
const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  return {
    defaultOutName: `video-${props.id}.mp4`,
  };
};
```

## 转换 props

在渲染前获取数据或转换 props：

```tsx
const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
  abortSignal,
}) => {
  const response = await fetch(props.dataUrl, { signal: abortSignal });
  const data = await response.json();

  return {
    props: {
      ...props,
      fetchedData: data,
    },
  };
};
```

当 Studio 中 props 变化时，`abortSignal` 会取消过时的请求。

## 返回值

所有字段均为可选。返回的值会覆盖 `<Composition>` 上的 props：

- `durationInFrames`：帧数
- `width`：合成宽度（像素）
- `height`：合成高度（像素）
- `fps`：每秒帧数
- `props`：传给组件的转换后的 props
- `defaultOutName`：默认输出文件名
- `defaultCodec`：渲染的默认编解码器
