# OpenMontage 中的 ManimCE 用法

> 来源：ManimCE 文档、3Blue1Brown FAQ/惯例、Theorem of Beethoven 教程，
> 以及现有 Layer 3 技能 `.agents/skills/manimce-best-practices/`

## 速查卡

```
RENDER QUALITY:   -qh (1080p60) for YouTube  |  -qm (720p30) for drafts
BACKGROUND:       Dark (#1a1a2e or BLACK)
MAX ELEMENTS:     3-4 new visual elements revealed simultaneously
PACING:           One concept per scene, build incrementally
EQUATION WRITE:   1.5-2.0s run_time
SHAPE CREATE:     0.8-1.2s run_time
WAIT AFTER:       1.0-2.0s (longer for complex equations)
2D vs 3D:         Default to 2D. 3D only when spatial relationship IS the concept.
```

## OpenMontage 渲染设置

| 标志 | 分辨率 | FPS | 用途 |
|------|-----------|-----|----------|
| `-ql` | 480x360 | 15 | 开发/测试 |
| `-qm` | 1280x720 | 30 | 草稿审阅 |
| `-qh` | 1920x1080 | 60 | 标准 YouTube 上传 |
| `-qp` | 2560x1440 | 60 | 高质量导出 |
| `-qk` | 3840x2160 | 60 | 4K 归档/精品 |

针对 OpenMontage 的 YouTube 横屏配置（1920x1080/30fps），使用 `-qh` 渲染后转码为 30fps，或设置自定义配置：

```ini
[CLI]
pixel_width = 1920
pixel_height = 1080
frame_rate = 30
```

## 动画时序

| 动画类型 | `run_time` | 速率函数 | 说明 |
|---------------|-----------|---------------|-------|
| 公式书写（`Write`） | 1.5-2.0s | `smooth`（默认） | 给观众时间解析 LaTeX |
| 公式变换 | 1.5s | `smooth` | 推导时使用 `TransformMatchingTex` |
| 图形创建（`Create`） | 0.8-1.2s | `smooth` | `Create()` 或 `DrawBorderThenFill()` |
| 颜色高亮 | 0.5s | `smooth` | 短暂吸引注意 |
| 镜头缩放 | 1.5-2.0s | `ease_in_out_cubic` | 平滑进入/退出 |
| 交错揭示 | `lag_ratio=0.1-0.2` | — | 网格/列表揭示用 `LaggedStart` |
| 揭示后等待 | 1.0-2.0s | — | 复杂公式可更长 |
| 快切 / 标点 | 0.3-0.5s | `rush_from` | 概念之间 |

## 场景构图

### 节奏规则（3Blue1Brown 惯例）

- **每个场景一个概念** — 逐步构建
- 先展示简单版本，再用 `Transform` 变为复杂版本
- 同时揭示的新视觉元素不超过 **3-4 个**
- 每次主要揭示后使用 `self.wait(1.5)`

### 2D 与 3D 选择

**使用 2D**（`Scene` 或 `MovingCameraScene`）适用于：
- 公式推导、函数图像、数轴、矩阵
- 二维向量空间（即便讲「高维」— 投影到二维）
- 状态图、流程图、时间线

**仅在以下情况使用 3D**（`ThreeDScene`）：
- 可视化曲面（`z = f(x,y)`）、体积或三维向量场
- 空间关系本身就是概念（叉积、曲面法线）
- 需要镜头环绕以揭示隐藏结构

**性能：** 3D 使用仅 CPU 的 Cairo 渲染 — 比 2D 慢约 5-10 倍。

## 颜色用法

| 语义角色 | 颜色 | Manim 常量 |
|--------------|-------|----------------|
| 待求变量 | 黄色 | `YELLOW` |
| 矩阵 / 算子 | 红色 | `RED` |
| 特征向量 / 结果 | 青色 | `TEAL` |
| 已知常数 | 蓝色 | `BLUE_C` |
| 标注 / 标签 | 绿色 | `GREEN` |
| 弱化 / 背景 | 50% 灰 | `GREY`, `opacity=0.5` |
| 错误 / 错误路径 | 深红 | `RED_E` |

**无障碍：** 避免仅用红绿区分。在色相变化之外配合亮度变化（`_A` 至 `_E` 色阶）。

**背景：** 视频输出始终使用深色背景（`BLACK` 或 `#1a1a2e`）。

## 在 OpenMontage 中应用

使用 `math_animate` 工具时：

1. **最终输出用 `-qh`**（1080p60），草稿用 `-qm`
2. **每个场景一个概念** — 将复杂证明拆成多个 Manim 场景
3. **遵循上表时序** — 公式不要过快（书写 1.5-2.0s）
4. **揭示后等待** — 关键洞察后至少 `self.wait(1.5)`
5. **深色背景** — 在配置中设置 `background_color=BLACK`
6. **语义化用色** — 未知量黄色、已知量蓝色、算子红色
7. **默认 2D** — 仅当理解必须依赖 3D 时使用 `ThreeDScene`
8. **复杂揭示交错** — 列表/网格用 `LaggedStart`，`lag_ratio=0.15`
9. **与旁白同步** — 场景总时长应与脚本中旁白片段时长相匹配
