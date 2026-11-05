# 过境动画 - 参考指南

**示例文件**：`examples/transit_animation.py`

## 用户查询场景

本示例适用于如下类型的需求：
- 「创建行星过境动画」
- 「展示加载圆点动画」
- 「动画演示钟摆摆动」
- 「创建波传播效果」
- 「展示轨道运动」

## 场景思考过程（3b1b 风格）

### 1. 核心概念
**过境/周期运动（Transit/Periodic Motion）**：物体沿路径运动、留下轨迹、呈现周期性行为。常用于天文过境、加载指示器、物理演示等场景。

### 2. 技术实现

#### 带快照的过境
```python
venus.add_updater(lambda m, dt: m.shift(dt * velocity * RIGHT))
copies = VGroup()
for _ in range(n_snapshots):
    self.wait(wait_time)
    copies.add(venus.copy().clear_updaters())
self.play(Transform(copies, VGroup(path)))  # Collapse to line
```

#### 带景深效果的轨道运动
```python
def update_planet(p):
    a = angle.get_value()
    x = 2.5 * np.cos(a)
    y = 0.5 * np.sin(a)  # Compressed y = tilted orbit
    p.move_to([x, y, 0])
    # Size varies with "depth"
    scale = 0.12 + 0.06 * np.sin(a)
    p.set_width(2 * scale)
```

#### 相位偏移振荡（加载圆点）
```python
for i, dot in enumerate(dots):
    phase = i * TAU / n_dots
    dot.add_updater(lambda m, p=phase: m.set_y(
        original_y + 0.3 * np.sin(3 * time.get_value() + p)
    ))
```

#### 钟摆物理
```python
omega = np.sqrt(g / length)  # Natural frequency
amplitude = PI / 4
theta.add_updater(lambda m: m.set_value(
    amplitude * np.cos(omega * time.get_value()) * np.exp(-0.05 * time.get_value())
))
```

### 3. 场景变体

| 场景 | 用途 |
|-------|---------|
| `TransitOfVenus` | 历史天文过境 |
| `OrbitalTransit` | 带景深的系外行星式轨道 |
| `LoadingDots` | 经典加载动画 |
| `WaveTransit` | 波脉冲传播 |
| `PendulumSwing` | 带轨迹的阻尼钟摆 |

## 关键模式

### 模式：复制并冻结
```python
copy = mobject.copy().clear_updaters()  # Snapshot current state
```

### 模式：连续时间 Updater
```python
time = ValueTracker(0)
time.add_updater(lambda m, dt: m.increment_value(dt))
```

## 运行命令

```bash
manimgl transit_animation.py TransitOfVenus -w
manimgl transit_animation.py LoadingDots -w
manimgl transit_animation.py PendulumSwing -w
```
