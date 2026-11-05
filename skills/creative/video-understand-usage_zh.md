# OpenMontage 中的视频理解用法

> 来源：OpenMontage video_understand 工具实现、CLIP/BLIP2/LLaVA 模型文档、OpenCV 图像质量指标

## 速查卡

```
DEFAULT MODE:     describe — generates captions for frames
FOR REVIEW:       quality — assesses blur, brightness, contrast
FOR Q&A:          qa mode with a query — "Is the speaker visible?" "Is the text readable?"
DEFAULT MODEL:    clip (fastest, good for classification)
FOR DETAIL:       blip2 or llava (slower, richer descriptions)
MAX FRAMES:       5 default for video — sample strategically, not exhaustively
```

## 何时使用 video_understand

- **审片阶段的视觉 QA** — 交付前检查渲染输出质量
- **素材分析** — 在规划前理解用户提供的素材内容
- **高光提取** — 识别视觉上最有趣的帧
- **质量门禁** — 对模糊、曝光、场景一致性做程序化检查
- **场景分类** — 按内容类型对素材分类
- **资产校验** — 验证生成图像是否符合预期场景描述

## 模式选择

| 模式 | 作用 | 适用场景 |
|------|-------------|-------------|
| `describe` | 为帧生成文本描述 | 理解素材内容、记录日志 |
| `qa` | 回答关于帧的特定问题 | 针对性检查（「文字是否可读？」「人脸是否可见？」） |
| `quality` | 数值化测量模糊、亮度、对比度 | 自动化质量门禁、对比不同 take |
| `classify` | 对场景类型分类 | 素材分拣、流水线路由 |

### 质量模式指标

| 指标 | 测量内容 | 差 | 好 |
|--------|-----------------|-----|------|
| `blur_score` | 拉普拉斯方差 | 低于 100 = 模糊 | 高于 500 = 清晰 |
| `brightness` | 像素均值（0-255） | 低于 50 = 过暗，高于 200 = 过曝 | 50-200 |
| `contrast` | 像素标准差 | 低于 30 = 平淡/发灰 | 高于 80 = 对比度良好 |

## 模型选择

| 模型 | 速度 | 能力 | 最适合 |
|-------|-------|-------------|----------|
| `clip` | 快 | 分类、相似度匹配 | 快速场景分类、批处理 |
| `blip2` | 中等 | 详细 caption、视觉 QA | 理解复杂场景、回答问题 |
| `llava` | 慢 | 最细致的理解与推理 | 深度分析、主观质量评估 |

### 模型选择规则

- 批处理与分类任务使用 `clip`
- 需要细节时，describe 与 qa 模式使用 `blip2`
- 仅在需要最全面理解时使用 `llava`

## 视频帧选取

- 默认在整段视频中均匀采样 `max_frames`（5）帧
- 使用 `frame_indices` 指定特定帧（例如在特定时间戳做质量检查）
- 质量审片时至少采样首帧、中间帧、末帧

## 常见工作流

### 1. 剪辑前素材审阅

```
video_understand (describe, 10 frames) → inform scene_plan
```

在规划切点或剪辑前分析用户素材。使用 `blip2` 生成详细描述以支撑场景规划。

### 2. 渲染后质量门禁

```
video_understand (quality) → pass/fail → re-render if needed
```

在合成最终视频后运行。若任一阵 blur_score < 100、brightness 不在 50-200、或 contrast < 30 则判定失败。

### 3. 高光选取

```
video_understand (describe, 20 frames) → rank by visual interest → select clips
```

多帧采样并逐帧描述，再选出视觉最吸引人的片段用于蒙太奇或预告片。

### 4. 资产校验

```
video_understand (qa, "Does this match: [scene description]?") → confirm or regenerate
```

生成图像或视频片段后，在继续流程前确认是否符合预期场景描述。

### 5. 口播/ talking-head 分析

```
video_understand (qa, "Is the speaker's face clearly visible?") → face_enhance if needed
```

在应用唇形同步或人脸修复工具前，检查人脸可见性与构图。

## 质量检查清单

- 描述与帧内实际内容一致
- 质量分数与人工目视检查相符（需人工 spot-check）
- 相似帧上 QA 答案一致
- 相邻帧分类类别稳定
- 质量门禁无假阳性（好帧通过、坏帧失败）

## 在 OpenMontage 中的应用

使用 `video_understand` 工具时：

1. **在 compose 阶段用 `quality` 模式作渲染后门禁** — 低于质量阈值的输出应拒绝
2. **在 talking-head 流水线开头用 `describe` 模式分析用户素材**
3. **批量质量检查用 `clip` 模型**（最快）— 仅在需要详细审阅时改用 `blip2`
4. **质量评估至少采样 3 帧** — 开头、中间、结尾
5. **通过阈值：** blur_score > 100，brightness 50-200，contrast > 30
6. **用 `qa` 模式校验生成资产：**「这张图像是否呈现 [预期内容]？」
7. **在 review 阶段**，将 video_understand 质量数据与 reviewer skill 的评分标准结合
8. **不要对长视频的每一帧都跑 video_understand** — 应策略性采样
