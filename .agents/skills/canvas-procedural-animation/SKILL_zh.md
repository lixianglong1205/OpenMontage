---
name: canvas-procedural-animation
description: 使用 p5.js/canvas 实现本地程序化角色效果：粒子、天气、挤压拉伸、走路循环与环境动效。
license: MIT
---

# Canvas 程序化动画

当使用 p5.js 或 Canvas 实现角色辅助动效时使用本技能：
雨、雪、落叶、羽毛、环境粒子、挤压拉伸或程序化走路循环。

## 成熟模式

p5.js 在 `setup()` 中初始化一次，并通过 `draw()` 持续重绘。渲染预览时，让动画状态由时间/帧值确定性驱动。

```js
function setup() {
  createCanvas(1920, 1080);
}

function draw() {
  const t = millis() / 1000;
  clear();
  drawCharacter(width / 2, height / 2 + sin(t * 8) * 8);
}
```

## 适用场景

- 粒子/天气叠加层。
- 环境动效。
- 简单的程序化躯体。
- 不需要单独创作 SVG 部件的效果。

## 不适用场景

- 复杂的面部表演（SVG/分层 rig 部件更易检查）。
- 需要精确帧确定性的最终渲染（除非运行时暴露帧索引控制）。

## 参考来源

- p5.js `setup()` reference: https://p5js.org/reference/p5/setup/
- p5.js `draw()` reference: https://p5js.org/reference/p5/draw/
- p5.js animation examples: https://p5js.org/examples/
