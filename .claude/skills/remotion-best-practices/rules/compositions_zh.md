---
name: compositions
description: 定义 Composition、Still、Folder、默认 props 与动态 metadata
metadata:
  tags: composition, still, folder, props, metadata
---

`<Composition>` 定义可渲染视频的组件、宽度、高度、fps 与时长。

通常放在 `src/Root.tsx` 文件中。

```tsx
import { Composition } from "remotion";
import { MyComposition } from "./MyComposition";

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComposition}
      durationInFrames={100}
      fps={30}
      width={1080}
      height={1080}
    />
  );
};
```

## 默认 Props

传入 `defaultProps` 为组件提供初始值。  
值必须可 JSON 序列化（支持 `Date`、`Map`、`Set` 与 `staticFile()`）。

```tsx
import { Composition } from "remotion";
import { MyComposition, MyCompositionProps } from "./MyComposition";

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComposition}
      durationInFrames={100}
      fps={30}
      width={1080}
      height={1080}
      defaultProps={
        {
          title: "Hello World",
          color: "#ff0000",
        } satisfies MyCompositionProps
      }
    />
  );
};
```

请用 `type` 声明 props，而非 `interface`，以保证 `defaultProps` 的类型安全。

## Folder

使用 `<Folder>` 在侧边栏中组织 Composition。  
Folder 名称只能包含字母、数字和连字符。

```tsx
import { Composition, Folder } from "remotion";

export const RemotionRoot = () => {
  return (
    <>
      <Folder name="Marketing">
        <Composition id="Promo" /* ... */ />
        <Composition id="Ad" /* ... */ />
      </Folder>
      <Folder name="Social">
        <Folder name="Instagram">
          <Composition id="Story" /* ... */ />
          <Composition id="Reel" /* ... */ />
        </Folder>
      </Folder>
    </>
  );
};
```

## Still

使用 `<Still>` 生成单帧图像。不需要 `durationInFrames` 或 `fps`。

```tsx
import { Still } from "remotion";
import { Thumbnail } from "./Thumbnail";

export const RemotionRoot = () => {
  return (
    <Still id="Thumbnail" component={Thumbnail} width={1280} height={720} />
  );
};
```

## 计算 Metadata

使用 `calculateMetadata` 根据数据动态设置尺寸、时长或 props。

```tsx
import { Composition, CalculateMetadataFunction } from "remotion";
import { MyComposition, MyCompositionProps } from "./MyComposition";

const calculateMetadata: CalculateMetadataFunction<
  MyCompositionProps
> = async ({ props, abortSignal }) => {
  const data = await fetch(`https://api.example.com/video/${props.videoId}`, {
    signal: abortSignal,
  }).then((res) => res.json());

  return {
    durationInFrames: Math.ceil(data.duration * 30),
    props: {
      ...props,
      videoUrl: data.url,
    },
  };
};

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComposition}
      durationInFrames={100} // Placeholder, will be overridden
      fps={30}
      width={1080}
      height={1080}
      defaultProps={{ videoId: "abc123" }}
      calculateMetadata={calculateMetadata}
    />
  );
};
```

该函数可返回 `props`、`durationInFrames`、`width`、`height`、`fps` 以及与 codec 相关的默认值。它在渲染开始前执行一次。

## 在另一 Composition 内嵌套 Composition

若要在某个 Composition 内再包含另一个 Composition，可使用带 `width` 与 `height` 属性的 `<Sequence>` 指定内层 Composition 的尺寸。

```tsx
<AbsoluteFill>
  <Sequence width={COMPOSITION_WIDTH} height={COMPOSITION_HEIGHT}>
    <CompositionComponent />
  </Sequence>
</AbsoluteFill>
```
