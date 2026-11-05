## 毁灭

### 页面燃烧

出场场景从某一角落开始被真实「烧掉」。火焰前沿以基于噪声的不规则边缘向外扩展，画布在燃烧边界绘制焦黑炭化线；火焰抵达时，单个文字字符/元素会碎裂并在重力作用下坠落。入场场景在燃烧后方逐渐显露。

此过渡由三个系统协同工作：

1. **火焰几何** — 从某一角落（例如右下）向外扩展的径向前沿，通过基于噪声的不规则性形成有机边缘
2. **场景裁剪** — 出场场景使用 SVG clip-path（`fill-rule: evenodd`）在匹配火焰前沿处挖洞。随火焰扩大，更多场景被裁切掉。所有内容（文字、图像、线条）随页面一起燃烧 — 无单独碎屑。
3. **焦黑边缘** — `<canvas>` 叠加层在火焰边界绘制径向渐变 fringe，模拟炭化效果

**何时使用：** 戏剧性揭示、尖锐/毁灭性氛围、游戏、赛博朋克。这是目录中最戏剧性的过渡 — 留给 hero 时刻使用。

**要求：**

- 用于燃烧边缘叠加的 `<canvas>` 元素
- 用于有机火焰边缘几何的噪声函数
- 带 evenodd fill-rule 的反向裁剪用 SVG clip-path

**火焰几何（确定性噪声）：**

```js
function noise(x) {
  var ix = Math.floor(x),
    fx = x - ix;
  var a = Math.sin(ix * 127.1 + 311.7) * 43758.5453;
  var b = Math.sin((ix + 1) * 127.1 + 311.7) * 43758.5453;
  var t = fx * fx * (3 - 2 * fx);
  return a - Math.floor(a) + (b - Math.floor(b) - (a - Math.floor(a))) * t;
}

function fireRadiusAtAngle(angle, progress) {
  var base = progress * maxRadius;
  return (
    base +
    noise(angle * 3 + progress * 4) * 50 +
    noise(angle * 8 + progress * 9) * 20 +
    noise(angle * 15 + progress * 15) * 8
  );
}
```

**入场场景时序：** 燃烧过程中不应看到入场场景。火焰吞噬出场场景时，**洞孔处透出黑色** — 这是戏剧性的关键。观众看着内容在黑暗中毁灭。

约在燃烧进度 90% 时，入场场景从黑色中**缓慢**淡入 — 先背景，再内容错开。使用较长、柔和的淡入（`power1.out`，0.8–1.2s 时长），让新场景像从暗处浮现，而非硬切。

```js
// Scene 2 stays at opacity: 0 during the burn — black behind the fire
tl.set("#s2-title", { opacity: 0 }, T);
tl.set("#s2-subtitle", { opacity: 0 }, T);

// At 90% through, scene bg fades in slowly from black
var contentReveal = T + BURN_DURATION * 0.9;
tl.to("#scene2", { opacity: 1, duration: 1.2, ease: "power1.out" }, contentReveal);

// Content fades in staggered on top, even slower
tl.to("#s2-title", { opacity: 1, duration: 1.0, ease: "power1.out" }, contentReveal + 0.5);
tl.to("#s2-subtitle", { opacity: 1, duration: 0.8, ease: "power1.out" }, contentReveal + 0.7);
```

**内容与页面一同燃烧 — 无坠落碎屑。** scene1 上的 clip-path 即效果本身 — 火焰形状扩大时，火焰边缘后的所有内容（文字、图像、线条）自然消失。不要克隆元素，不要生成坠落碎屑。内容是正在被吞噬的页面的一部分。焦黑 canvas 边缘在燃烧边界提供视觉炭化线。

**在燃烧结束时用 `tl.set` 隐藏 scene1 — 绝不在 `onComplete` 中。** 在 `onComplete` 里隐藏 scene1 在 scrub 时不可回退。应在精确的燃烧结束时刻使用 `tl.set`：

```js
tl.to(
  burnState,
  {
    progress: 1,
    duration: BURN_DURATION,
    ease: "none",
    onUpdate: function () {
      var wp = burnState.progress;
      var scene1 = document.getElementById("scene1");
      if (wp <= 0) {
        scene1.style.clipPath = "none"; // fully visible when rewound
      } else if (wp < 1) {
        scene1.style.clipPath = buildClipPath(wp);
      }
      drawEdge(wp);
    },
    // NO onComplete — use tl.set instead
  },
  T,
);

// Hide scene1 at exact burn end — reversible via timeline
tl.set("#scene1", { opacity: 0 }, T + BURN_DURATION);
tl.set("#scene1", { clipPath: "none" }, T + BURN_DURATION);
```

`onUpdate` 逐帧处理 clip-path 与 canvas 边缘。`tl.set` 负责最终隐藏 — GSAP 在向后 scrub 时会自动逆转，将 scene1 恢复为 `opacity: 1`。

`onUpdate` 回调是关键 — 它每帧运行，使 clip-path 与 canvas 边缘与时间轴同步推进。
