---
name: shapes
description: 圆形、正方形、矩形、多边形及几何图元
metadata:
  tags: shapes, circle, square, rectangle, polygon, geometry
---

# 几何图形

Manim 中的基本几何图元。

## 圆形（Circle）

```python
from manim import *

class CircleExample(Scene):
    def construct(self):
        # Default circle
        c1 = Circle()

        # With parameters
        c2 = Circle(
            radius=2,
            color=BLUE,
            fill_opacity=0.5,
            stroke_width=4
        )

        self.add(c1, c2)
```

### 圆形方法

```python
circle = Circle()

# Get properties
circle.get_radius()
circle.get_center()

# Create from points
Circle.from_three_points(p1, p2, p3)

# Surround another mobject
triangle = Triangle()
circle = Circle().surround(triangle)  # Circle wraps around triangle
circle = Circle().surround(triangle, buffer_factor=1.5)  # With padding
circle = Circle().surround(triangle, stretch=True)  # Stretch to fit
```

## 椭圆（Ellipse）

```python
class EllipseExample(Scene):
    def construct(self):
        ellipse = Ellipse(
            width=4,
            height=2,
            color=GREEN
        )
        self.add(ellipse)
```

## 正方形（Square）

```python
class SquareExample(Scene):
    def construct(self):
        # Default square
        s1 = Square()

        # With parameters
        s2 = Square(
            side_length=2,
            color=RED,
            fill_opacity=0.8
        )

        self.add(s1, s2)
```

## 矩形（Rectangle）

```python
class RectangleExample(Scene):
    def construct(self):
        rect = Rectangle(
            width=4,
            height=2,
            color=YELLOW,
            fill_opacity=0.5
        )
        self.add(rect)
```

### 圆角矩形（RoundedRectangle）

```python
class RoundedRectExample(Scene):
    def construct(self):
        rounded = RoundedRectangle(
            width=4,
            height=2,
            corner_radius=0.5,
            color=BLUE,
            fill_opacity=0.8
        )
        self.add(rounded)
```

## 三角形（Triangle）

```python
class TriangleExample(Scene):
    def construct(self):
        # Equilateral triangle
        tri = Triangle(color=PURPLE)

        # Custom triangle (using Polygon)
        custom_tri = Polygon(
            ORIGIN, RIGHT * 2, UP * 3,
            color=GREEN
        )

        self.add(tri, custom_tri.shift(RIGHT * 3))
```

## 多边形（Polygon）

由顶点定义任意多边形。

```python
class PolygonExample(Scene):
    def construct(self):
        # Pentagon
        pentagon = RegularPolygon(n=5, color=ORANGE)

        # Hexagon
        hexagon = RegularPolygon(n=6, color=TEAL)

        # Custom polygon
        custom = Polygon(
            [-2, -1, 0],
            [2, -1, 0],
            [2, 1, 0],
            [0, 2, 0],
            [-2, 1, 0],
            color=PINK
        )

        VGroup(pentagon, hexagon, custom).arrange(RIGHT, buff=1)
        self.add(pentagon, hexagon, custom)
```

## 正多边形（RegularPolygon）

```python
class RegularPolygonExamples(Scene):
    def construct(self):
        shapes = VGroup(
            RegularPolygon(n=3),   # Triangle
            RegularPolygon(n=4),   # Square
            RegularPolygon(n=5),   # Pentagon
            RegularPolygon(n=6),   # Hexagon
            RegularPolygon(n=8),   # Octagon
        ).arrange(RIGHT)
        self.add(shapes)
```

## 星形（Star）

```python
class StarExample(Scene):
    def construct(self):
        star = Star(
            n=5,                    # Number of points
            outer_radius=2,
            inner_radius=1,         # Optional: auto-calculated if not specified
            density=2,              # How vertices connect (affects shape)
            color=YELLOW,
            fill_opacity=1
        )
        self.add(star)

        # Different densities create different star patterns
        star_d2 = Star(7, outer_radius=2, density=2, color=RED)
        star_d3 = Star(7, outer_radius=2, density=3, color=PURPLE)
```

## 正多角星（RegularPolygram）

顶点按密度连接的星形类图形。

```python
class PolygramExample(Scene):
    def construct(self):
        # Pentagram (5-pointed star pattern)
        pentagram = RegularPolygram(5, radius=2)
        self.add(pentagram)
```

## 圆环（Annulus）

```python
class AnnulusExample(Scene):
    def construct(self):
        ring = Annulus(
            inner_radius=1,
            outer_radius=2,
            color=BLUE,
            fill_opacity=0.5
        )
        self.add(ring)
```

## 扇形与圆弧（Sector and Arc）

```python
class SectorArcExample(Scene):
    def construct(self):
        # Sector (pie slice)
        sector = Sector(
            radius=2,
            angle=PI/2,
            start_angle=0,
            color=RED,
            fill_opacity=0.8
        ).shift(LEFT * 2)

        # Arc (just the curve)
        arc = Arc(
            radius=2,
            angle=PI/2,
            start_angle=PI,
            color=BLUE
        ).shift(RIGHT * 2)

        self.add(sector, arc)
```

## 两点间圆弧（ArcBetweenPoints）

```python
class ArcBetweenPointsExample(Scene):
    def construct(self):
        arc = ArcBetweenPoints(
            start=LEFT * 2,
            end=RIGHT * 2,
            angle=PI/2,  # Curvature
            color=GREEN
        )
        self.add(arc)
```

## 点（Dot）

```python
class DotExample(Scene):
    def construct(self):
        # Default dot
        d1 = Dot()

        # Customized
        d2 = Dot(
            point=RIGHT * 2,
            radius=0.2,
            color=YELLOW
        )

        self.add(d1, d2)
```

## 常用图形操作

```python
shape = Square()

# Transform
shape.scale(2)
shape.rotate(PI/4)
shape.stretch(2, dim=0)  # Stretch horizontally

# Style
shape.set_fill(RED, opacity=0.5)
shape.set_stroke(WHITE, width=4)

# Position
shape.move_to(ORIGIN)
shape.shift(UP * 2)
shape.next_to(other, RIGHT)
```

## 最佳实践

1. **正多边形用 RegularPolygon** — 比手动构造 Polygon 更精确
2. **设置 fill_opacity 以保证可见** — 默认常为 0（透明）
3. **用 Dot 表示点** — 优于用小半径的 Circle
4. **UI 元素用 RoundedRectangle** — 外观更精致
5. **用 VGroup 组合图形** — 构建复杂图形
