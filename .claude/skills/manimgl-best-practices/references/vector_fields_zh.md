# 向量场 - 参考指南

**示例文件**：`examples/vector_fields.py`

## 用户查询场景

本示例适用于如下类型的需求：
- “创建向量场可视化”
- “展示粒子在场中流动”
- “可视化电荷产生的电场”
- “动画演示梯度下降”
- “展示流体流动”

## 场景构思流程（3b1b 风格）

### 1. 核心概念
**向量场（Vector Fields）**：空间中每一点都有一个向量，表示方向与大小。粒子沿场运动，从而揭示流动模式。

### 2. 技术实现

#### 手动箭头场（可移植做法）
```python
arrows = VGroup()
for x in np.arange(-3.5, 4, 0.7):
    for y in np.arange(-2.5, 3, 0.7):
        vx, vy = -y * 0.15, x * 0.15  # Rotation field
        arrow = Arrow(
            start=[x, y, 0],
            end=[x + vx, y + vy, 0],
            buff=0,
            stroke_width=2,
        )
        # Color by magnitude
        mag = np.sqrt(vx**2 + vy**2)
        arrow.set_color(interpolate_color(BLUE, YELLOW, mag / 0.5))
        arrows.add(arrow)
```

#### 粒子沿场运动
```python
def follow_field(mob, dt):
    x, y = mob.get_center()[:2]
    vx, vy = field_func(x, y)
    mob.shift(np.array([vx, vy, 0]) * dt)

dot.add_updater(follow_field)
trail = TracedPath(dot.get_center, stroke_color=RED)
```

#### 电偶极子场
```python
def E_field(pos):
    r1, r2 = pos - q1_pos, pos - q2_pos
    d1, d2 = np.linalg.norm(r1), np.linalg.norm(r2)
    E1 = r1 / d1**3   # From + charge
    E2 = -r2 / d2**3  # From - charge
    return E1 + E2
```

### 3. 场景变体

| 场景 | 用途 |
|-------|---------|
| `SimpleVectorField` | 旋转场与单个粒子 |
| `GradientFieldDemo` | 标量场 + 梯度箭头 |
| `ParticleFlow` | 涡旋中的多个粒子 |
| `ElectricDipole` | 正负电荷产生的场 |

## 关键模式

### 模式：按大小着色
```python
mag = np.linalg.norm([vx, vy])
color = interpolate_color(BLUE, YELLOW, min(mag * scale, 1))
arrow.set_color(color)
```

### 模式：大量箭头使用 LaggedStartMap
```python
self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.02, run_time=2))
```

### 模式：循环中为 Updater 使用闭包
```python
for i in range(n):
    dot = Dot(...)
    def make_updater():  # Closure captures current state
        def update(mob, dt):
            # use mob, not dot
            ...
        return update
    dot.add_updater(make_updater())
```

## 运行命令

```bash
manimgl vector_fields.py SimpleVectorField -w
manimgl vector_fields.py GradientFieldDemo -w
manimgl vector_fields.py ParticleFlow -w
manimgl vector_fields.py ElectricDipole -w
```
