---
name: hyperframes-three
description: 面向 HyperFrames 的 Three.js 与 WebGL 适配器模式。适用于创建确定性 Three.js 场景、WebGL 画布层、AnimationMixer 时间线、相机动画、着色器驱动视觉效果，或响应 HyperFrames hf-seek 事件的画布渲染。
---

# 面向 HyperFrames 的 Three.js

HyperFrames 通过 `three` 运行时适配器支持 Three.js。适配器不拥有你的场景；它发布 HyperFrames 时间并派发 seek 事件，以便你的合成能渲染精确帧。

## 契约

- 尽可能在同步阶段创建场景、相机、渲染器、材质与资源。
- 从 HyperFrames 时间渲染，而非挂钟时间。
- 监听 `hf-seek` 事件，并精确渲染该时刻。
- 在渲染关键的 seek 之前加载模型、纹理与 HDRI；不要在 seek 时再去拉取。
- 勿将 `requestAnimationFrame` 或 `renderer.setAnimationLoop` 作为渲染关键运动的唯一真相来源。

适配器会设置 `window.__hfThreeTime`，并在每次 seek 时派发 `new CustomEvent("hf-seek", { detail: { time } })`。

## 基本模式

```html
<canvas id="three-layer"></canvas>
<script type="module">
  import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";

  const canvas = document.getElementById("three-layer");
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  // Match these to your composition's frame size.
  renderer.setSize(1920, 1080, false);
  renderer.setPixelRatio(1);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1920 / 1080, 0.1, 100);
  camera.position.set(0, 0, 6);

  const mesh = new THREE.Mesh(
    new THREE.IcosahedronGeometry(1.4, 4),
    new THREE.MeshStandardMaterial({ color: 0x64d2ff, roughness: 0.38 }),
  );
  scene.add(mesh);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 2));

  function renderAt(time) {
    mesh.rotation.y = time * 0.7;
    mesh.rotation.x = Math.sin(time * 0.6) * 0.16;
    renderer.render(scene, camera);
  }

  window.addEventListener("hf-seek", (event) => {
    renderAt(event.detail.time);
  });

  renderAt(window.__hfThreeTime || 0);
</script>
```

```css
#three-layer {
  width: 100%;
  height: 100%;
  display: block;
}
```

## 加载插件（`GLTFLoader`、`OrbitControls` 等）

对于 `three/addons/` 下的任何内容，使用 importmap 以便裸说明符能正确解析。HyperFrames lint 同时识别此形式与上文内联 `+esm` 导入——按你的合成需求任选其一。

```html
<script type="importmap">
  {
    "imports": {
      "three": "https://cdn.jsdelivr.net/npm/three@0.181.2/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/"
    }
  }
</script>
<script type="module">
  import * as THREE from "three";
  import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
  import { OrbitControls } from "three/addons/controls/OrbitControls.js";
  // ...
</script>
```

将 importmap 中两处 `three` 版本钉在同一值。在 map 与裸导入之间混用版本会导致静默损坏。

## AnimationMixer 模式

对于 GLTF 或已编排的片段动画，直接 seek 混合器：

```js
function renderAt(time) {
  mixer.setTime(time);
  renderer.render(scene, camera);
}
```

若存在多个 mixer，请用同一 `time` 对全部进行 seek。

## 适用场景

- 确定性 3D 物体、产品旋转、带种子数据的粒子，以及着色器底板。
- 由 `time` 推导的相机运动。
- 资源已本地化且在验证完成前已加载的 GLTF 动画片段。

## 应避免

- 使用 `Date.now()`、`performance.now()` 或时钟增量更新场景状态。
- 将渲染关键工作留在自由运行的动画循环内。
- 在渲染时加载远程模型或纹理。
- 依赖设备像素比的输出。为视频渲染固定渲染器尺寸与像素比。
- 依赖上一帧历史的后期处理通道，除非你能从时间重建状态。

## 验证

编辑 Three.js 合成后：

```bash
npx hyperframes lint
npx hyperframes validate
```

## 致谢与参考

- HyperFrames 适配器源码：`packages/core/src/runtime/adapters/three.ts`。
- Three.js `WebGLRenderer` 文档：https://threejs.org/docs/pages/WebGLRenderer.html
- Three.js `AnimationMixer.setTime()` 文档：https://threejs.org/docs/pages/AnimationMixer.html
