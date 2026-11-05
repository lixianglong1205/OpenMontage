---
name: text-animations
description: Write、AddTextLetterByLetter、TypeWithCursor 文本动画
metadata:
  tags: text, write, typing, letter, cursor, animation
---

# 文本动画

专用于文本与公式的动画。

## Write

最常见的文本动画，模拟手写效果。

```python
from manim import *

class WriteExample(Scene):
    def construct(self):
        text = Text("Hello World")
        equation = MathTex(r"E = mc^2")

        self.play(Write(text))
        self.wait()
        self.play(Write(equation))
```

### Write 参数

```python
self.play(Write(
    text,
    run_time=2,           # Override auto-calculated time
    rate_func=linear,     # Timing curve
    reverse=False,        # Write backwards if True
))
```

`Write` 会根据文本长度自动调整 `run_time`。

## AddTextLetterByLetter

逐字符打出文本。

```python
class LetterByLetterExample(Scene):
    def construct(self):
        text = Text("Typing effect")

        self.play(AddTextLetterByLetter(
            text,
            time_per_char=0.1  # Speed of typing
        ))
```

**注意：** 仅适用于 `Text`，不适用于 `MathTex`。

## RemoveTextLetterByLetter

`AddTextLetterByLetter` 的逆过程——逐字符移除文本。

```python
class RemoveLetterByLetter(Scene):
    def construct(self):
        text = Text("Disappearing text")
        self.add(text)

        self.play(RemoveTextLetterByLetter(
            text,
            time_per_char=0.05
        ))
```

## TypeWithCursor

带可见光标的打字动画。

```python
class TypeWithCursorExample(Scene):
    def construct(self):
        text = Text("Typing with cursor")

        # Create cursor
        cursor = Rectangle(
            color=GREY_A,
            fill_color=GREY_A,
            fill_opacity=1.0,
            height=1.1,
            width=0.1,
        )

        self.play(TypeWithCursor(text, cursor))

        # Optional: blink cursor after typing
        self.play(Blink(cursor, blinks=3))
```

### 光标自定义

```python
# Line cursor
cursor = Line(UP * 0.5, DOWN * 0.5, color=WHITE, stroke_width=2)

# Block cursor
cursor = Rectangle(width=0.5, height=1, fill_opacity=0.8, color=WHITE)

# Custom cursor position
self.play(TypeWithCursor(
    text,
    cursor,
    buff=0.05,           # Space between text and cursor
    keep_cursor_y=True,  # Keep cursor at consistent height
    leave_cursor_on=True # Show cursor after animation
))
```

## Blink（用于光标）

```python
class BlinkExample(Scene):
    def construct(self):
        cursor = Rectangle(height=1, width=0.1, fill_opacity=1)
        self.add(cursor)

        self.play(Blink(cursor, blinks=5, time_on=0.3, time_off=0.3))
```

## 逐词动画

使用 `LaggedStart` 实现逐词出现：

```python
class WordByWord(Scene):
    def construct(self):
        # Split into individual Text objects
        words = VGroup(
            Text("Hello"),
            Text("World"),
            Text("!")
        ).arrange(RIGHT, buff=0.3)

        self.play(LaggedStart(
            *[Write(word) for word in words],
            lag_ratio=0.5
        ))
```

## 公式变换

在公式之间做动画过渡：

```python
class EquationTransform(Scene):
    def construct(self):
        eq1 = MathTex(r"a^2 + b^2 = c^2")
        eq2 = MathTex(r"c = \sqrt{a^2 + b^2}")

        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
```

## 文本高亮

```python
class HighlightText(Scene):
    def construct(self):
        text = Text("Important message")
        self.add(text)

        # Circumscribe (draw around)
        self.play(Circumscribe(text, color=YELLOW))

        # Indicate (pulse)
        self.play(Indicate(text, color=RED))

        # Flash
        self.play(Flash(text.get_center(), color=WHITE))
```

## 替换文本

```python
class ReplaceText(Scene):
    def construct(self):
        text1 = Text("Before")
        text2 = Text("After")

        self.play(Write(text1))
        self.wait()

        # Transform text
        self.play(Transform(text1, text2))

        # Or replacement transform
        self.play(ReplacementTransform(text1, text2))
```

## 彩色文本动画

```python
class ColoredTextAnimation(Scene):
    def construct(self):
        text = Text("Colorful")
        self.play(Write(text))

        # Animate color change per letter
        self.play(LaggedStart(
            *[char.animate.set_color(random_bright_color()) for char in text],
            lag_ratio=0.1
        ))
```

## 最佳实践

1. **多数文本用 Write** — 自然、流畅
2. **打字效果用 AddTextLetterByLetter** — 终端/代码风格
3. **交互感用 TypeWithCursor** — 适合教程
4. **公式过渡用 TransformMatchingTex** — 数学变换更顺滑
5. **用 time_per_char 调节节奏** — 通常 0.05–0.1 较合适
6. **逐字动画只用 Text（不用 MathTex）** — API 限制
