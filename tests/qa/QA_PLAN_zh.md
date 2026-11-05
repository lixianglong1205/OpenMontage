# 质量验证计划 — Phase 3.5 + G3.11

## 目的

使用真实 API 密钥运行每个工具，检查输出（查看图像、收听音频、观看视频），发现缺口并修复。这是将 Phase 3.5 标记为「已验证」之前的门禁。

## 测试脚本（均可直接运行）

| 脚本 | 测试的工具 | 使用的 API 密钥 | 预估成本 |
|--------|-------------|---------------|-----------|
| `test_01_tts.py` | `elevenlabs_tts` (ElevenLabs) | ELEVENLABS_API_KEY | ~$0.02 |
| `test_02_image_gen.py` | `image_gen` (GPT Image 2 + FLUX) | OPENAI_API_KEY, FAL_AI_API_KEY | ~$0.15 |
| `test_03_music.py` | `music_gen` (ElevenLabs) | ELEVENLABS_API_KEY | ~$0.10 |
| `test_04_audio_mix.py` | `audio_mixer` | None (仅 ffmpeg) | $0 |
| `test_05_video_compose.py` | `video_compose` | None (仅 ffmpeg) | $0 |
| `test_06_video_stitch.py` | `video_stitch` | None (仅 ffmpeg) | $0 |
| `test_07_playbook_intelligence.py` | `playbook_loader.py` 中的函数 | None (纯 Python) | $0 |
| `test_08_end_to_end.py` | 完整 animated-explainer 流水线 | None (ffmpeg fixtures) | $0 |

## 检查协议

对每项输出：
1. **音频文件**：使用 `ffprobe` 检查格式/时长/声道，然后**收听**（在媒体播放器中播放，或使用 Whisper 验证内容与提示词一致）
2. **图像文件**：使用 `ffprobe` 检查尺寸，然后**查看**（打开图像，检查构图、文字可读性、风格是否匹配）
3. **视频文件**：使用 `ffprobe` 检查分辨率/fps/时长/编解码器，然后**观看**（检查音画同步、转场、字幕时间轴）
4. **设计智能**：针对全部 3 个 playbook 运行，验证对比度与手动计算一致，检查 CVD 警告是否准确

## 已知风险区域

| 区域 | 风险 | 如何验证 |
|------|------|-----------------|
| TTS 音色选择 | 默认音色可能与 playbook 情绪不符 | 使用多个 voice ID 测试，与 playbook 的 `voice_style` 对比 |
| 图像生成一致性 | GPT Image/FLUX 输出随提示词波动很大 | 测试时在提示词前加上 playbook 的 `image_prompt_prefix` |
| 音乐时长对齐 | 音乐时长可能与旁白不一致 | 比较 `music.duration` 与 `tts.duration`，检查填充/循环 |
| 音频闪避时机 | 闪避可能对音乐切得过狠 | 检查波形：语音下音乐应约 duck 6dB，恢复应平滑 |
| 视频拼接转场 | 编解码器不匹配时交叉淡化可能闪烁 | 用匹配与不匹配的片段测试，检查 `auto_normalize` |
| 字幕烧录 | 移动端画幅下字号/位置可能被裁切 | 用 9:16 (TikTok) 与 16:9 (YouTube) 配置测试 |
| Remotion 渲染 | 组件可能在真实数据下失败 | 用全部 8 个组件构建测试合成，以 1080p 渲染 |
| Playbook 对比度 | 深底深字或浅底浅字主题的边界情况 | 测试全部 3 个 playbook + 一个故意低对比度的自定义主题 |

## 运行顺序

```bash
cd C:/Users/ishan/Documents/OpenMontage

# Phase 1: Individual tools (can run in parallel)
python tests/qa/test_01_tts.py
python tests/qa/test_02_image_gen.py
python tests/qa/test_03_music.py

# Phase 2: Composition (depends on Phase 1 outputs)
python tests/qa/test_04_audio_mix.py
python tests/qa/test_05_video_compose.py
python tests/qa/test_06_video_stitch.py

# Phase 3: Intelligence validation (no API calls)
python tests/qa/test_07_playbook_intelligence.py

# Phase 4: Full pipeline
python tests/qa/test_08_end_to_end.py
```


## 成功标准

- [ ] 全部 3 个 TTS 样本：语音清晰、内容正确、无伪影、≥44.1kHz
- [ ] 全部 4 张图像：符合提示意图、尺寸正确、无水印、构图良好
- [ ] 两条音乐轨：符合情绪提示、时长正确（±2s）、无突兀截断
- [ ] 音频混音：语音明显高于音乐、闪避平滑、无削波
- [ ] 视频合成：音画同步在 50ms 内、分辨率正确、可在 VLC 播放
- [ ] 视频拼接：转场平滑、无丢帧、画中画位置正确
- [ ] Playbook 智能：全部 3 个 playbook 通过 a11y，对比度与手动计算误差在 0.1 以内
- [ ] 端到端：60 秒讲解片无错误渲染，各阶段 checkpoint 正确
