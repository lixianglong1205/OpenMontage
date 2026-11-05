# 电影感视频流水线

> 来源：No Film School 编辑指南、StudioBinder 电影制作资源、Film Riot 制作教程、CinematographyDB 镜头数据库、Walter Murch《眨眼之间》（In the Blink of an Eye）

> 通用摄影词汇（机位、镜头、运动、对焦基元，以及五维规格：主体 / 主体运动 / 场景 / 空间构图 / 摄影机）见 `skills/creative/video-gen-prompting.md`。本文件在这些基元之上叠加电影感专用惯例——不重新定义它们。

## 速查卡

```
ASPECT RATIO:     2.39:1 (widescreen cinematic) or 16:9 with letterbox
LETTERBOX:        Black bars at top/bottom — 1920x800 active area in 1920x1080 frame
FRAME RATE:       24fps (cinematic standard)
SHOT DURATION:    4-8 seconds average (longer than explainer, shorter than documentary)
COLOR GRADE:      cinematic_warm or cinematic_cool profile
AUDIO:            Layered: dialogue + ambient + Foley + score
MUSIC:            60-90 BPM, orchestral or ambient, dynamic (not loop-based)
TARGET LUFS:      -14 LUFS integrated, -24 LUFS for quiet moments
```

## 用视觉成因替换情绪形容词

> **「电影感」和「史诗感」无法约束像素。** 电影感外观来自具体选择：画幅比、镜头、主光、调色、镜头时长与音频层数。写明这些——其余是装饰。
>
> CMU/Harvard CHAI 研究表明，主观措辞在标注者与模型解读间差异很大，意味着标记为「阴郁 moody」的节拍每次渲染会走向不同画面。用产生阴郁感的灯光 + 调色 + 镜头时长组合替换该形容词。脚本侧等价规则见 `skills/creative/storytelling.md` 中的「Anti-Subjective Rule」。
>
> | 情绪形容词 | 电影感转译 |
> |---|---|
> | "epic" | 2.39:1 letterbox, 24fps, 8s+ shot duration, orchestral score with crescendo |
> | "moody" | `moody_dark` grade at 0.6, key light at 1/8 fill, 6s+ contemplative shots, ambient bed at -28dB |
> | "intimate" | 1.85:1, 40-50mm equivalent, shallow DoF, 2 audio layers (dialogue + room tone), no music under dialogue |
> | "cinematic" | （禁用该词——选上表之一或描述实际选择） |

## 画幅比

| 比例 | 分辨率（1080p 画框内） | 观感 | 适用场景 |
|-------|---------------------------|------|-------------|
| **2.39:1** (anamorphic) | 1920x803（上下各 138px 黑边） | 史诗、电影感、宏大 | 电影感解说、品牌片 |
| **2.35:1** (scope) | 1920x817（上下各 131px 黑边） | 经典胶片 | 与 2.39:1 类似，略高 |
| **1.85:1** (flat) | 1920x1038（上下各 21px 黑边） | 适度电影感 | 轻 letterbox，戏剧感较弱 |
| **16:9** (no letterbox) | 1920x1080 | 标准 | 默认，无电影感处理 |

### 在 FFmpeg 中实现 Letterbox

```bash
# Add 2.39:1 letterbox (138px black bars top and bottom)
ffmpeg -i input.mp4 -vf "pad=1920:1080:0:138:black,crop=1920:1080:0:0" output.mp4

# Or render at native ratio and pad:
ffmpeg -i input.mp4 -vf "scale=1920:803,pad=1920:1080:0:138:black" output.mp4
```

**规则：** 仅当内容确实受益于电影感构图时使用 letterbox。不要给录屏或 talking head 加 letterbox——只会浪费像素。

## 镜头时长与节奏

### 各风格平均镜头长度

| 风格 | 平均镜头 | 每分钟切镜数 |
|-------|-------------|-------------|
| 动作/紧张 | 2-4s | 15-30 |
| 标准电影感 | 4-8s | 8-15 |
| 纪录片 | 6-12s | 5-10 |
| 沉思型 | 10-20s | 3-6 |
| 蒙太奇段落 | 1-3s | 20-40 |

### 节奏韵律

电影感节奏遵循 **呼吸式韵律**——刻意变化镜头长度：

```
Long (8s) → Medium (5s) → Short (3s) → Short (2s) → LONG (10s) → Medium (6s)
```

**切勿连续三次使用相同镜头长度**——会造成单调。

### Murch 法则

Walter Murch 的剪辑优先级（按重要性排序）：
1. **情感（Emotion）**——切点是否服务于情感弧线？
2. **故事（Story）**——切点是否推进叙事？
3. **节奏（Rhythm）**——切点在节奏上是否感觉正确？
4. **视线轨迹（Eye trace）**——观众在看哪里？
5. **二维平面（2D plane）**——银幕地理（180 度规则）
6. **三维空间（3D space）**——空间连续性

OpenMontage 采用电影感风格的解说：优先节奏与故事，而非空间连贯（因常在生成图像间切换，而非连续实拍）。

## 音频分层

电影感音频有 **4 层**（不仅是旁白 + 音乐）：

| 层 | 电平 | 内容 |
|-------|-------|---------|
| **对白/旁白** | -12 dB peak | 主声 |
| **音乐/配乐** | -24 to -18 dB | 管弦、氛围、动态 |
| **环境/ room tone** | -30 to -24 dB | 环境声床 |
| **Foley/SFX** | -18 to -12 dB | 具体动作音效 |

### 电影感音乐

| 特征 | 数值 |
|---------------|-------|
| BPM | 60-90（慢于标准解说） |
| 流派 | 管弦、氛围、钢琴、电影感电子 |
| 动态 | 动态（渐强、起伏、安静段落）——非循环 |
| 转调 | 叙事转折点 |
| 静音 | 关键揭示处刻意去掉音乐 3-5 秒 |

### 环境声

添加轻微环境层填充静音并增加纵深：
- Room tone / 空调嗡鸣（极低，-35 dB）
- 与主题匹配的环境声（城市、自然、实验室）
- 即使在旁白停顿时也产生「在场感」

## 电影感调色

| 外观 | Profile | 强度 | 特征 |
|------|---------|-----------|----------------|
| **暖色电影感** | `cinematic_warm` | 0.85 | 橙色高光、抬阴影 |
| **青橙（Teal & orange）** | `cinematic_cool` | 0.7 | 经典好莱坞大片观感 |
| **阴郁暗调** | `moody_dark` | 0.6 | 压黑、低饱和 |
| **复古胶片** | `vintage_film` | 0.7 | 褪色、暖 tint、降对比 |

**电影感调色规则：**
- 阴影应略抬（永不纯黑）
- 高光应略 roll off（永不纯白）
- 肤色须保持在 vectorscope 肤色线上
- 全片 clip 一致——整片一条 LUT/profile
- **若节拍被描述为「moody」，改写为产生阴郁感的灯光 + 调色 + 镜头时长组合。** 勿将情绪形容词传给素材/剪辑阶段。

## 在 OpenMontage 中应用

构建电影感风格内容时：

1. **设定画幅比**——真电影感用 2.39:1 letterbox，或 16:9 配 `cinematic_warm` 做 subtle 处理
2. **以 24fps 渲染**（若内容纯生成/动画，在 `video_compose` 中设置）
3. **镜头时长平均 4-8 秒**——刻意变化，勿连续三次同长
4. **分层音频**——旁白 + 音乐 + 环境至少；关键 moment 加 Foley SFX
5. **音乐 60-90 BPM**，动态（不循环）——`music_gen` 使用 "cinematic orchestral" 类 prompt
6. **关键揭示处去掉音乐 3-5 秒**——静音很有力
7. **用 `cinematic_warm` 或 `cinematic_cool` 调色**，强度 0.7-0.85
8. **图像 prompt** 应含 "cinematic lighting, shallow depth of field, film grain" 以匹配美学
9. **更慢旁白**——140-150 WPM（慢于标准解说 155 WPM）
