# ManimGL 场景

## 场景类型

ManimGL 提供多种场景类型：

### InteractiveScene（推荐）

大多数开发时的默认选择。支持使用 `-se` 标志进入交互模式。

```python
from manimlib import *

class MyScene(InteractiveScene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))
        self.wait()
```

### Scene（基类）

不带交互功能的基础场景：

```python
class BasicScene(Scene):
    def construct(self):
        self.play(Write(Text("Hello")))
```

### ThreeDScene

用于 3D 动画，并具备合适的相机设置：

```python
from manimlib import *

class My3DScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)
        self.camera.frame.reorient(-45*DEGREES, 75*DEGREES)
```

## construct 方法

所有场景逻辑都写在 `construct()` 中：

```python
class MyScene(InteractiveScene):
    def construct(self):
        # 1. Create mobjects
        circle = Circle(color=BLUE)
        square = Square(color=RED)

        # 2. Position them
        circle.shift(LEFT * 2)
        square.shift(RIGHT * 2)

        # 3. Animate
        self.play(ShowCreation(circle), ShowCreation(square))

        # 4. Wait for viewer
        self.wait(2)
```

## 添加与播放

```python
# Static add (instant, no animation)
self.add(circle)

# Animated add
self.play(ShowCreation(circle))
self.play(FadeIn(square))
```

## 场景方法

| 方法 | 说明 |
|--------|-------------|
| `self.play(*anims)` | 播放动画 |
| `self.wait(t)` | 等待 t 秒 |
| `self.add(*mobs)` | 立即添加 mobject |
| `self.remove(*mobs)` | 移除 mobject |
| `self.clear()` | 清除所有 mobject |
| `self.embed()` | 进入 IPython shell |

## 交互模式

使用 `-se` 标志运行，可从指定行进入：

```bash
manimgl scene.py MyScene -se 15
```

在 shell 中：
```python
checkpoint_paste()           # Run clipboard code with animations
checkpoint_paste(skip=True)  # Run instantly
checkpoint_paste(record=True) # Record while running
```

## 类属性

将场景配置定义为类属性：

```python
class MyScene(InteractiveScene):
    camera_class = ThreeDCamera  # Use 3D camera
    random_seed = 42             # For reproducibility

    def construct(self):
        ...
```
