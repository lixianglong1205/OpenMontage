---
name: animation-groups
description: 使用 AnimationGroup、LaggedStart、Succession 编排复杂动画序列
metadata:
  tags: animationgroup, laggedstart, succession, lag_ratio, sequence
---

# 动画组

控制多个动画如何一起播放。

## AnimationGroup

以可控时序同时播放多个动画。

```python
from manim import *

class AnimationGroupExample(Scene):
    def construct(self):
        circles = VGroup(*[Circle() for _ in range(5)]).arrange(RIGHT)

        # All animations play simultaneously (lag_ratio=0)
        self.play(AnimationGroup(
            *[Create(c) for c in circles],
            lag_ratio=0
        ))
```

### lag_ratio 参数

控制各动画开始之间的延迟：
- `lag_ratio=0`：全部同时开始
- `lag_ratio=0.5`：前一个完成 50% 时，下一个开始
- `lag_ratio=1`：前一个结束时，下一个才开始（顺序播放）

```python
class LagRatioDemo(Scene):
    def construct(self):
        squares = VGroup(*[Square() for _ in range(4)]).arrange(RIGHT)

        # Staggered start - each begins when previous is 25% done
        self.play(AnimationGroup(
            *[FadeIn(s) for s in squares],
            lag_ratio=0.25,
            run_time=2
        ))
```

## LaggedStart

便捷类，默认 `lag_ratio=0.05`（5% 重叠）。

```python
class LaggedStartExample(Scene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(10)]).arrange(RIGHT)

        # Rapid staggered animation
        self.play(LaggedStart(
            *[GrowFromCenter(d) for d in dots],
            lag_ratio=0.1
        ))
```

### 常见 LaggedStart 模式

```python
# Staggered fade in
self.play(LaggedStart(*[FadeIn(m) for m in mobjects], lag_ratio=0.2))

# Wave effect
self.play(LaggedStart(
    *[m.animate.shift(UP * 0.5) for m in mobjects],
    lag_ratio=0.1
))

# Staggered color change
self.play(LaggedStart(
    *[m.animate.set_color(RED) for m in mobjects],
    lag_ratio=0.15
))
```

## Succession

按顺序一个接一个播放动画（等价于 `lag_ratio=1`）。

```python
class SuccessionExample(Scene):
    def construct(self):
        circle = Circle().shift(LEFT * 2)
        square = Square()
        triangle = Triangle().shift(RIGHT * 2)

        # Animations play in sequence
        self.play(Succession(
            Create(circle),
            Create(square),
            Create(triangle)
        ))
```

### Succession 与多次 play() 调用

```python
# These are equivalent:

# Using Succession
self.play(Succession(
    Create(circle),
    Create(square)
))

# Using separate play calls
self.play(Create(circle))
self.play(Create(square))
```

当你希望把顺序动画当作一个整体处理时，Succession 很有用。

## 组合多种组类型

```python
class CombinedExample(Scene):
    def construct(self):
        group1 = VGroup(*[Circle() for _ in range(3)]).arrange(RIGHT).shift(UP)
        group2 = VGroup(*[Square() for _ in range(3)]).arrange(RIGHT).shift(DOWN)

        # First group appears with stagger, then second group
        self.play(Succession(
            LaggedStart(*[Create(c) for c in group1], lag_ratio=0.2),
            LaggedStart(*[Create(s) for s in group2], lag_ratio=0.2)
        ))
```

## LaggedStartMap

对 mobject 的所有子对象应用同一动画，并以交错时序播放。

```python
class LaggedStartMapExample(Scene):
    def construct(self):
        dots = VGroup(*[Dot(radius=0.16) for _ in range(35)]).arrange_in_grid(rows=5, cols=7)

        # Apply FadeIn to all dots with stagger
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.1))
        self.wait(0.5)

        # Change color with stagger using LaggedStart
        self.play(LaggedStart(
            *[dot.animate.set_color(YELLOW) for dot in dots],
            lag_ratio=0.05
        ))
```

LaggedStartMap 在对每个子对象应用相同动画时更简洁。若要改属性，请用 LaggedStart 配合 `.animate`。

## 带 run_time 的 AnimationGroup

总 `run_time` 会按 `lag_ratio` 在各动画之间分配。

```python
self.play(AnimationGroup(
    *[Create(c) for c in circles],
    lag_ratio=0.5,
    run_time=4  # Total duration is 4 seconds
))
```

## 实用示例

### 逐词出现文字

```python
class WordByWord(Scene):
    def construct(self):
        words = VGroup(
            Text("Hello"),
            Text("World"),
            Text("!")
        ).arrange(RIGHT)

        self.play(LaggedStart(
            *[Write(w) for w in words],
            lag_ratio=0.5
        ))
```

### 网格动画

```python
class GridAnimation(Scene):
    def construct(self):
        grid = VGroup(*[
            Square().scale(0.3)
            for _ in range(25)
        ]).arrange_in_grid(5, 5)

        # Diagonal wave effect
        self.play(LaggedStart(
            *[GrowFromCenter(s) for s in grid],
            lag_ratio=0.05
        ))
```

## 最佳实践

1. **用 LaggedStart 提升观感** — 交错动画更有动感
2. **lag_ratio 宜小（0.05–0.2）** — 过大则显得拖沓
3. **概念上独立的步骤用 Succession** — 动画在含义上彼此分开时
4. **随 lag_ratio 调整 run_time** — 对象越多，总时长往往需更长
