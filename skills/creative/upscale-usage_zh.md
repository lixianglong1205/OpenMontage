# OpenMontage 中的放大（Upscaling）用法

> 来源：Real-ESRGAN 文档、GFPGAN 人脸增强文档、Real-ESRGAN 论文（Wang 等，2021）、实际放大基准测试

## 速查卡

```
DEFAULT MODEL:    RealESRGAN_x4plus — real-world photos and video frames
DEFAULT SCALE:    4x (480p→1080p, 720p→4K)
ANIME MODEL:     RealESRGAN_x4plus_anime_6B — flat color areas, illustrations
FACE ENHANCE:    Enable face_enhance for footage with people (uses GFPGAN)
DENOISE:         0.5 default, raise to 0.8 for very noisy inputs
```

## 何时进行放大

| 场景 | 是否放大？ | 说明 |
|-----------|----------|-------|
| 用户提供 480p 或 720p 素材，目标为 1080p/4K | 是 | 最常见用例 |
| 生成的图像需要更高分辨率以用作视频帧 | 是 | AI 图像输出常为 512–1024px |
| 缩略图或静帧需要清晰细节 | 是 | 单帧放大很快 |
| 老旧/档案素材修复 | 是 | 配合提高 denoise_strength |
| 源已是 1080p+ 且目标为 1080p | **否** | 浪费算力，可能引入伪影 |
| 源已是 4K | **否** | 过度锐化会损害画质 |

## 模型选择

| 模型 | 适用场景 | 说明 |
|-------|----------|-------|
| `RealESRGAN_x4plus` | 真实照片、视频帧 | 默认选择 |
| `RealESRGAN_x4plus_anime_6B` | 动漫、插画、动态图形 | 保留平坦色块 |
| `RealESRNet_x4plus` | 最快选项，画质略低 | 速度优先时 |

## 放大倍数指引

| 倍数 | 用例 | 示例 |
|-------|----------|---------|
| 4x | 低分辨率源的标准放大 | 480p→1080p，720p→4K |
| 2x | 4x 过重时的适度放大 | 720p→1080p |

- **4x** 是最常见选择。480p 源目标 1080p，或 720p 目标 4K 时使用。
- **2x** 适用于源已是 720p、目标 1080p 的情况——避免多余处理及潜在伪影。
- **切勿单次放大超过 4x。** 画质会急剧下降，臆造细节会变得明显。

## 人脸增强

- 视频含人脸时启用 `face_enhance`
- 内部使用 GFPGAN 增强人脸区域，其余由 Real-ESRGAN 处理
- 对网络摄像头素材和老视频尤其有价值
- 无人脸内容勿启用——只增加耗时、无收益

## 去噪强度

| 源画质 | denoise_strength | 理由 |
|---------------|-----------------|-----------|
| 干净数字源 | 0.5（默认） | 几乎无需去噪 |
| 轻微压缩伪影 | 0.6 | 轻度清理，不过度平滑 |
| 老旧/噪点素材 | 0.7–0.8 | 档案类内容需较强去噪 |
| 极噪/低照度素材 | 0.8 | 实际可用的最大去噪 |

勿超过 0.8——更高值会破坏真实细节。

## 视频放大说明

- 视频放大会逐帧提取、放大、再合成
- 过程**很慢**——GPU 上约为实时的 5–10 倍
- 长视频可考虑只放大关键场景/片段，而非整段
- 音频保留自原片
- 输出文件会明显变大（4x 放大约 **16 倍** 体积）

## 常见工作流

### 工作流 1 — 用户提供的低分辨率素材

```
1. Assess source resolution (e.g., 480p webcam recording)
2. Choose scale factor: 4x for 480p→1080p, 2x for 720p→1080p
3. Enable face_enhance if footage contains people
4. Set denoise_strength based on source quality
5. Upscale → inspect output → proceed to compose stage
```

### 工作流 2 — AI 生成图像帧

```
1. Generate images at native model resolution (512-1024px)
2. Upscale with RealESRGAN_x4plus to target video resolution
3. Keep denoise_strength at 0.5 — AI output is clean
4. Do NOT enable face_enhance unless faces are prominent
```

### 工作流 3 — Manim / 动态图形帧

```
1. Render Manim at default resolution
2. Upscale with RealESRGAN_x4plus_anime_6B (preserves flat colors)
3. Keep denoise_strength at 0.5
4. Verify text and line art remain sharp
```

### 工作流 4 — 档案素材修复

```
1. Assess noise level and resolution
2. Set denoise_strength to 0.7-0.8
3. Enable face_enhance for footage with people
4. Use RealESRGAN_x4plus at 4x
5. Carefully inspect output for hallucinated details
```

## 质量检查清单

- [ ] 放大输出清晰且无可见伪影
- [ ] 人脸自然（无过度平滑或变形）
- [ ] 录屏中的文字/UI 仍可读
- [ ] 平坦色块无臆造细节
- [ ] 文件体积合理（4x 放大约 16 倍体积）

## 在 OpenMontage 中的应用

在 asset 阶段使用 `upscale` 工具时：

1. **在 compose 阶段之前放大**——属于素材准备步骤，而非后期处理
2. **对任何 talking-head 素材使用 `face_enhance=true`**——GFPGAN 可显著改善人脸质量
3. **Manim 输出或平坦插画帧使用 `RealESRGAN_x4plus_anime_6B` 模型**——保留干净边缘与平坦色块
4. **预算有限的流水线**——只放大 hero 镜头和缩略图，而非每一帧
5. **老旧/噪点素材将 `denoise_strength` 设为 0.7–0.8**，干净数字源保持 0.5
6. **检查放大输出是否有伪影**——过度锐化、臆造纹理、人脸变形
7. **源已是 720p、目标 1080p 时优先 2x 而非 4x**——算力更少、伪影更少
