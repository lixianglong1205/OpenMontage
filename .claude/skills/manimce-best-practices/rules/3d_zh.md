---
name: 3d
description: ThreeDScene、3D 对象、曲面与 3D 相机
metadata:
  tags: 3d, threedscene, surface, sphere, cube, camera
---

# Manim 中的 3D 图形

使用 ThreeDScene 创建 3D 可视化。

## ThreeDScene 基础

```python
from manim import *

class Basic3D(ThreeDScene):
    def construct(self):
        # Set camera angle
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Add 3D axes
        axes = ThreeDAxes()
        self.add(axes)
```

## 相机朝向

```python
class CameraOrientation(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        # phi: angle from z-axis (0 = top view, 90 = side view)
        # theta: rotation around z-axis
        # gamma: roll angle

        self.set_camera_orientation(
            phi=75 * DEGREES,
            theta=-45 * DEGREES,
            gamma=0
        )

        self.add(axes)
```

### 相机动画移动

```python
class AnimatedCamera(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.set_camera_orientation(phi=75*DEGREES, theta=0)

        # Animate camera movement
        self.move_camera(phi=45*DEGREES, theta=90*DEGREES, run_time=3)
```

### 持续相机旋转

```python
class RotatingCamera(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.set_camera_orientation(phi=75*DEGREES, theta=0)

        # Start ambient rotation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
```

## 3D 基本体

### Sphere

```python
class SphereExample(ThreeDScene):
    def construct(self):
        sphere = Sphere(radius=1, resolution=(20, 20))
        sphere.set_color(BLUE)

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(sphere)
```

### Cube / Prism

```python
class CubeExample(ThreeDScene):
    def construct(self):
        cube = Cube(side_length=2, fill_opacity=0.8)
        cube.set_color(RED)

        # Rectangular prism
        prism = Prism(dimensions=[3, 1, 2])

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(cube)
```

### Cylinder / Cone

```python
class CylinderCone(ThreeDScene):
    def construct(self):
        cylinder = Cylinder(radius=1, height=2, fill_opacity=0.8)
        cone = Cone(base_radius=1, height=2, fill_opacity=0.8)

        cylinder.shift(LEFT * 2)
        cone.shift(RIGHT * 2)

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(cylinder, cone)
```

### Torus

```python
class TorusExample(ThreeDScene):
    def construct(self):
        torus = Torus(major_radius=2, minor_radius=0.5)

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(torus)
```

## 3D 坐标轴

```python
class ThreeDAxesExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            z_length=6,
        )

        # Add axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(axes, x_label, y_label, z_label)
```

## 曲面图

```python
class SurfacePlot(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-2, 2])

        # Function z = f(x, y)
        surface = axes.plot_surface(
            lambda u, v: np.sin(u) * np.cos(v),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
            colorscale=[BLUE, GREEN, YELLOW, RED],
        )

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(axes, surface)
```

### Surface 类（独立使用）

```python
class SurfaceExample(ThreeDScene):
    def construct(self):
        def param_func(u, v):
            x = u
            y = v
            z = np.sin(np.sqrt(u**2 + v**2))
            return np.array([x, y, z])

        surface = Surface(
            param_func,
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
            fill_opacity=0.8,
        )
        surface.set_color_by_gradient(BLUE, GREEN)

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(surface)
```

## 3D 参数曲线

```python
class ParametricCurve3D(ThreeDScene):
    def construct(self):
        # Helix
        curve = ParametricFunction(
            lambda t: np.array([
                np.cos(t),
                np.sin(t),
                t * 0.2
            ]),
            t_range=[-4*PI, 4*PI],
            color=YELLOW
        )
        curve.set_shade_in_3d(True)

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(ThreeDAxes(), curve)
```

## 3D 着色

```python
class Shading3D(ThreeDScene):
    def construct(self):
        sphere = Sphere()

        # Enable shading for realistic lighting
        sphere.set_shade_in_3d(True)

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(sphere)
```

## Arrow3D 与 Line3D

```python
class Vectors3D(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        arrow = Arrow3D(ORIGIN, [2, 1, 2], color=RED)
        line = Line3D(ORIGIN, [-2, 1, 1], color=BLUE)

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(axes, arrow, line)
```

## 最佳实践

1. **始终设置相机朝向** — 默认视角可能无法很好展示 3D 效果
2. **使用 set_shade_in_3d 增强真实感** — 有助于形成深度感
3. **谨慎使用环境相机旋转** — 容易让观众迷失方向
4. **按所需细节匹配分辨率** — 分辨率越高，渲染越慢
5. **曲面使用 colorscale** — 便于表现高度或数值变化
