---
name: animations
description: Manim 中的动画类、播放动画与动画时序
metadata:
  tags: animation, play, run_time, rate_func, animate
---

# Manim 中的动画

动画会在一段时间内将 mobject 从一种状态插值到另一种状态。通过 `self.play()` 播放。

## `.animate` 语法

最常见的动画方式是使用 `.animate` 属性：

```python
# Move a square to the right
self.play(square.animate.shift(RIGHT))

# Scale up
self.play(circle.animate.scale(2))

# Change color
self.play(text.animate.set_color(RED))

# Chain multiple changes
self.play(square.animate.shift(RIGHT).rotate(PI/4).set_color(BLUE))
```

## 动画参数

### run_time
控制动画时长（秒）（默认：1）。

```python
self.play(Create(circle), run_time=2)  # 2 second animation
self.play(Create(circle), run_time=0.5)  # Half second
```

### rate_func
控制动画的时间曲线（缓动）。

```python
from manim import smooth, linear, there_and_back

self.play(square.animate.shift(RIGHT), rate_func=smooth)
self.play(square.animate.shift(RIGHT), rate_func=linear)
self.play(square.animate.shift(RIGHT), rate_func=there_and_back)
```

## 播放多个动画

### 同时播放

```python
# All play at the same time
self.play(
    Create(circle),
    FadeIn(square),
    Write(text)
)
```

### 顺序播放

```python
# One after another
self.play(Create(circle))
self.play(FadeIn(square))
self.play(Write(text))

# Or use Succession
self.play(Succession(
    Create(circle),
    FadeIn(square),
    Write(text)
))
```

## 常用动画类

### 创建类动画
```python
Create(mobject)           # Draw the mobject progressively
Write(text)               # Write text/equations
FadeIn(mobject)           # Fade in from transparent
DrawBorderThenFill(mob)   # Draw outline, then fill
GrowFromCenter(mobject)   # Grow from center point
```

### 移除类动画
```python
FadeOut(mobject)          # Fade to transparent
Uncreate(mobject)         # Reverse of Create
ShrinkToCenter(mobject)   # Shrink to center and disappear
```

### 变换类动画
```python
Transform(mob1, mob2)              # Morph mob1 into mob2
ReplacementTransform(mob1, mob2)   # Replace mob1 with mob2
TransformFromCopy(mob1, mob2)      # Keep mob1, create mob2
```

### 移动类动画
```python
MoveToTarget(mobject)     # Move to preset target
Rotate(mobject, angle)    # Rotate by angle
Circumscribe(mobject)     # Draw attention with circle
```

## 动画与即时变更

```python
# Animated change (visible transition)
self.play(circle.animate.set_color(RED))

# Instant change (no animation)
circle.set_color(RED)
self.add(circle)
```

## 最佳实践

1. **简单变换优先用 `.animate`** — 比显式 Animation 类更简洁
2. **保持合理的 run_time** — 多数动画 0.5–2 秒为宜
3. **用 rate_func 提升观感** — 通常 `smooth` 优于 `linear`
4. **将相关动画成组** — 概念上相关的动画应同时播放
