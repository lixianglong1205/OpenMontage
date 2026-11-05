---
name: updaters
description: 更新器（Updater）、ValueTracker 与动态动画
metadata:
  tags: updater, valuetracker, dynamic, always, add_updater
---

# 更新器与动态动画

更新器（Updater）使 mobject 能根据其他数值或 mobject 自动更新。

## 基础更新器

添加一个在每一帧都会执行的函数。

```python
from manim import *

class UpdaterExample(Scene):
    def construct(self):
        dot = Dot()
        label = Text("Follow me").next_to(dot, UP)

        # Label always follows the dot
        label.add_updater(lambda m: m.next_to(dot, UP))

        self.add(dot, label)
        self.play(dot.animate.shift(RIGHT * 3), run_time=2)
        self.play(dot.animate.shift(DOWN * 2), run_time=2)
```

## 更新器语法

```python
# Lambda function
mobject.add_updater(lambda m: m.move_to(target.get_center()))

# Named function
def follow_target(mob):
    mob.next_to(target, RIGHT)

mobject.add_updater(follow_target)

# With dt (delta time) parameter
def time_based_update(mob, dt):
    mob.rotate(dt * PI)  # Rotate based on time elapsed

mobject.add_updater(time_based_update)
```

## ValueTracker

一种持有数值的 mobject，非常适合用于动画化参数。

```python
class ValueTrackerExample(Scene):
    def construct(self):
        # Create tracker
        tracker = ValueTracker(0)

        # Create number display
        number = DecimalNumber(0, num_decimal_places=2)
        number.add_updater(lambda m: m.set_value(tracker.get_value()))

        # Create circle that grows with tracker
        circle = Circle()
        circle.add_updater(lambda m: m.set_width(tracker.get_value()))

        self.add(number, circle)

        # Animate the tracker
        self.play(tracker.animate.set_value(4), run_time=3)
        self.play(tracker.animate.set_value(1), run_time=2)
```

### ValueTracker 操作

```python
tracker = ValueTracker(5)

# Get and set value
current = tracker.get_value()
tracker.set_value(10)

# Increment
tracker.increment_value(2.5)

# Arithmetic operators (direct manipulation, no animation)
tracker += 1
tracker -= 2
tracker *= 3
tracker /= 2

# Animate changes
self.play(tracker.animate.set_value(100))
self.play(tracker.animate.increment_value(-50))
```

## 与 ValueTracker 配合的 DecimalNumber

显示随 tracker 变化的数字：

```python
class NumberDisplay(Scene):
    def construct(self):
        tracker = ValueTracker(0)

        number = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=True,
            font_size=72
        )
        number.add_updater(lambda m: m.set_value(tracker.get_value()))
        number.add_updater(lambda m: m.move_to(ORIGIN))

        self.add(number)
        self.play(tracker.animate.set_value(100), run_time=3)
```

## always_redraw

根据当前数值在每一帧重新创建 mobject。

```python
class AlwaysRedrawExample(Scene):
    def construct(self):
        tracker = ValueTracker(1)

        # Line that always connects two points based on tracker
        line = always_redraw(
            lambda: Line(
                LEFT * 2,
                RIGHT * 2 * tracker.get_value()
            )
        )

        self.add(line)
        self.play(tracker.animate.set_value(2), run_time=2)
        self.play(tracker.animate.set_value(0.5), run_time=2)
```

## 常见更新器模式

### 跟随另一个 Mobject
```python
follower.add_updater(lambda m: m.move_to(leader.get_center()))
follower.add_updater(lambda m: m.next_to(leader, RIGHT))
```

### 指向另一个 Mobject
```python
arrow = Arrow(ORIGIN, RIGHT)
arrow.add_updater(lambda m: m.put_start_and_end_on(
    start.get_center(),
    end.get_center()
))
```

### 持续旋转
```python
mobject.add_updater(lambda m, dt: m.rotate(dt * PI))
```

### 匹配属性
```python
# Match color
follower.add_updater(lambda m: m.set_color(leader.get_color()))

# Match position with offset
follower.add_updater(lambda m: m.move_to(leader.get_center() + UP))
```

## 移除更新器

```python
# Remove specific updater
mobject.remove_updater(updater_function)

# Remove all updaters
mobject.clear_updaters()

# Suspend temporarily
mobject.suspend_updating()
mobject.resume_updating()
```

## 动画中的更新器

播放动画时更新器仍会继续运行：

```python
class UpdaterDuringAnimation(Scene):
    def construct(self):
        dot = Dot()
        trail = TracedPath(dot.get_center, stroke_color=YELLOW)

        self.add(dot, trail)
        self.play(dot.animate.shift(RIGHT * 3 + UP * 2), run_time=3)
```

## TracedPath

用于绘制轨迹的内置更新器：

```python
class TracedPathExample(Scene):
    def construct(self):
        dot = Dot()
        path = TracedPath(dot.get_center, stroke_width=2, stroke_color=BLUE)

        self.add(dot, path)
        self.play(
            dot.animate.shift(RIGHT * 2),
            dot.animate.shift(UP * 2),
            run_time=3
        )
```

## 最佳实践

1. **用 ValueTracker 驱动需要动画化的参数** — 清晰且易于控制
2. **复杂图形用 always_redraw** — 当手写更新器变得繁琐时
3. **用完后清除更新器** — 避免性能问题
4. **保持更新器函数简单** — 复杂逻辑会拖慢渲染
5. **基于时间的动画使用 dt** — 与帧率无关
