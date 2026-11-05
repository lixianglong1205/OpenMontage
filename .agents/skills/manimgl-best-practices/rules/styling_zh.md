# ManimGL 中的样式

ManimGL 为 mobject 提供全面的样式选项，包括填充、描边、透明度以及特殊效果。

## 填充属性

### 基本填充

```python
from manimlib import *

# Set fill at creation
circle = Circle(fill_color=BLUE, fill_opacity=0.7)

# Set fill after creation
square = Square()
square.set_fill(RED, opacity=0.5)
```

### 填充示例

```python
class FillExample(Scene):
    def construct(self):
        # Solid fill
        solid = Circle(radius=1)
        solid.set_fill(BLUE, opacity=1.0)

        # Transparent fill
        transparent = Circle(radius=1)
        transparent.set_fill(GREEN, opacity=0.3)

        # No fill (just outline)
        outline = Circle(radius=1)
        outline.set_fill(opacity=0)
        outline.set_stroke(YELLOW, width=4)

        VGroup(solid, transparent, outline).arrange(RIGHT, buff=1)
        self.add(solid, transparent, outline)
```

## 描边属性

### 基本描边

```python
# Set stroke at creation
line = Line(stroke_color=WHITE, stroke_width=4)

# Set stroke after creation
circle = Circle()
circle.set_stroke(BLUE, width=3, opacity=0.8)
```

### 描边宽度

```python
# Different stroke widths
thin = Circle().set_stroke(width=1)
medium = Circle().set_stroke(width=4)
thick = Circle().set_stroke(width=10)

VGroup(thin, medium, thick).arrange(RIGHT, buff=0.5)
```

### 填充下方的描边

```python
# Draw stroke behind fill (useful for borders)
shape = Circle(fill_color=BLUE, fill_opacity=0.8)
shape.set_stroke(WHITE, width=6, opacity=1, background=True)
```

## 背描边（Backstroke）

`backstroke` 功能在文字或形状后方添加轮廓，以提升可见性。

```python
# Text with backstroke (black outline)
text = Text("Readable Text", font_size=60)
text.set_backstroke(BLACK, width=5)

# Works great over complex backgrounds
text.set_backstroke(BLACK, width=8, opacity=1.0)
```

### 背描边示例

```python
class BackstrokeExample(Scene):
    def construct(self):
        # Create complex background
        background = VGroup(*[
            Circle(radius=2 * np.random.random(), color=random_color())
            for _ in range(20)
        ])
        background.set_opacity(0.3)
        self.add(background)

        # Text with backstroke stands out
        text = Text("Clear and Readable", font_size=72, color=WHITE)
        text.set_backstroke(BLACK, width=10)
        self.add(text)
```

## 透明度控制

### 填充透明度

```python
# Control fill transparency
circle = Circle()
circle.set_fill_opacity(0.5)

# Animate opacity
self.play(circle.animate.set_fill_opacity(1.0))
```

### 描边透明度

```python
# Control stroke transparency
square = Square()
square.set_stroke_opacity(0.7)
```

### 整体透明度

```python
# Set both fill and stroke opacity
mobject = Circle()
mobject.set_opacity(0.5)  # Affects both fill and stroke
```

## 光泽（Gloss，3D）

### 为 3D 对象添加光泽

```python
# Make objects glossy/shiny
sphere = Sphere(radius=2, color=BLUE)
sphere.set_gloss(0.8)  # 0 (matte) to 1 (very glossy)

# Get gloss value
gloss_value = sphere.get_gloss()
```

## 阴影（Shadow，3D）

### 添加阴影

```python
# Add shadow to 3D objects
cube = Cube(color=RED)
cube.set_shadow(0.6)  # 0 (no shadow) to 1 (strong shadow)

# Get shadow value
shadow_value = cube.get_shadow()
```

## 组合样式

### 完整样式控制

```python
class CompleteStyling(Scene):
    def construct(self):
        shape = Circle(radius=2)

        # Set all properties
        shape.set_fill(BLUE, opacity=0.7)
        shape.set_stroke(WHITE, width=4, opacity=1.0)
        shape.set_backstroke(BLACK, width=6)

        self.add(shape)
```

## 样式匹配

### 从另一个 Mobject 匹配样式

```python
# Create styled source
source = Circle()
source.set_fill(BLUE, opacity=0.7)
source.set_stroke(WHITE, width=3)

# Match style
target = Square()
target.match_style(source)  # Copies all styling

# Match specific properties
target2 = Triangle()
target2.match_fill(source)   # Copy fill only
target2.match_stroke(source) # Copy stroke only
target2.match_color(source)  # Copy color only
```

## 渐变与颜色过渡

### 渐变填充

```python
# Gradient across submobjects
text = Text("Gradient")
text.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW)

# For shapes with submobjects
squares = VGroup(*[Square() for _ in range(10)])
squares.arrange(RIGHT)
squares.set_submobject_colors_by_gradient(RED, PURPLE)
```

## 视觉效果

### 发光效果

```python
# Create glow effect with multiple strokes
def add_glow(mobject, color=YELLOW, radius=0.5):
    glow_layers = VGroup(*[
        mobject.copy().set_stroke(
            color,
            width=width,
            opacity=0.3 / (i + 1)
        )
        for i, width in enumerate(range(2, 20, 2))
    ])
    return VGroup(glow_layers, mobject)

# Usage
circle = Circle(color=BLUE)
glowing_circle = add_glow(circle)
```

### 霓虹效果

```python
def neon_style(mobject, color=BLUE):
    mobject.set_fill(color, opacity=0.2)
    mobject.set_stroke(color, width=3)
    mobject.set_backstroke(color, width=10, opacity=0.5)
    return mobject

# Usage
neon_text = neon_style(Text("NEON", font_size=90), BLUE)
```

## 样式预设

### 创建可复用样式

```python
# Define style functions
def outline_style(mobject):
    mobject.set_fill(opacity=0)
    mobject.set_stroke(WHITE, width=3)
    return mobject

def solid_style(mobject, color=BLUE):
    mobject.set_fill(color, opacity=1.0)
    mobject.set_stroke(color, width=0)
    return mobject

def glass_style(mobject, color=BLUE):
    mobject.set_fill(color, opacity=0.3)
    mobject.set_stroke(WHITE, width=2, opacity=0.8)
    mobject.set_gloss(0.9)
    return mobject

# Usage
circle1 = outline_style(Circle())
circle2 = solid_style(Circle(), RED)
circle3 = glass_style(Circle(), GREEN)
```

## 动画化样式

### 样式过渡

```python
class StyleAnimation(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE, opacity=0)
        square.set_stroke(WHITE, width=1)

        self.add(square)
        self.wait()

        # Animate style changes
        self.play(
            square.animate.set_fill(BLUE, opacity=0.7),
            square.animate.set_stroke(WHITE, width=5)
        )
        self.wait()

        # Change colors
        self.play(
            square.animate.set_fill(RED, opacity=0.9),
            square.animate.set_stroke(YELLOW, width=3)
        )
        self.wait()
```

## 完整样式示例

```python
class ComprehensiveStyleExample(Scene):
    def construct(self):
        # Different styling approaches
        shapes = VGroup()

        # Filled shape
        filled = Circle(radius=0.8)
        filled.set_fill(BLUE, opacity=0.8)
        filled.set_stroke(width=0)
        shapes.add(filled)

        # Outlined shape
        outlined = Circle(radius=0.8)
        outlined.set_fill(opacity=0)
        outlined.set_stroke(WHITE, width=4)
        shapes.add(outlined)

        # Transparent with border
        transparent = Circle(radius=0.8)
        transparent.set_fill(GREEN, opacity=0.3)
        transparent.set_stroke(GREEN, width=3)
        shapes.add(transparent)

        # With backstroke
        backstroke = Circle(radius=0.8)
        backstroke.set_fill(YELLOW, opacity=0.6)
        backstroke.set_stroke(WHITE, width=2)
        backstroke.set_backstroke(BLACK, width=5)
        shapes.add(backstroke)

        # Gradient (multiple submobjects)
        gradient_circles = VGroup(*[
            Circle(radius=0.15).shift(i * 0.3 * RIGHT)
            for i in range(-2, 3)
        ])
        gradient_circles.set_submobject_colors_by_gradient(RED, YELLOW)
        shapes.add(gradient_circles)

        # Arrange and display
        shapes.arrange(RIGHT, buff=1)
        self.play(LaggedStart(*[
            FadeIn(shape)
            for shape in shapes
        ], lag_ratio=0.2))
        self.wait()

        # Animate style transitions
        self.play(
            filled.animate.set_opacity(0.3),
            outlined.animate.set_stroke(YELLOW, width=8),
            transparent.animate.set_fill(RED, opacity=0.8)
        )
        self.wait()
```

## 最佳实践

1. **分层用透明度**：使用透明效果展示重叠元素
2. **可读性用背描边**：在复杂背景上的文字添加背描边
3. **描边宽度一致**：用一致的宽度维持视觉层级
4. **填充与描边**：用填充表示区域，用描边表示边框
5. **3D 用光泽增强真实感**：为 3D 对象添加光泽使其更逼真
6. **匹配样式保持一致**：使用样式匹配获得统一外观
7. **渐变表达流动与关系**：用渐变表示过渡或关联

## 常见模式

### 强调用轮廓样式

```python
def emphasize(mobject):
    return mobject.set_stroke(YELLOW, width=8, opacity=1.0)
```

### 透明叠加层

```python
def overlay(mobject, color=BLUE):
    return mobject.set_fill(color, opacity=0.2)
```

### 简洁 UI 样式

```python
def ui_style(mobject):
    mobject.set_fill(BLUE_C, opacity=0.9)
    mobject.set_stroke(WHITE, width=2)
    return mobject
```

### 高亮文字

```python
text = Text("Important", font_size=60)
text.set_fill(YELLOW, opacity=1.0)
text.set_backstroke(BLACK, width=8)
text.set_stroke(WHITE, width=1)
```
