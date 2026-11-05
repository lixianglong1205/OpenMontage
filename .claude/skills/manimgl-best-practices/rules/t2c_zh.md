# ManimGL 中的 Tex 到颜色映射（t2c）

`t2c` 参数（tex_to_color_map）是为 LaTeX 表达式中特定部分着色的强大功能。

## 基本 t2c 用法

### 为数学符号着色

```python
from manimlib import *

class T2CExample(Scene):
    def construct(self):
        # Color specific variables
        equation = Tex(
            R"E = mc^2",
            t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
        )
        self.add(equation)
```

### 为子串着色

```python
# Color parts of the formula
formula = Tex(
    R"\int_0^1 x^2 \, dx = \frac{1}{3}",
    t2c={
        R"\int": BLUE,
        "x": GREEN,
        R"\frac{1}{3}": YELLOW
    }
)
```

## 高级 t2c 模式

### 为多处相同内容着色

```python
# All instances of a variable get colored
series = Tex(
    R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
    t2c={
        "n": BLUE,     # Colors all 'n's
        R"\pi": RED,
        R"\sum": GREEN
    }
)
```

### 与 isolate 配合使用 t2c

```python
# Isolate specific parts for individual control
equation = Tex(
    R"a^2 + b^2 = c^2",
    isolate=["a", "b", "c", "^2"],
    t2c={
        "a": RED,
        "b": GREEN,
        "c": BLUE,
        "^2": YELLOW
    }
)
```

## 动态着色

### set_color_by_tex

```python
# Color after creation
formula = Tex(R"f(x) = x^2 + 2x + 1")
formula.set_color_by_tex("x", BLUE)
formula.set_color_by_tex("f", GREEN)
formula.set_color_by_tex("1", YELLOW)
```

### 渐变着色

```python
# Apply gradient to entire formula
formula = Tex(R"\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}")
formula.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW)
```

## 文本着色（Text 类）

### Text 对象的 t2c

```python
# Color words in Text
text = Text(
    "The quick brown fox jumps",
    t2c={
        "quick": BLUE,
        "brown": ORANGE,
        "fox": GREEN
    }
)
```

### 多种样式选项

```python
# Combine t2c, t2f, t2s, t2w
text = Text(
    "Different styles and colors",
    t2c={"Different": RED, "colors": BLUE},
    t2f={"styles": "Consolas"},
    t2s={"styles": ITALIC},
    t2w={"Different": BOLD}
)
```

## 复杂示例

### 带颜色编码的物理方程

```python
class ColoredPhysicsEquation(Scene):
    def construct(self):
        # Maxwell's equation with color-coded components
        maxwell = Tex(
            R"\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}",
            t2c={
                R"\nabla": BLUE,
                R"\vec{E}": RED,
                R"\vec{B}": GREEN,
                "t": YELLOW
            }
        )
        self.play(Write(maxwell))
        self.wait()
```

### 分步推导

```python
class ColoredDerivation(Scene):
    def construct(self):
        # Initial equation
        eq1 = Tex(
            R"(a + b)^2 = a^2 + 2ab + b^2",
            t2c={"a": BLUE, "b": GREEN}
        )

        # Expanded form
        eq2 = Tex(
            R"(a + b)^2 = (a + b)(a + b)",
            t2c={"a": BLUE, "b": GREEN}
        )

        # Show transformation
        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
```

### 高亮特定项

```python
class HighlightTerms(Scene):
    def construct(self):
        # Quadratic formula with highlighted discriminant
        formula = Tex(
            R"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            t2c={
                "x": WHITE,
                "b": BLUE,
                "a": GREEN,
                "c": YELLOW,
                R"b^2 - 4ac": RED  # Discriminant in red
            }
        )

        # Add label for discriminant
        discriminant_label = Text("Discriminant", color=RED, font_size=30)
        discriminant_label.next_to(formula, DOWN)

        self.play(Write(formula))
        self.play(FadeIn(discriminant_label, shift=UP))
        self.wait()
```

## LaTeX 运算符着色

```python
# Color different operator types
expression = Tex(
    R"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}",
    t2c={
        R"\int": BLUE,          # Integral
        "e": GREEN,              # Exponential
        R"\pi": RED,            # Pi
        "x": YELLOW,            # Variable
        "2": ORANGE             # Exponent
    }
)
```

## 最佳实践

1. **使用 R 原始字符串**：在 ManimGL 中 LaTeX 字符串应始终使用 `R"..."`
2. **先测试 isolate**：用 `isolate=` 验证哪些部分可以独立着色
3. **一致的配色方案**：使用有意义的配色（例如变量用蓝色、常量用绿色）
4. **避免过度着色**：颜色过多会分散注意力
5. **用颜色强调重点**：高亮你希望观众关注的部分

## 常见模式

### 为数学内容建立配色方案

```python
MATH_COLORS = {
    "variables": BLUE,
    "constants": GREEN,
    "operators": YELLOW,
    "results": RED
}

equation = Tex(
    R"x^2 + y^2 = r^2",
    t2c={
        "x": MATH_COLORS["variables"],
        "y": MATH_COLORS["variables"],
        "r": MATH_COLORS["constants"]
    }
)
```

### 动画改变颜色

```python
class AnimateColorChange(Scene):
    def construct(self):
        formula = Tex(R"f(x) = x^2")

        # Start with one color
        formula.set_color(BLUE)
        self.add(formula)
        self.wait()

        # Animate to different colors
        self.play(formula.animate.set_color_by_tex("x", RED))
        self.wait()
```

## 故障排查

### 若 t2c 不起作用：

1. 检查子串是否与 LaTeX 字符串中完全一致
2. 使用 `isolate=` 分离需要着色的部分
3. 记住 LaTeX 中空格会影响匹配
4. 使用原始字符串 `R"..."`，不要用普通字符串

### 常见问题示例：

```python
# This might not work if spaces don't match:
wrong = Tex(R"a+b", t2c={"a + b": RED})  # Won't match "a+b"

# This will work:
right = Tex(R"a + b", t2c={"a": RED, "b": BLUE})
```
