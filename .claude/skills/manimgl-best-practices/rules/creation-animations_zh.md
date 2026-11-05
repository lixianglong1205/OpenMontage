# ManimGL 中的创建动画

创建动画（Creation animations）让 mobject 从无到有地出现。ManimGL 提供了多种动画类，用于不同的创建效果。

## ShowCreation

**注意**：ManimGL 使用 `ShowCreation`，而不是 ManimCE 中使用的 `Create`。

### 基本用法

```python
from manimlib import *

class CreationExample(Scene):
    def construct(self):
        circle = Circle()

        # ShowCreation draws the object
        self.play(ShowCreation(circle))
        self.wait()
```

### 不同的 Mobject

```python
# Works with any VMobject
self.play(ShowCreation(Circle()))
self.play(ShowCreation(Square()))
self.play(ShowCreation(Line(LEFT, RIGHT)))
self.play(ShowCreation(Text("Hello")))
```

### 反向创建

```python
# Uncreate (reverse of ShowCreation)
circle = Circle()
self.add(circle)
self.play(ShowCreation(circle, reverse=True))  # Uncreates
```

## Write

`Write` 动画专门用于文本和 LaTeX。

### 书写文本

```python
# Write text letter by letter
text = Text("Hello World", font_size=60)
self.play(Write(text))

# Write LaTeX
formula = Tex(R"\int_0^1 x^2 dx = \frac{1}{3}")
self.play(Write(formula))
```

### 书写速度

```python
# Control writing speed with run_time
text = Text("Fast", font_size=72)
self.play(Write(text), run_time=0.5)

text2 = Text("Slow", font_size=72)
self.play(Write(text2), run_time=3)
```

## FadeIn

将对象淡入画面。

### 基本 FadeIn

```python
circle = Circle()
self.play(FadeIn(circle))
```

### 带位移的 FadeIn

```python
# Fade in while shifting
text = Text("Appearing", font_size=60)
self.play(FadeIn(text, shift=UP))

# From different directions
self.play(FadeIn(circle, shift=DOWN))
self.play(FadeIn(square, shift=LEFT))
self.play(FadeIn(triangle, shift=RIGHT))
```

### 带缩放的 FadeIn

```python
# Fade in while scaling
circle = Circle()
self.play(FadeIn(circle, scale=0.5))  # Starts at half size

# Shrink while fading in
square = Square()
self.play(FadeIn(square, scale=2))  # Starts at double size
```

## DrawBorderThenFill

先绘制边框，再填充形状。

```python
class DrawBorderExample(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE, opacity=0.7)
        square.set_stroke(WHITE, width=4)

        self.play(DrawBorderThenFill(square))
        self.wait()
```

## GrowFromCenter

从中心向外生长对象。

```python
circle = Circle()
self.play(GrowFromCenter(circle))

# Control growth speed
square = Square()
self.play(GrowFromCenter(square), run_time=2)
```

## GrowFromEdge

从指定边缘生长对象。

```python
square = Square()

# Grow from different edges
self.play(GrowFromEdge(square, DOWN))
# or: UP, DOWN, LEFT, RIGHT
```

## GrowFromPoint

从指定点生长对象。

```python
circle = Circle()
point = np.array([2, 2, 0])

self.play(GrowFromPoint(circle, point))
```

## SpinInFromNothing

旋转并生长，使对象进入画面。

```python
star = Star()
self.play(SpinInFromNothing(star))
```

## 多个创建的 AnimationGroup

### 同时创建

```python
class MultipleCreations(Scene):
    def construct(self):
        shapes = VGroup(
            Circle().shift(LEFT * 2),
            Square(),
            Triangle().shift(RIGHT * 2)
        )

        # Create all simultaneously
        self.play(*[ShowCreation(shape) for shape in shapes])
        self.wait()
```

### 顺序创建

```python
# One after another
for shape in shapes:
    self.play(ShowCreation(shape))
    self.wait(0.2)
```

## LaggedStart

以交错延迟创建对象。

```python
class LaggedCreation(Scene):
    def construct(self):
        circles = VGroup(*[
            Circle(radius=0.5).shift(i * RIGHT)
            for i in range(-3, 4)
        ])

        # Staggered creation
        self.play(LaggedStart(
            *[ShowCreation(circle) for circle in circles],
            lag_ratio=0.2  # Delay between each
        ))
        self.wait()
```

## 对比：创建动画

```python
class CreationComparison(Scene):
    def construct(self):
        methods = [
            ("ShowCreation", ShowCreation),
            ("FadeIn", FadeIn),
            ("GrowFromCenter", GrowFromCenter),
            ("DrawBorderThenFill", DrawBorderThenFill),
        ]

        for name, AnimClass in methods:
            # Create label
            label = Text(name, font_size=30)
            label.to_edge(UP)

            # Create shape
            square = Square()
            square.set_fill(BLUE, opacity=0.7)
            square.set_stroke(WHITE, width=3)

            # Show animation
            self.play(Write(label))
            self.play(AnimClass(square))
            self.wait()
            self.play(FadeOut(VGroup(label, square)))
```

## 高级创建模式

### 部分创建

```python
# Show only part of the creation
line = Line(LEFT * 3, RIGHT * 3)
self.play(
    ShowCreation(line),
    rate_func=lambda t: smooth(t * 0.5)  # Only 50% created
)
```

### 反向速率函数

```python
# Create backwards
circle = Circle()
self.play(
    ShowCreation(circle),
    rate_func=lambda t: 1 - smooth(t)  # Reverse
)
```

### 创建时变色

```python
class ColoredCreation(Scene):
    def construct(self):
        line = Line(LEFT * 3, RIGHT * 3)
        line.set_color_by_gradient(BLUE, RED)

        self.play(ShowCreation(line), run_time=2)
        self.wait()
```

## 书写数学内容

### 书写公式

```python
class WriteEquation(Scene):
    def construct(self):
        equation = Tex(R"E = mc^2")
        equation.scale(2)

        self.play(Write(equation))
        self.wait()

        # Color parts
        equation.set_color_by_tex("E", BLUE)
        equation.set_color_by_tex("m", GREEN)
        equation.set_color_by_tex("c", YELLOW)
        self.wait()
```

### 书写多行内容

```python
class MultiLineWrite(Scene):
    def construct(self):
        lines = VGroup(
            Tex(R"a^2 + b^2 = c^2"),
            Tex(R"e^{i\pi} + 1 = 0"),
            Tex(R"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")
        )
        lines.arrange(DOWN, buff=0.5)

        # Write line by line
        for line in lines:
            self.play(Write(line))
            self.wait(0.5)
```

## 最佳实践

1. **形状用 ShowCreation**：适用于几何对象和路径
2. **文本用 Write**：适用于 Text 和 Tex 对象
3. **组用 FadeIn**：适合同时带入多个对象
4. **序列用 LaggedStart**：营造视觉节奏
5. **统一时长**：相关对象保持相近的 `run_time`
6. **动画与内容匹配**：根据场景选用合适的动画

## 常见模式

### 创建并高亮

```python
shape = Circle()
self.play(ShowCreation(shape))
self.play(shape.animate.set_color(YELLOW))
self.play(shape.animate.scale(1.5))
```

### 文本依次出现

```python
title = Text("Title", font_size=72)
subtitle = Text("Subtitle", font_size=48)

self.play(Write(title))
self.wait(0.3)
self.play(FadeIn(subtitle, shift=UP))
```

### 网格创建

```python
grid = VGroup(*[
    Square(side_length=0.5).shift([i, j, 0])
    for i in range(-3, 4)
    for j in range(-2, 3)
])

self.play(LaggedStart(
    *[ShowCreation(square) for square in grid],
    lag_ratio=0.01
))
```

## 完整示例

```python
class ComprehensiveCreation(Scene):
    def construct(self):
        # Title
        title = Text("Creation Animations", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Create shapes with different animations
        circle = Circle(radius=1, color=BLUE)
        circle.shift(LEFT * 3)

        square = Square(side_length=2, color=GREEN)
        square.set_fill(GREEN, opacity=0.5)

        triangle = Triangle(color=YELLOW)
        triangle.shift(RIGHT * 3)

        # Staggered creation
        self.play(
            ShowCreation(circle),
            FadeIn(square, scale=0.5),
            GrowFromCenter(triangle),
            run_time=2
        )
        self.wait()

        # Add formula
        formula = Tex(R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}")
        formula.next_to(title, DOWN, buff=1)
        self.play(Write(formula))
        self.wait(2)

        # Clear scene
        self.play(FadeOut(VGroup(title, circle, square, triangle, formula)))
```
