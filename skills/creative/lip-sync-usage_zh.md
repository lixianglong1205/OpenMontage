# OpenMontage 唇形同步用法

> 来源：Wav2Lip 论文（Prajwal 等，2020）、Wav2Lip-GAN 文档、OpenMontage
> `tools/lip_sync.py` 实现

## 速查卡

```
DEFAULT MODEL:    wav2lip (faster, good sync accuracy)
HIGHER QUALITY:   wav2lip_gan (better visual quality, slower)
FACE PADDING:     [0, 10, 0, 0] (top, bottom, left, right)
INPUT:            Video with visible face + audio to sync to
RESIZE FACTOR:    1 = full res (best), 2 = half res (recommended for drafts)
KEY RULE:         Use lip_sync for VIDEO input; use talking_head for PHOTO input
```

## 何时使用 lip_sync

唇形同步是**后期制作**步骤。在生成替换音频之后再使用。

- **配音 / 本地化** — 用翻译后的音频替换原声并对齐口型
- **音频替换** — 重录旁白并与现有视频同步
- **画外音修正** — 修复音画不同步
- **不用于照片转视频** — 请改用 `talking_head` 工具

## 关键区别 — lip_sync 与 talking_head

| | `lip_sync` | `talking_head` |
|---|---|---|
| **输入** | 已有视频 + 新音频 | 静态照片 + 音频 |
| **输出** | 口型已同步的视频 | 由照片生成的新视频 |
| **适用场景** | 配音、音频替换 | 虚拟形象生成、发言人视频 |

**决策规则：** 若已有该人物说话的视频素材，使用 `lip_sync`。若只有照片并希望让其“开口说话”，使用 `talking_head`。

## 模型选择指南

| 模型 | 质量 | 速度 | 最适合 |
|-------|---------|-------|----------|
| `wav2lip` | 口型同步好，下巴可能略糊 | 较快 | 快速配音、草稿 |
| `wav2lip_gan` | 嘴部周围视觉质量更好 | 较慢 | 成片、特写镜头 |

**决策规则：** 迭代与草稿用 `wav2lip`；成片或面部突出（特写、中景）时改用 `wav2lip_gan`。质量差异在嘴部与下巴区域最明显。

## 输入要求

- 视频全程需有清晰可见的人脸
- 面部应正对镜头，或侧向角度不超过约 30 度
- 人脸最小尺寸：宽度约 100px
- 音频应为清晰人声（非音乐或噪声）
- 音频长度应与视频长度大致匹配（误差在 10% 以内）

## 面部 padding

面部 padding 控制检测到的面部周围纳入同步区域的范围。格式：`[top, bottom, left, right]`。

| 场景 | Padding | 原因 |
|----------|---------|--------|
| 默认 talking-head 镜头 | `[0, 10, 0, 0]` | 适用于约 90% 的素材 |
| 下巴被裁切 | 增大索引 1（bottom） | 将遮罩向下延伸过下巴 |
| 额头被裁切 | 增大索引 0（top） | 将遮罩向上延伸过额头 |
| 人脸在画面中偏位 | 调整索引 2、3（left、right） | 补偿横向偏移 |

除非人脸在画面中明显偏位，否则 left/right 保持为 0。

## 缩放因子（Resize Factor）

| 值 | 分辨率 | 质量 | 速度 | 适用场景 |
|-------|-----------|---------|-------|----------|
| 1 | 全分辨率 | 最佳 | 最慢 | 成片 |
| 2 | 一半 | 良好 | 较快 | 草稿、迭代 |
| 3+ | 降低 | 下降 | 最快 | 仅快速预览 |

**建议：** 迭代时使用 `resize_factor=2`，最终输出使用 `resize_factor=1`。

## 常见工作流

### 1. 本地化配音

将视频翻译为其他语言并匹配口型运动。

```
transcriber(video) --> transcript
  --> translate script to target language
--> tts_selector(translated_script, target_language_voice)
  --> lip_sync(original_video, translated_audio)
```

### 2. 音频重录

替换旁白音频并重新同步说话人口型。

```
new_audio_recording
  --> lip_sync(original_video, new_audio)
  --> face_enhance (post-sync cleanup)
  --> compose
```

### 3. 多语言输出

从同一源视频产出多个语言版本。

```
source_video
  --> lip_sync(source_video, english_audio)   --> english_output
  --> lip_sync(source_video, spanish_audio)   --> spanish_output
  --> lip_sync(source_video, french_audio)    --> french_output
```

每种语言均以原始视频为源 — 不要串联 lip_sync 的输出。

## 质量检查清单

进入 compose 阶段前，请逐项核对每条 lip_sync 输出：

- [ ] **口型与新音频自然匹配** — 无不同步或滞后
- [ ] **嘴/下巴区域无视觉瑕疵** — 无模糊、涂抹或色差
- [ ] **面部区域与画面其余部分无缝融合** — 无可见边界
- [ ] **帧间无时间闪烁** — 帧间过渡平滑
- [ ] **音画同步紧密** — 口型与声音之间无可感知延迟

## 在 OpenMontage 中的应用

在后期制作中使用 `lip_sync` 工具时：

1. **先生成替换音频**（`tts_selector`、`elevenlabs_tts`、`openai_tts` 或 `piper_tts`），再唇形同步 — lip_sync 需要成品音频作为输入
2. **草稿与迭代用 `wav2lip`，成片用 `wav2lip_gan`** — 在创作循环中节省处理时间
3. **在 lip_sync 之后应用 `face_enhance`，而非之前** — lip_sync 会修改面部区域，先增强再同步是浪费
4. **本地化工作流中以原视频为源**，各语言分别同步 — 切勿串联 lip_sync 输出
5. **同步前确认音频长度与视频长度匹配** — 必要时裁剪或填充音频，使时长落在视频长度的 10% 以内
6. **面部 padding `[0, 10, 0, 0]` 适用于约 90% 的 talking-head 素材** — 仅在出现裁切瑕疵时再调整
7. **特写镜头务必使用 `wav2lip_gan`** — 在该景别下质量差异明显
