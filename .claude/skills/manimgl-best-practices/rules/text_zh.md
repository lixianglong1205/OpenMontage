# ManimGL 中的文本

ManimGL 通过 `Text` 与 `TexText` 类提供强大的文本渲染能力。

## Text 类

`Text` 类使用系统字体渲染文本，并提供丰富的样式选项。

### 基础文本创建

```python
from manimlib import *

class TextExample(Scene):
    def construct(self):
        # Basic text
        text = Text("Hello ManimGL")
        self.add(text)
```

### 字体定制

```python
# Specify font and size
text = Text("Custom Font", font="Consolas", font_size=90)

# Different fonts for different parts
text = Text(
    "Mixed fonts example",
    t2f={"Mixed": "Consolas", "fonts": "Arial"}
)
```

### 文本着色

```python
# Color entire text
text = Text("Colored Text", color=BLUE)

# Color specific words
text = Text(
    "The quick brown fox",
    t2c={"quick": BLUE, "brown": ORANGE, "fox": GREEN}
)
```

### 文本样式

```python
# Slant (italic)
text = Text(
    "Italic and bold text",
    t2s={"Italic": ITALIC},
    t2w={"bold": BOLD}
)

# Combine color, font, slant, and weight
text = Text(
    "Fully styled text",
    font="Arial",
    font_size=48,
    t2c={"styled": RED},
    t2s={"styled": ITALIC},
    t2w={"text": BOLD},
    t2f={"text": "Consolas"}
)
```

## TexText 类

`TexText` 将 LaTeX 渲染与文本结合，便于混排文字与数学公式。

### 基础 TexText

```python
# Text with LaTeX support
text = TexText("The integral $\\int_0^1 x^2 dx$ equals $\\frac{1}{3}$")

# With font size
text = TexText("Hello World", font_size=72)

# Isolate parts for coloring
text = TexText(
    "Einstein's $E = mc^2$",
    isolate=["E", "m", "c"]
)
text.set_color_by_tex("E", BLUE)
text.set_color_by_tex("m", GREEN)
text.set_color_by_tex("c", YELLOW)
```

## Text 与 TexText 对比

- **Text**：使用系统字体，无 LaTeX，字体控制更灵活
- **TexText**：支持 LaTeX 数学符号，使用 LaTeX 的文本渲染

### 何时使用哪一种

```python
# Use Text for pure text with custom fonts
title = Text("Machine Learning", font="Helvetica", font_size=60)

# Use TexText when mixing text and inline math
description = TexText("The function $f(x) = x^2$ is convex")

# Use Tex for pure mathematical expressions
formula = Tex(R"\sum_{i=1}^n i = \frac{n(n+1)}{2}")
```

## 文本定位

```python
# Basic positioning
text = Text("Top")
text.to_edge(UP)

# Arrange multiple texts
title = Text("Title")
subtitle = Text("Subtitle", font_size=36)
VGroup(title, subtitle).arrange(DOWN, buff=0.5)

# Set width
text = Text("Long text that needs to fit")
text.set_width(FRAME_WIDTH - 1)
```

## 带背景的文本

```python
# Set backstroke for readability
text = Text("With Background", font_size=60)
text.set_backstroke(BLACK, width=5)

# Background rectangle (manually)
from manimlib.mobject.svg.tex_mobject import BackgroundRectangle
text = Text("Text")
bg = BackgroundRectangle(text, color=BLACK, fill_opacity=0.8)
self.add(bg, text)
```

## 使用 VGroup 进行文本布局

```python
# Group multiple text objects
line1 = Text("First line")
line2 = Text("Second line")
line3 = Text("Third line")

paragraph = VGroup(line1, line2, line3)
paragraph.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
paragraph.to_edge(LEFT)
```

## 完整示例

```python
class ComprehensiveTextExample(Scene):
    def construct(self):
        # Title with custom font
        title = Text(
            "Text Rendering in ManimGL",
            font="Arial",
            font_size=72,
            color=BLUE
        )
        title.to_edge(UP)

        # Description with mixed styling
        desc = Text(
            "Mix different fonts, colors, and styles",
            font="Helvetica",
            font_size=36,
            t2c={"fonts": RED, "colors": GREEN, "styles": YELLOW},
            t2w={"Mix": BOLD}
        )
        desc.next_to(title, DOWN, buff=0.5)

        # Mathematical description using TexText
        math_desc = TexText(
            "For equations like $E = mc^2$, use Tex or TexText",
            font_size=30
        )
        math_desc.next_to(desc, DOWN, buff=1)

        # Add all with animations
        self.play(Write(title))
        self.play(FadeIn(desc, shift=DOWN))
        self.play(Write(math_desc))
        self.wait()
```

## 最佳实践

1. **字体可用性**：确保系统已安装所需字体
2. **UI 元素用 Text**：对外观控制更好
3. **混合内容用 TexText**：需要同时展示文字与数学时
4. **背景复杂时用描边**：在复杂背景上为文本添加 backstroke 以提高可读性
5. **布局用 VGroup**：将相关文本元素分组，便于定位
6. **t2c/t2f/t2s/t2w**：用字典为单个词设置样式

## 常见模式

### 创建带背景的标签文本

```python
def create_label(text_str, color=WHITE):
    label = Text(text_str, font_size=40, color=color)
    label.set_backstroke(BLACK, width=5)
    return label
```

### 多行文本与对齐

```python
lines = [Text(line) for line in [
    "Line 1",
    "Longer line 2",
    "Line 3"
]]
paragraph = VGroup(*lines)
paragraph.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
```

### 高亮文本

```python
sentence = Text(
    "This word is highlighted",
    t2c={"highlighted": YELLOW},
    t2w={"highlighted": BOLD}
)
```
