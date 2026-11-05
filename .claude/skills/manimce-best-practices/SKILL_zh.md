---
name: manimce-best-practices
description: |
  触发条件：(1) 用户提到「manim」「Manim Community」或「ManimCE」，(2) 代码包含 `from manim import *`，(3) 用户运行 `manim` CLI 命令，(4) 使用 Scene、MathTex、Create() 或 ManimCE 特有类。

  Manim Community Edition（社区维护的 Python 动画引擎）最佳实践。涵盖 Scene 结构、动画、LaTeX/MathTex、ThreeDScene 三维场景、相机控制、样式与 CLI 用法。

  不适用于 ManimGL/3b1b 版本（该版本使用 `manimlib` 导入与 `manimgl` CLI）。
---

## 如何使用

阅读各条规则文件以获取详细说明与代码示例：

### 核心概念
- [rules/scenes.md](rules/scenes.md) - Scene 结构、construct 方法与场景类型
- [rules/mobjects.md](rules/mobjects.md) - Mobject 类型、VMobject、Group 与定位
- [rules/animations.md](rules/animations.md) - 动画类、播放动画与 timing（时间控制）

### 创建与变换
- [rules/creation-animations.md](rules/creation-animations.md) - Create、Write、FadeIn、DrawBorderThenFill
- [rules/transform-animations.md](rules/transform-animations.md) - Transform、ReplacementTransform、形变
- [rules/animation-groups.md](rules/animation-groups.md) - AnimationGroup、LaggedStart、Succession

### 文本与数学
- [rules/text.md](rules/text.md) - Text mobject、字体与样式
- [rules/latex.md](rules/latex.md) - MathTex、Tex、LaTeX 渲染与公式着色
- [rules/text-animations.md](rules/text-animations.md) - Write、AddTextLetterByLetter、TypeWithCursor

### 样式与外观
- [rules/colors.md](rules/colors.md) - 颜色常量、渐变与颜色操作
- [rules/styling.md](rules/styling.md) - 填充、描边、透明度与视觉属性

### 定位与布局
- [rules/positioning.md](rules/positioning.md) - move_to、next_to、align_to、shift 等方法
- [rules/grouping.md](rules/grouping.md) - VGroup、Group、arrange 与布局模式

### 坐标系与作图
- [rules/axes.md](rules/axes.md) - Axes、NumberPlane、坐标系
- [rules/graphing.md](rules/graphing.md) - 函数绘图、参数曲线
- [rules/3d.md](rules/3d.md) - ThreeDScene、三维坐标轴、曲面、相机朝向

### 动画控制
- [rules/timing.md](rules/timing.md) - Rate function、缓动、run_time、lag_ratio
- [rules/updaters.md](rules/updaters.md) - Updater、ValueTracker、动态动画
- [rules/camera.md](rules/camera.md) - MovingCameraScene、缩放、平移、画幅操作

### 配置与 CLI
- [rules/cli.md](rules/cli.md) - 命令行界面、渲染选项、画质标志
- [rules/config.md](rules/config.md) - 配置系统、manim.cfg、设置项

### 形状与几何
- [rules/shapes.md](rules/shapes.md) - Circle、Square、Rectangle、Polygon 等几何图元
- [rules/lines.md](rules/lines.md) - Line、Arrow、Vector、DashedLine 与连接线

## 可运行示例

完整且经过测试的示例文件，演示常见模式：

- [examples/basic_animations.py](examples/basic_animations.py) - 形状创建、文本、交错动画、沿路径运动
- [examples/math_visualization.py](examples/math_visualization.py) - LaTeX 公式、分色数学、推导过程
- [examples/updater_patterns.py](examples/updater_patterns.py) - ValueTracker、动态动画、物理模拟
- [examples/graph_plotting.py](examples/graph_plotting.py) - 坐标轴、函数、面积、黎曼和、极坐标图
- [examples/3d_visualization.py](examples/3d_visualization.py) - ThreeDScene、曲面、三维相机、参数曲线

## 场景模板

复制并修改以下模板以启动新项目：

- [templates/basic_scene.py](templates/basic_scene.py) - 标准二维场景模板
- [templates/camera_scene.py](templates/camera_scene.py) - 带缩放/平移的 MovingCameraScene
- [templates/threed_scene.py](templates/threed_scene.py) - 含曲面与相机旋转的三维场景

## 快速参考

### 基本 Scene 结构
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Create mobjects
        circle = Circle()

        # Add to scene (static)
        self.add(circle)

        # Or animate
        self.play(Create(circle))

        # Wait
        self.wait(1)
```

### 渲染命令
```bash
# Basic render with preview
manim -pql scene.py MyScene

# Quality flags: -ql (low), -qm (medium), -qh (high), -qk (4k)
manim -pqh scene.py MyScene
```

### 与 3b1b/ManimGL 的主要差异

| 特性 | Manim Community | 3b1b/ManimGL |
|---------|-----------------|--------------|
| Import | `from manim import *` | `from manimlib import *` |
| CLI | `manim` | `manimgl` |
| Math text | `MathTex(r"\pi")` | `Tex(R"\pi")` |
| Scene | `Scene` | `InteractiveScene` |
| Package | `manim` (PyPI) | `manimgl` (PyPI) |

### Jupyter Notebook 支持

使用 `%%manim` 单元格魔法：

```python
%%manim -qm MyScene
class MyScene(Scene):
    def construct(self):
        self.play(Create(Circle()))
```

### 常见陷阱

1. **版本混淆** - 请使用 `manim`（Community），而非 `manimgl`（3b1b 版）
2. **检查导入** - `from manim import *` 为 ManimCE；`from manimlib import *` 为 ManimGL
3. **过时教程** - 视频教程可能已过时；优先参考官方文档
4. **manimpango 问题** - 若文本渲染失败，请检查 manimpango 安装要求
5. **PATH 问题（Windows）** - 若找不到 `manim` 命令，可使用 `python -m manim` 或检查 PATH

### 安装

```bash
# Install Manim Community
pip install manim

# Check installation
manim checkhealth
```

### 常用命令

```bash
manim -pql scene.py Scene    # Preview low quality (development)
manim -pqh scene.py Scene    # Preview high quality
manim --format gif scene.py  # Output as GIF
manim checkhealth            # Verify installation
manim plugins -l             # List plugins
```
