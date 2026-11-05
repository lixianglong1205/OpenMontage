# ManimGL 动画

## 动画系统概览

ManimGL 的动画系统围绕 `Animation` 基类构建。专用子类负责创建、变换与强调等效果。

## 播放动画

```python
# Single animation
self.play(ShowCreation(circle))

# Multiple animations simultaneously
self.play(
    ShowCreation(circle),
    Write(text),
)

# With run_time
self.play(ShowCreation(circle), run_time=2)

# With rate function
self.play(ShowCreation(circle), rate_func=smooth)
```

## 创建类动画

| 动画 | 说明 |
|-----------|-------------|
| `ShowCreation` | 绘制 VMobject 的路径（不是 ManimCE 中的 `Create`） |
| `Write` | 书写文本或 LaTeX |
| `DrawBorderThenFill` | 先描边再填充 |
| `FadeIn` | 淡入，可选方向 |
| `FadeOut` | 淡出，可选方向 |
| `GrowFromCenter` | 从中心放大 |
| `GrowFromPoint` | 从某点放大 |
| `GrowArrow` | 箭头专用 |

```python
# ShowCreation for paths
self.play(ShowCreation(circle))

# Write for text
self.play(Write(Tex(R"\pi")))

# FadeIn with direction
self.play(FadeIn(square, shift=UP))
```

## 变换类动画

| 动画 | 说明 |
|-----------|-------------|
| `Transform` | 将一个 mobject 变形为另一个（会修改原对象） |
| `ReplacementTransform` | 用目标对象替换源对象 |
| `TransformMatchingShapes` | 匹配相似形状 |
| `TransformMatchingTex` | 匹配 LaTeX 部分 |
| `FadeTransform` | 变换同时淡入淡出 |
| `MoveToTarget` | 移动到 mobject 的 `.target` |

```python
# Transform (modifies circle, becomes square)
self.play(Transform(circle, square))

# ReplacementTransform (removes circle, adds square)
self.play(ReplacementTransform(circle, square))

# Using .target
circle.generate_target()
circle.target.shift(RIGHT * 2)
circle.target.set_color(RED)
self.play(MoveToTarget(circle))
```

## 强调类动画

| 动画 | 说明 |
|-----------|-------------|
| `Indicate` | 闪烁/脉冲以吸引注意 |
| `ShowPassingFlash` | 沿路径闪光 |
| `Flash` | 光线爆发 |
| `Circumscribe` | 在周围画圆/矩形 |
| `Wiggle` | 摆动 mobject |
| `FlashAround` | 对象周围的闪光效果 |

```python
self.play(Indicate(important_text))
self.play(FlashAround(equation, run_time=2))
```

## 位移动画

```python
# Using .animate syntax
self.play(circle.animate.shift(RIGHT * 2))
self.play(circle.animate.scale(2).set_color(RED))

# Rotate
self.play(Rotate(square, PI/2))
self.play(Rotate(square, 90 * DEGREES))  # Same thing

# MoveAlongPath
path = Line(LEFT, RIGHT)
self.play(MoveAlongPath(dot, path))
```

## LaggedStart 与组

```python
# Staggered animations
self.play(LaggedStart(
    *[ShowCreation(mob) for mob in mobjects],
    lag_ratio=0.2
))

# AnimationGroup for simultaneous
self.play(AnimationGroup(
    ShowCreation(circle),
    Write(text),
    lag_ratio=0  # Simultaneous
))

# Succession for sequential
self.play(Succession(
    ShowCreation(circle),
    Write(text),
))
```

## 动画参数

所有动画的常用参数：

| 参数 | 说明 |
|-----------|-------------|
| `run_time` | 持续时间（秒） |
| `rate_func` | 缓动函数（smooth、linear 等） |
| `lag_ratio` | 分组动画的交错比例 |
| `remover` | 动画结束后移除 mobject |
| `introducer` | 在动画开始时添加 mobject |

```python
self.play(
    ShowCreation(circle),
    run_time=3,
    rate_func=there_and_back,
)
```

## 速率函数（Rate Functions）

常用 rate function：
- `smooth` - 默认平滑缓动
- `linear` - 匀速
- `rush_into` - 快起慢停
- `rush_from` - 慢起快停
- `there_and_back` - 去而复返
- `double_smooth` - 更平滑

## 等待

```python
self.wait()       # Default pause
self.wait(2)      # 2 second pause
self.wait(0.5)    # Half second
```
