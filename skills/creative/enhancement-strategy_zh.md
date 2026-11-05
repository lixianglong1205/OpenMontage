# 增强策略技能

## 何时使用

在决定如何增强 talking-head（Talking Head，口播/对镜头讲话）素材时使用本技能：选用哪些人脸/调色/音频预设、添加哪些叠加层，以及如何平衡增强效果与自然观感。

## 增强工具

| 工具 | 作用 | 推荐预设 |
|------|-------------|-------------------|
| `face_enhance` | 皮肤平滑、锐化、色调校正 | `talking_head_standard` |
| `color_grade` | 可控强度的电影感调色 | `cinematic_warm`，强度 0.85 |
| `audio_enhance` | 响度归一、降噪、均衡 | `clean_speech` |
| `code_snippet` | 将代码渲染为风格化叠加图 | `monokai` 主题 |
| `diagram_gen` | 生成框图/流程图作为叠加图 | `dark` 主题 |
| `image_selector` | AI 生成插图（需 API key） | — |

## 增强链路

按以下顺序应用——每一步可选，失败时优雅跳过：

```
raw footage
  → subtitle burn (video_compose)
  → face enhance (face_enhance)
  → color grade (color_grade)
  → audio enhance (audio_enhance)
  → final encode (video_compose)
```

### 人脸增强预设

| 预设 | 适用场景 |
|--------|-------------|
| `talking_head_standard` | 任意 talking head 默认——平滑 + 锐化 + 暖调 |
| `soft_skin` | 网络摄像头素材毛孔明显——轻柔磨皮 |
| `sharpen` | 画面偏软/模糊——增强边缘 |
| `brighten` | 偏暗/欠曝——提亮阴影与中间调 |
| `denoise` | 颗粒感（弱光、高 ISO）——时域降噪 |

### 调色配置

| 配置 | 观感 | 强度 |
|---------|------|-----------|
| `cinematic_warm` | 暖高光、抬阴影、略增饱和 | 0.85 |
| `cinematic_cool` | 青绿阴影、橙色高光 | 0.7 |
| `bright_clean` | 鲜明、提亮、YouTube 风格 | 0.8 |
| `moody_dark` | 压黑、降饱和——戏剧感 | 0.6 |
| `neutral` | 最小校正——仅归一化电平 | 1.0 |

### 音频增强预设

| 预设 | 适用场景 | 目标 |
|--------|-------------|--------|
| `clean_speech` | talking head 默认——完整处理链 | -16 LUFS |
| `voice_clarity` | 人声发闷——提升 3kHz/5kHz 存在感 | -16 LUFS |
| `podcast` | 访谈/播客——更强压缩 | -16 LUFS |
| `noise_reduce` | 环境嘈杂——激进 FFT 降噪 | -16 LUFS |
| `normalize_only` | 源已干净，仅需响度匹配 | -16 LUFS |

## 叠加层增强类型

| 类型 | 适用场景 | 工具 | 位置 |
|------|-------------|------|-----------|
| **Text overlay** | 关键词、数据、引用 | video_compose overlay | 上三分之一或下三分之一 |
| **Code snippet** | 技术内容、API 示例 | code_snippet → overlay | 画面侧边或全屏 |
| **Diagram** | 可视化讲解概念 | diagram_gen → overlay | 画面侧边或全屏 |
| **Lower third** | 讲者姓名、主题标签 | video_compose overlay | 画面下方 20% |

## 叠加密度指南

### 短视频（< 60 秒）
- 高密度：每 3–5 秒一次叠加
- 快速视觉变化、醒目文字
- 字幕**必选**（多数观众静音观看）

### 中视频（1–10 分钟）
- 中等密度：每 10–20 秒一次叠加
- 让讲者主导段落，减少视觉争抢

### 长视频（> 10 分钟）
- 低密度：每 30–60 秒一次叠加
- 仅在内容受益时增强（要点、复杂主题）

## 布局规则

1. **勿遮挡讲者面部**——眼、鼻、口须保持可见
2. **字幕放在下方 20%**——竖屏 margin_v: 50，横屏 40
3. **位置一致**——叠加一旦放在左侧，全程保持
4. **文字叠加停留 2–5 秒**——够读、又不显拖沓

## 决定增强什么

对脚本各段自问：

1. 讲者在讲可视化内容？→ 加示意图（`diagram_gen`）
2. 有关键数据或引用？→ 加文字叠加
3. 有代码或技术内容？→ 加代码截图（`code_snippet`）
4. 讲者连续出镜 > 30 秒？→ 考虑 B-roll 或叠加
5. 是开场或结尾？→ 用醒目文字叠加呈现核心信息

## 质量检查清单

- [ ] 人脸增强自然——不过度磨皮、不偏橙
- [ ] 调色可见但克制——肤色健康
- [ ] 音频归一至目标 LUFS——全程音量一致
- [ ] 字幕移动端可读，位于面部下方
- [ ] 叠加有信息价值（非纯装饰）
- [ ] 增强密度与内容时长、平台匹配
