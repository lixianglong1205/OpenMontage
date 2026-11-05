# OpenMontage 人脸修复使用指南

> 来源：CodeFormer 论文（Zhou 等，2022）、GFPGAN 文档、Real-ESRGAN 放大文档，
> 现有 Layer 2 技能见 `skills/creative/enhancement-strategy.md`

## 速查卡

```
DEFAULT MODEL:    CodeFormer with fidelity 0.5
ALTERNATIVE:      GFPGAN (faster, less controllable)
FIDELITY RANGE:   0 = max quality enhancement, 1 = max faithfulness to input
BG UPSAMPLER:     Enable to also upscale the background (Real-ESRGAN)
PROCESSING ORDER: face_restore BEFORE face_enhance — restore first, polish second
```

## 关键区分 — face_restore 与 face_enhance

| 工具 | 作用 | 适用场景 |
|------|-------------|-------------|
| `face_enhance` | FFmpeg 滤镜链 — 磨皮、色彩平衡、锐化 | 画质尚可、仅需润色的素材 |
| `face_restore` | AI 模型重建 — 重建退化的人脸细节 | 模糊、压缩严重、低分辨率等人脸质量差的素材 |

**决策规则：** 若人脸可辨认且只需润色，使用 `face_enhance`。若人脸退化、模糊或压缩严重到难以辨认，使用 `face_restore`。

## 模型选择

| 模型 | 优势 | 保真度控制 | 速度 |
|-------|----------|------------------|-------|
| CodeFormer | 质量更好、身份保持、可调 | 是（0–1 滑块） | 较慢 |
| GFPGAN | 基线表现良好、更简单 | 否 | 较快 |

### 保真度调节（仅 CodeFormer）

| 保真度 | 效果 | 使用场景 |
|----------|--------|----------|
| 0.0 | 最大增强 — 视觉质量最佳但可能改变身份 | 无法辨认的人脸、艺术用途 |
| 0.3 | 强修复 — 适合严重退化的人脸 | 老素材、重度压缩伪影 |
| 0.5 | 平衡（默认）— 修复与身份保持兼顾 | 通用修复 |
| 0.7 | 保守 — 轻度清理、强身份保持 | 网络摄像头素材、轻度退化 |
| 1.0 | 几乎不变 — 基本透传 | 测试、对比基线 |

## 常见工作流

### 1. 老素材修复

```
face_restore (fidelity 0.3) → color_grade → compose
```

针对档案/复古素材中人脸明显退化的重度修复。

### 2. 网络摄像头清理

```
face_restore (fidelity 0.7) → face_enhance (talking_head_standard) → compose
```

轻度修复后再润色 — 适合较新但画质一般的网络摄像头素材。

### 3. 低分辨率人脸 + 背景放大

```
face_restore (bg_upsampler=true) → compose
```

当人脸与背景都需改善时的单步修复。

### 4. 档案照片用于说话头

```
face_restore → talking_head tool (SadTalker)
```

在送入说话头动画流水线之前，先修复源人脸图像。

## 质量检查清单

接受 `face_restore` 输出前，请确认：

- [ ] 修复后的人脸比输入更清晰、更干净
- [ ] 身份得以保持 — 人物仍可辨认
- [ ] 无幻觉特征（多余眼睛、错误肤质、牙齿伪影等）
- [ ] 肤质自然，非塑料感/过度磨皮
- [ ] 跨帧一致（视频）— 修复/未修复质量之间无闪烁

## 在 OpenMontage 中的应用

使用 `face_restore` 工具时：

1. **在 processing 链中先 `face_restore` 后 `face_enhance`** — 先修复，后润色
2. **从 fidelity 0.5 起步**，根据目视检查再调整
3. **说话头流水线且源素材较差时**，在 assets 阶段应用 `face_restore`
4. **仅当人脸与背景都需改善时** 才启用 `bg_upsampler`
5. **切勿对已经良好的素材使用 `face_restore`** — 可能引入细微伪影
6. **并排对比输入与输出** — 人脸应仍是同一人
7. **对视频先抽关键帧测试 `face_restore` 参数**，再处理整段视频
