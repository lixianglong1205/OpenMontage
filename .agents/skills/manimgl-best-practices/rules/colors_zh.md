# ManimGL 中的颜色

ManimGL 提供丰富的颜色支持，包括内置颜色常量、渐变以及颜色处理工具。

## 颜色常量

### 基础颜色

```python
# Primary colors
RED, GREEN, BLUE
YELLOW, CYAN, MAGENTA

# Grayscale
WHITE, GREY, GRAY, BLACK

# Common colors
ORANGE, PURPLE, PINK, BROWN
MAROON, TEAL, GOLD
```

### 颜色变体

ManimGL 通过字母后缀提供颜色渐变系列：

```python
# Blue variations (darkest to lightest)
BLUE_E  # Darkest blue
BLUE_D
BLUE_C
BLUE_B
BLUE_A  # Lightest blue

# Similarly for other colors:
RED_E, RED_D, RED_C, RED_B, RED_A
GREEN_E, GREEN_D, GREEN_C, GREEN_B, GREEN_A
YELLOW_E, YELLOW_D, YELLOW_C, YELLOW_B, YELLOW_A
```

### 用法示例

```python
from manimlib import *

class ColorExample(Scene):
    def construct(self):
        # Create circles with different color variations
        circles = VGroup(*[
            Circle(radius=0.5, color=color)
            for color in [BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A]
        ])
        circles.arrange(RIGHT, buff=0.5)
        self.add(circles)
```

## 设置颜色

### 基本颜色设置

```python
# At creation
circle = Circle(color=BLUE)

# After creation
square = Square()
square.set_color(RED)

# Multiple mobjects
group = VGroup(Circle(), Square(), Triangle())
group.set_color(GREEN)
```

### 颜色动画

```python
class ColorAnimation(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        self.add(circle)

        # Animate color change
        self.play(circle.animate.set_color(RED))
        self.wait()

        # Another change
        self.play(circle.animate.set_color(YELLOW))
        self.wait()
```

## 渐变

### set_submobject_colors_by_gradient

```python
# Apply gradient to submobjects
text = Text("Gradient Text")
text.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW)

# Multiple objects with gradient
squares = VGroup(*[Square() for _ in range(10)])
squares.arrange(RIGHT)
squares.set_submobject_colors_by_gradient(RED, BLUE)
```

### 颜色插值

```python
from manimlib.utils.color import interpolate_color

# Create color between two colors
mid_color = interpolate_color(RED, BLUE, 0.5)  # Purple

# Create gradient programmatically
n_colors = 10
gradient = [
    interpolate_color(RED, BLUE, alpha)
    for alpha in np.linspace(0, 1, n_colors)
]
```

## 高级颜色技巧

### set_color_by_code (GLSL)

ManimGL 支持通过 GLSL 代码进行动态着色：

```python
# Color based on position
square = Square()
square.set_color_by_code("""
    color.r = x;
    color.g = y;
    color.b = 1.0;
""")
```

### set_color_by_xyz_func

```python
# Color based on 3D position
surface = Sphere(radius=2)
surface.set_color_by_xyz_func(
    glsl_snippet="float value = sqrt(x*x + y*y + z*z); return value;",
    min_value=0,
    max_value=5,
    colormap='viridis'
)
```

## 文本与 LaTeX 的颜色

### 为文本片段着色

```python
# Color specific words
text = Text(
    "Red, Green, and Blue",
    t2c={"Red": RED, "Green": GREEN, "Blue": BLUE}
)
```

### LaTeX 着色

```python
# Color math symbols
equation = Tex(
    R"E = mc^2",
    t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
)

# Color by tex substring
formula = Tex(R"\int_0^1 x^2 dx")
formula.set_color_by_tex("x", BLUE)
formula.set_color_by_tex(R"\int", RED)
```

## RGB 与十六进制颜色

### 使用 RGB 值

```python
from manimlib.utils.color import rgb_to_color

# RGB values (0-1 range)
custom_color = rgb_to_color([0.5, 0.3, 0.8])
circle = Circle(color=custom_color)

# RGB from 0-255 range (convert to 0-1)
custom_color = rgb_to_color([128/255, 77/255, 204/255])
```

### 使用十六进制颜色

```python
from manimlib.utils.color import hex_to_rgb, rgb_to_color

# Hex color
hex_color = "#FF5733"
rgb = hex_to_rgb(hex_color)
color = rgb_to_color(rgb)

circle = Circle(color=color)
```

## 不透明度与透明

### 设置不透明度

```python
# Transparent circle
circle = Circle(color=BLUE, fill_opacity=0.5)

# Change opacity
circle.set_opacity(0.7)

# Fill vs Stroke opacity
square = Square()
square.set_fill(BLUE, opacity=0.5)
square.set_stroke(WHITE, width=4, opacity=1.0)
```

## 颜色工具

### 从 Mobject 获取颜色

```python
circle = Circle(color=BLUE)

# Get color
color = circle.get_color()

# Get fill color
fill_color = circle.get_fill_color()

# Get stroke color
stroke_color = circle.get_stroke_color()
```

### 颜色匹配

```python
# Match color from another mobject
circle = Circle(color=BLUE)
square = Square()
square.match_color(circle)

# Match fill color
square.match_fill(circle)

# Match stroke
square.match_stroke(circle)
```

## 配色方案

### 创建一致的调色板

```python
# Define color scheme
COLOR_SCHEME = {
    "background": "#1e1e1e",
    "primary": BLUE_C,
    "secondary": GREEN_C,
    "accent": YELLOW_C,
    "text": WHITE,
    "highlight": RED_C
}

# Use in scene
class StyledScene(Scene):
    def construct(self):
        title = Text("Title", color=COLOR_SCHEME["primary"])
        subtitle = Text("Subtitle", color=COLOR_SCHEME["secondary"])
        highlight = Circle(color=COLOR_SCHEME["accent"])

        self.add(title, subtitle, highlight)
```

### 3Blue1Brown 配色

```python
# Grant's typical colors
BLUE_3B1B = BLUE_C
GREEN_3B1B = GREEN_C
YELLOW_3B1B = YELLOW_C
RED_3B1B = RED_C

# Background
BACKGROUND_COLOR = "#0a0a0a"
```

## 光泽与视觉属性

### 添加光泽（3D）

```python
# Add glossy appearance
sphere = Sphere(radius=2, color=BLUE)
sphere.set_gloss(0.8)  # 0 to 1

# Get gloss value
gloss = sphere.get_gloss()
```

### 阴影

```python
# Add shadow (for 3D)
cube = Cube(color=RED)
cube.set_shadow(0.5)  # 0 to 1

# Get shadow value
shadow = cube.get_shadow()
```

## 完整颜色示例

```python
class ComprehensiveColorExample(Scene):
    def construct(self):
        # Color variations showcase
        blue_shades = VGroup(*[
            Circle(radius=0.4, color=color)
            for color in [BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A]
        ])
        blue_shades.arrange(RIGHT, buff=0.3)
        blue_shades.to_edge(UP, buff=1)

        # Gradient
        squares = VGroup(*[Square(side_length=0.6) for _ in range(8)])
        squares.arrange(RIGHT, buff=0.2)
        squares.set_submobject_colors_by_gradient(RED, YELLOW, GREEN, BLUE)

        # Custom RGB color
        custom_circle = Circle(
            radius=1,
            color=rgb_to_color([0.8, 0.2, 0.6]),
            fill_opacity=0.7
        )
        custom_circle.shift(DOWN * 2)

        # Colored text
        text = Text(
            "Colorful Text",
            font_size=48,
            t2c={"Colorful": BLUE, "Text": GREEN}
        )
        text.next_to(custom_circle, UP, buff=0.5)

        # Add everything
        self.play(
            FadeIn(blue_shades, lag_ratio=0.1),
            FadeIn(squares, lag_ratio=0.1),
            ShowCreation(custom_circle),
            Write(text)
        )
        self.wait()

        # Animate color changes
        self.play(
            squares.animate.set_submobject_colors_by_gradient(PURPLE, ORANGE),
            custom_circle.animate.set_color(TEAL)
        )
        self.wait()
```

## 最佳实践

1. **使用命名常量**：为可读性，优先使用 `BLUE` 而非 RGB 数值
2. **一致的配色方案**：定义调色板以保持画面协调
3. **用渐变强调**：用渐变表现进展或元素之间的关系
4. **用不透明度分层**：用透明效果表现重叠元素
5. **颜色可访问性**：保证足够对比度以便观看
6. **LaTeX 使用 t2c**：为公式着色以突出重要部分
7. **避免过度使用**：颜色过多容易分散注意力

## 常见模式

### 彩虹渐变

```python
def rainbow_gradient(mobjects):
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    VGroup(*mobjects).set_submobject_colors_by_gradient(*colors)
```

### 过渡到指定颜色的动画

```python
self.play(
    circle.animate.set_color(RED),
    run_time=2
)
```

### 颜色循环

```python
colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
for color in colors:
    self.play(circle.animate.set_color(color), run_time=0.5)
    self.wait(0.2)
```
