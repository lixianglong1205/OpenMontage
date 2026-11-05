---
name: manimgl-best-practices
description: |
  触发条件：(1) 用户提到「manimgl」「ManimGL」或「3b1b manim」，(2) 代码包含 `from manimlib import *`，(3) 用户运行 `manimgl` CLI 命令，(4) 使用 InteractiveScene、self.frame、self.embed()、ShowCreation() 或 ManimGL 特有模式。

  ManimGL（Grant Sanderson 的 3Blue1Brown 版本）最佳实践——基于 OpenGL 的动画引擎，支持交互式开发。涵盖 InteractiveScene、带 t2c 的 Tex、相机帧控制、交互模式（-se 标志）、3D 渲染以及 checkpoint_paste() 工作流。

  不适用于 Manim Community Edition（使用 `manim` 导入和 `manim` CLI）。
---

## 如何使用

阅读各规则文件以获取详细说明与代码示例：

### 核心概念
- [rules/scenes.md](rules/scenes.md) - InteractiveScene、场景类型与 construct 方法
- [rules/mobjects.md](rules/mobjects.md) - Mobject 类型、VMobject、Group 与定位
- [rules/animations.md](rules/animations.md) - 动画类、播放动画与 timing

### 创建与变换
- [rules/creation-animations.md](rules/creation-animations.md) - ShowCreation、Write、FadeIn、DrawBorderThenFill
- [rules/transform-animations.md](rules/transform-animations.md) - Transform、ReplacementTransform、TransformMatchingTex
- [rules/animation-groups.md](rules/animation-groups.md) - LaggedStart、Succession、AnimationGroup

### 文本与数学
- [rules/tex.md](rules/tex.md) - Tex 类、原始字符串 R"..." 与 LaTeX 渲染
- [rules/text.md](rules/text.md) - Text mobject、字体与样式
- [rules/t2c.md](rules/t2c.md) - tex_to_color_map（t2c）为数学表达式着色

### 样式与外观
- [rules/colors.md](rules/colors.md) - 颜色常量、渐变、RGB、十六进制、GLSL 着色
- [rules/styling.md](rules/styling.md) - 填充、描边、不透明度、backstroke、gloss、shadow

### 3D 与相机
- [rules/3d.md](rules/3d.md) - 3D 对象、曲面、Sphere、Torus、参数曲面、光照
- [rules/camera.md](rules/camera.md) - frame.reorient()、欧拉角、fix_in_frame()、相机动画

### 交互式开发
- [rules/interactive.md](rules/interactive.md) - 使用 `-se` 标志的交互模式、checkpoint_paste()
- [rules/frame.md](rules/frame.md) - self.frame、相机控制、reorient 与缩放
- [rules/embedding.md](rules/embedding.md) - 用于 IPython 调试的 self.embed()、touch() 模式

### 配置与 CLI
- [rules/cli.md](rules/cli.md) - manimgl 命令、标志（-w、-o、-se、-l、-h）、渲染选项
- [rules/config.md](rules/config.md) - custom_config.yml、目录、相机设置、质量预设

## 可运行示例

完整且经过测试的示例文件，演示常见模式：

- [examples/basic_animations.py](examples/basic_animations.py) - 基础图形、文本与动画
- [examples/math_visualization.py](examples/math_visualization.py) - LaTeX 公式与数学内容
- [examples/graph_plotting.py](examples/graph_plotting.py) - 坐标轴、函数与绘图
- [examples/3d_visualization.py](examples/3d_visualization.py) - 带相机控制与曲面的 3D 场景
- [examples/updater_patterns.py](examples/updater_patterns.py) - 使用 updater 的动态动画

## 场景模板

复制并修改以下模板以开始新项目：

- [templates/basic_scene.py](templates/basic_scene.py) - 标准 2D 场景模板
- [templates/interactive_scene.py](templates/interactive_scene.py) - 带 self.embed() 的 InteractiveScene
- [templates/3d_scene.py](templates/3d_scene.py) - 带 frame.reorient() 的 3D 场景
- [templates/math_scene.py](templates/math_scene.py) - 数学推导与公式

## 快速参考

### 基础场景结构
```python
from manimlib import *

class MyScene(InteractiveScene):
    def construct(self):
        # Create mobjects
        circle = Circle()

        # Add to scene (static)
        self.add(circle)

        # Or animate
        self.play(ShowCreation(circle))  # Note: ShowCreation, not Create

        # Wait
        self.wait(1)
```

### 渲染命令
```bash
# Render and preview
manimgl scene.py MyScene

# Interactive mode - drop into shell at line 15
manimgl scene.py MyScene -se 15

# Write to file
manimgl scene.py MyScene -w

# Low quality for testing
manimgl scene.py MyScene -l
```

### 与 ManimCE 的主要差异

| 特性 | ManimGL (3b1b) | Manim Community |
|---------|----------------|-----------------|
| 导入 | `from manimlib import *` | `from manim import *` |
| CLI | `manimgl` | `manim` |
| 数学文本 | `Tex(R"\pi")` | `MathTex(r"\pi")` |
| 场景 | `InteractiveScene` | `Scene` |
| 创建动画 | `ShowCreation` | `Create` |
| 相机 | `self.frame` | `self.camera.frame` |
| 固定于帧 | `mob.fix_in_frame()` | `self.add_fixed_in_frame_mobjects(mob)` |
| 包名 | `manimgl` (PyPI) | `manim` (PyPI) |

### 交互式开发工作流

ManimGL 的杀手锏是交互式开发：

```bash
# Start at line 20 with state preserved
manimgl scene.py MyScene -se 20
```

在交互模式下：
```python
# Copy code to clipboard, then run:
checkpoint_paste()           # Run with animations
checkpoint_paste(skip=True)  # Run instantly (no animations)
checkpoint_paste(record=True) # Record while running
```

### 相机控制（self.frame）

```python
# Get the camera frame
frame = self.frame

# Reorient in 3D (phi, theta, gamma, center, height)
frame.reorient(45, -30, 0, ORIGIN, 8)

# Animate camera movement
self.play(frame.animate.reorient(60, -45, 0))

# Fix mobjects to stay in screen space during 3D movement
title.fix_in_frame()
```

### 使用 Tex 类的 LaTeX

```python
# Use raw strings with capital R
formula = Tex(R"\int_0^1 x^2 \, dx = \frac{1}{3}")

# Color mapping with t2c
equation = Tex(
    R"E = mc^2",
    t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
)

# Isolate substrings for animation
formula = Tex(R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}")
formula.set_color_by_tex("n", BLUE)
```

### 常见模式

#### 嵌入调试
```python
def construct(self):
    circle = Circle()
    self.play(ShowCreation(circle))
    self.embed()  # Drops into IPython shell here
```

#### 设置 3D 地面平面
```python
self.set_floor_plane("xz")  # Makes xy the viewing plane
```

#### 文本可读性 backstroke
```python
text = Text("Label")
text.set_backstroke(BLACK, 5)  # Black outline behind text
```

### 安装

```bash
# Install ManimGL
pip install manimgl

# Check installation
manimgl --version
```

### 常见陷阱

1. **版本混淆** - 确保使用 `manimgl`，而非 `manim`（社区版）
2. **ShowCreation 与 Create** - ManimGL 使用 `ShowCreation`，不是 `Create`
3. **Tex 与 MathTex** - ManimGL 使用带大写 R 原始字符串的 `Tex`
4. **self.frame 与 self.camera.frame** - ManimGL 直接使用 `self.frame`
5. **fix_in_frame()** - 在 mobject 上调用，而非 scene
6. **交互模式** - 交互式开发使用 `-se` 标志

## 许可与署名

本技能中的示例代码改编自 Grant Sanderson 的 [3Blue1Brown 视频仓库](https://github.com/3b1b/videos)。

**许可：** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

- **需署名** - 须同时注明 3Blue1Brown 与改编者
- **非商业** - 不得用于商业用途
- **相同方式共享** - 衍生作品须采用相同许可

完整说明见 [LICENSE.txt](LICENSE.txt)。
