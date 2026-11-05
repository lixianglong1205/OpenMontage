# 音频响应式动画

用音乐、人声或任意声音驱动画面。任何 GSAP 可动画化的属性都可以响应预先提取的音频数据。

## 音频数据格式

```js
var AUDIO_DATA = {
  fps: 30,
  totalFrames: 900,
  frames: [{ bands: [0.82, 0.45, 0.31, ...] }, ...]
};
```

- `frames[i].bands[]` — 各频段振幅，取值 0–1。索引 0 为低音，索引越高越偏高音。
- 每个频段在整首曲目内独立归一化。

## 将音频映射到视觉

| 音频信号              | 视觉属性                          | 效果                       |
| --------------------- | --------------------------------- | -------------------------- |
| 低音（bands[0]）      | `scale`                           | 节拍脉冲                   |
| 高音（bands[12-14]）  | `textShadow`、`boxShadow`         | 发光强度                   |
| 整体振幅              | `opacity`、`y`、`backgroundColor` | 呼吸感、抬升、色彩变化     |
| 中频（bands[4-8]）    | `borderRadius`、`width`           | 形状变形                   |

任意 GSAP 可补间属性都适用 — `clipPath`、`filter`、SVG 属性、CSS 自定义属性等。

## 内容优先，而非媒介

音频提供**节奏与强度**。视觉语汇来自叙事本身。

**切勿添加：** 均衡器条、频谱分析仪、波形显示、音符剪贴画、泛用粒子系统、彩虹色循环、节拍上的白闪、抽象脉冲光球。

**应当：** 让内容决定视觉形态，让音频驱动其行为。低音使暖意 _膨胀_。高音使 _对比_ 更锐利。视觉选择应来自「这段内容给人的感觉是什么？」

## 采样模式

音频响应必须通过 `for` 循环配合 `tl.call()` 逐帧采样，而不能用单次 tween：

```js
// ✅ Correct — sample every frame
for (var f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    (function (frame) {
      return function () {
        draw(frame);
      };
    })(AUDIO_DATA.frames[f]),
    [],
    f / AUDIO_DATA.fps,
  );
}

// ❌ Wrong — single tween, doesn't react to audio
gsap.to(".el", { scale: 1.2, duration: totalDuration });
```

若不逐帧采样，成片实际上不会对音频做出反应。

## textShadow 注意事项

在父容器上设置 `textShadow`，且子元素为半透明（例如未激活字幕词为 `rgba(255,255,255,0.3)`）时，会在所有子元素后方出现可见的发光矩形。修复方式：在容器上用 `scale` 做节拍脉冲，但仅对当前激活的单个词应用 `textShadow`。

## 指南

- **文字宜克制** — 缩放变化约 3–6%，柔和发光。剧烈脉冲会让文字难以阅读。
- **非文字元素可更大** — 背景与形状可承受约 10–30% 的幅度变化。
- **匹配能量感** — 企业风格 = 克制；音乐视频 = 戏剧化。
- **确定性** — 使用预提取数据，不用 Web Audio API，不做运行时分析。

## 约束

- 所有音频数据必须预先提取（使用本技能 `scripts/` 中的 `extract-audio-data.py`）
- 禁止使用 `Math.random()` 或 `Date.now()`
- 音频响应与其余动画共用同一条 GSAP 时间线
