---
name: camera
description: MovingCameraScene、缩放、平移与相机操控
metadata:
  tags: camera, zoom, pan, frame, movingcamerascene, 3d
---

# 相机控制

通过操控相机来控制观众看到的内容。

## MovingCameraScene

用于带相机运动（缩放、平移）的 2D 场景。

```python
from manim import *

class CameraExample(MovingCameraScene):
    def construct(self):
        circle = Circle()
        square = Square().shift(RIGHT * 3)
        self.add(circle, square)

        # Access camera frame
        # self.camera.frame is the viewable area
```

## 缩放

### 通过缩放帧实现放大/缩小

```python
class ZoomExample(MovingCameraScene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(100)])
        dots.arrange_in_grid(10, 10, buff=0.3)
        self.add(dots)

        # Zoom in (make frame smaller)
        self.play(self.camera.frame.animate.scale(0.5))
        self.wait()

        # Zoom out (make frame larger)
        self.play(self.camera.frame.animate.scale(4))
```

### 缩放到指定宽度

```python
class ZoomToWidth(MovingCameraScene):
    def construct(self):
        text = Text("Focus on me!")
        self.add(text)

        # Zoom to fit text with padding
        self.play(
            self.camera.frame.animate.set(width=text.width * 1.5)
        )
```

## 平移

### 将相机移动到某位置

```python
class PanExample(MovingCameraScene):
    def construct(self):
        c1 = Circle().shift(LEFT * 3)
        c2 = Circle().shift(RIGHT * 3)
        self.add(c1, c2)

        # Pan to first circle
        self.play(self.camera.frame.animate.move_to(c1))
        self.wait()

        # Pan to second circle
        self.play(self.camera.frame.animate.move_to(c2))
```

### 缩放与平移组合

```python
class ZoomAndPan(MovingCameraScene):
    def construct(self):
        square = Square().shift(LEFT * 2)
        triangle = Triangle().shift(RIGHT * 2)
        self.add(square, triangle)

        # Zoom in and pan simultaneously
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(square)
        )
        self.wait()

        # Move to triangle (still zoomed)
        self.play(self.camera.frame.animate.move_to(triangle))
```

## 保存与恢复相机状态

```python
class SaveRestoreCamera(MovingCameraScene):
    def construct(self):
        circle = Circle()
        self.add(circle)

        # Save current state
        self.camera.frame.save_state()

        # Make changes
        self.play(self.camera.frame.animate.scale(0.3).move_to(circle))
        self.wait()

        # Restore to saved state
        self.play(Restore(self.camera.frame))
```

## auto_zoom

自动缩放以适配 mobject。

```python
class AutoZoomExample(MovingCameraScene):
    def construct(self):
        squares = VGroup(*[
            Square().shift(RIGHT * i + UP * j)
            for i in range(-2, 3) for j in range(-2, 3)
        ])
        self.add(squares)

        # Zoom to fit specific mobject
        self.play(self.camera.auto_zoom(squares[0]))
        self.wait()

        # Zoom to fit all with margin
        self.play(self.camera.auto_zoom(squares, margin=1))
```

## 3D 相机（ThreeDScene）

```python
class ThreeDCameraExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Sphere()
        self.add(axes, sphere)

        # Set initial camera orientation
        self.set_camera_orientation(
            phi=75 * DEGREES,    # Angle from z-axis
            theta=-45 * DEGREES  # Angle around z-axis
        )
```

### 相机动画旋转

```python
class RotatingCamera(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.set_camera_orientation(phi=75 * DEGREES, theta=0)

        # Continuous rotation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
```

### 移动 3D 相机

```python
class Move3DCamera(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Animate camera movement
        self.move_camera(
            phi=45 * DEGREES,
            theta=45 * DEGREES,
            run_time=3
        )
```

## 相机背景

```python
class CameraBackground(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = BLUE_E

        circle = Circle()
        self.add(circle)
```

## 最佳实践

1. **缩放/平移请用 MovingCameraScene** — 普通 Scene 的相机是静态的
2. **复杂运动前先保存状态** — 便于恢复
3. **动态内容可用 auto_zoom** — 自动适配内容
4. **保持相机运动平滑** — 避免让观众头晕
5. **3D 相机旋转宜少用** — 容易让人迷失方向
