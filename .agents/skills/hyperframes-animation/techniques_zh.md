# 视觉技法参考

来自 HyperFrames 生产视频的 13 种成熟技法。在分镜与合成中使用它们，产出视觉丰富、专业的成片。每种技法都包含可改编的最小代码模式。

这些并非高阶技巧——它们是标准 motion design 模式，每个合成至少应使用其中 2–3 种。

## 目录

- SVG 路径绘制
- Canvas 2D 程序化艺术
- CSS 3D 变换
- 逐词 kinetic typography（动态排版）
- Lottie 动画
- 视频合成
- 逐字符打字
- 可变字体轴动画
- GSAP MotionPathPlugin
- 速度匹配转场
- 音频驱动动画
- clip-path 揭示遮罩
- WebGL 片段着色器艺术
- 何时使用什么

> **将实时 HTML/CSS 捕获为 GPU 纹理**（3D 旋转 + bloom、磁扭曲、碎裂、液面、传送门，以及 GLSL 后处理）是独立、更重的能力——见 `adapters/html-in-canvas-patterns.md`。每条视频用于 1–3 个 hero beat，而非每个 beat。
>
> **缓动词汇**——完整的 ease 族调色板（角色 + 情绪映射）在 `adapters/gsap-easing-and-stagger.md`。每个合成至少应使用 3 种不同的 easing。
>
> **命名文本动画效果**（24 个 ID，如 `typewriter`、`kinetic-center-build`、`soft-blur-in`）来自外部 `animate-text` skill——见 `adapters/animate-text.md` 了解词汇表及如何加载。

---

## 1. SVG 路径绘制

路径实时自绘，如同用笔描线。用于揭示示意图、箭头、连接线或品牌标识。

```html
<svg viewBox="0 0 400 200">
  <path
    class="draw-path"
    d="M 50 100 L 200 50 L 350 100"
    stroke="#c84f1c"
    stroke-width="4"
    fill="none"
    stroke-linecap="round"
  />
</svg>
<style>
  .draw-path {
    stroke-dasharray: 280;
    stroke-dashoffset: 280;
  }
</style>
<script>
  tl.to(".draw-path", { strokeDashoffset: 0, duration: 0.7, ease: "power2.out" }, 0.5);
</script>
```

使用 `path.getTotalLength()` 动态计算 dasharray 值。

---

## 2. Canvas 2D 程序化艺术

动画噪声、粒子场、数据可视化——任何逐帧演变的内容。用 GSAP 代理驱动。

```html
<canvas id="proc-canvas" width="1920" height="1080"></canvas>
<script>
  var canvas = document.getElementById("proc-canvas");
  var ctx = canvas.getContext("2d");

  function hash(x, y) {
    var n = x * 374761393 + y * 668265263;
    n = (n ^ (n >> 13)) * 1274126177;
    return ((n ^ (n >> 16)) & 0x7fffffff) / 0x7fffffff;
  }

  function drawFrame(t) {
    ctx.fillStyle = "#0a0a0a";
    ctx.fillRect(0, 0, 1920, 1080);
    for (var i = 0; i < 200; i++) {
      var x = hash(i, 0) * 1920;
      var y = hash(i, 1) * 1080;
      var brightness = hash(i, Math.floor(t * 10)) * 255;
      ctx.fillStyle = "rgba(255, 255, 255, " + brightness / 255 + ")";
      ctx.beginPath();
      ctx.arc(x, y, 2, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  var proxy = { time: 0 };
  tl.to(
    proxy,
    {
      time: 5,
      duration: 5,
      ease: "none",
      onUpdate: function () {
        drawFrame(proxy.time);
      },
    },
    0,
  );
</script>
```

`hash()` 函数是确定性的——同一帧每次渲染结果相同。

---

## 3. CSS 3D 变换

透视旋转营造纵深。用于产品展示、卡片翻转、建筑揭示。

```html
<div class="stage" style="perspective: 900px;">
  <div class="card-3d" style="transform-style: preserve-3d;">
    <div class="face front">Product</div>
    <div class="face back" style="transform: rotateY(180deg);">Details</div>
  </div>
</div>
<script>
  tl.to(".card-3d", { rotationY: 360, rotationX: 15, duration: 1.2, ease: "sine.inOut" }, 0);
</script>
```

始终在父元素上设置 `perspective`，在动画元素上设置 `transform-style: preserve-3d`。

---

## 4. 逐词动态排版

词语逐个出现，与 transcript.json 时间戳同步。旁白驱动视频的核心技法。

```html
<div class="headline">
  <span class="word w-0">Anything</span>
  <span class="word w-1">a</span>
  <span class="word w-2">browser</span>
  <span class="word w-3">can</span>
  <span class="word w-4">render</span>
</div>
<style>
  .word {
    display: inline-block;
    opacity: 0;
    margin: 0 0.12em;
  }
</style>
<script>
  // Word onset times from transcript.json (seconds relative to beat start)
  var timings = [0.0, 0.23, 0.28, 0.63, 0.78];
  var slides = [80, 60, 50, 25, 12]; // horizontal slide decay (px)

  document.querySelectorAll(".word").forEach(function (word, i) {
    tl.from(
      word,
      {
        x: slides[i],
        y: 14,
        opacity: 0,
        duration: 0.35,
        ease: "power2.out",
      },
      timings[i],
    );
  });
</script>
```

横向滑动距离逐词衰减（80→12px）——模拟镜头逐渐稳定。

---

## 5. Lottie 动画

在合成内播放的矢量动画。用于 logo、角色动画、图标。

```html
<div id="logo-anim" class="lottie" style="width:500px;height:500px;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
<script>
  window.__hfLottie = window.__hfLottie || [];

  const anim = lottie.loadAnimation({
    container: document.getElementById("logo-anim"),
    renderer: "svg",
    loop: false,
    autoplay: false,
    path: "../capture/assets/lottie/animation-0.json",
  });
  window.__hfLottie.push(anim); // REQUIRED — adapter seeks every registered instance

  gsap.set("#logo-anim", { scale: 0.3, opacity: 0 });
  tl.to("#logo-anim", { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.6)" }, 0.2);
</script>
```

`autoplay: false` + `loop: false` + `window.__hfLottie.push()` 为必填——HyperFrames 将每个已注册播放器 seek 到合成时间，若保留 `autoplay`/`loop` 则按墙钟运行且渲染非确定性。适配器 seek 绝对时间（无 modulo 循环、无 playback-rate 缩放）：将重复周期或非默认速度烘焙进 Lottie 资源或显式时间线，再验证渲染。完整约定及 `.lottie`/dotLottie 变体：`adapters/lottie.md`。

---

## 6. 视频合成

在合成内嵌入真实视频素材。视频须 `muted` 且 `playsinline`。

```html
<div class="video-frame" style="width:680px;height:840px;border-radius:16px;overflow:hidden;">
  <video
    id="footage"
    src="../capture/assets/videos/clip.mp4"
    muted
    playsinline
    style="width:100%;height:100%;object-fit:cover;"
  ></video>
</div>
<script>
  // Video playback is controlled by the framework — don't call play() manually
  tl.from(".video-frame", { scale: 0.9, opacity: 0, duration: 0.3, ease: "power2.out" }, 0);
</script>
```

HyperFrames 运行时处理视频 seek 与播放。

---

## 7. 逐字符打字

使用 `tl.call()` 逐字符更新文本内容的终端打字效果。

```html
<div class="terminal-line">
  <span class="prompt">❯</span>
  <span class="typed" id="typed-text"></span>
  <span class="cursor" style="width:11px;height:22px;background:#333;display:inline-block;"></span>
</div>
<script>
  var CMD = "npx hyperframes init";
  var typed = document.getElementById("typed-text");

  // Cursor blinks
  tl.to(".cursor", { opacity: 0, duration: 0.12, yoyo: true, repeat: 20, ease: "steps(1)" }, 0);

  // Type each character
  for (var i = 0; i < CMD.length; i++) {
    (function (idx) {
      tl.call(
        function () {
          typed.textContent = CMD.substring(0, idx + 1);
        },
        null,
        (idx / CMD.length) * 0.9,
      );
    })(i);
  }
</script>
```

光标闪烁使用 `ease: "steps(1)"`——产生离散开/关。

---

## 8. 可变字体轴动画

动画 `font-variation-settings` 以实时重塑字形。适用于带 optical size（opsz）、weight（wght）、softness（SOFT）等轴的可变字体。

```html
<style>
  /* Load the captured local variable font — do NOT use Google Fonts @import.
     Replace this placeholder with an @font-face pointing to ../capture/assets/fonts/. */
  @font-face {
    font-family: "Fraunces";
    src: url("../capture/assets/fonts/Fraunces-Variable.woff2") format("woff2");
    font-weight: 100 900;
    font-style: normal;
    font-display: block;
  }
  .wordmark {
    --opsz: 144;
    --wght: 440;
    font-family: "Fraunces", serif;
    font-variation-settings:
      "opsz" var(--opsz),
      "wght" var(--wght);
    font-size: 200px;
  }
</style>
<script>
  tl.to(".wordmark", { "--opsz": 72, "--wght": 300, duration: 0.45, ease: "power2.out" }, 0);
</script>
```

轴动画时字形会微妙重塑——optical size 调整细节，weight 改变粗细。

---

## 9. GSAP MotionPathPlugin

沿任意 SVG 路径动画元素。用于沿曲线滑动的控件、沿轨迹的粒子、引导式揭示。

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/MotionPathPlugin.min.js"></script>
<div class="dot" style="width:20px;height:20px;background:#2a8a7c;border-radius:50%;"></div>
<script>
  gsap.registerPlugin(MotionPathPlugin);
  tl.to(
    ".dot",
    {
      motionPath: { path: "M 12 300 C 280 280 520 80 820 50 S 1200 48 1308 38" },
      duration: 1.5,
      ease: "power2.out",
    },
    0,
  );
</script>
```

---

## 10. 速度匹配转场

退出当前 beat、进入下一 beat 时匹配速度——营造连续运动的感知。

```javascript
// EXIT (in outgoing composition): accelerating with blur
tl.to(
  ".content",
  {
    y: -150,
    filter: "blur(30px)",
    opacity: 0,
    duration: 0.33,
    ease: "power2.in", // accelerates
  },
  beatDuration - 0.33,
);

// ENTRY (in incoming composition): decelerating from blur
gsap.set(".content", { y: 150, filter: "blur(30px)" });
tl.to(
  ".content",
  {
    y: 0,
    filter: "blur(0px)",
    duration: 1.0,
    ease: "power2.out", // decelerates
  },
  0,
);
```

两条曲线在切点处速度最快——观众感知为平滑的镜头运动。匹配 ease 族：退出用 `.in`，进入用 `.out`。

---

## 11. 音频驱动动画

从正在播放的音频驱动任意 GSAP 可 tween 属性。低音在底鼓上脉冲 logo。高音在镲片上点亮 CTA。振幅在安静乐句中让背景「呼吸」。效果：运动与音轨锁定的感受，预写 tween 难以达到。

**何时使用：** 任何带音乐或戏剧旁白的视频——品牌 reel、产品发布、 hype 剪辑。平静/教程节奏可跳过。

**原理：** 预提取音频频段到 JSON，再通过 `tl.call()` 逐帧采样：

```js
// audio-data.json: { fps: 30, totalFrames: 900, frames: [{ bands: [0.82, 0.45, 0.31, ...] }, ...] }
for (var f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    (function (frame) {
      return function () {
        var bass = frame.bands[0]; // 0–1
        var treble = frame.bands[13];
        gsap.set(".logo", { scale: 1 + bass * 0.04 }); // 3–4% pulse on bass
        gsap.set(".cta", { filter: `drop-shadow(0 0 ${treble * 24}px #00C3FF)` });
      };
    })(AUDIO_DATA.frames[f]),
    [],
    f / AUDIO_DATA.fps,
  );
}
```

必须逐帧采样——单个 tween 无法反应。使用提取脚本：

```bash
python3 skills/hyperframes-creative/scripts/extract-audio-data.py narration.wav --fps 30 --bands 16 -o audio-data.json
```

文字/logo 强度保持 subtle（缩放 ≤5%，光晕 ≤30%）——小元素上的音频驱动易被读成抖动。更大背景可推到 10–30%。

**切勿：** 均衡器条、频谱分析仪、波形显示、频闪、彩虹色循环。音频提供的是_时机与强度_；视觉词汇仍来自品牌。完整 API 与反模式见 `skills/hyperframes-creative/references/audio-reactive.md`。

---

## 12. Clip-Path 揭示遮罩

固定窗口，内容从中滑过——文字或图像从一侧进入，被不可见边界裁剪。与 SVG 路径绘制不同：遮罩静态，内容移动。

```html
<div id="reveal-mask">
  <div id="reveal-content">Your headline text here</div>
</div>
<style>
  #reveal-mask {
    position: absolute;
    inset: 0;
    clip-path: inset(0 200px 0 0); /* clips 200px from right */
    display: flex;
    align-items: center;
    justify-content: center;
  }
  #reveal-content {
    font-size: 108px;
    white-space: nowrap;
  }
</style>
<script>
  // Content starts offscreen right, slides left through the mask window
  gsap.set("#reveal-content", { x: 400, opacity: 0 });
  tl.to("#reveal-content", { x: 0, opacity: 1, duration: 1, ease: "power2.out" }, 0);
</script>
```

变体：`clip-path: circle(0% at 50% 50%)` → `circle(100%)` 做 iris 揭示。`clip-path: polygon(...)` 做自定义形状。

---

## 13. WebGL 片段着色器艺术

完整 GPU 生成式背景——域扭曲 FBM 噪声、余弦调色板着色、虹彩有机图案。远比 Canvas 2D 丰富。

```html
<canvas id="shader-bg" width="1920" height="1080"></canvas>
<script>
  var canvas = document.getElementById("shader-bg");
  var gl = canvas.getContext("webgl");
  if (!gl) {
    /* fallback to gradient */
  }

  var fsrc = `
    precision mediump float;
    varying vec2 v_uv;
    uniform float u_time;
    uniform vec2 u_res;

    float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
    float noise(vec2 p) {
      vec2 i = floor(p), f = fract(p);
      f = f * f * (3.0 - 2.0 * f);
      return mix(mix(hash(i), hash(i+vec2(1,0)), f.x),
                 mix(hash(i+vec2(0,1)), hash(i+vec2(1,1)), f.x), f.y);
    }
    float fbm(vec2 p) {
      float v = 0.0, a = 0.5;
      mat2 R = mat2(0.8, 0.6, -0.6, 0.8);
      for (int i = 0; i < 5; i++) { v += a*noise(p); p = R*p*2.02; a *= 0.5; }
      return v;
    }
    vec3 palette(float t) {
      return vec3(0.5)+vec3(0.5)*cos(6.28318*(vec3(1)*t+vec3(0.0,0.33,0.67)));
    }
    void main() {
      vec2 uv = v_uv; uv.x *= u_res.x/u_res.y;
      float t = u_time * 0.4;
      vec2 q = vec2(fbm(uv*3.0+t*0.3), fbm(uv*3.0+vec2(5.2,1.3)+t*0.2));
      vec2 r = vec2(fbm(uv*3.0+q*4.0+vec2(1.7,9.2)+t*0.15), fbm(uv*3.0+q*4.0+vec2(8.3,2.8)+t*0.1));
      float n = fbm(uv*3.0+r*2.0);
      vec3 col = palette(n*2.0+t*0.2);
      col = mix(col, palette(length(q)*3.0+t*0.1), 0.4);
      col *= 0.7+0.3*n;
      float vig = 1.0-0.4*length(v_uv-0.5);
      gl_FragColor = vec4(col*vig, 1.0);
    }
  `;

  // Compile, link, set up fullscreen quad, then render via GSAP proxy:
  var proxy = { time: 0.5 };
  tl.to(
    proxy,
    {
      time: 5,
      duration: BEAT_DUR,
      ease: "none",
      onUpdate: function () {
        gl.uniform1f(uTime, proxy.time);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      },
    },
    0,
  );
</script>
```

无 WebGL 的环境务必提供 Canvas 2D 渐变回退。

---

## 何时使用什么

| 视频能量 | 可组合的技法 |
| ------------------------------ | --------------------------------------------------------------- |
| 高冲击（发布、促销） | 逐词排版 + 速度匹配转场 + 计数器动画 |
| 电影感（导览、故事） | SVG 路径绘制 + 视频合成 + 3D 变换 |
| 技术向（开发工具、API） | 逐字符打字 + Canvas 2D 程序化 + MotionPath |
| 高端（奢侈品、企业） | 可变字体动画 + Lottie + 慢速速度匹配转场 |
| 数据驱动（统计、指标） | Canvas 2D 程序化 + 计数器动画 + SVG 路径绘制 |
