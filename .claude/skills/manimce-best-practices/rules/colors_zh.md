---
name: colors
description: Manim 中的颜色常量、渐变与颜色操作
metadata:
  tags: color, colors, gradient, rgb, hex, palette
---

# Manim 中的颜色

Manim 提供预定义的颜色常量，并支持自定义颜色。

## 颜色常量

### 原色
```python
RED, GREEN, BLUE
YELLOW, ORANGE, PINK, PURPLE
WHITE, BLACK, GREY (or GRAY)
```

### 颜色变体（深浅）
多数颜色都有从 `_A`（最浅）到 `_E`（最深）的变体：
```python
BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E
RED_A, RED_B, RED_C, RED_D, RED_E
GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E
GREY_A, GREY_B, GREY_C, GREY_D, GREY_E
```

### 常用命名颜色
```python
TEAL, TEAL_A, TEAL_B, TEAL_C, TEAL_D, TEAL_E
GOLD, GOLD_A, GOLD_B, GOLD_C, GOLD_D, GOLD_E
MAROON, MAROON_A, MAROON_B, MAROON_C, MAROON_D, MAROON_E
PURPLE, PURPLE_A, PURPLE_B, PURPLE_C, PURPLE_D, PURPLE_E
```

### 特殊颜色
```python
PURE_RED, PURE_GREEN, PURE_BLUE  # RGB primaries
LIGHT_GREY, DARK_GREY
LIGHTER_GREY, DARKER_GREY
LIGHT_BROWN, DARK_BROWN
```

## 使用颜色

### 创建时设置颜色
```python
circle = Circle(color=RED)
square = Square(color=BLUE, fill_color=GREEN, fill_opacity=0.5)
text = Text("Hello", color=YELLOW)
```

### 创建后设置颜色
```python
circle = Circle()
circle.set_color(RED)
```

## 十六进制颜色

```python
# Use hex strings
circle = Circle(color="#FF5733")
square = Square(color="#2ECC71")

# RGB values (0-1 range)
from manim import rgb_to_color
custom = rgb_to_color([0.5, 0.2, 0.8])
```

## 填充色与描边色

```python
square = Square()
square.set_fill(RED, opacity=0.8)      # Interior color
square.set_stroke(BLUE, width=4)       # Border color
```

### 组合样式
```python
square = Square(
    color=BLUE,            # Sets both fill and stroke
    fill_opacity=0.5,      # Fill transparency
    stroke_width=4         # Border thickness
)
```

## 渐变

### 在 Mobject 上设置颜色渐变
```python
text = Text("GRADIENT")
text.set_color_by_gradient(RED, YELLOW, GREEN)
```

### 沿路径渐变
```python
line = Line(LEFT * 3, RIGHT * 3)
line.set_color_by_gradient(BLUE, GREEN, YELLOW)
```

## 颜色插值

在两种颜色之间生成中间色：

```python
from manim import interpolate_color

# Get color halfway between RED and BLUE
mid_color = interpolate_color(RED, BLUE, 0.5)

# Create a range of colors
colors = [interpolate_color(RED, BLUE, alpha) for alpha in np.linspace(0, 1, 10)]
```

## ManimColor 类

如需高级颜色操作，可直接使用 ManimColor：

```python
from manim import ManimColor

# Create from various formats
color1 = ManimColor("#FF0000")           # From hex
color2 = ManimColor((0.0, 1.0, 0.5))     # From RGB floats (0-1)
color3 = ManimColor([255, 165, 0])       # From RGB ints (0-255)

# Color manipulation methods
lighter = color1.lighter()               # Lighter version
darker = color1.darker()                 # Darker version
inverted = color1.invert()               # Inverted color
with_alpha = color1.opacity(0.5)         # With 50% opacity

# Convert formats
hex_str = color1.to_hex()                # To hex string
rgb = color1.to_rgb()                    # To RGB float array
hsv = color1.to_hsv()                    # To HSV array

# Interpolation
mixed = color1.interpolate(color2, 0.5)  # Blend two colors
```

## 不透明度

```python
# Set opacity (0 = transparent, 1 = opaque)
circle = Circle(fill_opacity=0.5, stroke_opacity=0.8)

# Modify opacity
circle.set_opacity(0.5)         # Both fill and stroke
circle.set_fill_opacity(0.7)    # Fill only
circle.set_stroke_opacity(0.3)  # Stroke only
```

## 按数值着色

根据数值为 mobject 着色（适用于数据可视化）：

```python
class ColorByValue(Scene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(10)]).arrange(RIGHT)

        for i, dot in enumerate(dots):
            # Color from blue (cold) to red (hot)
            dot.set_color(interpolate_color(BLUE, RED, i / 9))

        self.add(dots)
```

## 随机颜色

```python
from manim import random_color, random_bright_color

circle = Circle(color=random_color())
square = Square(color=random_bright_color())
```

## 动画用的颜色列表

```python
class ColorCycle(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)

        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        for color in colors:
            self.play(circle.animate.set_color(color), run_time=0.5)
```

## 最佳实践

1. **用颜色变体营造层次** - 阴影用 `BLUE_E`，高光用 `BLUE_A`
2. **保持颜色一致** - 相关概念使用相同颜色
3. **用不透明度做层叠** - 半透明填充可显示重叠区域
4. **考虑色觉无障碍** - 避免仅用红绿区分
5. **谨慎使用渐变** - 过多渐变容易分散注意力
