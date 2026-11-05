---
name: text
description: Manim 中的 Text 图元、字体与文本样式
metadata:
  tags: text, font, typography, markup, paragraph
---

# Manim 中的文本

`Text` 类使用 Pango/Cairo 渲染文本，支持多种字体与样式。

## 基础文本

```python
from manim import *

class TextExample(Scene):
    def construct(self):
        text = Text("Hello World")
        self.play(Write(text))
```

## 文本参数

```python
text = Text(
    "Hello World",
    font_size=48,           # Size (default: 48)
    color=BLUE,             # Text color
    font="Arial",           # Font family
    weight=BOLD,            # NORMAL, BOLD, etc.
    slant=ITALIC,           # NORMAL, ITALIC, OBLIQUE
    line_spacing=1.5,       # Space between lines
)
```

## 字号

```python
# Using font_size parameter
small = Text("Small", font_size=24)
medium = Text("Medium", font_size=48)
large = Text("Large", font_size=72)

# Using scale after creation
text = Text("Hello").scale(2)
```

## 自定义字体

```python
# Use any installed system font
text = Text("Custom Font", font="Comic Sans MS")
text = Text("Monospace", font="Courier New")
text = Text("Serif", font="Times New Roman")
```

## 使用 MarkupText 设置文本样式

在同一 Text 对象内用 Pango 标记实现混合样式：

```python
class MarkupExample(Scene):
    def construct(self):
        text = MarkupText(
            f'all in red <span fgcolor="{YELLOW}">except this</span>',
            color=RED
        )
        self.play(Write(text))
```

### 可用的标记标签

```python
# Bold and italic
text = MarkupText('<b>Bold</b> and <i>Italic</i>')

# Colors using fgcolor
text = MarkupText('<span fgcolor="yellow">Yellow</span>')

# Subscripts and superscripts
text = MarkupText('H<sub>2</sub>O and x<sup>2</sup>')

# Font size
text = MarkupText('<big>Big</big> and <small>small</small>')

# Underline and strikethrough
text = MarkupText('<u>Underline</u> and <s>Strike</s>')

# Double underline with color
text = MarkupText('<span underline="double" underline_color="green">text</span>')

# Monospace
text = MarkupText('type <tt>help</tt> for help')
```

### MarkupText 中的渐变

```python
# Global gradient
text = MarkupText("nice gradient", gradient=(BLUE, GREEN))

# Inline gradient
text = MarkupText(
    'nice <gradient from="RED" to="YELLOW">colored</gradient> text'
)
```

### 转义特殊字符

```python
# Must escape these characters:
# > as &gt;
# < as &lt;
# & as &amp;
text = MarkupText("5 &gt; 3 and 2 &lt; 4")
```

## 多行文本

```python
# Using \n for line breaks
text = Text("Line 1\nLine 2\nLine 3")

# Using Paragraph for better control
from manim import Paragraph

para = Paragraph(
    "This is a longer text",
    "that spans multiple lines",
    "with automatic alignment",
    line_spacing=0.5
)
```

## 为文本局部着色

```python
class ColoredText(Scene):
    def construct(self):
        text = Text("Hello World")
        text[0:5].set_color(RED)    # "Hello" in red
        text[6:11].set_color(BLUE)  # "World" in blue
        self.play(Write(text))
```

## 渐变文本

```python
text = Text("Gradient Text")
text.set_color_by_gradient(RED, YELLOW, GREEN)
```

## 访问字符

```python
text = Text("ABCDE")

# Individual characters
text[0]  # 'A'
text[1]  # 'B'

# Slices
text[0:3]  # 'ABC'
text[-1]   # 'E'

# Iterate
for char in text:
    char.set_color(random_color())
```

## 文本定位

```python
# Standard positioning methods work
text = Text("Hello")
text.to_edge(UP)
text.to_corner(UL)
text.move_to(ORIGIN)
text.next_to(other_mobject, DOWN)
```

## 最佳实践

1. **普通文本用 Text** — 简单且快速
2. **混合样式用 MarkupText** — 需要多种颜色或字重时
3. **数学公式用 MathTex** — Text 不渲染 LaTeX
4. **在系统级安装字体** — Manim 使用系统字体
5. **保持 font_size 一致** — 相关文本使用相同字号
