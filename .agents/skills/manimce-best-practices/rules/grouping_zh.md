---
name: grouping
description: VGroup、Group、arrange 及布局模式
metadata:
  tags: vgroup, group, arrange, layout, grid, submobjects
---

# 分组 Mobject

将多个 mobject 组织成组，以便统一操作。

## VGroup

VGroup（Vectorized Group，矢量化组）用于分组 VMobject，最为常用。

```python
from manim import *

class VGroupExample(Scene):
    def construct(self):
        # Create a group
        group = VGroup(
            Circle(),
            Square(),
            Triangle()
        )

        # Operations apply to all members
        group.set_color(RED)
        group.shift(UP)

        self.add(group)
```

## Group

Group 用于混合不同类型的 mobject（VMobject、ImageMobject 等）。

```python
class GroupExample(Scene):
    def construct(self):
        # Mix different types
        text = Text("Hello")
        group = Group(
            Circle(),
            text
        )
        self.add(group)
```

## 创建组

```python
# From individual mobjects
group = VGroup(circle, square, triangle)

# From a list
shapes = [Circle(), Square(), Triangle()]
group = VGroup(*shapes)

# Using list comprehension
group = VGroup(*[Circle() for _ in range(5)])

# Empty group, add later
group = VGroup()
group.add(Circle())
group.add(Square())
```

## arrange

将 mobject 排成一行。

```python
class ArrangeExample(Scene):
    def construct(self):
        # Horizontal arrangement (default)
        row = VGroup(*[Circle().scale(0.3) for _ in range(5)])
        row.arrange(RIGHT, buff=0.5).shift(UP * 2)

        # Vertical arrangement
        column = VGroup(*[Square().scale(0.3) for _ in range(4)])
        column.arrange(DOWN, buff=0.5).shift(LEFT * 2)

        # With custom buffer
        spaced = VGroup(*[Triangle().scale(0.3) for _ in range(3)])
        spaced.arrange(RIGHT, buff=1).shift(DOWN * 2)

        self.add(row, column, spaced)
```

### 方向选项
```python
group.arrange(RIGHT)      # Left to right
group.arrange(LEFT)       # Right to left
group.arrange(UP)         # Bottom to top
group.arrange(DOWN)       # Top to bottom
```

## arrange_in_grid

按网格排列。

```python
class GridExample(Scene):
    def construct(self):
        # Auto grid
        grid = VGroup(*[Square().scale(0.3) for _ in range(20)])
        grid.arrange_in_grid()

        # Specify rows and columns
        grid = VGroup(*[Circle().scale(0.2) for _ in range(12)])
        grid.arrange_in_grid(rows=3, cols=4)

        # With spacing
        grid.arrange_in_grid(rows=3, cols=4, buff=0.5)

        self.add(grid)
```

## 访问组成员

```python
group = VGroup(Circle(), Square(), Triangle())

# By index
first = group[0]          # Circle
second = group[1]         # Square
last = group[-1]          # Triangle

# Slicing
first_two = group[0:2]    # VGroup with Circle and Square

# Iteration
for mob in group:
    mob.set_color(random_color())

# Length
num_items = len(group)
```

## 修改组

```python
group = VGroup(Circle(), Square())

# Add mobjects
group.add(Triangle())
group.add(Star(), Pentagon())

# Remove mobjects
group.remove(circle)

# Insert at position
group.insert(0, new_mobject)

# Submobjects list
group.submobjects  # List of all children
```

## 组变换

```python
group = VGroup(Circle(), Square(), Triangle()).arrange(RIGHT)

# All transformations apply to entire group
group.shift(UP * 2)
group.scale(0.5)
group.rotate(PI / 4)
group.set_color(BLUE)

# But can target individuals
group[0].set_color(RED)  # Just the circle
```

## 嵌套组

```python
class NestedGroups(Scene):
    def construct(self):
        # Create sub-groups
        row1 = VGroup(*[Circle() for _ in range(3)]).arrange(RIGHT)
        row2 = VGroup(*[Square() for _ in range(3)]).arrange(RIGHT)
        row3 = VGroup(*[Triangle() for _ in range(3)]).arrange(RIGHT)

        # Group of groups
        all_rows = VGroup(row1, row2, row3).arrange(DOWN)

        self.add(all_rows)
```

## 常用组方法

```python
group = VGroup(Circle(), Square(), Triangle())

# Get bounding box info
group.get_center()
group.get_width()
group.get_height()

# Set position for whole group
group.move_to(ORIGIN)
group.to_edge(LEFT)

# Copy entire group
group_copy = group.copy()

# Match layout of another group
group1.match_height(group2)
group1.match_width(group2)
```

## 最佳实践

1. **VMobject 使用 VGroup** — 性能与兼容性更好
2. **创建后再 arrange** — 不要先逐个定位再成组
3. **组名要有语义** — 用 `equation_parts`，不要用 `group1`
4. **用嵌套组表达结构** — 例如列中的行等
5. **需要时复制组** — 避免意外修改原组
