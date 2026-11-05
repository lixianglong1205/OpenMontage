# ManimGL 中的 3D

ManimGL 具备强大的 3D 能力，并配有灵活的相机系统。与 ManimCE 不同，ManimGL 不需要专门的 ThreeDScene 类。

## 基础 3D 设置

### 创建 3D 对象

```python
from manimlib import *

class Basic3DScene(Scene):
    def construct(self):
        # Get camera frame
        frame = self.camera.frame

        # Set 3D orientation
        frame.reorient(20, 70)  # theta, phi in degrees

        # Create 3D objects
        sphere = Sphere(radius=2)
        sphere.set_color(BLUE, opacity=0.7)

        self.add(sphere)
```

## 相机帧控制

### frame.reorient()

`reorient()` 方法是控制 3D 相机朝向的主要方式。

```python
# frame.reorient(theta, phi, gamma=0, center=ORIGIN, height=8)

# Front view
frame.reorient(0, 0)

# Isometric view
frame.reorient(20, 70)

# Top-down view
frame.reorient(0, 90)

# Side view
frame.reorient(90, 90)
```

### 相机动画

```python
class AnimatedCamera(Scene):
    def construct(self):
        frame = self.camera.frame

        # Create object
        cube = Cube()
        self.add(cube)

        # Animate camera rotation
        self.play(frame.animate.reorient(30, 60))
        self.wait()

        # Continuous rotation
        frame.add_updater(lambda m, dt: m.increment_theta(0.2 * dt))
        self.wait(10)
```

### 帧方法

```python
# Set Euler angles
frame.set_euler_angles(theta=30*DEGREES, phi=70*DEGREES)

# Increment angles (useful for rotation)
frame.increment_theta(10*DEGREES)
frame.increment_phi(5*DEGREES)
frame.increment_gamma(2*DEGREES)

# Get current angles
theta = frame.get_theta()
phi = frame.get_phi()
```

## 3D 几何图元

### Sphere

```python
sphere = Sphere(
    radius=2,
    resolution=(20, 20),  # (u_resolution, v_resolution)
    color=BLUE
)
sphere.set_opacity(0.7)
```

### Cube

```python
cube = Cube(
    side_length=2,
    color=GREEN,
    fill_opacity=0.8
)
```

### Surface

```python
# Parametric surface
surface = Surface(
    lambda u, v: np.array([u, v, u**2 + v**2]),
    u_range=(-2, 2),
    v_range=(-2, 2),
    resolution=(20, 20)
)
```

### Torus

```python
torus = Torus(
    r1=2,  # Major radius
    r2=0.5,  # Minor radius
    color=YELLOW
)
```

### Cylinder

```python
cylinder = Cylinder(
    height=3,
    radius=1,
    color=RED
)
```

### 3D 线与形状

```python
# 3D Line
line = Line3D(
    start=[-2, -2, -2],
    end=[2, 2, 2],
    color=WHITE,
    width=0.05
)

# 3D Disk
disk = Disk3D(radius=1.5, color=PURPLE)

# 3D Square
square = Square3D(side_length=2, color=ORANGE)
```

## 纹理曲面

### 为 3D 对象添加纹理

```python
class TexturedSphere(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        # Create sphere with texture
        sphere = Sphere(radius=2)

        # Apply texture from URL or local file
        textured_sphere = TexturedSurface(
            surface=sphere,
            # Can use URL or local path
            image_file="path/to/texture.jpg"
        )

        self.add(textured_sphere)

        # Rotate camera
        self.play(frame.animate.increment_theta(360*DEGREES), run_time=10)
```

### 地球示例

```python
earth = Sphere(radius=2, resolution=(40, 40))
textured_earth = TexturedSurface(
    earth,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"
)
```

## 3D 坐标轴

### ThreeDAxes

```python
axes = ThreeDAxes(
    x_range=(-5, 5, 1),
    y_range=(-5, 5, 1),
    z_range=(-5, 5, 1),
    width=10,
    height=10,
    depth=10
)
axes.add_coordinate_labels(font_size=20)
```

### 3D 中的 NumberPlane

```python
# XY plane
xy_plane = NumberPlane(
    x_range=(-5, 5),
    y_range=(-5, 5)
)

# XZ plane (horizontal floor)
xz_plane = NumberPlane(
    x_range=(-5, 5),
    y_range=(-5, 5)
)
xz_plane.rotate(90*DEGREES, axis=RIGHT)
```

## 参数曲面

### 创建自定义曲面

```python
# Paraboloid
paraboloid = Surface(
    lambda u, v: np.array([
        u,
        v,
        u**2 + v**2
    ]),
    u_range=(-2, 2),
    v_range=(-2, 2),
    resolution=(30, 30),
    color=BLUE
)

# Wave surface
wave = Surface(
    lambda u, v: np.array([
        u,
        v,
        np.sin(u) * np.cos(v)
    ]),
    u_range=(-PI, PI),
    v_range=(-PI, PI),
    resolution=(40, 40)
)
```

### 曲面网格

```python
# Create surface
surface = Sphere(radius=2)

# Add mesh overlay
mesh = SurfaceMesh(surface)
mesh.set_stroke(BLUE, width=1, opacity=0.5)

self.add(surface, mesh)
```

## 固定在帧中的对象

### fix_in_frame()

在相机旋转时，让 2D 元素（如标签）保持固定。

```python
class FixedLabels(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        # 3D object that rotates with camera
        cube = Cube()
        self.add(cube)

        # 2D title that stays fixed
        title = Text("3D Cube", font_size=60)
        title.to_edge(UP)
        title.fix_in_frame()  # Stays in screen space
        self.add(title)

        # Rotate camera
        self.play(frame.animate.reorient(50, 80), run_time=3)
```

## 光照

### 光源

```python
# Access light source
light = self.camera.light_source

# Move light
light.move_to([10, 10, 10])

# Animate light movement
self.play(light.animate.move_to([0, 0, 10]), run_time=2)
```

### 光泽与阴影

```python
# Add gloss to objects
sphere = Sphere(radius=2)
sphere.set_gloss(0.8)  # 0 to 1

# Add shadow
sphere.set_shadow(0.5)  # 0 to 1
```

## 复杂 3D 场景示例

```python
class Complex3DScene(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 75)

        # Create axes
        axes = ThreeDAxes(
            x_range=(-3, 3),
            y_range=(-3, 3),
            z_range=(-3, 3)
        )

        # Create parametric surface
        surface = Surface(
            lambda u, v: np.array([
                u,
                v,
                np.sin(np.sqrt(u**2 + v**2))
            ]),
            u_range=(-3, 3),
            v_range=(-3, 3),
            resolution=(30, 30),
            color=BLUE
        )
        surface.set_opacity(0.7)

        # Add mesh
        mesh = SurfaceMesh(surface)
        mesh.set_stroke(WHITE, 0.5, opacity=0.3)

        # Add title (fixed in frame)
        title = Text("Sinc Function Surface", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()
        title.set_backstroke(BLACK, 5)

        # Build scene
        self.add(axes, surface, mesh, title)
        self.wait()

        # Rotate camera smoothly
        self.play(
            frame.animate.reorient(45, 70),
            run_time=3
        )
        self.wait()

        # Add continuous rotation
        frame.add_updater(lambda m, dt: m.increment_theta(20 * dt))
        self.wait(10)
```

## 交互式 3D 控制

使用 `manimgl` 运行时，可与 3D 场景交互：

- 按 `d` + 移动鼠标：旋转相机
- 按 `z` + 滚动：放大/缩小
- 按 `r`：将相机重置为默认位置
- 按 `q`：退出交互模式

## 最佳实践

1. **使用 reorient()**：比手动设置欧拉角更清晰
2. **标签使用 fix_in_frame()**：保持 UI 元素可读
3. **合适的分辨率**：最终渲染用更高分辨率，开发时用较低分辨率
4. **透明度体现深度**：将 opacity 设为小于 1 以便透视曲面
5. **光照很重要**：调整光源位置以获得更好的可视化效果
6. **连续旋转**：使用 updater 实现平滑的相机旋转
7. **帧率考量**：开发阶段 3D 场景可能需要较低的帧率

## 常见模式

### 绕对象旋转相机

```python
# 360-degree rotation
self.play(
    frame.animate.increment_theta(360*DEGREES),
    run_time=10,
    rate_func=linear
)
```

### 创建地面平面

```python
floor = NumberPlane(
    x_range=(-10, 10),
    y_range=(-10, 10),
    background_line_style={"stroke_color": GREY, "stroke_width": 1}
)
floor.rotate(90*DEGREES, RIGHT)
floor.shift(2*DOWN)
```

### 多视角展示

```python
# Show from different angles
angles = [(0, 0), (20, 70), (45, 45), (90, 90)]

for theta, phi in angles:
    self.play(frame.animate.reorient(theta, phi))
    self.wait()
```
