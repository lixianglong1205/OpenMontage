# 文本模块 · 动效词汇（primitive → GSAP）

具名 primitive 供 Director 在 `motion` 字符串中引用、由 Builder 实现。`code_hint` 为与框架无关的物理描述；GSAP recipe 即 HF 实现方式。若有合适的 HF **registry component**（见文末），应优先选用，勿重复造轮子。

## 入场（Entry）

| primitive                     | GSAP recipe（写入 CSS 终态）                               | 适用风格                     |
| ----------------------------- | -------------------------------------------------------------- | ------------------------- |
| `slide_bottom/top/left/right` | `from({ y:±150 / x:±200, opacity:0, ease:"power4.out" })`      | 沉稳、递进、专业 |
| `scale_grow`                  | `from({ scale:0, opacity:0, duration:.6, ease:"power2.out" })` | 沉稳、柔和              |
| `scale_punch`                 | `from({ scale:.6, opacity:0, ease:"back.out(2.2)" })`          | 冲击、动感         |
| `fade_in`                     | `from({ opacity:0, duration:.4 })`                             | 低调、含蓄                    |
| `fade_blur`                   | `from({ opacity:0, filter:"blur(14px)" })`                     | 电影感、梦幻         |
| `typewriter`                  | 通过 clip/`SplitText` 宽度步进揭示                         | 技术感、叙事      |
| `word_reveal`                 | 逐词 `from({opacity:0,y:..}, stagger:.1)`                  | 叙事                |
| `wave`                        | 逐字母 `from({y:..}, stagger:{each:.04})`                  | 流动、音乐感                  |
| `bounce_in`                   | `from({y:-120}, ease:"bounce.out")`                            | 活泼、俏皮                   |
| `slam`                        | `from({ y:-300, ease:"power4.out" })` + 落地时 `shake`          | 冲击、厚重             |

## 强调（Emphasis）（原位，常在节拍上）

| primitive     | GSAP recipe                                                          | 适用风格              |
| ------------- | -------------------------------------------------------------------- | ------------------ |
| `scale_pulse` | 在节拍处 `to({ scale:1.12, yoyo:true, repeat:1, ease:"sine.inOut" })` | 有节奏、峰值     |
| `shake`       | `to({ keyframes:[{x:-9},{x:9},{x:0}], ease:"none" })`                | 紧迫、强烈    |
| `glow`        | `to({ textShadow:"0 0 46px <ink/accent>", yoyo:true, repeat:1 })`    | 重要、魔法感 |
| `color_shift` | `to({ color:"<accent>" })`（或在 CSS 中对词使用 accent）            | 动态            |

## 退场（Exit）

| primitive   | GSAP recipe                                        | 适用风格      |
| ----------- | -------------------------------------------------- | ---------- |
| `fade_out`  | `to({ opacity:0, duration:.4, ease:"power2.in" })` | 收尾     |
| `slide_out` | `to({ y/x: off, opacity:0, ease:"power2.in" })`    | 转场 |
| `scale_out` | `to({ scale:1.06, opacity:0, ease:"power2.in" })`  | 转场 |

## 点缀图形（非文本）

`underline_sweep` `fromTo({scaleX:0},{scaleX:1}, transformOrigin:"left center")` · `bar_wipe` · `hold_breath` `to({scale:1.015, ease:"sine.inOut"})`。

## 合适时优先使用 HF registry 组件

`caption-kinetic-slam` · `caption-editorial-emphasis` · `caption-neon-glow` · `caption-glitch-rgb` · `caption-particle-burst` · `caption-weight-shift` · `caption-matrix-decode` · `caption-pill-karaoke` · `shimmer-sweep`。这些为预构建、生态内且已通过渲染测试的组件 — Builder 在动手实现同等效果前应优先选用。
