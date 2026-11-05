# ManimGL 中的交互式嵌入（Interactive Embedding）

ManimGL 的 `self.embed()` 功能会在场景执行过程中进入交互式 IPython shell，使调试与实验非常高效。

## 基本用法

### 在场景中添加 embed()

```python
from manimlib import *

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))

        # Drop into interactive shell here
        self.embed()

        # Code continues after you exit the shell
        self.play(circle.animate.shift(RIGHT))
        self.wait()
```

### 使用嵌入运行

```bash
# Run scene - will pause at embed() point
manimgl scene.py MyScene
```

## 交互式命令

### Shell 中可用内容

当 `self.embed()` 打开 IPython shell 时，你可以使用：

```python
# Scene methods (abbreviated - no 'self.' needed)
play(animation)              # Play animation
add(mobject)                 # Add mobject to scene
remove(mobject)              # Remove mobject
wait(duration)               # Wait for duration
clear()                      # Clear scene

# Camera/frame control
frame                        # Access camera frame
play(frame.animate.shift(RIGHT))

# All local variables from construct()
circle, square, text, etc.   # Your mobjects

# Interactive camera
touch()                      # Enter touch mode (press 'q' to exit)
                            # Press 'd' + mouse to rotate
                            # Press 'z' + scroll to zoom
                            # Press 'r' to reset

# Exit shell and continue
exit()                       # Continue scene execution
```

## 实用示例

### 调试动画

```python
class DebugScene(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.add(circle, square)

        # Problem with this animation?
        self.play(circle.animate.move_to(square))

        # Debug it interactively
        self.embed()

        # In the shell:
        # >>> play(circle.animate.set_color(RED))
        # >>> circle.get_center()
        # >>> square.get_center()
```

### 实验布局与位置

```python
class PositioningExperiment(Scene):
    def construct(self):
        shapes = VGroup(*[
            Circle(radius=0.5) for _ in range(5)
        ])

        # Try different arrangements interactively
        self.add(shapes)
        self.embed()

        # In the shell, try:
        # >>> play(shapes.animate.arrange(RIGHT, buff=1))
        # >>> play(shapes.animate.arrange(DOWN, buff=0.5))
        # >>> play(shapes.animate.arrange_in_grid(rows=2))
```

### 探索颜色与样式

```python
class StyleExploration(Scene):
    def construct(self):
        text = Text("Experiment", font_size=72)
        self.add(text)
        self.embed()

        # In the shell:
        # >>> play(text.animate.set_color(BLUE))
        # >>> text.set_backstroke(BLACK, width=10)
        # >>> play(text.animate.scale(2))
```

## embed() 高级用法

### 多个嵌入点

```python
class MultipleEmbeds(Scene):
    def construct(self):
        # First checkpoint
        circle = Circle()
        self.play(ShowCreation(circle))
        self.embed()  # First pause

        # Second checkpoint
        square = Square()
        self.play(ShowCreation(square))
        self.embed()  # Second pause

        # Third checkpoint
        self.play(FadeOut(VGroup(circle, square)))
        self.embed()  # Third pause
```

### 条件嵌入

```python
class ConditionalEmbed(Scene):
    def construct(self):
        DEBUG = True

        circle = Circle()
        self.play(ShowCreation(circle))

        if DEBUG:
            self.embed()  # Only embed in debug mode

        self.play(circle.animate.shift(RIGHT))
```

## 与 `-se` 标志配合使用

### 跳过并嵌入（Skip and Embed）

`-se` 标志会跳到指定行并进入嵌入：

```python
class LargeScene(Scene):
    def construct(self):
        # Line 5
        circle = Circle()
        self.play(ShowCreation(circle))

        # Line 10
        square = Square()
        self.play(ShowCreation(square))

        # Line 15
        text = Text("Hello")
        self.play(Write(text))

        # Line 20
        self.play(FadeOut(VGroup(circle, square, text)))
```

```bash
# Skip directly to line 15 and embed
manimgl scene.py LargeScene -se 15
```

## checkpoint_paste()

### 交互式执行代码

`checkpoint_paste()` 会运行剪贴板中的代码：

```python
class CheckpointScene(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.embed()
```

```bash
# Run the scene
manimgl scene.py CheckpointScene
```

在 shell 中：

```python
# Copy this code to clipboard first:
"""
square = Square()
play(ShowCreation(square))
play(square.animate.next_to(circle, RIGHT))
"""

# Then in the shell:
>>> checkpoint_paste()              # Runs with animations
>>> checkpoint_paste(skip=True)     # Runs instantly
>>> checkpoint_paste(record=True)   # Records while running
```

## 保存与恢复状态

### save_state() 与 restore()

```python
class StateManagement(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.add(circle, square)

        # Save current state
        self.save_state()

        # Make changes
        self.play(circle.animate.shift(RIGHT * 3))
        self.play(square.animate.shift(LEFT * 3))

        self.embed()

        # In the shell:
        # >>> restore()  # Revert to saved state
```

## 交互式 3D 探索

### touch() 模式

```python
class Interactive3D(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        # Create 3D object
        sphere = Sphere(radius=2, color=BLUE)
        self.add(sphere)

        self.embed()

        # In the shell:
        # >>> touch()
        # Now you can:
        # - Press 'd' and move mouse to rotate
        # - Press 'z' and scroll to zoom
        # - Press 'r' to reset camera
        # - Press 'q' to exit touch mode
```

## 调试模式

### 检查 Mobject 属性

```python
class InspectProperties(Scene):
    def construct(self):
        circle = Circle(radius=2, color=BLUE)
        circle.shift(RIGHT * 3)
        self.add(circle)
        self.embed()

        # In the shell:
        # >>> circle.get_center()
        # >>> circle.get_color()
        # >>> circle.get_width()
        # >>> circle.get_height()
        # >>> circle.get_all_points()
```

### 测试动画时长

```python
class TimingTest(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.embed()

        # In the shell, test different timings:
        # >>> play(circle.animate.shift(RIGHT), run_time=0.5)
        # >>> play(circle.animate.shift(LEFT), run_time=2)
        # >>> play(circle.animate.shift(UP), run_time=1, rate_func=smooth)
```

### 迭代构建复杂场景

```python
class IterativeBuilding(Scene):
    def construct(self):
        self.embed()

        # Build entire scene in the shell:
        # >>> title = Text("My Animation")
        # >>> title.to_edge(UP)
        # >>> add(title)
        #
        # >>> circles = VGroup(*[Circle(radius=0.5) for _ in range(5)])
        # >>> circles.arrange(RIGHT, buff=0.5)
        # >>> play(LaggedStart(*[ShowCreation(c) for c in circles], lag_ratio=0.2))
        #
        # >>> formula = Tex(R"E = mc^2")
        # >>> formula.next_to(circles, DOWN, buff=1)
        # >>> play(Write(formula))
```

## 最佳实践

1. **用于调试**：动画不符合预期时添加 `self.embed()`
2. **自由实验**：在 shell 中尝试不同做法，再写回代码
3. **实验前 save_state()**：出错时便于回滚
4. **大场景用 -se**：直接跳到问题区域，不必看完整个动画
5. **用 checkpoint_paste() 快速迭代**：测试代码片段
6. **3D 用 touch()**：找到合适机位必不可少
7. **最终渲染前移除 embed()**：别忘了去掉调试用嵌入

## 常见模式

### 快速实验模式

```python
# Add at problem point
self.embed()

# In shell, test fix
play(mobject.animate.scale(2))  # Test different values

# If it works, add to code
# exit()
```

### 交互式开发模式

```python
# Start with minimal setup
class Scene(Scene):
    def construct(self):
        self.embed()

# Build everything in the shell
# Copy successful commands back to code
```

### 3D 相机设置模式

```python
# Get to 3D scene
frame.reorient(20, 70)
add(sphere)
self.embed()

# Find perfect angle
touch()  # Rotate with mouse
# Press 'q' when done
# Check frame.get_theta(), frame.get_phi()
# Add those values to code
```

## 故障排除

### embed() 不工作

- 确保使用 `manimgl` 命令运行
- 确认已安装 IPython
- 检查 `embed()` 之前是否有语法错误

### 无法访问变量

- 变量必须在 `self.embed()` 之前定义
- 使用 `locals()` 或 `globals()` 查看可用变量

### Shell 立即退出

- 除非要继续执行场景，否则不要调用 `exit()`
- 按 Ctrl+D 退出并继续
- 使用 `quit()` 或 `exit()` 关闭 shell

## 示例：完整的交互式开发

```python
class InteractiveDevelopment(Scene):
    def construct(self):
        # Start with embed
        self.embed()

        # In the shell, build everything:
        """
        # Create title
        title = Text("Interactive Development", font_size=60)
        title.to_edge(UP)
        play(Write(title))

        # Create content
        circle = Circle(radius=1.5, color=BLUE)
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(WHITE, width=3)
        play(ShowCreation(circle))

        # Add label
        label = Text("Circle", font_size=36)
        label.next_to(circle, DOWN)
        play(FadeIn(label, shift=UP))

        # Animate
        play(
            circle.animate.shift(RIGHT * 2),
            label.animate.shift(RIGHT * 2)
        )

        wait(2)

        # When happy, copy all this code to your construct method
        exit()
        """
```

这让 ManimGL 在快速原型与调试方面非常强大！
