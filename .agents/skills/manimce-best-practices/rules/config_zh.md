---
name: config
description: 配置系统、manim.cfg 与各项设置
metadata:
  tags: config, configuration, settings, manim.cfg, options
---

# 配置

通过配置文件与代码来设置 Manim 的行为。

## 配置优先级

Manim 按以下顺序读取配置（优先级从高到低）：
1. 命令行参数（最高优先级）
2. 当前目录下的用户 `manim.cfg`
3. 用户全局配置
4. 默认值（最低优先级）

## manim.cfg 文件

在项目目录中创建 `manim.cfg` 文件：

```ini
[CLI]
# Preview after rendering
preview = True

# Default quality
quality = medium_quality

# Output format
format = mp4

# Frame rate
frame_rate = 30

[output]
# Custom output directory
media_dir = ./media

# Save last frame as PNG
save_last_frame = False

[renderer]
# Background color
background_color = BLACK

[style]
# Default font
font = Arial
```

## 常用配置项

### CLI 节

```ini
[CLI]
# Quality presets: low_quality, medium_quality, high_quality, production_quality, fourk_quality
quality = medium_quality

# Preview video after rendering
preview = True

# Frame rate
frame_rate = 30

# Output format: mp4, gif, mov, webm, png
format = mp4

# Transparent background
transparent = False

# Progress bar: display, leave, none
progress_bar = display
```

### 渲染器节

```ini
[renderer]
# Background color (hex or color name)
background_color = #1e1e1e

# Renderer type: cairo, opengl
renderer = cairo
```

### 分辨率

```ini
[CLI]
# Frame dimensions
pixel_width = 1920
pixel_height = 1080
```

## 在代码中配置

在 Python 代码中访问并修改配置：

```python
# Access config values
config.pixel_width  # e.g., 1920
config.frame_rate  # e.g., 30
config.background_color  # e.g., BLACK

# Modify config (before creating scenes)
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60
config.background_color = BLUE_E
```

### 在 Scene 中

```python
class MyScene(Scene):
    def construct(self):
        # Access frame dimensions
        width = config.frame_width
        height = config.frame_height

        # Create rectangle matching frame size
        frame_rect = Rectangle(
            width=width,
            height=height,
            stroke_color=WHITE
        )
        self.add(frame_rect)
```

## 背景色

### 在配置文件中

```ini
[renderer]
background_color = BLACK
# Or hex color
background_color = #1a1a2e
```

### 在代码中

```python
class DarkBackground(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        # ... rest of scene
```

## 输出目录结构

默认 media 目录结构：
```
media/
├── videos/
│   └── scene_file/
│       ├── 480p15/       # Low quality
│       ├── 720p30/       # Medium quality
│       ├── 1080p60/      # High quality
│       └── 2160p60/      # 4K quality
├── images/
│   └── scene_file/
│       └── SceneName.png
└── Tex/                  # LaTeX cache
```

### 自定义输出目录

```ini
[output]
media_dir = ./output
```

或通过 CLI：
```bash
manim --media_dir ./output file.py Scene
```

## Tex 配置

用于 LaTeX 渲染：

```ini
[tex]
# Custom preamble
preamble = \usepackage{amsmath}\usepackage{amssymb}

# Tex compiler
tex_compiler = latex
```

## 缓存

```ini
[CLI]
# Disable caching (useful for debugging)
disable_caching = True

# Max cached files
max_files_cached = 100
```

## 查看当前配置

```bash
# Show all config values
manim cfg show

# Show specific section
manim cfg show CLI

# Write current config to file
manim cfg write
```

## 项目专用配置

在项目根目录创建 `manim.cfg`：

```ini
[CLI]
quality = high_quality
preview = True
frame_rate = 60

[renderer]
background_color = #0d1117

[output]
media_dir = ./renders
```

## 插件

Manim 提供可扩展的插件系统：

```bash
# List installed plugins
manim plugins -l

# Install a plugin
pip install manim-pluginname
```

在 `manim.cfg` 中启用插件：

```ini
[CLI]
plugins = manim-pluginname
# For multiple plugins:
plugins = plugin1,plugin2
```

## 最佳实践

1. **用 manim.cfg 设定项目默认值** — 团队内设置一致
2. **开发阶段使用较低画质** — 迭代更快
3. **在配置中设置 background_color** — 不必在每个 Scene 里重复
4. **使用自定义 media_dir** — 渲染输出更有条理
5. **将 manim.cfg 纳入版本控制** — 与协作者共享设置
