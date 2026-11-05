---
name: lottie-bodymovin
description: 在 After Effects 导出 Lottie 动画时，用于实现迪士尼 12 条动画原则
---

# Lottie 动画原则

使用 Lottie（Bodymovin）实现全部 12 条迪士尼动画原则，用于矢量动画。

## 1. 挤压与拉伸（Squash and Stretch）

在导出前的 After Effects 中：
- 让 Scale X 与 Scale Y 反向动画
- 使用表达式：`s = transform.scale[1]; [100 + (100-s), s]`

```javascript
// Control at runtime
lottie.setSpeed(1.5); // affect squash timing
```

## 2. 预备动作（Anticipation）

组织 AE 合成结构：
1. **第 0–10 帧**：蓄力姿势
2. **第 10–40 帧**：主要动作
3. **第 40–50 帧**：落定

```javascript
// Play anticipation segment
anim.playSegments([0, 10], true);
setTimeout(() => anim.playSegments([10, 50], true), 200);
```

## 3. 演出布局（Staging）

```javascript
// Layer multiple Lotties
<div className="scene">
  <Lottie animationData={background} style={{ opacity: 0.6 }} />
  <Lottie animationData={hero} style={{ zIndex: 10 }} />
</div>
```

## 4. 连续动作 / 姿势到姿势（Straight Ahead / Pose to Pose）

在 AE 中采用姿势到姿势：
- 在关键姿势处打关键帧
- 让 AE 在关键帧之间插值
- 使用 Easy Ease 平滑过渡

```javascript
// Jump to specific poses
anim.goToAndStop(25, true); // frame 25
```

## 5. 跟随与重叠动作（Follow Through and Overlapping Action）

在 After Effects 中：
- 子图层关键帧错开 2–4 帧
- 使用父子关系配合延迟表达式
- `thisComp.layer("Parent").transform.position.valueAtTime(time - 0.05)`

## 6. 缓入缓出（Slow In and Slow Out）

AE 关键帧设置：
- 选中关键帧 > Easy Ease（F9）
- 用 Graph Editor 调整曲线
- 贝塞尔手柄控制加减速

```javascript
// Adjust playback speed dynamically
anim.setSpeed(0.5); // slower
anim.setSpeed(2); // faster
```

## 7. 弧线运动（Arc）

在 After Effects 中：
- 使用运动路径（position 属性）
- 将关键帧转为 Bezier
- 拖动手柄形成弧线
- 或使用「Auto-Orient to Path」

## 8. 次要动作（Secondary Action）

```javascript
// Trigger secondary animation
mainAnim.addEventListener('complete', () => {
  secondaryAnim.play();
});

// Or sync with frame
mainAnim.addEventListener('enterFrame', (e) => {
  if (e.currentTime > 15) particleAnim.play();
});
```

## 9. 时间节奏（Timing）

```javascript
anim.setSpeed(0.5);  // half speed - dramatic
anim.setSpeed(1);    // normal
anim.setSpeed(2);    // double speed - snappy

// Or control frame rate in AE export
// 24fps = cinematic, 30fps = smooth, 60fps = fluid
```

## 10. 夸张（Exaggeration）

在 After Effects 中：
- 将 scale 推到 100% 以上（120–150%）
- 旋转过冲
- 使用 Overshoot 表达式
- `amp = 15; freq = 3; decay = 5; n = 0; time_start = key(1).time; if (time > time_start) { n = (time - time_start) / thisComp.frameDuration; amp * Math.sin(freq*n) / Math.exp(decay*n/100); } else { 0; }`

## 11. 立体造型（Solid Drawing）

在 After Effects 中：
- 使用 3D 图层
- 应用透视摄像机
- 动画 Z 轴位置与旋转
- 使用景深

## 12. 吸引力（Appeal）

在 AE 中的设计原则：
- 平滑曲线优于尖角
- 一致的时间节奏模式
- 悦目的配色
- 干净的矢量形状

```javascript
// React Lottie with hover
<Lottie
  animationData={data}
  onMouseEnter={() => anim.setDirection(1)}
  onMouseLeave={() => anim.setDirection(-1)}
/>
```

## Lottie 实现

```javascript
import Lottie from 'lottie-react';
import animationData from './animation.json';

<Lottie
  animationData={animationData}
  loop={true}
  autoplay={true}
  style={{ width: 200, height: 200 }}
/>
```

## Lottie 关键能力

- `playSegments([start, end])` - 播放指定帧区间
- `setSpeed(n)` - 控制时间节奏
- `setDirection(1/-1)` - 正向/反向
- `goToAndStop(frame)` - 姿势控制
- `addEventListener` - 帧事件
- 通过 `lottie-interactivity` 实现交互
