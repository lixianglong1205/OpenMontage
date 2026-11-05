# ManimGL 交互式开发

ManimGL 的杀手级功能是交互式开发模式，让你无需重新渲染整个场景即可快速迭代。

## 启动交互模式

使用 `-se`（skip and embed，跳过并嵌入）标志并指定行号：

```bash
# Enter interactive mode at line 20
manimgl scene.py MyScene -se 20

# Enter at the beginning
manimgl scene.py MyScene -se 1
```

场景会运行到该行，然后进入 IPython shell。

## checkpoint_paste()

核心工作流函数。将代码复制到剪贴板，然后：

```python
# Run code from clipboard with full animations
checkpoint_paste()

# Run instantly without animations (for quick iteration)
checkpoint_paste(skip=True)

# Record animations while running
checkpoint_paste(record=True)
```

### 典型工作流

1. 编写场景，并预留占位行
2. 在该行使用 `-se` 运行
3. 将动画代码复制到剪贴板
4. 调用 `checkpoint_paste()` 进行测试
5. 反复迭代直到满意
6. 将代码移入实际文件

## self.embed()

以编程方式进入 IPython shell：

```python
class MyScene(InteractiveScene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))

        self.embed()  # Pause here, enter shell

        # Code below runs after you exit the shell
        self.play(FadeOut(circle))
```

在 shell 中，你可以完全访问：
- `self` - 场景对象
- 作用域内所有 mobject
- 所有 ManimGL 函数

## 交互式 Shell 命令

进入 shell 后：

```python
# Inspect current mobjects
self.mobjects

# Add something new
square = Square()
self.play(ShowCreation(square))

# Clear and try again
self.clear()

# Exit shell and continue scene
exit()
# or Ctrl+D
```

## 快速迭代模式

```python
class DevelopScene(InteractiveScene):
    def construct(self):
        # Setup that doesn't change often
        axes = Axes()
        self.add(axes)

        # Breakpoint for development
        self.embed()

        # Code you're iterating on goes here
        # (Or use checkpoint_paste() in the shell)
```

## 录制模式

当你想捕获交互过程中的操作时：

```python
# Start recording
checkpoint_paste(record=True)

# All animations are now recorded
# When done, video is saved
```

## 常用 Shell 变量

```python
# Current frame (camera)
self.frame

# All mobjects
self.mobjects

# Specific mobjects by type
[m for m in self.mobjects if isinstance(m, Circle)]

# Frame center
self.frame.get_center()
```

## 调试技巧

```python
# Print mobject info
print(circle.get_center())
print(circle.get_height())
print(circle.get_color())

# Highlight a mobject
circle.set_color(YELLOW)
self.wait(0.1)

# Check what's in the scene
print(len(self.mobjects))
```

## 退出并继续

```python
# After interactive session, continue scene
exit()  # or Ctrl+D

# The scene continues from where it left off
```

## 最佳实践

1. **开发时使用 `-se`** - 比重新渲染快得多
2. **将 setup 代码放在 embed 之前** - 复用状态
3. **使用 `checkpoint_paste(skip=True)`** - 用于快速测试
4. **使用 `checkpoint_paste(record=True)`** - 效果满意后再录制
5. **将代码组织成函数** - 便于粘贴和测试
