# ManimGL 中的动画组

动画组（Animation Groups）用于协调多个动画，使它们同时播放、顺序播放或以交错时序播放。

## AnimationGroup

将多个动画一起运行。

### 基本用法

```python
from manimlib import *

class GroupExample(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        circle.shift(LEFT * 2)
        square.shift(RIGHT * 2)

        # Run both animations simultaneously
        self.play(AnimationGroup(
            ShowCreation(circle),
            ShowCreation(square)
        ))
        self.wait()
```

### 简写语法

```python
# Equivalent to AnimationGroup
self.play(
    ShowCreation(circle),
    ShowCreation(square)
)
```

## LaggedStart

以交错延迟启动各动画。

### 基本 LaggedStart

```python
class LaggedStartExample(Scene):
    def construct(self):
        circles = VGroup(*[
            Circle(radius=0.5).shift(i * RIGHT)
            for i in range(-3, 4)
        ])

        # Staggered creation
        self.play(LaggedStart(
            *[ShowCreation(c) for c in circles],
            lag_ratio=0.2,  # Delay ratio between animations
            run_time=3
        ))
        self.wait()
```

### lag_ratio 参数

```python
# lag_ratio controls the delay
# 0 = all at once (like AnimationGroup)
# 1 = completely sequential (like Succession)
# 0.5 = overlapping animations

# Subtle overlap
self.play(LaggedStart(*animations, lag_ratio=0.1))

# More pronounced stagger
self.play(LaggedStart(*animations, lag_ratio=0.5))

# Nearly sequential
self.play(LaggedStart(*animations, lag_ratio=0.9))
```

## Succession

按顺序一个接一个地播放动画。

```python
class SuccessionExample(Scene):
    def construct(self):
        shapes = VGroup(
            Circle().shift(LEFT * 2),
            Square(),
            Triangle().shift(RIGHT * 2)
        )

        # One after another (no overlap)
        self.play(Succession(
            ShowCreation(shapes[0]),
            ShowCreation(shapes[1]),
            ShowCreation(shapes[2])
        ))
        self.wait()
```

### Succession 与多次顺序 play() 调用

```python
# Using Succession (all in one play call)
self.play(Succession(
    animation1,
    animation2,
    animation3
))

# Equivalent to separate play calls
self.play(animation1)
self.play(animation2)
self.play(animation3)
```

## 组合动画组

### 嵌套组

```python
class NestedGroups(Scene):
    def construct(self):
        # Top row
        top = VGroup(*[Circle().shift(i*RIGHT) for i in range(-2, 3)])

        # Bottom row
        bottom = VGroup(*[Square().shift(i*RIGHT + 2*DOWN) for i in range(-2, 3)])

        # Stagger within each row, but rows appear simultaneously
        self.play(
            LaggedStart(*[ShowCreation(c) for c in top], lag_ratio=0.2),
            LaggedStart(*[ShowCreation(s) for s in bottom], lag_ratio=0.2),
        )
        self.wait()
```

### 顺序组

```python
# First group, then second group
self.play(Succession(
    LaggedStart(*[ShowCreation(t) for t in top], lag_ratio=0.2),
    LaggedStart(*[ShowCreation(b) for b in bottom], lag_ratio=0.2)
))
```

## LaggedStartMap

对 mobject 应用动画构造器，并带交错时序。

```python
class LaggedStartMapExample(Scene):
    def construct(self):
        dots = VGroup(*[
            Dot().shift(i * RIGHT + j * UP)
            for i in range(-3, 4)
            for j in range(-2, 3)
        ])

        # Apply FadeIn to all dots with lag
        self.play(LaggedStartMap(
            FadeIn, dots,
            lag_ratio=0.05
        ))
        self.wait()
```

## 时序控制

### 组的 run_time

```python
# Total time for all animations
self.play(LaggedStart(
    *animations,
    lag_ratio=0.2,
    run_time=5  # Total duration
))

# Each animation's individual timing
self.play(LaggedStart(
    ShowCreation(circle, run_time=2),
    ShowCreation(square, run_time=1),
    lag_ratio=0.3
))
```

### 组与 rate_func

```python
# Apply rate function to entire group
self.play(
    LaggedStart(*animations, lag_ratio=0.2),
    rate_func=smooth
)

# Different rate functions for each
self.play(
    ShowCreation(circle, rate_func=linear),
    ShowCreation(square, rate_func=rush_into),
    ShowCreation(triangle, rate_func=rush_from)
)
```

## 实用示例

### 文字出现

```python
class TextReveal(Scene):
    def construct(self):
        title = Text("Animated Title", font_size=72)
        subtitle = Text("With smooth appearance", font_size=40)
        subtitle.next_to(title, DOWN)

        # Title letters appear one by one
        self.play(LaggedStart(
            *[FadeIn(char, shift=UP) for char in title],
            lag_ratio=0.05
        ))
        self.wait(0.3)

        # Subtitle fades in
        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait()
```

### 网格动画

```python
class GridAnimation(Scene):
    def construct(self):
        grid = VGroup(*[
            Square(side_length=0.8).shift([i, j, 0])
            for i in range(-3, 4)
            for j in range(-2, 3)
        ])

        # Ripple effect
        self.play(LaggedStart(
            *[ShowCreation(square) for square in grid],
            lag_ratio=0.02,
            run_time=4
        ))
        self.wait()
```

### 波浪效果

```python
class WaveEffect(Scene):
    def construct(self):
        dots = VGroup(*[
            Dot().shift(i * 0.5 * RIGHT)
            for i in range(-10, 11)
        ])

        # Wave up and down
        def wave_animation(dot, delay):
            return Succession(
                Wait(delay),
                dot.animate.shift(UP),
                dot.animate.shift(DOWN)
            )

        self.add(dots)
        self.play(*[
            wave_animation(dot, i * 0.1)
            for i, dot in enumerate(dots)
        ])
        self.wait()
```

### 级联效果

```python
class CascadeEffect(Scene):
    def construct(self):
        squares = VGroup(*[
            Square(side_length=1).shift(i * 1.5 * DOWN)
            for i in range(-2, 3)
        ])

        # Cascade from top to bottom
        self.play(LaggedStart(
            *[
                AnimationGroup(
                    square.animate.shift(RIGHT * 3),
                    square.animate.set_color(random_color())
                )
                for square in squares
            ],
            lag_ratio=0.3
        ))
        self.wait()
```

## 同时变换

### 多对象变换

```python
class SimultaneousTransforms(Scene):
    def construct(self):
        shapes = VGroup(
            Circle().shift(LEFT * 3),
            Square().shift(LEFT),
            Triangle().shift(RIGHT),
            Star().shift(RIGHT * 3)
        )

        self.play(LaggedStart(
            *[ShowCreation(s) for s in shapes],
            lag_ratio=0.2
        ))
        self.wait()

        # Transform all simultaneously with different targets
        targets = [
            Square().shift(LEFT * 3),
            Circle().shift(LEFT),
            Star().shift(RIGHT),
            Triangle().shift(RIGHT * 3)
        ]

        self.play(*[
            Transform(s, t)
            for s, t in zip(shapes, targets)
        ])
        self.wait()
```

## 最佳实践

1. **用 LaggedStart 营造视觉节奏**：让动画更有动感
2. **lag_ratio 调参**：
   - 0.1–0.3 适合轻微效果
   - 0.5 适合平衡的重叠
   - 0.8–1.0 接近顺序播放
3. **嵌套组**：组合使用以实现复杂编排
4. **总 run_time**：在组上设置以保持整体时长一致
5. **勿滥用**：过多交错动画容易分散注意力

## 常见模式

### 全部淡出

```python
# Fade out all objects with lag
self.play(LaggedStart(
    *[FadeOut(mob) for mob in self.mobjects],
    lag_ratio=0.1
))
```

### 逐步构建复杂图形

```python
# Build parts sequentially
self.play(Succession(
    ShowCreation(axes),
    ShowCreation(graph),
    Write(labels),
    FadeIn(legend)
))
```

### 揭示示意图

```python
# Reveal components with rhythm
components = [background, main_shape, decorations, labels]
self.play(LaggedStart(
    *[FadeIn(c, scale=0.8) for c in components],
    lag_ratio=0.4
))
```

### 同步移动

```python
# Move multiple objects together
objects = VGroup(circle, square, triangle)
self.play(*[
    obj.animate.shift(RIGHT * 2)
    for obj in objects
])
```

## 完整示例

```python
class ComprehensiveGrouping(Scene):
    def construct(self):
        # Title
        title = Text("Animation Groups", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Create grid of dots
        dots = VGroup(*[
            Dot(color=interpolate_color(BLUE, RED, i/20))
            .shift([
                (i % 7 - 3) * 0.8,
                (i // 7 - 1.5) * 0.8,
                0
            ])
            for i in range(21)
        ])

        # Lagged appearance
        self.play(LaggedStart(
            *[FadeIn(dot, scale=0.5) for dot in dots],
            lag_ratio=0.05,
            run_time=3
        ))
        self.wait()

        # Synchronized color change
        self.play(*[
            dot.animate.set_color(YELLOW)
            for dot in dots
        ])
        self.wait()

        # Cascade disappearance
        self.play(LaggedStart(
            *[FadeOut(dot, shift=DOWN) for dot in dots],
            lag_ratio=0.05,
            run_time=2
        ))

        # Clean up
        self.play(FadeOut(title))
        self.wait()
```

## 调试动画组

### 打印时序信息

```python
# Check total duration
group = LaggedStart(*animations, lag_ratio=0.2)
print(f"Group duration: {group.get_run_time()}")

# Visualize timing
for i, anim in enumerate(animations):
    print(f"Animation {i}: starts at {i * 0.2 * group.get_run_time()}")
```

### 测试 lag_ratio 取值

```python
# Try different values to find the right feel
for lag in [0.1, 0.3, 0.5, 0.7]:
    self.play(LaggedStart(*animations, lag_ratio=lag))
    self.wait()
```
