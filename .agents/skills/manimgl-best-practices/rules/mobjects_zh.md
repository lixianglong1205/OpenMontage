# ManimGL Mobject

## Mobject 层级

```
Mobject (base class)
├── VMobject (vectorized - most common)
│   ├── VGroup
│   ├── Circle, Square, Rectangle, Line, Arrow
│   ├── Tex, Text, TexText
│   └── Axes, NumberPlane
├── Group (non-vectorized container)
├── ImageMobject
├── Point
└── 3D objects (Surface, ParametricSurface, etc.)
```

## 创建 Mobject

```python
# Geometric shapes
circle = Circle(radius=1, color=BLUE)
square = Square(side_length=2)
rect = Rectangle(width=3, height=2)
line = Line(LEFT, RIGHT)
arrow = Arrow(ORIGIN, UP)

# Text
text = Text("Hello")
math = Tex(R"\pi r^2")

# Groups
group = VGroup(circle, square)
```

## 定位

```python
# Absolute position
circle.move_to(ORIGIN)
circle.move_to(RIGHT * 2 + UP)

# Relative to screen edges
circle.to_edge(UP)
circle.to_edge(LEFT, buff=1)
circle.to_corner(UL)

# Relative to other mobjects
square.next_to(circle, RIGHT)
square.next_to(circle, DOWN, buff=0.5)

# Alignment
group.align_to(other, UP)
group.align_to(other, LEFT)

# Shifting
circle.shift(RIGHT * 2)
circle.shift(UP + RIGHT)
```

## 样式

```python
# Fill
circle.set_fill(BLUE, opacity=0.5)

# Stroke (outline)
circle.set_stroke(WHITE, width=2)
circle.set_stroke(color=RED, width=4, opacity=0.8)

# Both
circle.set_style(
    fill_color=BLUE,
    fill_opacity=0.5,
    stroke_color=WHITE,
    stroke_width=2
)

# Color (affects both fill and stroke)
circle.set_color(RED)

# Backstroke (outline behind for readability)
text.set_backstroke(BLACK, 5)
```

## VGroup

用于容纳向量化 mobject 的容器：

```python
# Create group
shapes = VGroup(circle, square, triangle)

# Arrange
shapes.arrange(RIGHT, buff=0.5)
shapes.arrange(DOWN, aligned_edge=LEFT)
shapes.arrange_in_grid(rows=2, cols=3)

# Apply to all
shapes.set_color(BLUE)
shapes.scale(0.5)
shapes.shift(UP)

# Access elements
shapes[0]  # First element
shapes[-1]  # Last element
shapes[1:3]  # Slice
```

## Group 与 VGroup

```python
# VGroup - for vectorized mobjects (VMobject subclasses)
vgroup = VGroup(Circle(), Square())

# Group - for any mobjects including images, 3D, etc.
group = Group(ImageMobject("photo.png"), Circle())
```

## 常用方法

| 方法 | 说明 |
|--------|-------------|
| `.move_to(point)` | 将中心移动到指定点 |
| `.shift(vector)` | 按向量平移 |
| `.scale(factor)` | 按因子缩放 |
| `.rotate(angle)` | 按角度旋转（弧度） |
| `.next_to(mob, dir)` | 置于另一 mobject 旁边 |
| `.align_to(mob, dir)` | 与另一 mobject 对齐边缘 |
| `.to_edge(dir)` | 移到屏幕边缘 |
| `.to_corner(corner)` | 移到屏幕角落 |
| `.get_center()` | 获取中心点 |
| `.get_width()` | 获取宽度 |
| `.get_height()` | 获取高度 |
| `.copy()` | 创建副本 |

## 生成 Target

用于动画过渡到修改后的版本：

```python
circle.generate_target()
circle.target.shift(RIGHT * 2)
circle.target.scale(2)
circle.target.set_color(RED)

self.play(MoveToTarget(circle))
```

## 保存与恢复状态

```python
circle.save_state()
self.play(circle.animate.shift(RIGHT).scale(2))
# Later...
self.play(Restore(circle))
```

## Updater

动态行为：

```python
# Always follow another mobject
label.add_updater(lambda m: m.next_to(dot, UP))

# Time-based
circle.add_updater(lambda m, dt: m.rotate(dt))

# Value-based with ValueTracker
tracker = ValueTracker(0)
circle.add_updater(
    lambda m: m.set_fill(opacity=tracker.get_value())
)
self.play(tracker.animate.set_value(1))
```

## 实用快捷方式

```python
# f_always for common updater patterns
label.f_always.next_to(dot, UP)

# always (function form)
always(label.next_to, dot, UP)
```
