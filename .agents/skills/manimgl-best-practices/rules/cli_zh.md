# ManimGL 命令行界面

ManimGL 使用 `manimgl` 命令渲染场景，并提供多种强大标志以适配不同工作流。

## 基本用法

### 运行场景

```bash
# Basic syntax
manimgl scene_file.py SceneName

# Example
manimgl my_animation.py SquareToCircle
```

### 自动选择场景

```bash
# If only one scene in file, it runs automatically
manimgl my_animation.py

# If multiple scenes, presents a menu to choose from
manimgl my_animations.py
```

## 常用标志

### 写入文件

```bash
# Write to file (no preview)
manimgl scene.py MyScene -w

# Write and open the file
manimgl scene.py MyScene -o

# Show final frame only
manimgl scene.py MyScene -s

# Save final frame as image and show
manimgl scene.py MyScene -so
```

### 交互模式

```bash
# Skip to line 15 and enter interactive mode
manimgl scene.py MyScene -se 15

# Interactive mode at specific line
manimgl scene.py MyScene --skip_animations --embed 20
```

### 显示选项

```bash
# Fullscreen window
manimgl scene.py MyScene -f

# Custom window size
manimgl scene.py MyScene --resolution 1920,1080

# Hide progress bar
manimgl scene.py MyScene --quiet
```

## 质量与分辨率

### 分辨率预设

```bash
# Low quality (for testing)
manimgl scene.py MyScene -l

# Medium quality
manimgl scene.py MyScene -m

# High quality (1080p)
manimgl scene.py MyScene -h

# 4K quality
manimgl scene.py MyScene --uhd

# Custom resolution
manimgl scene.py MyScene --resolution 2560,1440
```

### 帧率

```bash
# Set frame rate (default is 60)
manimgl scene.py MyScene --frame_rate 30

# Lower frame rate for faster renders
manimgl scene.py MyScene --frame_rate 15
```

## 高级标志

### 跳转到指定动画

```bash
# Skip to nth animation
manimgl scene.py MyScene -n 5

# Skip animations (instant mode)
manimgl scene.py MyScene --skip_animations
```

### 输出选项

```bash
# Specify output file
manimgl scene.py MyScene -o output.mp4

# Save as GIF
manimgl scene.py MyScene --format gif

# Transparent background
manimgl scene.py MyScene --transparent
```

### 配置

```bash
# Use custom config file
manimgl scene.py MyScene --config_file custom_config.yml

# Set specific config values
manimgl scene.py MyScene --config camera_config.frame_rate=30
```

## 交互式开发

### `-se` 标志

`-se`（skip and embed，跳过并嵌入）是 ManimGL 的杀手级功能：

```bash
# Drop into interactive shell at line 15
manimgl scene.py MyScene -se 15
```

在交互式 shell 中：

```python
# Use abbreviated commands (no self.)
play(circle.animate.shift(RIGHT))
add(Square())
remove(circle)
wait(2)

# Copy code to clipboard, then:
checkpoint_paste()              # Run with animations
checkpoint_paste(skip=True)     # Run instantly
checkpoint_paste(record=True)   # Record while running

# Interactive camera control
touch()  # Press 'd' + mouse to rotate, 'z' + scroll to zoom

# Exit
exit()
```

## 文件组织

### 从不同目录运行

```bash
# From same directory as manimlib/
manimgl project/scene.py MyScene

# With absolute path
manimgl /full/path/to/scene.py MyScene

# With relative path
manimgl ../other_project/scene.py MyScene
```

## 组合标志

### 常见组合

```bash
# High quality, write and open
manimgl scene.py MyScene -h -o

# Low quality, fullscreen, for testing
manimgl scene.py MyScene -l -f

# Skip animations, final frame only
manimgl scene.py MyScene -s --skip_animations

# Interactive at line 20, low quality
manimgl scene.py MyScene -l -se 20

# Save as GIF, high quality
manimgl scene.py MyScene -h --format gif -o
```

## 工作流示例

### 开发工作流

```bash
# 1. Initial testing (low quality, fast)
manimgl scene.py MyScene -l

# 2. Interactive debugging at specific point
manimgl scene.py MyScene -l -se 25

# 3. Check final frame
manimgl scene.py MyScene -s

# 4. Final render (high quality, save and open)
manimgl scene.py MyScene -h -o
```

### 快速预览工作流

```bash
# Show final frame immediately
manimgl scene.py MyScene -s

# If it looks good, render full animation
manimgl scene.py MyScene -o
```

### 批量渲染

```bash
# Render multiple scenes
for scene in Scene1 Scene2 Scene3; do
    manimgl scenes.py $scene -h -w
done
```

## 调试标志

### 详细输出

```bash
# Show detailed output
manimgl scene.py MyScene --verbose

# Show all debug info
manimgl scene.py MyScene --debug
```

### 性能分析

```bash
# Show performance stats
manimgl scene.py MyScene --profile

# Detailed timing information
manimgl scene.py MyScene --timing
```

## 配置覆盖

### 临时修改配置

```bash
# Override window size
manimgl scene.py MyScene --config window_config.size=fullscreen

# Override output directory
manimgl scene.py MyScene --config directories.output=/tmp/manim

# Multiple overrides
manimgl scene.py MyScene \
    --config camera_config.frame_rate=30 \
    --config camera_config.pixel_width=1280
```

## 帮助与信息

### 获取帮助

```bash
# Show all available flags
manimgl --help

# Show version
manimgl --version

# List scenes in file without running
manimgl scene.py --list_scenes
```

## 完整 CLI 参考

### 主要标志一览

```bash
# Quality/Resolution
-l, --low_quality           # 480p, 15fps
-m, --medium_quality        # 720p, 30fps
-h, --high_quality          # 1080p, 60fps
--uhd                       # 4K, 60fps
--resolution WIDTHxHEIGHT   # Custom resolution

# Output
-w, --write_file            # Write to file
-o, --open                  # Write and open
-s, --show_last_frame       # Show final frame
--format FORMAT             # Output format (mp4, gif, png)
--transparent               # Transparent background

# Playback
-f, --fullscreen            # Fullscreen window
-n NUM, --skip_to NUM       # Skip to animation number
--skip_animations           # Skip all animations

# Interactive
-e, --embed                 # Drop into IPython shell
--skip_animations --embed   # Interactive at end (skip animations)
-se LINE, --skip_and_embed  # Interactive at line number

# Configuration
--config_file FILE          # Custom config file
--config KEY=VALUE          # Override config value

# Debugging
--verbose                   # Verbose output
--debug                     # Debug mode
--quiet                     # Minimize output
--profile                   # Performance profiling

# Other
--version                   # Show version
--help                      # Show help
--list_scenes               # List scenes in file
```

## 最佳实践

1. **开发时使用 `-l`**：低质量快速迭代
2. **调试时使用 `-se`**：在问题位置进入交互模式
3. **快速检查使用 `-s`**：全片渲染前先确认最终帧
4. **定稿使用 `-h -o`**：准备好后输出高质量结果
5. **合理组合标志**：例如 `-l -f` 用于全屏测试
6. **自定义配置**：不同项目使用不同配置文件
7. **脚本化常用命令**：为频繁操作创建 shell 别名

## 常用别名

添加到 `.bashrc` 或 `.zshrc`：

```bash
# Quick preview
alias mgl='manimgl -l'

# Final render
alias mgf='manimgl -h -o'

# Interactive debug
alias mgd='manimgl -l -se'

# Show final frame
alias mgs='manimgl -s'
```

## 故障排除

### 常见问题

```bash
# Scene not found
manimgl scene.py  # Lists all scenes if you don't specify

# Can't find manimlib
# Ensure you're in the directory with manimlib/ or use full paths

# Window not showing
# Check window_config in custom_config.yml

# Poor performance
# Use -l flag, reduce frame_rate, or lower resolution
```

## 示例命令

```bash
# Simple preview
manimgl examples/basic_animations.py SquareToCircle

# High quality render
manimgl examples/basic_animations.py SquareToCircle -h -o

# Interactive debugging at line 30
manimgl examples/basic_animations.py SquareToCircle -se 30

# Save as GIF
manimgl examples/basic_animations.py SquareToCircle --format gif -o

# Custom resolution
manimgl examples/basic_animations.py SquareToCircle --resolution 2560,1440

# Skip to 5th animation and show
manimgl examples/basic_animations.py SquareToCircle -n 5

# Fullscreen, low quality for testing
manimgl examples/basic_animations.py SquareToCircle -l -f
```
