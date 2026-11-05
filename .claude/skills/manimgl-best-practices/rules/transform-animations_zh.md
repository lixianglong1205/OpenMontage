# ManimGL 中的变换动画

变换动画可将一个 mobject（数学对象）变形为另一个，或对 mobject 的属性变化进行动画。

## Transform

基础的 `Transform` 将一个 mobject 变为与另一个 mobject 相同的外观。

### 基础 Transform

```python
from manimlib import *

class BasicTransform(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        self.play(ShowCreation(square))
        self.wait()

        # Transform square into circle
        self.play(Transform(square, circle))
        self.wait()

        # Note: After transform, square now looks like circle
        # but it's still the square object
```

### 要点

执行 `Transform(A, B)` 之后：
- 对象 A 仍保留在场景中
- 对象 A 现在看起来像 B
- 对象 B 不会被加入场景

## ReplacementTransform

`ReplacementTransform` 用目标对象替换源对象。

```python
class ReplacementTransformExample(Scene):
    def construct(self):
        square = Square(color=BLUE)
        circle = Circle(color=RED)

        self.play(ShowCreation(square))
        self.wait()

        # Replace square with circle
        self.play(ReplacementTransform(square, circle))
        self.wait()

        # After this, circle is in the scene, not square
```

### 如何选择

```python
# Use Transform when:
# - You want to keep the same mobject reference
square.transform_into_circle = lambda: Transform(square, Circle())

# Use ReplacementTransform when:
# - You want to swap objects
# - The target object should remain
self.play(ReplacementTransform(old_text, new_text))
```

## TransformMatchingTex

通过匹配子串，对 LaTeX 表达式进行变形。

```python
class TexTransformExample(Scene):
    def construct(self):
        eq1 = Tex(R"a^2 + b^2 = c^2")
        eq2 = Tex(R"a^2 = c^2 - b^2")

        self.play(Write(eq1))
        self.wait()

        # Matching parts smoothly transform
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
```

### 配合颜色映射

```python
class ColoredTexTransform(Scene):
    def construct(self):
        # Set up equations with colors
        eq1 = Tex(
            R"(a + b)^2 = a^2 + 2ab + b^2",
            t2c={"a": BLUE, "b": GREEN}
        )
        eq2 = Tex(
            R"(a + b)^2 = (a + b)(a + b)",
            t2c={"a": BLUE, "b": GREEN}
        )

        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
```

### 使用 isolate 参数

```python
# Isolate specific parts for better matching
eq1 = Tex(
    R"x^2 + 2x + 1",
    isolate=["x", "^2", "+", "1", "2"]
)
eq2 = Tex(
    R"(x + 1)^2",
    isolate=["x", "^2", "+", "1", "(", ")"]
)

self.play(Write(eq1))
self.wait()
self.play(TransformMatchingTex(eq1, eq2))
```

### 使用 key 映射

```python
# Map specific substrings
eq1 = Tex(R"x^2 + y^2 = r^2")
eq2 = Tex(R"a^2 + b^2 = c^2")

self.play(Write(eq1))
self.wait()
self.play(TransformMatchingTex(
    eq1, eq2,
    key_map={
        "x": "a",
        "y": "b",
        "r": "c"
    }
))
```

## TransformMatchingShapes

通过匹配相似形状对对象进行变形。

```python
class ShapeTransform(Scene):
    def construct(self):
        # Source group
        source = VGroup(
            Circle(radius=0.5, color=BLUE),
            Square(side_length=1, color=GREEN),
            Triangle(color=YELLOW)
        )
        source.arrange(RIGHT, buff=0.5)

        # Target group
        target = VGroup(
            Circle(radius=1, color=RED),
            Square(side_length=0.5, color=PURPLE),
            Triangle(color=ORANGE)
        )
        target.arrange(DOWN, buff=0.5)

        self.play(ShowCreation(source))
        self.wait()
        self.play(TransformMatchingShapes(source, target))
        self.wait()
```

## MoveToTarget

为 mobject 设定目标状态并动画过渡到该状态。

```python
class MoveToTargetExample(Scene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))

        # Set target state
        circle.generate_target()
        circle.target.shift(RIGHT * 3)
        circle.target.scale(2)
        circle.target.set_color(YELLOW)

        # Animate to target
        self.play(MoveToTarget(circle))
        self.wait()
```

### 多个目标

```python
# Set up multiple mobjects with targets
square = Square()
triangle = Triangle()

square.generate_target()
square.target.shift(LEFT * 2)

triangle.generate_target()
triangle.target.shift(RIGHT * 2)

self.play(
    MoveToTarget(square),
    MoveToTarget(triangle)
)
```

## FadeTransform

在两个对象之间进行交叉淡入淡出。

```python
class FadeTransformExample(Scene):
    def construct(self):
        text1 = Text("Hello", font_size=72)
        text2 = Text("World", font_size=72)

        self.play(Write(text1))
        self.wait()

        # Smooth cross-fade
        self.play(FadeTransform(text1, text2))
        self.wait()
```

## Rotate

旋转 mobject。

```python
# Rotate by angle
square = Square()
self.play(Rotate(square, PI / 2))  # 90 degrees

# Rotate around a point
self.play(Rotate(square, PI, about_point=ORIGIN))

# Rotate around an axis (for 3D)
self.play(Rotate(cube, PI, axis=RIGHT))
```

## Rotating（连续旋转）

创建持续旋转动画。

```python
# Continuous rotation
square = Square()
self.play(Rotating(square, radians=2*PI, run_time=4))

# Infinite rotation with updater
square.add_updater(lambda m, dt: m.rotate(0.1 * dt))
self.wait(10)
```

## ScaleInPlace

在不改变中心位置的情况下缩放。

```python
circle = Circle()
self.play(ScaleInPlace(circle, 2))  # Double size

# Scale around a point
self.play(ScaleInPlace(circle, 0.5, about_point=RIGHT))
```

## ApplyMethod

对任意 mobject 方法进行动画。

```python
# Using .animate syntax (preferred)
self.play(circle.animate.shift(RIGHT))
self.play(circle.animate.scale(2))
self.play(circle.animate.set_color(BLUE))

# Old syntax (still works)
self.play(ApplyMethod(circle.shift, RIGHT))
self.play(ApplyMethod(circle.scale, 2))
```

## 复杂变换

### apply_complex_function

使用复数运算进行变换。

```python
class ComplexTransform(Scene):
    def construct(self):
        plane = ComplexPlane()
        plane.add_coordinate_labels(font_size=20)

        # Create shape on complex plane
        circle = Circle(radius=1, color=BLUE)

        self.add(plane, circle)
        self.wait()

        # Apply complex function (e.g., z^2)
        self.play(
            circle.animate.apply_complex_function(lambda z: z**2),
            run_time=3
        )
        self.wait()
```

### apply_function

使用任意函数进行变换。

```python
# Apply custom transformation
grid = NumberPlane()

def wavy_transform(point):
    x, y, z = point
    return np.array([
        x,
        y + 0.5 * np.sin(2 * x),
        z
    ])

self.play(
    grid.animate.apply_function(wavy_transform),
    run_time=3
)
```

## 变换序列

### 多步变换

```python
class TransformSequence(Scene):
    def construct(self):
        shapes = [
            Square(color=BLUE),
            Circle(color=GREEN),
            Triangle(color=YELLOW),
            Star(color=RED)
        ]

        current = shapes[0]
        self.play(ShowCreation(current))

        # Transform through each shape
        for next_shape in shapes[1:]:
            self.play(ReplacementTransform(current, next_shape))
            current = next_shape
            self.wait(0.3)
```

### 推导式变换

```python
class DerivationTransform(Scene):
    def construct(self):
        # Mathematical derivation
        steps = [
            Tex(R"x^2 - 4 = 0"),
            Tex(R"x^2 = 4"),
            Tex(R"x = \pm 2"),
        ]

        current = steps[0]
        self.play(Write(current))
        self.wait()

        for next_step in steps[1:]:
            next_step.move_to(current)
            self.play(TransformMatchingTex(current.copy(), next_step))
            current = next_step
            self.wait()
```

## 最佳实践

1. **Transform 与 ReplacementTransform**：
   - 需要保留对象引用时使用 `Transform`
   - 需要交换对象时使用 `ReplacementTransform`

2. **TransformMatchingTex**：
   - 使用 `isolate=` 控制匹配粒度
   - 使用 `key_map=` 做显式映射
   - 颜色保持一致以获得平滑过渡

3. **时间**：
   - 复杂变换使用更长的 `run_time`
   - 动画时长与内容重要性相匹配

4. **`.animate` 语法**：
   - 简单变换时优先使用
   - 更易读、更简洁

5. **路径弧度**：
   - 添加 `path_arc=90*DEGREES` 可让变换沿曲线路径进行

## 常见模式

### 方程变形

```python
eq = Tex(R"2x + 4 = 10")
self.play(Write(eq))

eq2 = Tex(R"2x = 6")
eq2.move_to(eq)
self.play(TransformMatchingTex(eq.copy(), eq2))

eq3 = Tex(R"x = 3")
eq3.move_to(eq2)
self.play(TransformMatchingTex(eq2.copy(), eq3))
```

### 形状变形

```python
shape = Circle()
self.play(ShowCreation(shape))

for new_shape in [Square(), Triangle(), Star(), Circle()]:
    self.play(Transform(shape, new_shape))
    self.wait(0.5)
```

### 文本替换

```python
text1 = Text("Before")
self.play(Write(text1))

text2 = Text("After")
text2.move_to(text1)
self.play(FadeTransform(text1, text2))
```

## 完整示例

```python
class ComprehensiveTransform(Scene):
    def construct(self):
        # Title
        title = Text("Transformations", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))

        # Shape transformations
        shape = Square(color=BLUE)
        self.play(ShowCreation(shape))
        self.wait()

        self.play(Transform(shape, Circle(color=GREEN)))
        self.wait()

        self.play(Transform(shape, Triangle(color=YELLOW)))
        self.wait()

        # Mathematical transformation
        eq1 = Tex(R"a^2 + b^2 = c^2")
        eq1.next_to(title, DOWN, buff=1)
        self.play(
            FadeOut(shape),
            Write(eq1)
        )
        self.wait()

        eq2 = Tex(R"c = \sqrt{a^2 + b^2}")
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        self.wait()

        # Clean up
        self.play(FadeOut(VGroup(title, eq2)))
```
