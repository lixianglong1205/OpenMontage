# 积分可视化 - 参考指南

**示例文件**：`examples/integration_visualization.py`

## 用户查询场景

本示例适用于如下类型的提问：
- 「展示曲线下的面积」
- 「可视化黎曼和（Riemann sums）收敛到积分」
- 「动画演示定积分的累积过程」
- 「展示 e^(-x) 的积分等于 1」

## 场景构思过程（3b1b 风格）

### 1. 核心概念
**定积分**：积分 ∫f(x)dx 表示曲线 f(x) 下方累积的面积。矩形越来越窄的黎曼和会收敛到真实的积分值。

### 2. 技术实现

#### 动画面积填充（使用 Polygon）
```python
def get_area_polygon():
    t = t_tracker.get_value()
    xs = np.linspace(0, t, 50)
    # Points along curve
    points = [axes.c2p(x, f(x)) for x in xs]
    # Close the polygon along x-axis
    points.append(axes.c2p(t, 0))
    points.append(axes.c2p(0, 0))
    poly = Polygon(*points)
    poly.set_fill(BLUE_E, opacity=0.5)
    poly.set_stroke(width=0)
    return poly

area = always_redraw(get_area_polygon)
```

**要点**：ManimGL 没有 `axes.get_area()`，需要手动用曲线上的点构建多边形。

#### 黎曼和矩形
```python
for i in range(n):
    x = start + i * dx
    height = f(x)
    rect = Rectangle(
        width=dx * axes.x_axis.get_unit_size(),
        height=height * axes.y_axis.get_unit_size(),
    )
    rect.move_to(axes.c2p(x + dx/2, height/2))
```

### 3. 场景变体

| 场景 | 用途 |
|-------|---------|
| `AreaUnderCurve` | 基础累积面积动画 |
| `RiemannSums` | 矩形收敛（n=4,8,16,32） |
| `ExponentialDecay` | ∫e^(-x)dx = 1，带实时面积计数 |

## 关键模式

### 模式：实时数值显示
```python
value_label = Tex(r"\text{Area} \approx 0.00")
value_num = value_label.make_number_changeable("0.00")
value_num.add_updater(lambda m: m.set_value(computed_area))
```

### 模式：逐步细化矩形
```python
for n in [4, 8, 16, 32]:
    new_rects = create_rectangles(n)
    self.play(ReplacementTransform(current_rects, new_rects))
    current_rects = new_rects
```

## 运行命令

```bash
manimgl integration_visualization.py AreaUnderCurve -w
manimgl integration_visualization.py RiemannSums -w
manimgl integration_visualization.py ExponentialDecay -w
```
