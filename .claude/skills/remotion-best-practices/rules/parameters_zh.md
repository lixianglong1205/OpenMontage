---
name: parameters
description: 通过添加 Zod schema 使视频可参数化
metadata:
  tags: parameters, zod, schema
---

要让视频可参数化，可以为 composition 添加 Zod schema。

首先，必须安装 `zod`。

在项目中查找 lockfile，并根据包管理器运行对应命令：

若找到 `package-lock.json`，使用以下命令：

```bash
npm i zod
```

若找到 `bun.lockb`，使用以下命令：

```bash
bun i zod
```

若找到 `yarn.lock`，使用以下命令：

```bash
yarn add zod
```

若找到 `pnpm-lock.yaml`，使用以下命令：

```bash
pnpm i zod
```

然后，可以在组件旁定义 Zod schema：

```tsx title="src/MyComposition.tsx"
import { z } from "zod";

export const MyCompositionSchema = z.object({
  title: z.string(),
});

const MyComponent: React.FC<z.infer<typeof MyCompositionSchema>> = () => {
  return (
    <div>
      <h1>{props.title}</h1>
    </div>
  );
};
```

在根文件中，可将 schema 传给 composition：

```tsx title="src/Root.tsx"
import { Composition } from "remotion";
import { MycComponent, MyCompositionSchema } from "./MyComposition";

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComponent}
      durationInFrames={100}
      fps={30}
      width={1080}
      height={1080}
      defaultProps={{ title: "Hello World" }}
      schema={MyCompositionSchema}
    />
  );
};
```

此后，用户可以在侧边栏中可视化编辑该参数。

Zod 支持的所有 schema 类型，Remotion 均支持。

Remotion 要求顶层类型为 `z.object()`，因为 React 组件的 props 集合始终是对象。

## Color picker

若要添加颜色选择器，请使用 `@remotion/zod-types` 中的 `zColor()`。

若尚未安装，使用以下命令：

```bash
npx remotion add @remotion/zod-types # If project uses npm
bunx remotion add @remotion/zod-types # If project uses bun
yarn remotion add @remotion/zod-types # If project uses yarn
pnpm exec remotion add @remotion/zod-types # If project uses pnpm
```

然后从 `@remotion/zod-types` 导入 `zColor`：

```tsx
import { zColor } from "@remotion/zod-types";
```

并在 schema 中使用：

```tsx
export const MyCompositionSchema = z.object({
  color: zColor(),
});
```
