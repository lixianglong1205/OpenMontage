---
name: axes
description: Manim 中的 Axes、NumberPlane 与坐标系
metadata:
  tags: axes, numberplane, coordinate, grid, numberline
---

# 坐标系

创建用于数学可视化的坐标轴、网格与数轴。

## Axes

基础二维坐标轴。

```python
from manim import *

class AxesExample(Scene):
    def construct(self):
        # Default axes
        axes = Axes()
        self.add(axes)
```

### 自定义 Axes

```python
class CustomAxes(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-5, 5, 1],      # [min, max, step]
            y_range=[-3, 3, 1],
            x_length=10,              # Physical length on screen
            y_length=6,
            axis_config={
                "color": BLUE,
                "include_tip": True,
                "include_numbers": True,
            },
            x_axis_config={
                "numbers_to_include": [-4, -2, 0, 2, 4],
            },
            y_axis_config={
                "numbers_to_include": [-2, 0, 2],
            },
        )
        self.add(axes)
```

### 添加标签

```python
class AxesLabels(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 3])

        # Add axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        # Custom labels
        x_label = axes.get_x_axis_label(MathTex(r"\theta"))
        y_label = axes.get_y_axis_label(MathTex(r"f(\theta)"))

        self.add(axes, x_label, y_label)
```

## NumberPlane

带坐标轴的网格——显示坐标线。

```python
class NumberPlaneExample(Scene):
    def construct(self):
        # Default plane
        plane = NumberPlane()
        self.add(plane)
```

### 自定义 NumberPlane

```python
class CustomPlane(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={
                "color": WHITE,
            },
        )
        self.add(plane)
```

## ComplexPlane

用于可视化复数。

```python
class ComplexPlaneExample(Scene):
    def construct(self):
        plane = ComplexPlane()

        # Plot complex number
        z = complex(2, 1)  # 2 + i
        dot = Dot(plane.n2p(z), color=YELLOW)
        label = MathTex("2+i").next_to(dot, UR)

        self.add(plane, dot, label)
```

## NumberLine

单条数轴。

```python
class NumberLineExample(Scene):
    def construct(self):
        line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
            include_tip=True,
        )
        self.add(line)
```

## 坐标转换

```python
class CoordinateConversion(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 3])

        # Convert coordinates to screen position
        point = axes.c2p(2, 1)  # coords_to_point: (2, 1) -> screen position

        # Convert screen position to coordinates
        coords = axes.p2c(point)  # point_to_coords: screen -> (x, y)

        dot = Dot(point, color=RED)
        self.add(axes, dot)
```

### 简写方法

```python
axes = Axes()

# c2p = coords_to_point
axes.c2p(x, y)

# p2c = point_to_coords
axes.p2c(point)

# i2gp = input_to_graph_point (for graphs)
axes.i2gp(x, graph)

# For NumberPlane/ComplexPlane
plane.n2p(complex_number)  # number_to_point
plane.p2n(point)           # point_to_number
```

## ThreeDAxes

用于三维可视化。

```python
class ThreeDAxesExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            z_length=6,
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)
```

## 绘制点

```python
class PlotPoints(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 3])

        points = [(1, 2), (-2, 1), (3, -1), (0, 2)]
        dots = VGroup(*[
            Dot(axes.c2p(x, y), color=YELLOW)
            for x, y in points
        ])

        self.add(axes, dots)
```

## 最佳实践

1. **设置合适的范围**——不要包含不必要的空白区域
2. **使 x_length/y_length 与范围比例一致**——避免形变
3. **变换场景使用 NumberPlane**——网格能清晰展示形变
4. **所有坐标相关操作使用 c2p**——不要手动换算
5. **刻度数字宜少不宜多**——过多数字会使画面杂乱
