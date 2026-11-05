# 视频制作中的调色（Color Grading）

> 来源：BBC Academy 色彩标准、Filmmaker IQ 色彩科学系列、DaVinci Resolve
> 调色理论（Blackmagic 文档）、WCAG 2.1 对比度指南、FFmpeg 滤镜
> 文档、Adobe 色彩无障碍研究、Wong (2011) 色盲友好调色板

## 速查卡

```
PROFILES:       cinematic_warm | cinematic_cool | moody_dark | bright_clean | vintage_film | high_contrast | neutral
LUT FORMAT:     .cube (3D LUT) — industry standard, FFmpeg lut3d filter
INTENSITY:      0.6-0.85 for subtle grades, 1.0 for full effect
SKIN TONE:      Vectorscope should fall on the "skin tone line" (~123° on I-line)
COLOR SPACE:    BT.709 for web delivery, BT.2020 for HDR only
BIT DEPTH:      Grade in 10-bit when possible, deliver in 8-bit for web
```

## FFmpeg 滤镜参考

`color_grade` 工具使用以下 FFmpeg 滤镜。理解它们有助于你编写 `custom_vf` 链。

### 核心滤镜

| 滤镜 | 用途 | 关键参数 |
|--------|---------|----------------|
| `eq` | 亮度、对比度、饱和度、伽马 | `contrast=1.0:saturation=1.0:brightness=0.0:gamma=1.0` |
| `colorbalance` | 阴影/中间调/高光中的 RGB 调整 | `rs/gs/bs`（阴影）、`rm/gm/bm`（中间调）、`rh/gh/bh`（高光）— 范围 -1.0 至 1.0 |
| `curves` | 各通道色调曲线 | `all='0/0 0.5/0.5 1/1'` 或分通道 `red=`、`green=`、`blue=` |
| `colortemperature` | 白平衡偏移 | `temperature=6500`（中性）— 数值越低越冷，越高越暖 |
| `lut3d` | 应用外部 .cube LUT | `lut3d='path/to/file.cube'` |
| `hue` | 色相旋转与饱和度 | `h=0:s=1` — h 为度，s 为倍数 |
| `normalize` | 自动将直方图拉伸至全范围 | `blackpt=black:whitept=white:smoothing=0` |

### 滤镜链顺序

按以下顺序应用滤镜以获得可预测的结果：

```
1. normalize          (auto-levels if source is flat/log)
2. colortemperature   (white balance correction)
3. colorbalance       (shadow/mid/highlight color shifts)
4. curves             (contrast and tone shaping)
5. eq                 (final contrast/saturation/brightness tweak)
6. lut3d              (creative LUT — applied LAST, on corrected footage)
```

## 按内容类型选择配置文件

| 内容类型 | 推荐配置文件 | 强度 | 原因 |
|-------------|-------------------|-----------|-----|
| 企业 / SaaS 讲解 | `bright_clean` | 0.8 | 干净、专业、易亲近 |
| 科学 / 教育 | `neutral` | 1.0 | 色彩准确呈现很重要 |
| 叙事 / 故事 | `cinematic_warm` | 0.85 | 暖调有助于情感连接 |
| 科技 / 深色主题 | `cinematic_cool` | 0.7 | 与深色 UI 截图相得益彰 |
| 戏剧 / 严肃话题 | `moody_dark` | 0.6-0.7 | 营造氛围又不压死细节 |
| 生活方式 / 社交媒体 | `high_contrast` | 0.8 | 在移动端醒目、抓注意力 |
| 复古 / 怀旧 | `vintage_film` | 0.7 | 轻微褪色感，不过度 |

## 按情绪定制的参数配方

当内置配置文件不合适时，可将以下作为 `custom_vf` 的起点：

### 暖调 / 亲切

```
colorbalance=rs=0.06:gs=0.02:bs=-0.04:rh=0.05:gh=0.01:bh=-0.03,
eq=contrast=1.05:saturation=1.08:brightness=0.01
```

### 冷调 / 技术感

```
colorbalance=rs=-0.03:gs=-0.01:bs=0.06:rh=-0.02:gh=0.01:bh=0.04,
eq=contrast=1.06:saturation=0.95
```

### 高能量

```
curves=all='0/0 0.15/0.08 0.5/0.52 0.85/0.92 1/1',
eq=contrast=1.15:saturation=1.2
```

### 低调 / 严肃

```
curves=all='0/0.04 0.25/0.22 0.5/0.47 0.75/0.73 1/0.94',
eq=contrast=1.03:saturation=0.75:brightness=-0.02
```

## LUT 工作流

### 何时使用 LUT
- 统一不同相机/来源的素材
- 模拟特定胶片 stock
- 在多条视频中保持品牌色彩一致
- 将 LOG/flat 机内配置转为显示色彩

### LUT 应用最佳实践
1. **先校正再调色** — 先 normalize/白平衡，再应用创意 LUT
2. **强度 < 1.0** — 全强度 LUT 通常过重；0.6–0.8 较常见
3. **先在肤色上测试** — 若画面有人，肤色必须自然
4. **每个项目一个 LUT** — 场景间换 LUT 会造成视觉不一致
5. **LUT 文件位置** — 放在项目相对路径 `assets/luts/`，用 `lut_path` 引用

### FFmpeg LUT 应用
```bash
# Apply LUT at 70% intensity (blend with original)
ffmpeg -i input.mp4 -vf "split[a][b];[b]lut3d='my_lut.cube'[graded];[a][graded]blend=all_mode=normal:all_opacity=0.7" output.mp4
```

## 肤色保护

肤色是调色中最关键的元素 — 观众会立刻察觉不自然的肤色。

**肤色线（Skin Tone Line）：**
- 在 vectorscope 上，健康肤色（各人种）大致落在约 123 度的一条窄线上（红与黄之间）
- 若调色把肤色推离该线，应降低饱和度或调整色相

**规则：**
- 含人物的素材饱和度勿超过 1.2
- 调色后检查一帧可见肤色 — 若偏橙、绿或品红，应回退
- `cinematic_warm` 在强度 0.85 时已预调以保持肤色自然
- 对 `moody_dark`，强度保持在 0.6–0.7，避免肤色发灰

## 无障碍

### 色盲友好设计（Wong 调色板）

为与调色视频配套的图形、叠加层或示意图生成内容时，使用经验证对常见色觉缺陷均安全的调色板：

| 颜色 | Hex | 用途 |
|-------|-----|---------|
| Black | `#000000` | 文字、描边 |
| Orange | `#E69F00` | 主强调色 |
| Sky Blue | `#56B4E9` | 次强调色 |
| Bluish Green | `#009E73` | 正向/成功 |
| Yellow | `#F0E442` | 高亮/警告 |
| Blue | `#0072B2` | 链接、信息 |
| Vermillion | `#D55E00` | 错误/危险 |
| Reddish Purple | `#CC79A7` | 第三强调色 |

### WCAG 对比度要求

| 元素 | 最低比例 | 标准 |
|---------|--------------|----------|
| 背景上的正文 | 4.5:1 | WCAG AA |
| 背景上的大字号文字（>18pt） | 3:1 | WCAG AA |
| 正文（增强） | 7:1 | WCAG AAA |
| UI 组件 / 图形对象 | 3:1 | WCAG 2.1 |

**实用规则：** 调色后，烧录进视频的任何文字叠加或字幕相对调色后的背景仍须满足 4.5:1 对比度。在代表性帧上用对比度检查工具验证。

## 在 OpenMontage 中应用

使用 `color_grade` 工具时：

1. **按内容类型选配置文件** — 用上表，不要什么都默认 `cinematic_warm`
2. **强度从 0.8 起步**，而非 1.0 — 在移动屏上 subtle 更易读
3. **先对单帧测试**再整片调色 — 节省渲染时间
4. **在人脸增强之后调色** — `skills/creative/enhancement-strategy.md` 中的增强链顺序为：字幕 → 人脸 → 色彩 → 音频 → 成片
5. **同一视频内所有片段用同一配置文件** — 视觉一致至关重要
6. **对生成画面**（image_selector、math_animate），用较轻调色（0.5–0.6），因其已带风格
7. **生成图形**（示意图、代码片段、叠加层）使用 Wong 调色板，保证色盲无障碍
8. **自定义调色**时遵循上述滤镜链顺序，参数微调 — 每次约 ±0.05，再复查
