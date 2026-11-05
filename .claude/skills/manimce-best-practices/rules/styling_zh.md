---
name: styling
description: mobject 的填充、描边、透明度与视觉样式
metadata:
  tags: fill, stroke, opacity, style, width, appearance
---

# Mobject 样式

通过填充、描边和透明度等设置控制 mobject 的视觉外观。

## 填充属性

填充控制形状的内部区域。

```python
from manim import *

class FillExample(Scene):
    def construct(self):
        # Set fill on creation
        circle = Circle(fill_color=BLUE, fill_opacity=0.8)

        # Set fill after creation
        square = Square()
        square.set_fill(RED, opacity=0.5)

        self.add(circle, square)
```

### 填充方法
```python
mobject.set_fill(color=RED)                    # Color only
mobject.set_fill(RED, opacity=0.5)             # Color and opacity
mobject.set_fill(opacity=0.5)                  # Opacity only
mobject.set_fill_color(RED)                    # Color only (alternative)
mobject.set_fill_opacity(0.5)                  # Opacity only (alternative)
```

## 描边属性

描边控制形状的轮廓/边框。

```python
class StrokeExample(Scene):
    def construct(self):
        # Set stroke on creation
        circle = Circle(stroke_color=BLUE, stroke_width=4)

        # Set stroke after creation
        square = Square()
        square.set_stroke(RED, width=8)

        self.add(circle, square)
```

### 描边方法
```python
mobject.set_stroke(color=RED)                  # Color only
mobject.set_stroke(RED, width=4)               # Color and width
mobject.set_stroke(width=4)                    # Width only
mobject.set_stroke(opacity=0.5)                # Opacity only
mobject.set_stroke_color(RED)                  # Color only (alternative)
mobject.set_stroke_width(4)                    # Width only (alternative)
mobject.set_stroke_opacity(0.5)                # Opacity only (alternative)
```

### 描边宽度参考
```python
# Common stroke widths
DEFAULT_STROKE_WIDTH = 4
thin = 1
normal = 4
thick = 8
very_thick = 12
```

## 组合样式

```python
class CombinedStyling(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE, opacity=0.5)
        square.set_stroke(YELLOW, width=6)
        self.add(square)
```

### 方法链式调用
```python
square = Square().set_fill(RED, 0.5).set_stroke(WHITE, 4)
```

## set_style 方法

一次性设置多项样式属性：

```python
square = Square()
square.set_style(
    fill_color=BLUE,
    fill_opacity=0.5,
    stroke_color=WHITE,
    stroke_width=4,
    stroke_opacity=1
)
```

## 透明度

控制 mobject 的透明程度：

```python
# Overall opacity
mobject.set_opacity(0.5)  # Affects both fill and stroke

# Separate opacities
mobject.set_fill_opacity(0.8)
mobject.set_stroke_opacity(0.3)

# Fade effect
mobject.fade(0.5)  # 0.5 = 50% faded (opposite of opacity)
```

## 背景矩形

在文字或其他 mobject 后方添加背景：

```python
class BackgroundExample(Scene):
    def construct(self):
        text = Text("Important!")
        bg = BackgroundRectangle(text, fill_opacity=0.8, buff=0.1)
        group = VGroup(bg, text)
        self.add(group)
```

## 对子 mobject 应用样式

```python
# Apply to all submobjects (family=True, default)
group.set_fill(RED, opacity=0.5, family=True)

# Apply only to parent, not submobjects
group.set_fill(RED, opacity=0.5, family=False)
```

## 基于位置的样式

```python
class GradientFill(Scene):
    def construct(self):
        squares = VGroup(*[Square() for _ in range(5)]).arrange(RIGHT)

        for i, sq in enumerate(squares):
            opacity = (i + 1) / 5
            sq.set_fill(BLUE, opacity=opacity)

        self.add(squares)
```

## 复制样式

```python
# Copy style from another mobject
source = Circle().set_fill(RED, 0.5).set_stroke(WHITE, 4)
target = Square()
target.match_style(source)  # Now has same fill and stroke
```

## 最佳实践

1. **形状使用 fill_opacity** — 完全不透明的填充可能遮挡其他元素
2. **描边宽度保持一致** — 选定一种宽度并贯穿使用
3. **填充与描边形成对比** — 不同颜色有助于轮廓清晰
4. **用 BackgroundRectangle 提升可读性** — 在复杂背景上的文字后方使用
5. **链式调用使代码更简洁** — 过长时可换行拆分
