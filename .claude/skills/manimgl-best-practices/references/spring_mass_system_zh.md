# 弹簧-质量系统 - 参考指南

**示例文件**：`examples/spring_mass_system.py`

## 用户查询场景

本示例适用于如下类型的需求：
- “创建一个带振荡的弹簧动画”
- “展示阻尼谐振动”
- “可视化弹簧上质量的物理仿真”
- “为弹簧-质量系统做动画并附带实时曲线图”
- “比较不同的阻尼系数”

## 场景构思过程（3b1b 风格）

### 1. 明确核心概念
**阻尼谐振动（Damped Harmonic Motion）**：质量块连在弹簧上发生振荡，因摩擦/阻尼而振幅随时间衰减。运动方程为：`x'' = -kx - μv`

### 2. 视觉设计决策

**为何用参数化螺旋线表示弹簧？**
- 三维线圈看起来更逼真
- 质量移动时弹簧能自然拉伸
- 使用 `ParametricCurve` 实现平滑渲染

**为何在数轴上跟踪位置？**
- 提供定量反馈
- 显示精确的位移数值
- 便于理解运动方向

### 3. 技术实现

#### 创建自包含的物理组件
```python
class SpringMassSystem(VGroup):
    def __init__(self, x0=0, v0=0, k=3, mu=0.1, ...):
        # Store physics state
        self.k = k
        self.mu = mu
        self.velocity = v0

        # Add physics updater
        self.add_updater(lambda m, dt: m.time_step(dt))
```

**要点**：将物理与视觉封装在同一 `VGroup` 子类中，便于复用并保持动画代码简洁。

#### 物理积分（欧拉法）
```python
def time_step(self, delta_t, dt_size=0.01):
    state = [self.get_x(), self.velocity]
    for _ in range(sub_steps):
        x, v = state
        acceleration = -self.k * x - self.mu * v
        state[0] += v * true_dt
        state[1] += acceleration * true_dt
```

#### 动态速度/力向量
```python
def get_velocity_vector(self, scale_factor=0.5, color=GREEN):
    vector = Vector(RIGHT, fill_color=color)
    vector.add_updater(lambda m: m.put_start_and_end_on(
        self.mass.get_center(),
        self.mass.get_center() + scale_factor * self.velocity * RIGHT
    ))
    return vector
```

### 4. 场景变体

| 场景 | 用途 |
|-------|---------|
| `SpringMassDemo` | 基础振荡，含速度/力向量 |
| `SpringWithGraph` | 使用 TracedPath 的实时 x(t) 曲线 |
| `MultipleSprings` | 比较不同阻尼值 |

## 关键模式示例

### 模式：可暂停的物理更新
```python
def pause(self):
    self._is_running = False

def unpause(self):
    self._is_running = True
```

### 模式：用 TracedPath 绘制曲线
```python
tracking_point = Point()
tracking_point.add_updater(lambda p: p.move_to(
    axes.c2p(time_tracker.get_value(), spring.get_x())
))
position_graph = TracedPath(tracking_point.get_center, stroke_color=BLUE)
```

## 运行命令

```bash
# Basic demo
manimgl spring_mass_system.py SpringMassDemo -w

# With real-time graph
manimgl spring_mass_system.py SpringWithGraph -w

# Compare damping
manimgl spring_mass_system.py MultipleSprings -w
```
