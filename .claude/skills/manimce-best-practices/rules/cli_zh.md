---
name: cli
description: 命令行界面、渲染选项与画质标志
metadata:
  tags: cli, render, quality, preview, command, terminal
---

# Manim CLI

用于渲染场景的 `manim` 命令行界面。

## 基本用法

```bash
# Render a scene
manim file.py SceneName

# With preview (opens video after rendering)
manim -p file.py SceneName

# Preview with low quality (fast)
manim -pql file.py SceneName
```

## 画质标志

适用于不同场景的画质预设：

```bash
# Low Quality: 854x480, 15fps (fast for testing)
manim -ql file.py SceneName

# Medium Quality: 1280x720, 30fps
manim -qm file.py SceneName

# High Quality: 1920x1080, 60fps
manim -qh file.py SceneName

# 2K Quality: 2560x1440, 60fps
manim -qp file.py SceneName

# 4K Quality: 3840x2160, 60fps
manim -qk file.py SceneName
```

### 常用组合

```bash
# Preview + Low Quality (development workflow)
manim -pql file.py SceneName

# Preview + High Quality (final check)
manim -pqh file.py SceneName
```

## 预览标志

```bash
# -p: Open video after rendering
manim -p file.py SceneName

# Without -p: Render only (no auto-open)
manim file.py SceneName
```

## 渲染多个场景

```bash
# Render all scenes in file
manim -a file.py

# Render specific scenes
manim file.py Scene1 Scene2 Scene3
```

## 输出选项

### 仅保存最后一帧

```bash
# -s: Save only the last frame as PNG
manim -s file.py SceneName

# With quality
manim -sql file.py SceneName
```

### 输出格式

```bash
# GIF output
manim --format gif file.py SceneName

# PNG sequence
manim --format png file.py SceneName

# WebM (default is MP4)
manim --format webm file.py SceneName
```

### 自定义输出目录

```bash
manim -o custom_name file.py SceneName
manim --media_dir /path/to/output file.py SceneName
```

## 帧控制

```bash
# Start from specific animation number
manim -n 5 file.py SceneName

# Render frames from animation 3 to 7
manim -n 3,7 file.py SceneName
```

## 分辨率与帧率

```bash
# Custom resolution
manim -r 1920,1080 file.py SceneName

# Custom frame rate
manim --fps 24 file.py SceneName

# Both
manim -r 1280,720 --fps 30 file.py SceneName
```

## 透明背景

```bash
# Render with transparent background
manim -t file.py SceneName
```

## 渲染器选择

```bash
# Cairo renderer (default, 2D)
manim --renderer cairo file.py SceneName

# OpenGL renderer (3D, faster preview)
manim --renderer opengl file.py SceneName
```

## 其他实用标志

```bash
# Verbose output
manim -v DEBUG file.py SceneName

# Quiet mode
manim -v WARNING file.py SceneName

# Show progress bar
manim --progress_bar display file.py SceneName

# Disable caching
manim --disable_caching file.py SceneName

# Write to movie even if no animations
manim --write_to_movie file.py SceneName
```

## 帮助

```bash
# Show all options
manim --help

# Show render command options
manim render --help
```

## 其他命令

```bash
# Check installation and dependencies
manim checkhealth

# Initialize new project
manim init

# Show config values
manim cfg show

# Write current config to file
manim cfg write

# List installed plugins
manim plugins -l
```

## Jupyter Notebook 支持

在 Jupyter notebook 中使用 `%%manim` 单元格魔法：

```python
%%manim -qm -v WARNING MyScene
class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

标志与 CLI 用法相同（`-qm`、`-ql` 等）。

## 典型开发工作流

```bash
# 1. Develop with fast preview
manim -pql scene.py MyScene

# 2. Check at medium quality
manim -pqm scene.py MyScene

# 3. Final render at high quality
manim -qh scene.py MyScene

# 4. Create GIF for sharing
manim --format gif -qm scene.py MyScene
```

## 最佳实践

1. **开发时使用 -pql** - 快速迭代循环
2. **最终输出使用 -qh** - 画质好，渲染时间合理
3. **缩略图使用 -s** - 快速截取最后一帧
4. **谨慎使用 -a** - 会渲染全部场景，可能很慢
5. **演示用 --format gif** - 便于分享与嵌入
