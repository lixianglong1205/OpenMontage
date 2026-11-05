# ManimGL 交互式开发

ManimGL 的杀手级功能是交互式开发模式，让你无需重新渲染整个场景即可快速迭代。

## 启动交互模式

使用 `-se`（skip and embed，跳过并嵌入）标志并指定行号：

```bash
# 在第 20 行进入交互模式
manimgl scene.py MyScene -se 20

# 从开头进入
manimgl scene.py MyScene -se 1
```

场景会运行到该行，然后进入 IPython shell。

## checkpoint_paste()

核心工作流函数。将代码复制到剪贴板，然后：

```python
# 从剪贴板运行代码并播放完整动画
checkpoint_paste()

# 立即运行、不播放动画（用于快速迭代）
checkpoint_paste(skip=True)

# 运行同时录制动画
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

        self.embed()  # 在此暂停，进入 shell

        # 退出 shell 后执行下方代码
        self.play(FadeOut(circle))
```

在 shell 中，你可以完全访问：
- `self` - 场景实例
- 作用域内所有 mobject
- 所有 ManimGL 函数

## 交互式 Shell 命令

进入 shell 后：

```python
# 查看当前 mobject
self.mobjects

# 添加新对象
square = Square()
self.play(ShowCreation(square))

# 清空后重试
self.clear()

# 退出 shell 并继续场景
exit()
# 或 Ctrl+D
```

## 快速迭代模式

```python
class DevelopScene(InteractiveScene):
    def construct(self):
        # 不常改动的设置
        axes = Axes()
        self.add(axes)

        # 开发断点
        self.embed()

        # 正在迭代的代码放在这里
        # （或在 shell 中使用 checkpoint_paste()）
```

## 录制模式

当你想捕获交互过程中的操作时：

```python
# 开始录制
checkpoint_paste(record=True)

# 此后所有动画都会被录制
# 完成后视频会保存
```

## 常用 Shell 变量

```python
# 当前帧（相机）
self.frame

# 所有 mobject
self.mobjects

# 按类型筛选 mobject
[m for m in self.mobjects if isinstance(m, Circle)]

# 帧中心
self.frame.get_center()
```

## 调试技巧

```python
# 打印 mobject 信息
print(circle.get_center())
print(circle.get_height())
print(circle.get_color())

# 高亮某个 mobject
circle.set_color(YELLOW)
self.wait(0.1)

# 查看场景中有哪些对象
print(len(self.mobjects))
```

## 退出并继续

```python
# 交互会话结束后继续场景
exit()  # 或 Ctrl+D

# 场景会从暂停处继续执行
```

## 最佳实践

1. **开发时使用 `-se`** - 比重新渲染快得多
2. **将设置代码放在 embed 之前** - 复用状态
3. **使用 `checkpoint_paste(skip=True)`** - 用于快速测试
4. **使用 `checkpoint_paste(record=True)`** - 效果满意后再录制
5. **将代码组织成函数** - 便于粘贴和测试
