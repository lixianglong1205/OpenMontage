---
name: latex
description: Manim 中的 MathTex、Tex、LaTeX 渲染与公式样式
metadata:
  tags: latex, mathtex, tex, equation, formula, math
---

# Manim 中的 LaTeX

Manim 使用 LaTeX 渲染数学表达式和格式化文本。

## MathTex 与 Tex

- **MathTex**：自动将内容包裹在数学模式（`align*` 环境）中
- **Tex**：原始 LaTeX——由你控制模式

```python
from manim import *

class LaTeXComparison(Scene):
    def construct(self):
        # MathTex - auto math mode
        math = MathTex(r"E = mc^2")

        # Tex - need explicit math delimiters
        tex = Tex(r"$E = mc^2$")

        # Both render the same
        VGroup(math, tex).arrange(DOWN)
        self.add(math, tex)
```

## 基础 MathTex

```python
class MathTexExample(Scene):
    def construct(self):
        # Simple equation
        eq1 = MathTex(r"x^2 + y^2 = z^2")

        # Fractions
        eq2 = MathTex(r"\frac{a}{b}")

        # Square roots
        eq3 = MathTex(r"\sqrt{2}")

        # Greek letters
        eq4 = MathTex(r"\alpha + \beta = \gamma")

        # Integrals
        eq5 = MathTex(r"\int_0^\infty e^{-x} dx")

        # Summations
        eq6 = MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n^2}")

        equations = VGroup(eq1, eq2, eq3, eq4, eq5, eq6).arrange_in_grid(2, 3)
        self.add(equations)
```

## 为公式各部分着色

### 使用 set_color_by_tex

```python
class ColoredEquation(Scene):
    def construct(self):
        eq = MathTex(r"e^{i\pi} + 1 = 0")
        eq.set_color_by_tex("e", RED)
        eq.set_color_by_tex(r"\pi", BLUE)
        eq.set_color_by_tex("i", GREEN)
        self.add(eq)
```

### 使用 substrings_to_isolate

若要精确着色，先隔离子串：

```python
class IsolatedColoring(Scene):
    def construct(self):
        eq = MathTex(
            r"e^x = x^0 + x^1 + \frac{1}{2}x^2 + \cdots",
            substrings_to_isolate=["x"]
        )
        eq.set_color_by_tex("x", YELLOW)
        self.add(eq)
```

### 使用 index_labels 调试

```python
class DebugLabels(Scene):
    def construct(self):
        eq = MathTex(r"\frac{a}{b}")
        # Add index labels to see which index is which part
        self.add(index_labels(eq[0]))
        self.add(eq)
```

### 直接索引

```python
eq = MathTex(r"a + b = c")
eq[0][0].set_color(RED)   # 'a'
eq[0][2].set_color(BLUE)  # 'b'
eq[0][4].set_color(GREEN) # 'c'
```

## 多部分公式

将公式拆成多个部分以便单独控制：

```python
class MultiPartEquation(Scene):
    def construct(self):
        eq = MathTex("a", "^2", "+", "b", "^2", "=", "c", "^2")

        eq[0].set_color(RED)    # a
        eq[3].set_color(BLUE)   # b
        eq[6].set_color(GREEN)  # c

        self.play(Write(eq))
```

## 含数学的文本（Tex）

```python
class MixedContent(Scene):
    def construct(self):
        # Mix text and math
        tex = Tex(r"The area is $A = \pi r^2$")
        self.play(Write(tex))
```

## 自定义 LaTeX 宏包

```python
class CustomPackage(Scene):
    def construct(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{mathrsfs}")

        eq = Tex(
            r"$\mathscr{L}$",
            tex_template=template
        )
        self.add(eq)
```

## 公式对齐

```python
class AlignedEquations(Scene):
    def construct(self):
        eqs = MathTex(
            r"a &= b + c \\",
            r"d &= e + f + g \\",
            r"h &= i"
        )
        self.add(eqs)
```

## 常用 LaTeX 符号

```python
# Greek letters
MathTex(r"\alpha \beta \gamma \delta \epsilon")
MathTex(r"\Gamma \Delta \Theta \Lambda \Pi")

# Operators
MathTex(r"\times \div \pm \mp \cdot")

# Relations
MathTex(r"\leq \geq \neq \approx \equiv")

# Arrows
MathTex(r"\rightarrow \leftarrow \Rightarrow \Leftrightarrow")

# Sets
MathTex(r"\in \notin \subset \supset \cup \cap")

# Calculus
MathTex(r"\int \iint \oint \partial \nabla")
```

## 字号

```python
# Using font_size parameter
eq = MathTex(r"E = mc^2", font_size=72)

# Using scale
eq = MathTex(r"E = mc^2").scale(2)
```

## 最佳实践

1. **使用原始字符串**——LaTeX 始终使用 `r"..."`
2. **纯数学用 MathTex**——比手动加 `$...$` 更简单
3. **混合内容用 Tex**——文本与数学混排时
4. **拆分以便动画控制**——将要分别动画的部分拆开
5. **使用 substrings_to_isolate**——可靠地为重复元素着色
