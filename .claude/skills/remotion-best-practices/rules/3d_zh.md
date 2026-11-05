---
name: 3d
description: 在 Remotion 中使用 Three.js 与 React Three Fiber 制作 3D 内容。
metadata:
  tags: 3d, three, threejs
---

# 在 Remotion 中使用 Three.js 与 React Three Fiber

请遵循 React Three Fiber 与 Three.js 的最佳实践。  
此外还需遵守以下 Remotion 特有规则：

## 前提条件

首先需安装 `@remotion/three` 包。  
若尚未安装，请使用以下命令：

```bash
npx remotion add @remotion/three # If project uses npm
bunx remotion add @remotion/three # If project uses bun
yarn remotion add @remotion/three # If project uses yarn
pnpm exec remotion add @remotion/three # If project uses pnpm
```

## 使用 ThreeCanvas

你必须将 3D 内容包裹在 `<ThreeCanvas>` 中，并配置适当的光照。  
`<ThreeCanvas>` 必须提供 `width` 与 `height` 属性。

```tsx
import { ThreeCanvas } from "@remotion/three";
import { useVideoConfig } from "remotion";

const { width, height } = useVideoConfig();

<ThreeCanvas width={width} height={height}>
  <ambientLight intensity={0.4} />
  <directionalLight position={[5, 5, 5]} intensity={0.8} />
  <mesh>
    <sphereGeometry args={[1, 32, 32]} />
    <meshStandardMaterial color="red" />
  </mesh>
</ThreeCanvas>;
```

## 禁止非 `useCurrentFrame()` 驱动的动画

着色器、模型等不得自行播放动画。  
除非由 `useCurrentFrame()` 驱动，否则不允许任何动画。  
否则渲染时会出现闪烁。

禁止使用 `@react-three/fiber` 的 `useFrame()`。

## 使用 `useCurrentFrame()` 做动画

使用 `useCurrentFrame()` 实现动画。

```tsx
const frame = useCurrentFrame();
const rotationY = frame * 0.02;

<mesh rotation={[0, rotationY, 0]}>
  <boxGeometry args={[2, 2, 2]} />
  <meshStandardMaterial color="#4a9eff" />
</mesh>;
```

## 在 `<ThreeCanvas>` 内使用 `<Sequence>`

`<ThreeCanvas>` 内部的任意 `<Sequence>` 的 `layout` 属性必须设为 `none`。

```tsx
import { Sequence } from "remotion";
import { ThreeCanvas } from "@remotion/three";

const { width, height } = useVideoConfig();

<ThreeCanvas width={width} height={height}>
  <Sequence layout="none">
    <mesh>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="#4a9eff" />
    </mesh>
  </Sequence>
</ThreeCanvas>;
```
