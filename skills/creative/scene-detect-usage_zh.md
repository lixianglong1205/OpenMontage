# OpenMontage 场景检测用法

> 来源：PySceneDetect 文档、FFmpeg scenedetect 滤镜文档、PySceneDetect
> GitHub issues #187（阈值调优）与 #226（adaptive 讨论）

## 速查卡

```
DEFAULT METHOD:   content (ContentDetector) — works for most content
DEFAULT THRESH:   27.0 (range 0-255)
MIN SCENE LEN:    1.0s default, 2.0-3.0s for educational video
TUNING:           Generate stats CSV first, inspect content_val column
HARD CUTS:        Use content detector
FADE TO BLACK:    Use threshold detector
MIXED CONTENT:    Use adaptive detector
```

## 算法选择

| 方法 | 默认阈值 | 适用场景 | 工作原理 |
|--------|------------------|----------|-------------|
| `content` | 27.0 | 镜头之间的硬切 | 相邻帧 HSV 色差（0-255） |
| `threshold` | 12.0 | 淡入/淡出至黑场 | 平均像素亮度；检测经黑场的过渡 |
| `adaptive` | 3.0 | 含摄像机运动的混合内容 | 帧差滚动平均；适应局部节奏 |

## 阈值调优指南

### ContentDetector（默认，从这里开始）

| 现象 | 操作 | 新阈值 |
|---------|--------|---------------|
| 误切过多 | 提高阈值 | 35-45 |
| 漏检真实切点 | 降低阈值 | 20-22 |
| 快节奏内容（MV、动作片） | 提高 | 35-40 |
| 慢节奏/静态内容（口播、演示） | 降低 | 20-25 |
| 动画内容（Manim、动态图形） | 提高 | 30-35 |

### AdaptiveDetector

- 滚动平均的倍数（默认 3.0）
- 当快速摄像机运动导致 ContentDetector 误报时，通常优于 ContentDetector
- 适合 OpenMontage 讲解类：Manim 段落较静、实拍可能有运动时的默认选择

### ThresholdDetector

- 仅适用于刻意使用淡入淡出至黑场的视频
- 多数 AI 生成视频不使用淡入淡出 — 优先 `content` 或 `adaptive`

## 调优工作流

1. **先生成统计文件：**
   ```bash
   scenedetect -i video.mp4 --stats stats.csv detect-content
   ```

2. **查看 `stats.csv`** — 关注 `content_val` 列。峰值 = 场景变化。

3. **将阈值** 设在最小真实峰值略下方。

4. **设置 `min_scene_length`** 以抑制微场景：
   - 教育类视频：最短 2.0-3.0 秒
   - 快节奏内容：0.5-1.0 秒
   - 默认：1.0 秒

### 分量权重（进阶）

ContentDetector 得分 = HSV + 边缘差的加权和：

```
weights = (delta_hue, delta_sat, delta_lum, delta_edges)
Default: (1.0, 1.0, 1.0, 0.0)
```

对有色相过渡但真实切点较少的动画内容：
```
weights=(1.0, 0.5, 1.0, 0.2), threshold=32
```

## 检测后处理场景列表

检测完成后，清理场景列表：

1. **合并过短片段** — 短于 `min_scene_length` 的场景应并入相邻场景
2. **校验边界** — 确认场景边界与旁白停顿对齐（讲解类）
3. **标注场景** — 将检测到的场景映射到脚本段落，供剪辑阶段使用

## 内容类型预设

| 内容类型 | 方法 | 阈值 | 最短场景时长 |
|-------------|--------|-----------|-----------------|
| 口播（单机位） | content | 22 | 3.0s |
| 口播（多机位） | content | 27 | 1.0s |
| 屏幕录制 | content | 30 | 2.0s |
| 动画讲解 | adaptive | 3.0 | 2.0s |
| 快节奏蒙太奇 | content | 40 | 0.5s |
| 含淡入淡出的纪录片 | threshold | 12 | 2.0s |

## 在 OpenMontage 中的应用

使用 `scene_detect` 工具时：

1. **从 `content` 方法、阈值 27 开始** — 适用于多数内容
2. **口播流水线**：阈值降至 22，`min_scene_length` 设为 3.0s
3. **动画讲解流水线**：使用 `adaptive`，默认阈值 3.0
4. **调优时务必先生成 stats CSV** — 不要凭猜测设阈值
5. **教育类内容将 min_scene_length 设为 2.0s**，避免微场景
6. **用检测结果指导剪辑阶段** — 将场景映射到脚本段落
7. **AI 生成视频片段** 用 `content` 而非 `threshold` — AI 视频很少使用淡入淡出至黑场
