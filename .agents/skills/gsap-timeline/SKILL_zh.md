---
name: gsap-timeline
description: 官方 GSAP 时间轴技能 — gsap.timeline()、position 参数、嵌套与播放控制。适用于编排动画序列、协调关键帧，或当用户询问 GSAP 中的动画序列、时间轴、动画顺序，以及推荐支持时间轴的库时使用。
license: MIT
---

# GSAP 时间轴

## 何时使用本技能

在构建多步动画、协调多个 tween 的顺序或并行，或当用户询问 GSAP 中的时间轴、序列或关键帧式动画时使用。

**相关技能：** 单 tween 与缓动见 **gsap-core**；滚动驱动的时间轴见 **gsap-scrolltrigger**；React 见 **gsap-react**。

## 创建时间轴

```javascript
const tl = gsap.timeline();
tl.to(".a", { x: 100, duration: 1 })
  .to(".b", { y: 50, duration: 0.5 })
  .to(".c", { opacity: 0, duration: 0.3 });
```

默认情况下，tween 会**依次追加**（appended）。使用 **position 参数**（position parameter）将 tween 放置在特定时间点或相对于其他 tween 的位置。

## Position 参数

第三个参数（或 vars 中的 position 属性）控制放置方式：

- **Absolute（绝对）**：`1` — 在第 1 秒开始。
- **Relative（相对，默认）**：`"+=0.5"` — 在上一个结束后 0.5s；`"-=0.2"` — 在上一个结束前 0.2s。
- **Label（标签）**：`"labelName"` — 在该标签处；`"labelName+=0.3"` — 标签后 0.3s。
- **Placement（相对最近添加的动画）**：`"<"` — 与最近添加的动画同时开始；`">"` — 在最近添加的动画结束时开始（默认）；`"<0.2"` — 在最近添加的动画开始后 0.2s。

示例：

```javascript
tl.to(".a", { x: 100 }, 0);           // at 0
tl.to(".b", { y: 50 }, "+=0.5");      // 0.5s after last end
tl.to(".c", { opacity: 0 }, "<");     // same start as previous
tl.to(".d", { scale: 2 }, "<0.2");    // 0.2s after previous start
```

## 时间轴默认值

向时间轴传入 defaults，使所有子 tween 继承：

```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });
tl.to(".a", { x: 100 }).to(".b", { y: 50 }); // both use 0.5s and power2.out
```

## 时间轴选项（构造函数）

- **paused: true** — 创建时为暂停状态；调用 `.play()` 开始播放。
- **repeat**、**yoyo** — 与 tween 相同；作用于整个时间轴。
- **onComplete**、**onStart**、**onUpdate** — 时间轴级回调。
- **defaults** — 合并到每个子 tween 的 vars。

## 标签

添加并使用标签，使序列更易读、易维护：

```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");
tl.addLabel("outro", "+=0.5");
tl.to(".b", { opacity: 0 }, "outro");
tl.play("outro");  // start from "outro"
tl.tweenFromTo("intro", "outro"); // pauses the timeline and returns a new Tween that animates the timeline's playhead from intro to outro with no ease.
```

## 嵌套时间轴

时间轴可以包含其他时间轴。

```javascript
const master = gsap.timeline();
const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });
master.add(child, 0);
master.to(".c", { opacity: 0 }, "+=0.2");
```

## 控制播放

- **tl.play()** / **tl.pause()**
- **tl.reverse()** / **tl.progress(1)** 然后 **tl.reverse()**
- **tl.restart()** — 从头开始。
- **tl.time(2)** — 定位到第 2 秒。
- **tl.progress(0.5)** — 定位到 50%。
- **tl.kill()** — 终止时间轴并（默认）终止其子动画。

## 官方 GSAP 最佳实践

- ✅ 编排序列时优先使用时间轴
- ✅ 使用 **position 参数**（第三个参数）将 tween 放在特定时间或相对标签的位置。
- ✅ 用 `addLabel()` 添加 **标签**，使序列更易读、易维护。
- ✅ 在时间轴构造函数中传入 **defaults**，让子 tween 继承 duration、ease 等。
- ✅ 将 ScrollTrigger 放在时间轴（或顶层 tween）上，而不是时间轴内部的 tween 上。

## 避免

- ❌ 能用 **时间轴** 编排时不要用 **delay** 链式串联动画；多步动画请用 `gsap.timeline()` 与 position 参数。
- ❌ 多个子 tween 共用 duration 或 ease 时，别忘了传入 **defaults**（例如 `defaults: { duration: 0.5, ease: "power2.out" }`）。
- ❌ 别忘了时间轴构造函数上的 **duration** 与 tween 的 duration 不是同一概念；时间轴的「duration」由其子动画决定。
- ❌ 不要嵌套内含 ScrollTrigger 的动画；ScrollTrigger 只应放在顶层 Tween/时间轴上。
