---
name: scenes
description: Manim 中的 Scene 结构、construct 方法及 Scene 类型
metadata:
  tags: scene, construct, setup, render, ThreeDScene, MovingCameraScene
---

# Manim 中的 Scene

Scene 是所有动画发生的画布。每个 Manim 动画都在 Scene 类中定义。

## 基本 Scene 结构

所有动画代码都位于 Scene 子类的 `construct()` 方法内。

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.wait(1)
```

## Scene 生命周期方法

### construct()
定义动画的主方法。渲染时会自动调用。

### setup()
在 `construct()` 之前调用。用于在动画逻辑开始之前需要完成的初始化。

```python
class MyScene(Scene):
    def setup(self):
        self.camera.background_color = BLUE_E

    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

## Scene 方法

### 添加与移除对象

```python
# Add without animation (instant)
self.add(mobject)
self.add(mobject1, mobject2, mobject3)

# Remove without animation
self.remove(mobject)

# Clear all mobjects
self.clear()
```

### 播放动画

```python
# Play a single animation
self.play(Create(circle))

# Play multiple animations simultaneously
self.play(Create(circle), FadeIn(square))

# With run_time
self.play(Create(circle), run_time=2)
```

### 等待

```python
# Wait for 1 second (default)
self.wait()

# Wait for specific duration
self.wait(2)
```

## Scene 类型

### Scene（默认）
用于大多数动画的标准 2D Scene。

### ThreeDScene
用于可控制相机朝向的 3D 动画。

```python
class My3DScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes()
        sphere = Sphere()
        self.add(axes, sphere)
```

### MovingCameraScene
用于需要相机移动（缩放、平移）的动画。

```python
class ZoomScene(MovingCameraScene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.play(self.camera.frame.animate.scale(0.5).move_to(circle))
```

## 单文件中的多个 Scene

渲染指定 Scene：
```bash
manim -pql file.py Scene1
```

渲染全部 Scene：
```bash
manim -pql -a file.py
```
