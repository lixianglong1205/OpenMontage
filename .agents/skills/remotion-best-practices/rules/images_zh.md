---
name: images
description: 在 Remotion 中使用 `<Img>` 组件嵌入图片
metadata:
  tags: images, img, staticFile, png, jpg, svg, webp
---

# 在 Remotion 中使用图片

## `<Img>` 组件

始终使用 `remotion` 提供的 `<Img>` 组件来显示图片：

```tsx
import { Img, staticFile } from "remotion";

export const MyComposition = () => {
  return <Img src={staticFile("photo.png")} />;
};
```

## 重要限制

**必须使用 `remotion` 的 `<Img>` 组件。** 不要使用：

- 原生 HTML `<img>` 元素
- Next.js 的 `<Image>` 组件
- CSS 的 `background-image`

`<Img>` 组件会确保图片在渲染前完全加载，避免视频导出时出现闪烁和空白帧。

## 使用 staticFile() 引用本地图片

将图片放在 `public/` 文件夹中，并用 `staticFile()` 引用它们：

```
my-video/
├─ public/
│  ├─ logo.png
│  ├─ avatar.jpg
│  └─ icon.svg
├─ src/
├─ package.json
```

```tsx
import { Img, staticFile } from "remotion";

<Img src={staticFile("logo.png")} />;
```

## 远程图片

远程 URL 可直接使用，无需 `staticFile()`：

```tsx
<Img src="https://example.com/image.png" />
```

请确保远程图片已启用 CORS。

对于动画 GIF，请改用 `@remotion/gif` 中的 `<Gif>` 组件。

## 尺寸与定位

使用 `style` 属性控制大小和位置：

```tsx
<Img
  src={staticFile("photo.png")}
  style={{
    width: 500,
    height: 300,
    position: "absolute",
    top: 100,
    left: 50,
    objectFit: "cover",
  }}
/>
```

## 动态图片路径

使用模板字符串引用动态文件：

```tsx
import { Img, staticFile, useCurrentFrame } from "remotion";

const frame = useCurrentFrame();

// Image sequence
<Img src={staticFile(`frames/frame${frame}.png`)} />

// Selecting based on props
<Img src={staticFile(`avatars/${props.userId}.png`)} />

// Conditional images
<Img src={staticFile(`icons/${isActive ? "active" : "inactive"}.svg`)} />
```

此模式适用于：

- 图片序列（逐帧动画）
- 用户专属头像或资料图片
- 基于主题的图标
- 随状态变化的图形

## 获取图片尺寸

使用 `getImageDimensions()` 获取图片的宽高：

```tsx
import { getImageDimensions, staticFile } from "remotion";

const { width, height } = await getImageDimensions(staticFile("photo.png"));
```

可用于计算宽高比或设置合成尺寸：

```tsx
import {
  getImageDimensions,
  staticFile,
  CalculateMetadataFunction,
} from "remotion";

const calculateMetadata: CalculateMetadataFunction = async () => {
  const { width, height } = await getImageDimensions(staticFile("photo.png"));
  return {
    width,
    height,
  };
};
```
