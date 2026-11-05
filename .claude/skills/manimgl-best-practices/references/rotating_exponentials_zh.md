# 旋转指数 - 参考指南

**示例文件**：`examples/rotating_exponentials.py`

## 用户查询场景

本示例适用于如下类型的查询：
- "Visualize e^(it) on the complex plane"
- "Show Euler's formula animation"
- "Demonstrate how cosine comes from rotating exponentials"
- "Create a complex plane with rotating vector"
- "Show e^(iπ) = -1 visually"

## 场景构思过程（3b1b 风格）

### 1. 核心概念
**欧拉公式（Euler's Formula）**：`e^(it) = cos(t) + i·sin(t)` —— 复平面上一个旋转的单位向量。两个反向旋转的指数相加可得到实部余弦。

### 2. 视觉设计决策

**为何使用 ComplexPlane？**
- 复数的自然坐标系
- 内置网格与标签
- `n2p()` 方法将复数转换为点

**为何展示轨迹路径？**
- 揭示单位圆如何自然出现
- 展示角度与位置之间的关系

### 3. 技术实现

#### 带 TracedPath 的旋转向量
```python
time_tracker = ValueTracker(0)

vector = Vector(RIGHT, color=YELLOW)
vector.add_updater(lambda v: v.put_start_and_end_on(
    ORIGIN,
    plane.n2p(np.exp(1j * time_tracker.get_value()))
))

tip_dot = Dot(color=YELLOW)
tip_dot.add_updater(lambda d: d.move_to(vector.get_end()))

traced = TracedPath(tip_dot.get_center, stroke_color=BLUE)
```

#### 反向旋转以得到余弦
```python
# e^(it) rotates counter-clockwise
v1.add_updater(lambda v: v.put_start_and_end_on(
    ORIGIN, plane.n2p(np.exp(1j * t))
))
# e^(-it) rotates clockwise
v2.add_updater(lambda v: v.put_start_and_end_on(
    ORIGIN, plane.n2p(np.exp(-1j * t))
))
# Sum is always real: 2cos(t)
```

### 4. 场景变体

| 场景 | 用途 |
|-------|---------|
| `RotatingExponential` | 基础 e^(it) 可视化 |
| `CounterRotatingExponentials` | 展示 e^(it) + e^(-it) = 2cos(t) |
| `EulersFormula` | 经典的 e^(iπ) = -1 |
| `ComplexExponentialSpiral` | 衰减螺旋 e^((a+bi)t) |

## 关键模式

### 模式：用 always_redraw 绘制圆弧
```python
angle_arc = always_redraw(lambda: Arc(
    start_angle=0,
    angle=time_tracker.get_value() % TAU,
    radius=0.3,
    color=GREEN
))
```

### 模式：复数转点
```python
# Using ComplexPlane.n2p() (number to point)
point = plane.n2p(1 + 2j)  # Complex number
point = plane.n2p(np.exp(1j * theta))  # Euler form
```

## 运行命令

```bash
manimgl rotating_exponentials.py RotatingExponential -w
manimgl rotating_exponentials.py CounterRotatingExponentials -w
manimgl rotating_exponentials.py EulersFormula -w
manimgl rotating_exponentials.py ComplexExponentialSpiral -w
```
