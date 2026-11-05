---
name: timing
description: 速率函数、easing、run_time 与动画时间控制
metadata:
  tags: timing, rate_func, easing, smooth, linear, run_time
---

# 动画时间控制

使用 timing 参数控制动画的速度与节奏感。

## run_time

控制动画持续多少秒。

```python
from manim import *

class RunTimeExample(Scene):
    def construct(self):
        circle = Circle()

        # Default (1 second)
        self.play(Create(circle))

        # Longer animation
        self.play(circle.animate.shift(RIGHT), run_time=3)

        # Quick animation
        self.play(circle.animate.set_color(RED), run_time=0.5)
```

## 速率函数（Rate Functions）

速率函数控制动画在时间轴上的推进方式（缓动 easing）。

### 使用速率函数

```python
self.play(
    circle.animate.shift(RIGHT),
    rate_func=smooth
)
```

### 常用速率函数

```python
# Smooth start and end (default for most animations)
smooth

# Constant speed
linear

# Start slow, end fast
rush_into

# Start fast, end slow
rush_from

# Go there and back
there_and_back

# Go there and back with pause
there_and_back_with_pause

# Double smooth (extra smooth)
double_smooth

# Stay put (useful for delays in AnimationGroup)
lingering
```

### Ease 函数（类似 CSS）

```python
# Ease in (start slow)
ease_in_sine
ease_in_quad
ease_in_cubic
ease_in_expo
ease_in_circ
ease_in_back    # Slight overshoot at start

# Ease out (end slow)
ease_out_sine
ease_out_quad
ease_out_cubic
ease_out_expo
ease_out_circ
ease_out_back   # Slight overshoot at end
ease_out_bounce # Bouncy ending

# Ease in-out (slow at both ends)
ease_in_out_sine
ease_in_out_quad
ease_in_out_cubic
ease_in_out_expo
ease_in_out_circ
ease_in_out_back
```

## 视觉对比

```python
class RateFuncComparison(Scene):
    def construct(self):
        funcs = [linear, smooth, rush_into, rush_from, there_and_back]
        names = ["linear", "smooth", "rush_into", "rush_from", "there_and_back"]

        dots = VGroup()
        labels = VGroup()

        for i, (func, name) in enumerate(zip(funcs, names)):
            dot = Dot().shift(LEFT * 4 + DOWN * i)
            label = Text(name, font_size=24).next_to(dot, LEFT)
            dots.add(dot)
            labels.add(label)

        self.add(dots, labels)

        self.play(*[
            dot.animate(rate_func=func).shift(RIGHT * 8)
            for dot, func in zip(dots, funcs)
        ], run_time=3)
```

## 组合 run_time 与 rate_func

```python
self.play(
    square.animate.shift(RIGHT * 3),
    run_time=2,
    rate_func=ease_out_bounce
)
```

## there_and_back

动画先向前播放，再反向回到起点。

```python
class ThereAndBackExample(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # Moves right then back to start
        self.play(
            square.animate.shift(RIGHT * 2),
            rate_func=there_and_back,
            run_time=2
        )
```

## 自定义速率函数

自定义速率函数（参数 t 从 0 到 1，返回值表示进度 0 到 1）：

```python
def my_rate_func(t):
    # Quadratic ease
    return t ** 2

self.play(
    circle.animate.shift(RIGHT),
    rate_func=my_rate_func
)
```

## wait() 时间控制

```python
# Wait for default time (1 second)
self.wait()

# Wait for specific duration
self.wait(2)    # 2 seconds
self.wait(0.5)  # Half second
```

## 动画速度倍率

在 AnimationGroup 上设置 `run_time` 会影响所有子动画：

```python
self.play(AnimationGroup(
    Create(circle),
    Create(square),
    lag_ratio=0.5
), run_time=3)  # Total duration is 3 seconds
```

## 最佳实践

1. **多数动画使用 smooth** - 观感自然
2. **匀速运动使用 linear** - 机械感、精确移动
3. **活泼效果使用 ease_out_bounce** - 更抓注意力
4. **run_time 保持在 0.5–3 秒** - 维持观众注意力
5. **强调时使用 there_and_back** - 临时展示后回到原位
6. **rate_func 与内容匹配** - 优雅用 smooth，趣味用弹跳类
