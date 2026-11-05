---
name: creation-animations
description: Create、Write、FadeIn、DrawBorderThenFill 等创建类动画
metadata:
  tags: create, write, fadein, fadeout, grow, shrink, uncreate
---

# 创建类动画（Creation Animations）

将 mobject 引入场景的动画。

## Create

沿 VMobject 的路径逐步绘制。

```python
from manim import *

class CreateExample(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

适用场景：几何图形、直线、箭头。

## Write

模拟手写效果。最适合文字与公式。

```python
class WriteExample(Scene):
    def construct(self):
        text = Text("Hello World")
        equation = MathTex(r"E = mc^2")

        self.play(Write(text))
        self.wait()
        self.play(Write(equation))
```

`Write` 会根据文本长度自动设置合适的时长。

## DrawBorderThenFill

先绘制轮廓，再填充形状内部。

```python
class DrawBorderExample(Scene):
    def construct(self):
        square = Square(fill_opacity=0.8, color=BLUE)
        self.play(DrawBorderThenFill(square))
```

适用场景：带填充的形状，且希望先强调轮廓。

## FadeIn / FadeOut

简单的透明度过渡。

```python
class FadeExample(Scene):
    def construct(self):
        circle = Circle()

        # Fade in
        self.play(FadeIn(circle))
        self.wait()

        # Fade out
        self.play(FadeOut(circle))
```

### 方向性淡入淡出

```python
# Fade in from a direction
self.play(FadeIn(square, shift=UP))      # Fade in while moving up
self.play(FadeIn(square, shift=LEFT))    # Fade in from right

# Fade out to a direction
self.play(FadeOut(square, shift=DOWN))   # Fade out while moving down
```

### 缩放淡入淡出

```python
self.play(FadeIn(circle, scale=0.5))   # Fade in while growing
self.play(FadeOut(circle, scale=2))    # Fade out while shrinking
```

## GrowFromCenter / ShrinkToCenter

```python
class GrowExample(Scene):
    def construct(self):
        circle = Circle()

        self.play(GrowFromCenter(circle))
        self.wait()
        self.play(ShrinkToCenter(circle))
```

## GrowFromPoint

从指定点生长。

```python
self.play(GrowFromPoint(circle, ORIGIN))
self.play(GrowFromPoint(circle, LEFT * 3))
```

## GrowFromEdge

从指定边生长。

```python
self.play(GrowFromEdge(square, LEFT))   # Grow from left edge
self.play(GrowFromEdge(square, DOWN))   # Grow from bottom edge
```

## SpinInFromNothing

物体在旋转的同时放大出现。

```python
self.play(SpinInFromNothing(circle))
```

## Uncreate

`Create` 的逆过程——擦除 mobject。

```python
self.play(Create(circle))
self.wait()
self.play(Uncreate(circle))  # Erases in reverse
```

## AddTextLetterByLetter

逐字符打出文本。

```python
class TypingExample(Scene):
    def construct(self):
        text = Text("Hello World")
        self.play(AddTextLetterByLetter(text, time_per_char=0.1))
```

**注意：** 仅适用于 `Text`，不适用于 `MathTex`。

## 最佳实践

1. **文字用 Write** — 比 Create 更自然
2. **形状用 Create** — 清晰的渐进绘制
3. **快速引入用 FadeIn** — 当绘制过程不重要时
4. **移除与创建配对** — 若用 Create 引入，则用 Uncreate 移除；若用 FadeIn，则用 FadeOut
