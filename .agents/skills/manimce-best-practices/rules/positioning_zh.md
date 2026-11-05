---
name: positioning
description: move_to、next_to、align_to、shift 及定位相关方法
metadata:
  tags: position, move_to, next_to, shift, align, layout
---

# Manim 中的定位

在场景中放置与移动 mobject 的方法。

## 坐标系

Manim 使用的坐标系约定如下：
- 原点 (0, 0, 0) 位于屏幕中心
- X 轴：左 (-) 到右 (+)
- Y 轴：下 (-) 到上 (+)
- Z 轴：内 (-) 到外 (+)（用于 3D）

### 方向常量
```python
UP = np.array([0, 1, 0])
DOWN = np.array([0, -1, 0])
LEFT = np.array([-1, 0, 0])
RIGHT = np.array([1, 0, 0])
ORIGIN = np.array([0, 0, 0])

# Diagonals
UL = UP + LEFT      # Upper left
UR = UP + RIGHT     # Upper right
DL = DOWN + LEFT    # Lower left
DR = DOWN + RIGHT   # Lower right
```

## move_to

移动到绝对位置。

```python
from manim import *

class MoveToExample(Scene):
    def construct(self):
        circle = Circle()

        # Move to origin
        circle.move_to(ORIGIN)

        # Move to specific coordinates
        circle.move_to(RIGHT * 2 + UP * 1)

        # Move to another mobject's position
        square = Square().shift(LEFT * 2)
        circle.move_to(square)

        # Move to a specific point of another mobject
        circle.move_to(square.get_top())
```

## shift

相对于当前位置移动。

```python
class ShiftExample(Scene):
    def construct(self):
        circle = Circle()

        # Shift in one direction
        circle.shift(RIGHT)
        circle.shift(UP * 2)

        # Shift in multiple directions
        circle.shift(RIGHT * 2 + UP * 1)

        # Chain shifts
        circle.shift(LEFT).shift(DOWN)
```

## next_to

相对于另一个 mobject 定位。

```python
class NextToExample(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        triangle = Triangle()

        # Place circle to the right of square
        circle.next_to(square, RIGHT)

        # With buffer (spacing)
        triangle.next_to(square, DOWN, buff=0.5)

        # Aligned to specific edge
        circle.next_to(square, RIGHT, aligned_edge=UP)
```

### buff 参数
```python
# Default buffer
circle.next_to(square, RIGHT)  # Uses DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

# Custom buffer
circle.next_to(square, RIGHT, buff=0)    # No gap
circle.next_to(square, RIGHT, buff=1)    # 1 unit gap
circle.next_to(square, RIGHT, buff=0.5)  # Half unit gap
```

## align_to

与另一个 mobject 对齐边缘。

```python
class AlignToExample(Scene):
    def construct(self):
        square = Square().shift(LEFT)
        circle = Circle().shift(RIGHT)

        # Align circle's left edge with square's left edge
        circle.align_to(square, LEFT)

        # Align tops
        circle.align_to(square, UP)

        # Align to a point
        circle.align_to(ORIGIN, DOWN)
```

## 边缘方法

定位到屏幕边缘。

```python
class EdgeExample(Scene):
    def construct(self):
        # To screen edges
        text1 = Text("Top").to_edge(UP)
        text2 = Text("Bottom").to_edge(DOWN)
        text3 = Text("Left").to_edge(LEFT)
        text4 = Text("Right").to_edge(RIGHT)

        # With buffer
        text5 = Text("Buffered").to_edge(UP, buff=1)
```

## 角落方法

定位到屏幕角落。

```python
class CornerExample(Scene):
    def construct(self):
        t1 = Text("UL").to_corner(UL)
        t2 = Text("UR").to_corner(UR)
        t3 = Text("DL").to_corner(DL)
        t4 = Text("DR").to_corner(DR)

        # With buffer
        t5 = Text("Buffered").to_corner(UL, buff=0.5)
```

## center

在屏幕上居中，或相对另一个 mobject 居中。

```python
mobject.center()           # Center on screen
mobject.center_on(other)   # Center on another mobject (custom helper)
```

## 获取位置

```python
circle = Circle()

# Get various points
circle.get_center()        # Center point
circle.get_top()           # Top edge center
circle.get_bottom()        # Bottom edge center
circle.get_left()          # Left edge center
circle.get_right()         # Right edge center
circle.get_corner(UL)      # Upper left corner
circle.get_corner(DR)      # Lower right corner
circle.get_start()         # Start of path
circle.get_end()           # End of path
```

## 动画定位

```python
class AnimatedPosition(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # Animate movement
        self.play(square.animate.shift(RIGHT * 2))
        self.play(square.animate.move_to(UP * 2))
        self.play(square.animate.to_edge(LEFT))
```

## 最佳实践

1. **相对定位用 next_to** — 保持对象之间的相对关系
2. **绝对定位用 move_to** — 精确坐标
3. **微调用 shift** — 快速偏移
4. **屏幕布局用 to_edge/to_corner** — 响应式布局
5. **用 buff 调节视觉间距** — 避免元素挤在一起
