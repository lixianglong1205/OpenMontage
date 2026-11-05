# ManimGL LaTeX（Tex 类）

## Tex 与 MathTex

**注意：** ManimGL 使用 `Tex` 类（不像 ManimCE 那样使用 `MathTex`）。

```python
# ManimGL - use Tex with capital R raw strings
formula = Tex(R"\int_0^1 x^2 \, dx = \frac{1}{3}")

# NOT like ManimCE:
# formula = MathTex(r"\int...")  # Wrong for ManimGL
```

## 使用大写 R 的原始字符串

始终使用大写 `R` 作为原始字符串前缀，以避免转义问题：

```python
# Good - capital R
Tex(R"\frac{a}{b}")
Tex(R"\vec{v}")
Tex(R"\sum_{n=1}^{\infty}")

# Also works but less readable
Tex("\\frac{a}{b}")
```

## 使用 t2c 进行颜色映射

使用 `t2c`（tex_to_color）参数为公式中的特定部分着色：

```python
equation = Tex(
    R"E = mc^2",
    t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
)
```

更复杂的着色示例：

```python
formula = Tex(
    R"\vec{F} = m\vec{a}",
    t2c={
        R"\vec{F}": BLUE,
        R"\vec{a}": RED,
        "m": GREEN,
    }
)
```

## set_color_by_tex

在创建后为部分公式着色：

```python
formula = Tex(R"\sum_{n=1}^{\infty} \frac{1}{n^2}")
formula.set_color_by_tex("n", BLUE)
formula.set_color_by_tex(R"\infty", YELLOW)
```

## 隔离子串

获取公式的各部分以便做动画：

```python
formula = Tex(R"a^2 + b^2 = c^2")

# Access by index
a_squared = formula[0]  # "a^2"

# Or use isolate parameter
formula = Tex(
    R"a^2", "+", R"b^2", "=", R"c^2",
)
# Now formula[0] is "a^2", formula[1] is "+", etc.
```

## Text 与 Tex

```python
# Regular text
text = Text("Hello World")

# LaTeX math
math = Tex(R"\pi \approx 3.14159")

# Mixed (use TexText for text in math context)
mixed = TexText("The value of ", R"$\pi$", " is important")
```

## TexText

用于可能包含行内数学公式的文本：

```python
sentence = TexText(
    "The area is ", R"$\pi r^2$", ".",
    t2c={R"$\pi r^2$": YELLOW}
)
```

## 对齐方程

```python
equations = Tex(R"""
    \begin{align*}
    f(x) &= x^2 + 2x + 1 \\
    &= (x + 1)^2
    \end{align*}
""")
```

## 常用 LaTeX 符号

```python
# Greek letters
Tex(R"\alpha, \beta, \gamma, \delta, \theta, \phi, \pi")

# Operators
Tex(R"\sum, \prod, \int, \oint, \partial")

# Relations
Tex(R"\leq, \geq, \neq, \approx, \equiv")

# Sets
Tex(R"\in, \subset, \cup, \cap, \emptyset")

# Arrows
Tex(R"\rightarrow, \leftarrow, \Rightarrow, \Leftrightarrow")

# Fractions
Tex(R"\frac{a}{b}, \dfrac{a}{b}")

# Roots
Tex(R"\sqrt{x}, \sqrt[3]{x}")

# Matrices
Tex(R"\begin{pmatrix} a & b \\ c & d \end{pmatrix}")
```

## 字号

```python
# Use font_size parameter
small = Tex(R"\pi", font_size=24)
large = Tex(R"\pi", font_size=72)

# Or scale after creation
small.scale(1.5)
```

## 背描边以提高可读性

将文字放在彩色背景上时：

```python
label = Tex(R"f(x)")
label.set_backstroke(BLACK, 5)  # Black outline
```

## 调试 LaTeX

若 LaTeX 无法正常渲染：

1. 检查 LaTeX 安装是否缺少宏包
2. 先尝试更简单的表达式
3. 查看输出目录中的中间 `.tex` 文件
4. 在数学模式中用 `\text{}` 表示普通文本
