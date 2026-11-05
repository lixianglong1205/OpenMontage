---
name: ltx2
description: 使用 LTX-2.3 22B 进行 AI 视频生成 — 文生视频、图生视频片段，用于视频制作。适用于生成视频片段、图像动画化、创建 B-roll、动画背景或动态内容。触发词包括 video generation、animate image、b-roll、motion、video clip、text-to-video、image-to-video。
---

# LTX-2.3 视频生成

使用 LTX-2.3 22B DiT 模型，根据文本提示或图像生成约 5 秒的视频片段。
在 Modal（A100-80GB）上运行。需在 `.env` 中配置 `MODAL_LTX2_ENDPOINT_URL`。

## 快速参考

```bash
# Text-to-video
python3 tools/ltx2.py --prompt "A sunset over the ocean, golden light on waves, cinematic" --output sunset.mp4

# Image-to-video (animate a still image)
python3 tools/ltx2.py --prompt "Gentle camera drift, soft ambient motion" --input photo.jpg --output animated.mp4

# Custom resolution and duration
python3 tools/ltx2.py --prompt "..." --width 1024 --height 576 --num-frames 161 --output wide.mp4

# Fast mode (fewer steps, quicker)
python3 tools/ltx2.py --prompt "..." --quality fast --output quick.mp4

# Reproducible output
python3 tools/ltx2.py --prompt "..." --seed 42 --output reproducible.mp4
```

## 参数

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| `--prompt` | （必填） | 视频的文字描述 |
| `--input` | - | 图生视频的输入图像 |
| `--width` | 768 | 视频宽度（须能被 64 整除） |
| `--height` | 512 | 视频高度（须能被 64 整除） |
| `--num-frames` | 121 | 帧数，须满足 `(n-1) % 8 == 0` |
| `--fps` | 24 | 每秒帧数 |
| `--quality` | standard | `standard`（30 步）或 `fast`（15 步） |
| `--steps` | 30 | 直接覆盖推理步数 |
| `--seed` | random | 可复现输出的随机种子 |
| `--output` | auto | 输出文件路径 |
| `--negative-prompt` | sensible default | 需要避免的内容 |

## 有效帧数

`(n - 1) % 8 == 0`：25（约 1 秒）、49（约 2 秒）、73（约 3 秒）、97（约 4 秒）、**121（约 5 秒，默认）**、161（约 6.7 秒）、193（约 8 秒，实际可用上限）。

## 常用分辨率

| 分辨率 | 比例 | 说明 |
|------------|-------|-------|
| 768x512 | 3:2 | 默认，平衡较好 |
| 512x512 | 1:1 | 方形，最快 |
| 1024x576 | 16:9 | 宽屏 |
| 576x1024 | 9:16 | 竖屏 |

## 提示词指南

LTX-2 对电影化描述响应良好。可叠加以下维度：

- **镜头：** "Slow dolly forward"、"Aerial drone shot"、"Tracking shot"、"Static wide angle"
- **光照：** "Golden hour"、"Cinematic lighting"、"Neon-lit"、"Soft diffused light"
- **运动：** "Timelapse of..."、"Slow motion"、"Gentle camera drift"、"Gradually transitions"
- **风格：** "Shot on 35mm film"、"Documentary style"、"Clean minimal aesthetic"
- **负向：** 默认隐含避免 "worst quality, blurry, jittery, watermark, text, logo"

提示词建议控制在 200 词以内，对场景描述要具体。

### 好的提示词

```
# Atmospheric b-roll
"Aerial drone shot slowly flying over turquoise ocean waves breaking on white sand, golden hour sunlight, cinematic"

# Product/tech scene
"Close-up of hands typing on a mechanical keyboard, shallow depth of field, soft desk lamp lighting, cozy atmosphere"

# Abstract background
"Dark moody abstract background with flowing blue light streaks, subtle geometric grid, bokeh particles floating, cinematic tech atmosphere"

# Animate a portrait
"Professional headshot, subtle natural head movement, confident warm expression, studio lighting, shallow depth of field"

# Animate a slide/screenshot
"Gentle subtle particle effects floating across a presentation slide, soft ambient light shifts, very slight camera drift"
```

### 差的提示词

```
# Too vague
"A cool video"

# Too many competing ideas
"A cat riding a skateboard while juggling fire on the moon during a thunderstorm"

# Describing text/UI (model can't render text reliably)
"A website showing the text 'Welcome to our platform'"
```

## 视频制作使用场景

### B-Roll 片段
在旁白场景之间生成约 5 秒的氛围镜头作为切镜：
```bash
python3 tools/ltx2.py --prompt "Futuristic holographic interface, glowing data visualizations, clean workspace, cinematic" --output broll_tech.mp4
python3 tools/ltx2.py --prompt "Aerial view of European city at golden hour, modern architecture" --output broll_europe.mp4
```

### 幻灯片动画背景
传入幻灯片截图并添加轻微动态：
```bash
python3 tools/ltx2.py --prompt "Gentle particle effects, soft ambient light shifts, very slight camera drift" --input slide.png --output animated_slide.mp4
```

### 人像动画
让静态头像产生自然微动：
```bash
python3 tools/ltx2.py --prompt "Subtle natural head movement, warm expression, professional lighting" --input headshot.png --output animated_portrait.mp4
```

### 品牌片头/片尾
为标题卡生成抽象动态背景：
```bash
python3 tools/ltx2.py --prompt "Dark moody background with flowing blue and coral light streaks, bokeh particles, cinematic tech atmosphere, no text" --output intro_bg.mp4
```

### 与其他工具组合

LTX-2 生成原始片段。可与工具链其余部分配合：

| 工作流 | 工具 |
|----------|-------|
| 生成片段 → 超分 | `ltx2.py` → `upscale.py` |
| 生成片段 → 加入 Remotion | `ltx2.py` → 在合成中使用 `<OffthreadVideo>` |
| 生成图像 → 动画化 | `flux2.py` → `ltx2.py --input` |
| 生成片段 → 提取音频 | `ltx2.py` → `ffmpeg -i clip.mp4 -vn audio.wav` |
| 生成片段 → 添加旁白 | `ltx2.py` → 与 `qwen3_tts.py` 输出混音 |

## 技术细节

- **模型：** LTX-2.3 22B DiT（Lightricks），bf16
- **GPU：** Modal 上的 A100-80GB（约 $4.68/小时）
- **推理：** 每片段约 2.5 分钟（768x512，121 帧，30 步）
- **成本：** 每 5 秒片段约 $0.20–0.25
- **冷启动：** 约 60–90 秒（加载约 55GB 权重）
- **输出：** H.264 MP4，带同步环境音（24fps）
- **最长时长：** 每片段约 8 秒（193 帧）

### 已知限制

- **训练数据伪影：** 约 30% 的生成结果可能带有训练数据中的多余 logo/文字。可换 `--seed` 重试。
- **文字渲染：** 无法在视频中可靠生成可读文字。请改用 Remotion 叠加层。
- **最长时长：** 每片段约 8 秒。更长内容需拼接。
- **音频：** 生成音频仅为环境/氛围音。语音与音乐请使用旁白/音乐工具。
- **许可：** Community License — 年收入低于 $1000 万可免费使用，超过需商业许可。

## 设置

```bash
# 1. Create Modal secret for HuggingFace (one-time)
modal secret create huggingface-token HF_TOKEN=hf_your_token

# 2. Deploy (downloads ~55GB of weights, takes ~10 min)
modal deploy docker/modal-ltx2/app.py

# 3. Save endpoint URL to .env
echo "MODAL_LTX2_ENDPOINT_URL=https://yourname--video-toolkit-ltx2-ltx2-generate.modal.run" >> .env

# 4. Test
python3 tools/ltx2.py --prompt "A candle flickering on a dark table, cinematic" --output test.mp4
```

**重要：** HuggingFace token 需具备 read-access 权限。部署前请接受 [Gemma 3 license](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized)。未认证下载会严重限流。
