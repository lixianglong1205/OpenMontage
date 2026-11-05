# OpenMontage 口型/说话头生成用法

> 来源：SadTalker 论文（Zhang 等，2023）、MuseTalk 文档，以及既有 Layer 2 技能
> `skills/creative/face-restore-usage.md` 与 `skills/creative/enhancement-strategy.md`

## 速查卡

```
DEFAULT MODEL:    sadtalker
INPUT:            One face photo + one audio file → animated talking video
EXPRESSION:       expression_scale=1.0 (0.5 = subtle, 1.5 = expressive)
STILL MODE:       false (true = mouth-only animation, head stays fixed)
PREPROCESS:       crop (default — crops face, animates, pastes back)
KEY RULE:         Generate audio FIRST, then pass to talking_head
```

## 何时使用 talking_head 工具

| 场景 | 是否使用 talking_head？ |
|------|-------------------------|
| 用单张照片制作虚拟形象口播视频 | 是 |
| 个性化消息——用自定义旁白驱动证件照/头像 | 是 |
| 没有视频素材但有照片 | 是 |
| 多语言虚拟形象——同一张脸、不同音轨 | 是 |
| 已有视频素材需要处理 | 否——使用 talking-head 流水线 |
| 将已有视频与新音频对口型 | 否——使用 `lip_sync` 工具 |

## 输入要求

### 照片

- 清晰、正脸、光照良好
- 最低分辨率：256×256 像素
- 最佳效果：512×512 或更大
- 表情中性、直视镜头
- 避免：极端角度、遮挡面部的配饰（大墨镜、口罩）、一张图里多张脸

### 音频

- 干净的语音——WAV 或 MP3
- 采样率：16 kHz 或更高
- 音频时长决定输出视频时长
- 送入 talking_head 前去除背景噪声——干净音频带来更干净的对口型

## 模型选择

| 模型 | 优势 | 劣势 |
|------|------|------|
| sadtalker | 自然的头部运动、表情范围好、久经验证 | 极端表情可能吃力 |
| musetalk | 对口型质量更高、嘴部区域更锐利 | 头部运动更受约束 |

**默认使用 `sadtalker`**，除非对口型精度是最高优先级。

## 参数参考

### 预处理模式

| 模式 | 作用 | 何时使用 |
|------|------|----------|
| `crop` | 裁剪面部区域、驱动动画、贴回原画面 | 默认——最适合头像与肖像 |
| `resize` | 将整幅输入缩放到模型尺寸 | 需要模型分辨率下的全画幅输出时 |
| `full` | 无预处理——输入直接送入模型 | 进阶——输入须已为模型所需尺寸 |

### expression_scale 调节

| 数值 | 效果 | 适用场景 |
|------|------|----------|
| 0.5 | 克制、头部运动最小 | 企业、正式、保守风格 |
| 0.7 | 沉稳、专业 | 商务演示、新闻风格 |
| 1.0 | 自然对话感（默认） | 通用、讲解类 |
| 1.5 | 富有表现力、活力充沛 | 社交媒体、高互动内容 |
| >1.5 | 易出现伪影 | 除非刻意风格化，否则避免 |

### still_mode

| 数值 | 效果 | 适用场景 |
|------|------|----------|
| `false`（默认） | 说话时头部自然运动 | 更真实、对话感 |
| `true` | 仅嘴部动画，头部固定 | 正式/企业观感，或头部运动产生伪影时 |

## 常见工作流

### 1. 虚拟形象口播

```
photo + elevenlabs_tts → talking_head → face_enhance → compose
```

标准虚拟形象视频：从脚本生成语音、驱动照片、面部精修、合成成片。

### 2. 多语言虚拟形象

```
photo + tts per language → talking_head per language → compose variants
```

同一张脸、各语言一条音轨。每种语言各生成一条 talking-head 视频，用于本地化内容。

### 3. 快速社交内容

```
headshot + script → piper_tts → talking_head → subtitle_gen → compose
```

快速出片的社交视频：本地生成语音、驱动动画、加字幕、合成。

### 4. 照片到讲解视频

```
talking_head output → compose with diagram overlays
```

将 talking-head 视频作为讲解层，合成时再叠加示意图、图表或录屏。

## 质量检查清单

接受 talking_head 输出前，请确认：

- [ ] 嘴部动作与音频自然匹配
- [ ] 头部运动有机、不机械
- [ ] 面部边缘与下颌无可见伪影
- [ ] 眨眼自然（非僵住或过快）
- [ ] 输出分辨率满足目标平台
- [ ] 表情强度与旁白语气一致

## 在 OpenMontage 中的用法

使用 `talking_head` 工具时：

1. **先生成音频**（通过 `tts_selector`、`elevenlabs_tts`、`openai_tts` 或 `piper_tts`），再传入 talking_head
2. **以 `expression_scale=1.0` 为基线**——仅在高能量内容时提高
3. **始终在 talking_head 之后使用 `face_enhance`** 以润色输出
4. **企业/专业内容**使用 `still_mode=true` 与 `expression_scale=0.7`
5. **源照片质量直接决定输出质量**——使用手头最佳照片
6. **crop 模式是最稳妥的默认**——仅当 crop 构图不佳时再试 `resize` 或 `full`
7. **全片生成前先预览约 5 秒片段**——尽早发现伪影
8. **降级策略：** 若 SadTalker 不可用但 Wav2Lip 可用，可从照片录一段简单静态视频，再用 `lip_sync` 工具对口型
