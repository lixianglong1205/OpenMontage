# ManimGL 帧（相机）控制

## CameraFrame

在 ManimGL 中，相机控制通过 `self.camera.frame` 完成（CameraFrame 是一个 Mobject）：

```python
frame = self.camera.frame

# Set euler angles for 3D orientation
frame.set_euler_angles(
    theta=-30 * DEGREES,
    phi=70 * DEGREES,
)
```

**注意：** 在 InteractiveScene 中，也可以使用 `self.frame` 作为快捷方式。

## CameraFrame 方法（来自官方文档）

CameraFrame 继承标准 Mobject 方法，并额外提供以下专用方法：

- `.to_default_state()` - 重置相机
- `.set_euler_angles(theta, phi, gamma)` - 设置全部角度
- `.set_theta(theta)` - 水平旋转
- `.set_phi(phi)` - 垂直旋转
- `.set_gamma(gamma)` - 滚转
- `.increment_theta(dtheta)` - 增加 theta
- `.increment_phi(dphi)` - 增加 phi
- `.increment_gamma(dgamma)` - 增加 gamma

还继承：`.shift()`、`.scale()`、`.move_to()`

```python
# Look down at 45 degrees, rotated 30 degrees
self.frame.reorient(45, -30, 0, ORIGIN, 8)

# Animate the reorientation
self.play(
    self.frame.animate.reorient(60, -45, 0, (1, 0, 0), 10),
    run_time=3
)
```

## 常用相机操作

### 缩放

```python
# Zoom in (smaller height = closer)
self.play(self.frame.animate.set_height(4))

# Zoom out
self.play(self.frame.animate.set_height(12))
```

### 平移

```python
# Move camera center
self.play(self.frame.animate.move_to(RIGHT * 3))

# Shift camera
self.play(self.frame.animate.shift(UP * 2))
```

### 组合运动

```python
self.play(
    self.frame.animate.reorient(50, -40, 0, (2, 1, 0), 6).set_anim_args(run_time=3)
)
```

## fix_in_frame()

在 3D 相机动画过程中，将 mobject 固定在屏幕空间中：

```python
title = Text("My Title")
title.to_edge(UP)
title.fix_in_frame()  # Call on the mobject, not the scene!

self.add(title)

# Title stays fixed while camera moves
self.play(self.frame.animate.reorient(60, -45, 0))
```

**与 ManimCE 的关键区别：** 在 ManimCE 中调用 `self.add_fixed_in_frame_mobjects(title)`。在 ManimGL 中调用 `title.fix_in_frame()`。

## set_floor_plane()

为 3D 场景设置地面平面朝向：

```python
self.set_floor_plane("xz")  # y is up, xz is floor
self.set_floor_plane("xy")  # z is up, xy is floor (default)
```

## 帧动画语法

```python
# Chain with set_anim_args for run_time
self.play(
    self.frame.animate.reorient(45, -30, 0, ORIGIN, 8).set_anim_args(run_time=2)
)

# Multiple frame operations
self.play(
    self.frame.animate.shift(RIGHT * 2).set_height(6),
    run_time=1.5
)
```

## 背景矩形

在带 3D 相机动画的场景中，添加背景：

```python
background = FullScreenRectangle()
background.set_fill(BLACK, 1)
background.fix_in_frame()
self.add(background)
```

## 完整 3D 示例

```python
class Camera3DDemo(InteractiveScene):
    def construct(self):
        # Background
        bg = FullScreenRectangle()
        bg.set_fill(GREY_E, 1)
        bg.fix_in_frame()
        self.add(bg)

        # Title fixed in frame
        title = Text("3D Demo")
        title.to_edge(UP)
        title.fix_in_frame()
        self.add(title)

        # 3D content
        cube = Cube(side_length=2)
        cube.set_color(BLUE)
        self.add(cube)

        # Animate camera
        self.play(
            self.frame.animate.reorient(60, -45, 0, ORIGIN, 8),
            run_time=3
        )

        # Rotate around
        self.play(
            self.frame.animate.reorient(60, 45, 0),
            run_time=4
        )
```
