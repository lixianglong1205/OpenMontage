# 时间轴与标签

HyperFrames 是 seek 驱动的运行时。每个 composition 构建一条暂停的时间轴，将其挂到 `window.__timelines["<composition-id>"]`，由 HyperFrames 对其 seek。切勿为渲染关键动画调用 `.play()`。

## 创建时间轴

```javascript
const tl = gsap.timeline({
  paused: true,
  defaults: { duration: 0.5, ease: "power2.out" },
});

tl.to(".a", { x: 100 }).to(".b", { y: 50 }).to(".c", { opacity: 0 });
```

时间轴选项：

- **paused: true** — 在 HyperFrames 中必需。由框架驱动播放头。
- **repeat**、**yoyo** — 作用于整条时间轴。禁止使用 `repeat: -1`；请使用有限次数。
- **defaults** — 合并到每个子 tween 的 vars。用此替代在每一行重复写 `ease` 和 `duration`。

## 位置参数

`.to()`/`.from()`/`.fromTo()` 的第三个参数控制 tween 在时间轴上的放置位置：

| 形式           | 含义                              |
| -------------- | ------------------------------------ |
| `0`, `1.5`     | 绝对时间（秒）             |
| `"+=0.5"`      | 时间轴结束后再过 0.5 秒   |
| `"-=0.2"`      | 时间轴结束前 0.2 秒  |
| `"intro"`      | 位于 `intro` 标签处                 |
| `"intro+=0.3"` | `intro` 标签后再过 0.3 秒         |
| `"<"`          | 与上一个 tween 同时开始     |
| `">"`          | 紧接上一个 tween 结束之后  |
| `"<0.2"`       | 上一个 tween 开始后 0.2 秒 |
| `">-0.1"`      | 上一个 tween 结束前 0.1 秒  |

```javascript
tl.to(".a", { x: 100 }, 0);
tl.to(".b", { y: 50 }, "<"); // same start as .a
tl.to(".c", { opacity: 0 }, "<0.2"); // 0.2s after .b starts
```

优先使用位置参数而非 `delay:` — 它组合更自然，且在重构、重排 tween 时仍成立。

## 标签

```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");

tl.addLabel("outro", "+=0.5");
tl.to(".a", { opacity: 0 }, "outro");
```

标签让长时间轴更易读，并让多个 tween 在同一节拍汇合，而无需反复写绝对时间。

## 嵌套时间轴

```javascript
const master = gsap.timeline({ paused: true });

const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });

master.add(child, 0);
```

在 HyperFrames 中，**不要**将子 composition 的时间轴嵌套进宿主。通过 `data-composition-src` 加载的子 composition 由 HyperFrames 根据各自的 `data-start` 独立 seek。嵌套仅用于将**同一** composition 时间轴内的片段分组。

## 子 composition 内：优先 `fromTo` 而非 `from`

在子 composition 内的入场 tween，优先使用 `gsap.fromTo()` 而非 `gsap.from()`：

```javascript
// Sub-composition entrance — survives re-seek cleanly
tl.fromTo(".title", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0.2);
```

原因：每当宿主 clip 变为可见时，HyperFrames 会重新 seek 子 composition。`gsap.from()` 在**注册时**（页面加载）快照起始状态；当播放头跳回 `data-start` 之前时，该快照可能与实际 CSS 状态不同步，元素会渲染在错误位置。`gsap.fromTo()` 显式声明两端点，因此每次 seek 回去都会产生相同的起始状态。

在顶层（独立）composition 中两种写法均可 — 没有通过挂载周期反复 re-seek 的问题。

## 播放控制（仅调试 / 预览）

```javascript
tl.play();
tl.pause();
tl.reverse();
tl.restart();
tl.time(2);
tl.progress(0.5);
tl.kill();
```

在浏览器中预览时很有用。在渲染输出中 HyperFrames 在内部调用 `seek()` — 你的时间轴必须在每次被 seek 到相同时间值时产生一致的状态。
