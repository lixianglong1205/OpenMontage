# HTML-in-Canvas 模式

HyperFrames 最强大的视觉能力：将任意实时 HTML/CSS 捕获为 GPU 纹理，再通过 WebGL 着色器、Three.js 3D 场景或后期处理效果进行渲染——60fps、像素级精确，并支持全部 CSS 特性。

**当某个 beat 需要超越平面 GSAP 动画的电影感呈现时，请阅读本文。** 每条视频建议用于 1–3 个 hero beat，而非每个 beat。其余 beat 可使用标准 GSAP——平面 beat 与 HTML-in-Canvas beat 之间的对比本身即是视觉叙事的一部分。

---

## 核心样板（每个 HTML-in-Canvas 合成共用）

每个 HTML-in-Canvas 效果都共享这一结构。掌握一次，即可适配任意效果。

```html
<!-- 1. Source HTML — your content goes inside a layoutsubtree canvas -->
<canvas
  id="hic-source"
  layoutsubtree
  width="1920"
  height="1080"
  style="position:absolute;inset:0;opacity:0;"
>
  <div id="hic-content" style="width:1920px;height:1080px;">
    <!-- YOUR HTML CONTENT HERE — text, images, cards, dashboards, anything -->
  </div>
</canvas>

<!-- 2. Render target — the visible canvas that shows the effect -->
<canvas id="hic-output" width="1920" height="1080" style="position:absolute;inset:0;"></canvas>
```

```js
// 3. Feature detection — always check, always provide fallback
function isHiCSupported() {
  var tc = document.createElement("canvas");
  if (!("layoutSubtree" in tc)) return false;
  tc.setAttribute("layoutsubtree", "");
  var ctx = tc.getContext("2d");
  return ctx && typeof ctx.drawElementImage === "function";
}
var apiOk = isHiCSupported();

// 4. Capture function — call this every frame in onUpdate
var capCanvas = document.getElementById("hic-source");
var capCtx = capCanvas.getContext("2d");
function captureContent() {
  if (apiOk) {
    capCtx.drawElementImage(document.getElementById("hic-content"), 0, 0, 1920, 1080);
  }
}

// 5. Drive from GSAP timeline — capture + render every frame
tl.to(
  proxy,
  {
    /* your animation properties */
    duration: BEAT_DURATION,
    ease: "sine.inOut",
    onUpdate: function () {
      captureContent();
      // render your effect here (Three.js or WebGL2)
    },
  },
  0,
);
```

**Fallback：** 当 `drawElementImage` 不可用时（未开启 Chrome 标志的预览环境），可绘制纯色占位或使用 Canvas 2D 文本。HyperFrames 渲染器会自动启用该标志——成片视频中效果**会**正常工作。完整 fallback 示例见 liquid-glass 区块。

---

## 效果目录

### 1. 3D 旋转与 Bloom（Three.js）

**视觉效果：** 内容悬浮于 3D 空间，缓慢旋转，亮边带有电影感辉光。如同在暗色剧场中展示的产品截图。

**适用场景：** Hero 产品展示、功能揭晓、带高级质感的 CTA。

**关键 Three.js 组件：** `PlaneGeometry` + `CanvasTexture` + `EffectComposer` + `UnrealBloomPass`

```js
// After the boilerplate above, add:
var scene3d = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(45, 1920 / 1080, 0.1, 100);
camera.position.set(0, 0, 4);

var renderer = new THREE.WebGLRenderer({
  canvas: document.getElementById("hic-output"),
  antialias: true,
  alpha: true,
});
renderer.setSize(1920, 1080);

var texture = new THREE.CanvasTexture(capCanvas);
var mesh = new THREE.Mesh(
  new THREE.PlaneGeometry(3.6, 2.2),
  new THREE.MeshBasicMaterial({ map: texture }),
);
scene3d.add(mesh);

// Post-processing: bloom for cinematic glow.
// EffectComposer / RenderPass / UnrealBloomPass are ES-module named imports
// (see the import block below) — they're NOT properties of THREE in modern
// versions. Three.js r150+ removed the UMD `examples/js/` globals.
var composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene3d, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(1920, 1080), 0.3, 0.4, 0.85));

var proxy = { rotY: -0.12, zoom: 4.2 };
tl.to(
  proxy,
  {
    rotY: 0.12,
    zoom: 3.6,
    duration: BEAT_DURATION,
    ease: "sine.inOut",
    onUpdate: function () {
      captureContent();
      texture.needsUpdate = true;
      mesh.rotation.y = proxy.rotY;
      camera.position.z = proxy.zoom;
      composer.render();
    },
  },
  0,
);
```

**通过 ESM 加载 Three.js 与后期处理（使用 `type="module"` 脚本）：**

```html
<script type="module">
  import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";
  import { EffectComposer } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/EffectComposer.js";
  import { RenderPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/RenderPass.js";
  import { ShaderPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/ShaderPass.js";
  import { UnrealBloomPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/UnrealBloomPass.js";
  // ... rest of composition code using these imports
</script>
```

Three.js r152 起移除了 `examples/js/` 路径。请使用 `examples/jsm/`（ES 模块）配合 `three@0.181.2`——与 HyperFrames Three.js 适配器所用版本一致。

---

### 2. 磁性光标扭曲（原生 WebGL2）

**视觉效果：** 内容向移动点弯折、扭曲，如同磁铁拉动像素；扭曲处 RGB 通道产生色差分离。

**适用场景：** 交互感、带光标的产品演示、「看这里」的功能高光时刻。

**关键技术：** 自定义片元着色器，高斯扭曲 + 色差分离。无需 Three.js——仅原生 WebGL2。

```js
// WebGL2 setup
var gl = document.getElementById("hic-output").getContext("webgl2", {
  alpha: false,
  preserveDrawingBuffer: true,
});

// Vertex shader — full-screen quad
var VS = `#version 300 es
in vec2 a_pos;
out vec2 v_uv;
void main() {
  v_uv = a_pos * 0.5 + 0.5;
  gl_Position = vec4(a_pos, 0.0, 1.0);
}`;

// Fragment shader — magnetic warp + chromatic aberration
var FS = `#version 300 es
precision highp float;
in vec2 v_uv;
out vec4 fragColor;
uniform sampler2D u_tex;
uniform vec2 u_cursor;   // cursor position (0-1)
uniform float u_strength; // warp strength (0-1)

void main() {
  vec2 uv = v_uv;
  vec2 delta = uv - u_cursor;
  float dist = length(delta);
  float warp = u_strength * exp(-dist * dist * 8.0);
  vec2 warped = uv - delta * warp * 0.3;

  // Chromatic aberration at distortion site
  float aberration = warp * 0.008;
  float r = texture(u_tex, warped + vec2(aberration, 0.0)).r;
  float g = texture(u_tex, warped).g;
  float b = texture(u_tex, warped - vec2(aberration, 0.0)).b;
  fragColor = vec4(r, g, b, 1.0);
}`;

// Compile, link, setup quad geometry, upload texture...
// (See registry/blocks/vfx-magnetic/vfx-magnetic.html for complete implementation)

// Drive cursor position from GSAP
var proxy = { cx: 0.2, cy: 0.5, strength: 0.0 };
tl.to(
  proxy,
  {
    cx: 0.8,
    cy: 0.4,
    strength: 1.0,
    duration: BEAT_DURATION,
    ease: "power2.inOut",
    onUpdate: function () {
      captureContent();
      // Upload texture, set uniforms, draw
      gl.uniform2f(cursorLoc, proxy.cx, proxy.cy);
      gl.uniform1f(strengthLoc, proxy.strength);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    },
  },
  0,
);
```

---

### 3. 碎裂 / 碎片爆炸（Three.js）

**视觉效果：** 内容碎成几何碎片飞散，露出后方画面。

**适用场景：** 戏剧性转场、「挣脱束缚」时刻、张力释放。

**关键技术：** 将源纹理细分为三角形网格碎片（`BufferGeometry`），再用 GSAP 驱动每块碎片的位置/旋转。完整 1156 行实现见 `registry/blocks/vfx-shatter/vfx-shatter.html`。核心思路：

```js
// 1. Capture content to texture (same boilerplate)
// Seeded PRNG for determinism — Math.random() is banned
function mulberry32(seed) {
  return function () {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
var rng = mulberry32(42);

// 2. Create N triangle fragments from the texture
var fragments = [];
for (var i = 0; i < NUM_FRAGMENTS; i++) {
  var geom = new THREE.BufferGeometry();
  var mesh = new THREE.Mesh(geom, new THREE.MeshBasicMaterial({ map: texture }));
  scene3d.add(mesh);
  fragments.push({ mesh: mesh, targetPos: randomExplosionVector(rng), delay: rng() * 0.5 });
}

// 3. Animate: first hold still, then EXPLODE
tl.to({}, { duration: holdTime }, 0);
fragments.forEach(function (frag) {
  tl.to(
    frag.mesh.position,
    {
      x: frag.targetPos.x,
      y: frag.targetPos.y,
      z: frag.targetPos.z,
      duration: 0.8,
      ease: "power3.in",
    },
    holdTime + frag.delay,
  );
  tl.to(
    frag.mesh.rotation,
    { x: rng() * 4, y: rng() * 4, duration: 0.8, ease: "power2.in" },
    holdTime + frag.delay,
  );
});
```

---

### 4. 液体 / 流体表面（Three.js）

**视觉效果：** 内容浮于涟漪起伏的液面之上，具备实时波浪动力学；或内容本身即液面，如水波般起伏。

**适用场景：** 有机/高级感、环境背景、「活」的产品展示。

**关键技术：** 高度细分的 `PlaneGeometry`，顶点着色器中用噪声函数驱动顶点位移。1244 行完整实现见 `registry/blocks/vfx-liquid-background/vfx-liquid-background.html`。核心思路：

```js
// Custom vertex shader with wave displacement
var vertexShader = `
  varying vec2 vUv;
  uniform float u_time;
  void main() {
    vUv = uv;
    vec3 pos = position;
    // Sine wave displacement
    pos.z += sin(pos.x * 3.0 + u_time * 2.0) * 0.15;
    pos.z += cos(pos.y * 2.5 + u_time * 1.5) * 0.1;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  }
`;

var mesh = new THREE.Mesh(
  new THREE.PlaneGeometry(4, 3, 64, 64), // heavily subdivided for smooth waves
  new THREE.ShaderMaterial({
    vertexShader: vertexShader,
    fragmentShader: `varying vec2 vUv; uniform sampler2D u_tex;
      void main() { gl_FragColor = texture2D(u_tex, vUv); }`,
    uniforms: {
      u_tex: { value: texture },
      u_time: { value: 0 },
    },
  }),
);
```

---

### 5. 传送门 / 维度揭晓（Three.js）

**视觉效果：** 发光的圆形传送门打开，内容从另一维度中浮现。

**适用场景：** 产品揭晓、「进入应用」时刻、hero 功能引入。

完整 863 行实现见 `registry/blocks/vfx-portal/vfx-portal.html`。

---

## 何时使用 HTML-in-Canvas 与标准 GSAP

| 场景                         | 选用                                  | 原因                                  |
| -------------------------------- | ------------------------------------ | ------------------------------------ |
| Hero 产品截图展示 | HTML-in-Canvas（3D 旋转 + bloom） | 让平面 UI 具备电影感         |
| 功能列表 / 数据指标             | 标准 GSAP                        | 以内容为主，无需 3D     |
| CTA / 品牌揭晓               | HTML-in-Canvas（portal 或 magnetic）  | 让时刻令人难忘           |
| 社会证明 / Logo             | 标准 GSAP                        | 有序级联，信任感稳定     |
| 幕间转场          | HTML-in-Canvas（shatter）             | 戏剧性的幕间断点                   |
| 背景氛围            | HTML-in-Canvas（liquid surface）      | 高级环境质感                 |
| 快速功能卡片              | 标准 GSAP                        | 速度优先，3D 会拖慢节奏 |

---

## 可自行构建的更多效果

以下尚未收录于 VFX 区块——可从核心样板 + 自定义片元着色器自行搭建。每种效果都是对捕获纹理应用单一 GLSL 函数。

### 6. 噪声溶解

内容溶解为噪声粒子，露出后方。适合转场。

```glsl
// Fragment shader — noise-based dissolve
uniform float u_progress; // 0.0 = fully visible, 1.0 = fully dissolved
uniform sampler2D u_tex;

float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

void main() {
  vec2 uv = v_uv;
  float noise = hash(uv * 50.0);
  float threshold = u_progress;
  if (noise < threshold) {
    // Edge glow at the dissolve boundary
    float edge = smoothstep(threshold - 0.05, threshold, noise);
    fragColor = vec4(1.0, 0.6, 0.2, 1.0) * (1.0 - edge); // orange edge glow
  } else {
    fragColor = texture(u_tex, uv);
  }
}
```

### 7. 全息 / 虹彩

内容呈现随时间移动的彩虹色全息光泽。高级、未来感。

```glsl
uniform float u_time;
uniform sampler2D u_tex;

void main() {
  vec4 color = texture(u_tex, v_uv);
  // Iridescent color shift based on position + time
  float angle = v_uv.x * 6.28 + v_uv.y * 3.14 + u_time * 0.5;
  vec3 holo = vec3(
    sin(angle) * 0.5 + 0.5,
    sin(angle + 2.094) * 0.5 + 0.5,
    sin(angle + 4.189) * 0.5 + 0.5
  );
  // Blend holographic over content (subtle overlay)
  fragColor = vec4(mix(color.rgb, holo, 0.15 + 0.1 * sin(u_time)), color.a);
}
```

### 8. 扫描线 + CRT

复古 CRT 显示器观感——扫描线、轻微桶形畸变、磷光辉光。适合「代码」或「终端」类 beat。

```glsl
uniform sampler2D u_tex;
uniform float u_time;

void main() {
  vec2 uv = v_uv;
  // Barrel distortion (CRT curvature)
  vec2 centered = uv - 0.5;
  float dist = dot(centered, centered);
  uv = uv + centered * dist * 0.15;

  vec4 color = texture(u_tex, uv);
  // Scan lines
  float scanline = sin(uv.y * 800.0) * 0.04;
  color.rgb -= scanline;
  // Slight RGB offset (phosphor)
  color.r = texture(u_tex, uv + vec2(0.001, 0.0)).r;
  color.b = texture(u_tex, uv - vec2(0.001, 0.0)).b;
  // Vignette
  float vignette = 1.0 - dist * 2.0;
  fragColor = vec4(color.rgb * vignette, 1.0);
}
```

### 9. 磨砂玻璃模糊

内容处于磨砂玻璃之后——可见但柔化，带轻微光折射。适合「幕后」或「即将推出」时刻。

```glsl
uniform sampler2D u_tex;
uniform float u_blur; // 0.0 = clear, 1.0 = full frost

void main() {
  vec2 uv = v_uv;
  vec4 color = vec4(0.0);
  // Box blur with offset
  float radius = u_blur * 0.015;
  for (float x = -2.0; x <= 2.0; x += 1.0) {
    for (float y = -2.0; y <= 2.0; y += 1.0) {
      color += texture(u_tex, uv + vec2(x, y) * radius);
    }
  }
  color /= 25.0;
  // Add frost noise texture
  float frost = fract(sin(dot(uv * 200.0, vec2(12.9898, 78.233))) * 43758.5453);
  color.rgb += frost * 0.03 * u_blur;
  fragColor = color;
}
```

### 10. 像素排序 / 故障艺术

像素以竖条或横条重排——数字艺术美学。适合科技/创意品牌。

```glsl
uniform sampler2D u_tex;
uniform float u_intensity; // 0-1

void main() {
  vec2 uv = v_uv;
  // Random horizontal displacement per row
  float row = floor(uv.y * 80.0);
  float noise = fract(sin(row * 127.1) * 43758.5);
  float displace = step(0.7, noise) * u_intensity * 0.1;
  // Shift UV with RGB split
  float r = texture(u_tex, uv + vec2(displace, 0.0)).r;
  float g = texture(u_tex, uv).g;
  float b = texture(u_tex, uv - vec2(displace * 0.5, 0.0)).b;
  fragColor = vec4(r, g, b, 1.0);
}
```

---

## 创建任意自定义效果

上文片元着色器均为模板。模式始终一致：

1. **用 `drawElementImage` 捕获 HTML 内容**（文首样板）
2. **将捕获的 canvas 上传为 WebGL 纹理**
3. **编写片元着色器**，从纹理读取并输出修改后的颜色
4. **在 `onUpdate` 中通过 GSAP 驱动着色器 uniform**

ShaderToy、The Book of Shaders、CodePen 等处的任意 GLSL 效果均可改编：

1. 找到喜欢的效果（搜索「GLSL [效果名]」或浏览 shadertoy.com）
2. 复制片元着色器
3. 将 `iResolution` 替换为 `vec2(1920.0, 1080.0)`，将 `iTime` 替换为你的 `u_time` uniform
4. 添加 `uniform sampler2D u_tex;` 以接入捕获的内容纹理
5. 将 uniform 接到 GSAP 代理值

**平面之外的形体创意：**

- `SphereGeometry` — 内容贴于球体（世界地图、全球触达）
- `CylinderGeometry` — 内容贴于旋转圆柱（轮播/滚动感）
- `TorusGeometry` — 内容绕环包裹（无限、循环）
- `BoxGeometry` — 内容贴于 3D 盒子（产品包装、骰子）
- GLTF 模型 — 内容作为屏幕纹理贴于手机、笔记本、显示器（见 `vfx-iphone-device`）

**后期处理叠加**（Three.js `EffectComposer`）：

- Bloom + 胶片颗粒 = 电影感
- Bloom + 色差 = 镜头效果
- 景深 + 暗角 = 聚焦注意力
- 胶片颗粒 + 扫描线 = 复古
- 多 Pass 可叠加——按需添加

**你不限于本文所列效果。** 只要能想象某种视觉处理，就可以实现。HTML-in-Canvas API 提供源素材（任意 HTML 渲染为纹理），WebGL/Three.js 则对如何呈现该素材提供无上限的创意控制。
