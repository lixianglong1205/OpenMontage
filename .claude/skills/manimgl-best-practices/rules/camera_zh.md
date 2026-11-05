# ManimGL 中的 Camera 与 Frame

ManimGL 的相机系统以 `CameraFrame` 为核心，可通过 `self.camera.frame` 访问。它让你能灵活控制 2D 与 3D 视角。

## 访问 Camera Frame

```python
from manimlib import *

class CameraExample(Scene):
    def construct(self):
        # Get the camera frame
        frame = self.camera.frame

        # frame is a Mobject, so it has all Mobject methods
        # move_to, shift, scale, rotate, etc.
```

## 2D 相机移动

### 基本移动

```python
# Shift the camera
self.play(frame.animate.shift(RIGHT * 2))

# Move to a specific position
self.play(frame.animate.move_to([3, 2, 0]))

# Scale (zoom)
self.play(frame.animate.scale(0.5))  # Zoom in
self.play(frame.animate.scale(2))    # Zoom out
```

### 跟随对象

```python
class FollowObject(Scene):
    def construct(self):
        frame = self.camera.frame
        dot = Dot(color=RED)

        # Camera follows dot
        frame.add_updater(lambda m: m.move_to(dot))

        # Move dot around
        self.add(dot)
        self.play(dot.animate.shift(RIGHT * 5), run_time=3)
        self.play(dot.animate.shift(UP * 3), run_time=2)
        self.wait()
```

### Frame 尺寸

```python
# Set frame width/height
frame.set_width(10)
frame.set_height(6)

# Animate frame size
self.play(frame.animate.set_width(20), run_time=2)
```

## 3D 相机朝向

### reorient() 方法

`reorient()` 是 ManimGL 中设置 3D 相机朝向的主要方式。

```python
# Signature:
# frame.reorient(theta, phi, gamma=0, center=ORIGIN, height=8)

# Parameters:
# - theta: Rotation around z-axis (azimuthal angle) in degrees
# - phi: Angle from z-axis (polar angle) in degrees
# - gamma: Roll angle in degrees (optional)
# - center: Point the camera looks at (optional)
# - height: Frame height (optional)

# Common views:
frame.reorient(0, 0)        # Front view (XY plane)
frame.reorient(20, 70)      # Isometric-like view
frame.reorient(0, 90)       # Top-down view (XY plane from above)
frame.reorient(90, 90)      # Side view (YZ plane)
frame.reorient(45, 45)      # Diagonal view
```

### 欧拉角（Euler Angles）

```python
# Set angles individually
frame.set_theta(30 * DEGREES)
frame.set_phi(70 * DEGREES)
frame.set_gamma(0 * DEGREES)

# Set all at once
frame.set_euler_angles(
    theta=30 * DEGREES,
    phi=70 * DEGREES,
    gamma=0 * DEGREES
)

# Get current angles
theta = frame.get_theta()
phi = frame.get_phi()
gamma = frame.get_gamma()
```

### 增量旋转

```python
# Increment angles (useful for animations)
frame.increment_theta(10 * DEGREES)
frame.increment_phi(5 * DEGREES)
frame.increment_gamma(2 * DEGREES)

# Animated increments
self.play(frame.animate.increment_theta(90 * DEGREES))
```

## 相机动画

### 简单相机动画

```python
class AnimateCamera(Scene):
    def construct(self):
        frame = self.camera.frame

        cube = Cube()
        self.add(cube)

        # Reorient to isometric view
        self.play(frame.animate.reorient(20, 70), run_time=2)
        self.wait()

        # Rotate around object
        self.play(frame.animate.increment_theta(360 * DEGREES), run_time=8)
        self.wait()
```

### 连续相机运动

```python
class ContinuousRotation(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        sphere = Sphere(radius=2, color=BLUE)
        self.add(sphere)

        # Add continuous rotation updater
        frame.add_updater(lambda m, dt: m.increment_theta(20 * dt))

        # Let it rotate for 10 seconds
        self.wait(10)

        # Stop rotation
        frame.clear_updaters()
        self.wait()
```

### 相机缩放

```python
class ZoomEffect(Scene):
    def construct(self):
        frame = self.camera.frame

        objects = VGroup(*[Square() for _ in range(5)])
        objects.arrange(RIGHT, buff=1)
        self.add(objects)

        # Zoom out to see all objects
        self.play(frame.animate.set_width(20), run_time=2)
        self.wait()

        # Zoom in on first object
        self.play(
            frame.animate.set_width(2).move_to(objects[0]),
            run_time=2
        )
        self.wait()
```

## 将 Mobject 固定于 Frame

### fix_in_frame() 方法

在相机移动时，让 2D 元素固定在屏幕空间中。

```python
class FixedInFrame(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        # 3D object that moves with camera
        cube = Cube(color=BLUE)
        self.add(cube)

        # 2D label that stays fixed
        title = Text("Rotating Cube", font_size=60)
        title.to_edge(UP)
        title.fix_in_frame()  # Fixes it to screen space
        self.add(title)

        # Rotate camera - cube rotates, title stays fixed
        self.play(frame.animate.reorient(60, 80), run_time=3)
        self.wait()
```

### 多个固定元素

```python
class MultipleFixed(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(30, 70)

        # 3D content
        surface = Sphere(radius=2, color=BLUE, opacity=0.7)
        self.add(surface)

        # Fixed UI elements
        title = Text("3D Visualization", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()

        subtitle = Text("Interactive Camera", font_size=30, color=GREY)
        subtitle.next_to(title, DOWN)
        subtitle.fix_in_frame()

        controls = Text("Press 'd' to rotate", font_size=24)
        controls.to_corner(DL)
        controls.fix_in_frame()

        self.add(title, subtitle, controls)

        # Rotate camera
        self.play(frame.animate.increment_theta(180 * DEGREES), run_time=6)
```

## 重置相机

```python
# Reset to default state
frame.to_default_state()

# Animate reset
self.play(frame.animate.to_default_state())
```

## 相机中心

```python
# Set what the camera looks at
frame.set_center([2, 3, 0])

# Animate center change
self.play(frame.animate.set_center([0, 0, 2]))

# Get current center
center = frame.get_center()
```

## 高级相机模式

### 绕对象轨道相机

```python
class OrbitCamera(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(30, 70)

        # Central object
        torus = Torus(r1=2, r2=0.5, color=YELLOW)
        self.add(torus)

        # Orbit 360 degrees
        self.play(
            frame.animate.increment_theta(360 * DEGREES),
            run_time=10,
            rate_func=linear
        )
```

### 相机沿路径移动

```python
class CameraPath(Scene):
    def construct(self):
        frame = self.camera.frame

        # Create path
        path = Circle(radius=5)
        self.add(path)

        # Dot to follow
        dot = Dot(color=RED)
        dot.move_to(path.point_from_proportion(0))

        # Camera follows dot
        frame.add_updater(lambda m: m.move_to(dot))

        # Move dot along path
        self.play(
            MoveAlongPath(dot, path),
            run_time=8,
            rate_func=linear
        )
```

### 多个相机位置

```python
class CameraTour(Scene):
    def construct(self):
        frame = self.camera.frame

        # Create scene
        objects = VGroup(
            Square(side_length=2, color=RED).shift(LEFT * 3),
            Circle(radius=1, color=BLUE),
            Triangle(color=GREEN).shift(RIGHT * 3)
        )
        self.add(objects)

        # Tour each object
        for obj in objects:
            self.play(
                frame.animate.set_width(3).move_to(obj),
                run_time=2
            )
            self.wait()

        # Return to overview
        self.play(
            frame.animate.set_width(14).move_to(ORIGIN),
            run_time=2
        )
```

### 使用 Updater 的动态相机

```python
class DynamicCamera(Scene):
    def construct(self):
        frame = self.camera.frame

        # Moving object
        dot = Dot(color=RED)

        # Camera tracks and zooms based on distance from origin
        def update_frame(frame):
            frame.move_to(dot)
            dist = np.linalg.norm(dot.get_center())
            frame.set_width(max(8, dist * 2))

        frame.add_updater(update_frame)

        # Move dot around
        self.add(dot)
        self.play(dot.animate.shift(RIGHT * 5 + UP * 3), run_time=4)
        self.play(dot.animate.shift(LEFT * 8 + DOWN * 2), run_time=4)
        self.wait()
```

## 光源

### 访问与移动光源

```python
class LightControl(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        # Get light source
        light = self.camera.light_source

        # Create 3D object
        sphere = Sphere(radius=2, color=BLUE)
        sphere.set_gloss(0.8)
        self.add(sphere)

        # Show light position (for debugging)
        light_indicator = Dot(color=YELLOW)
        light_indicator.add_updater(lambda m: m.move_to(light.get_center()))
        self.add(light_indicator)

        # Move light around
        self.play(light.animate.move_to([5, 5, 5]), run_time=2)
        self.wait()
        self.play(light.animate.move_to([-5, -5, 5]), run_time=2)
        self.wait()
```

## 最佳实践

1. **保存 frame 引用**：在开头使用 `frame = self.camera.frame`
2. **3D 使用 reorient()**：比逐个设置角度更清晰
3. **UI 使用 fix_in_frame()**：保持标签与标题可读
4. **平滑过渡**：为相机移动设置合适的 `run_time`
5. **rate_func=linear**：用于连续旋转
6. **to_default_state()**：需要时重置相机
7. **跟随用 Updater**：用 updater 跟踪移动对象

## 常见模式

### 缩放与平移

```python
def zoom_to(self, mobject, scale_factor=1.5):
    frame = self.camera.frame
    self.play(
        frame.animate
            .set_width(mobject.get_width() * scale_factor)
            .move_to(mobject),
        run_time=2
    )
```

### 360 度展示

```python
def showcase_3d(self, mobject):
    frame = self.camera.frame
    frame.reorient(20, 70)
    self.play(
        frame.animate.increment_theta(360 * DEGREES),
        run_time=8,
        rate_func=linear
    )
```

### 画中画效果

```python
# Small inset camera view
small_frame = self.camera.frame.copy()
small_frame.set_width(4)
small_frame.to_corner(UR, buff=0.5)
small_frame.fix_in_frame()
```
