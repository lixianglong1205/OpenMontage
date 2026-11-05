---
name: mobjects
description: Manim 中的 Mobject 类型、VMobject 与 mobject 层级结构
metadata:
  tags: mobject, vmobject, group, submobjects, hierarchy
---

# Manim 中的 Mobjects

Mobject（Mathematical Object，数学对象）是 Manim 中所有可显示对象的基类。

## Mobject 层级结构

```
Mobject (base class)
├── VMobject (Vectorized Mobject - most common)
│   ├── Circle, Square, Rectangle, Polygon
│   ├── Line, Arrow, Vector
│   ├── Text, MathTex, Tex
│   ├── Axes, NumberPlane
│   └── VGroup
├── ImageMobject (for images)
├── PMobject (point clouds)
└── Group (for non-VMobject collections)
```

## VMobject（Vectorized Mobject，矢量化 Mobject）

你常用的大多数图形都是 VMobject——它们由 Bézier 曲线定义。

```python
# Common VMobjects
circle = Circle()
square = Square()
rect = Rectangle(width=4, height=2)
triangle = Triangle()
polygon = Polygon(ORIGIN, RIGHT, UP)
line = Line(LEFT, RIGHT)
arrow = Arrow(LEFT, RIGHT)
```

## 创建自定义 VMobject

```python
class CustomShape(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define points using set_points_as_corners or set_points_smoothly
        self.set_points_as_corners([
            LEFT, UP, RIGHT, DOWN, LEFT
        ])
```

## Mobject 属性

### 位置与尺寸

```python
mobject.get_center()      # Returns center point
mobject.get_width()       # Returns width
mobject.get_height()      # Returns height
mobject.get_top()         # Top edge center point
mobject.get_bottom()      # Bottom edge center point
mobject.get_left()        # Left edge center point
mobject.get_right()       # Right edge center point
```

### 包围盒角点

```python
mobject.get_corner(UL)    # Upper left corner
mobject.get_corner(UR)    # Upper right corner
mobject.get_corner(DL)    # Lower left corner
mobject.get_corner(DR)    # Lower right corner
```

## 子 Mobject（Submobjects）

Mobject 可以将其他 mobject 作为子 mobject 包含在内。

```python
# Access submobjects
group = VGroup(Circle(), Square())
group.submobjects      # List of child mobjects
group[0]               # First submobject (Circle)
group[1]               # Second submobject (Square)

# Iterate over submobjects
for mob in group:
    mob.set_color(RED)
```

## 复制 Mobject

```python
# Create a copy
circle_copy = circle.copy()

# Copy and position
circle_copy = circle.copy().shift(RIGHT * 2)
```

## 方法链式调用

大多数 mobject 方法返回 `self`，因此可以链式调用：

```python
circle = Circle().set_color(RED).shift(LEFT).scale(2)
```

## 最佳实践

1. **自定义形状时使用 VMobject**——渲染与动画支持更好
2. **优先使用 VGroup 而非 Group**——VGroup 与大多数动画配合更佳
3. **复用时使用 copy()**——避免意外修改原对象
4. **为可读性链式调用方法**——若链过长则拆成多行
