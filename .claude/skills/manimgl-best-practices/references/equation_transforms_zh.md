# 方程变换 - 参考指南

**示例文件**：`examples/equation_transforms.py`

## 用户查询场景

本示例适用于如下类型的需求：
- 「逐步展示方程推导」
- 「动画演示二次公式推导」
- 「高亮方程中的部分项」
- 「用颜色跟踪展示变量代换」
- 「用花括号标注方程各部分含义」

## 场景设计思路（3b1b 风格）

### 1. 核心概念
**数学推导**：逐步操纵方程时，对各项进行颜色编码并平滑动画化变换，会更清晰易懂。

### 2. 技术实现

#### 使用 t2c 为各项着色
```python
eq = Tex(
    r"ax^2 + bx + c = 0",
    t2c={"a": RED, "b": GREEN, "c": BLUE, "x": YELLOW}
)
```

#### 平滑的方程变换
```python
eq1 = Tex(r"ax^2 + bx + c = 0", t2c=colors)
eq2 = Tex(r"x^2 + \frac{b}{a}x + \frac{c}{a} = 0", t2c=colors)
self.play(TransformMatchingTex(eq1.copy(), eq2))
```

**要点**：`TransformMatchingTex` 会在两个方程之间匹配字符并平滑变形过渡。

#### 用 SurroundingRectangle 高亮
```python
part = eq[r"a^2"]  # Select by tex string
rect = SurroundingRectangle(part, color=RED, buff=0.05)
self.play(ShowCreation(rect))
```

#### 花括号标注
```python
brace = Brace(eq["F"], UP, color=BLUE)
label = brace.get_text("Force", font_size=30)
self.play(GrowFromCenter(brace), FadeIn(label, UP))
```

### 3. 场景变体

| 场景 | 用途 |
|-------|---------|
| `QuadraticFormula` | 完整推导并带步骤标签 |
| `HighlightAndTransform` | 高亮 + 视觉证明 |
| `BraceAnnotations` | F=ma 并标注各部分 |
| `ColorCodedSubstitution` | 换元法并跟踪颜色 |

## 关键模式

### 模式：步骤标签
```python
step_label = Text("Divide by a", font_size=24, color=GREY)
step_label.next_to(eq2, LEFT, buff=0.5)
self.play(FadeIn(step_label, LEFT))
```

### 模式：最终答案框
```python
final = Tex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
box = SurroundingRectangle(final, color=GOLD, buff=0.2)
self.play(ShowCreation(box))
```

### 模式：选取方程片段
```python
# By tex substring
eq["x^2"]  # Returns submobject matching "x^2"
eq[r"\frac{b}{a}"]  # LaTeX commands work too

# By index
eq[0]  # First character/group
```

## 运行命令

```bash
manimgl equation_transforms.py QuadraticFormula -w
manimgl equation_transforms.py HighlightAndTransform -w
manimgl equation_transforms.py BraceAnnotations -w
manimgl equation_transforms.py ColorCodedSubstitution -w
```
