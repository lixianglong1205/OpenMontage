# ManimGL 中的配置

ManimGL 使用 `custom_config.yml` 文件进行配置。这些文件控制目录、相机设置、窗口属性等。

## 配置文件位置

### 默认位置

ManimGL 按以下顺序查找 `custom_config.yml`：

1. 当前目录
2. 父目录（递归向上直至项目根目录）
3. ManimGL 安装目录

```
my_project/
├── custom_config.yml      # Project-specific config
├── scenes/
│   ├── custom_config.yml  # Scenes-specific config (overrides project config)
│   └── scene.py
└── manimlib/              # ManimGL installation
```

### 多个配置文件

```bash
# Use specific config file
manimgl scene.py MyScene --config_file /path/to/config.yml

# Project structure with multiple configs
project/
├── custom_config.yml          # Default for project
├── experiments/
│   ├── custom_config.yml      # Overrides for experiments
│   └── test_scene.py
└── final/
    ├── custom_config.yml      # High quality settings
    └── final_scene.py
```

## 基本配置

### 最小 custom_config.yml

```yaml
# Directories
directories:
  output: "./media/videos"
  raster_images: "./media/images"
  vector_images: "./media/svg"
  sounds: "./media/sounds"
  data: "./media/data"

# Window configuration
window_config:
  size: "default"  # or "fullscreen"

# Camera settings
camera_config:
  pixel_height: 1080
  pixel_width: 1920
  frame_rate: 60
```

## 详细配置选项

### 目录配置

```yaml
directories:
  # Where rendered videos are saved
  output: "/path/to/output/videos"

  # Where temporary files go
  temporary_storage: "/tmp/manim"

  # Image resources
  raster_images: "./assets/images"
  vector_images: "./assets/svg"

  # Audio resources
  sounds: "./assets/audio"

  # Data files
  data: "./assets/data"

  # LaTeX templates
  tex_templates: "./assets/tex_templates"

  # Font directory
  fonts: "./assets/fonts"
```

### 相机配置

```yaml
camera_config:
  # Resolution
  pixel_width: 1920
  pixel_height: 1080

  # Frame rate
  frame_rate: 60

  # Background color
  background_color: "#000000"

  # Frame settings
  frame_height: 8.0
  frame_width: 14.222222222222221  # 16:9 aspect ratio

  # Quality presets
  # These override pixel_width, pixel_height, frame_rate
  quality:
    low:
      pixel_width: 854
      pixel_height: 480
      frame_rate: 15
    medium:
      pixel_width: 1280
      pixel_height: 720
      frame_rate: 30
    high:
      pixel_width: 1920
      pixel_height: 1080
      frame_rate: 60
    ultra_high:
      pixel_width: 3840
      pixel_height: 2160
      frame_rate: 60
```

### 窗口配置

```yaml
window_config:
  # Window size: "default", "fullscreen", or [width, height]
  size: "default"
  # size: "fullscreen"
  # size: [1280, 720]

  # Window position on screen
  position: "UR"  # Upper right
  # Options: UL, UR, DL, DR, TOP, BOTTOM, LEFT, RIGHT, CENTER

  # Monitor to display on (for multi-monitor setups)
  monitor: 0

  # Window title
  window_title: "ManimGL Preview"

  # Show file name in title
  show_file_name_in_title: true
```

### 样式配置

```yaml
style:
  # Default color constants
  background_color: "#000000"

  # Font settings
  font: "Consolas"
  tex_font: "Latin Modern Math"

  # Default stroke width
  stroke_width: 4

  # Default animation run time
  default_animation_run_time: 1.0
```

### 通用导入配置

```yaml
# Auto-import common modules
universal_import_line: |
  from manimlib import *
  import numpy as np
  import itertools as it
```

## 质量预设

### 命令行覆盖

```bash
# Use low quality preset
manimgl scene.py MyScene -l

# Use medium quality
manimgl scene.py MyScene -m

# Use high quality
manimgl scene.py MyScene -h

# Use 4K quality
manimgl scene.py MyScene --uhd
```

### 自定义质量预设

```yaml
camera_config:
  quality:
    custom:
      pixel_width: 2560
      pixel_height: 1440
      frame_rate: 120
```

## LaTeX 配置

### TeX 配置

```yaml
tex_config:
  # TeX compiler
  tex_compiler: "latex"  # or "xelatex", "lualatex"

  # TeX template
  tex_template: "tex_template.tex"

  # Additional packages
  tex_packages:
    - "amsmath"
    - "amssymb"
    - "mathtools"

  # Text to LaTeX map
  text_to_replace: {
    # Replacements for common symbols
    "pi": "\\pi",
    "alpha": "\\alpha"
  }
```

## 项目专用配置

### 开发配置（快速迭代）

```yaml
# dev_config.yml
directories:
  output: "./output/dev"

camera_config:
  pixel_height: 480
  pixel_width: 854
  frame_rate: 15

window_config:
  size: [1280, 720]
  position: "UR"
```

用法：

```bash
manimgl scene.py MyScene --config_file dev_config.yml
```

### 生产配置（高质量）

```yaml
# prod_config.yml
directories:
  output: "./output/final"

camera_config:
  pixel_height: 2160
  pixel_width: 3840
  frame_rate: 60

style:
  default_animation_run_time: 1.5
```

## 运行时配置覆盖

### 命令行覆盖

```bash
# Override single value
manimgl scene.py MyScene --config camera_config.frame_rate=30

# Override multiple values
manimgl scene.py MyScene \
  --config camera_config.frame_rate=30 \
  --config camera_config.pixel_width=1280 \
  --config camera_config.pixel_height=720

# Override output directory
manimgl scene.py MyScene --config directories.output=/tmp/manim_output
```

## 完整配置示例

### 完整 custom_config.yml

```yaml
# Directory Configuration
directories:
  output: "./media/videos"
  temporary_storage: "/tmp/manim"
  raster_images: "./assets/images"
  vector_images: "./assets/svg"
  sounds: "./assets/audio"
  data: "./assets/data"
  tex_templates: "./assets/tex"
  fonts: "./assets/fonts"

# Camera Configuration
camera_config:
  pixel_width: 1920
  pixel_height: 1080
  frame_rate: 60
  background_color: "#0a0a0a"
  frame_height: 8.0
  frame_width: 14.222222222222221

# Window Configuration
window_config:
  size: "default"
  position: "UR"
  monitor: 0
  window_title: "ManimGL Preview"
  show_file_name_in_title: true

# Style Configuration
style:
  background_color: "#0a0a0a"
  font: "Consolas"
  tex_font: "Latin Modern Math"
  stroke_width: 4
  default_animation_run_time: 1.0

# TeX Configuration
tex_config:
  tex_compiler: "latex"
  tex_template: "tex_template.tex"
  tex_packages:
    - "amsmath"
    - "amssymb"
    - "mathtools"
    - "physics"

# Universal Imports
universal_import_line: |
  from manimlib import *
  import numpy as np
  import itertools as it
  import random

# Logging
log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR
```

## 最佳实践

1. **区分开发与生产配置**：开发与最终渲染使用不同配置文件
2. **项目级配置**：在项目根目录保留 `custom_config.yml`
3. **测试时覆盖**：用 `--config` 标志做临时修改
4. **版本控制**：将 `custom_config.yml` 提交到 git
5. **记录自定义设置**：用注释说明非标准取值
6. **路径一致**：使用相对路径以便移植
7. **质量预设**：使用内置质量标志（`-l`、`-m`、`-h`），而非手动改分辨率

## 常见配置

### YouTube 视频（1080p）

```yaml
camera_config:
  pixel_width: 1920
  pixel_height: 1080
  frame_rate: 60
  background_color: "#000000"
```

### 快速测试

```yaml
camera_config:
  pixel_width: 854
  pixel_height: 480
  frame_rate: 15
```

### 4K 制作

```yaml
camera_config:
  pixel_width: 3840
  pixel_height: 2160
  frame_rate: 60
```

### 竖屏视频（TikTok/Shorts）

```yaml
camera_config:
  pixel_width: 1080
  pixel_height: 1920
  frame_rate: 60
  frame_height: 14.222222222222221
  frame_width: 8.0
```

## 故障排除

### 配置未加载

```bash
# Check which config is being used
manimgl scene.py MyScene --verbose

# Specify config explicitly
manimgl scene.py MyScene --config_file ./custom_config.yml
```

### 无效配置

- 确保 YAML 语法正确（缩进、冒号等）
- 检查配置键名是否拼写错误
- 确认路径存在且可访问
- 含空格的路径请用引号括起来

### 性能问题

```yaml
# Reduce quality for testing
camera_config:
  pixel_width: 854
  pixel_height: 480
  frame_rate: 15

# Use temporary storage on SSD
directories:
  temporary_storage: "/path/to/fast/storage"
```
