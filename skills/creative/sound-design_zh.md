# 视频制作中的声音设计

> 来源：W3C 无障碍标准、BBC 音频指南、YouTube/TikTok 平台规格、
> Sweetwater 母带指南、ElevenLabs 文档、Boris FX、HookSounds、Artlist

## 速查卡

```
DIALOGUE:       -12 dB peak  |  -16 to -14 LUFS integrated
MUSIC BED:      -30 to -20 dB (18-20 dB below dialogue)
SFX:            -18 to -12 dB (6 dB below dialogue minimum)
WHOOSH TIMING:  Start 10-20ms before visual, duration 400-500ms
MUSIC BPM:      Calm 60-80 | Standard 90-110 | Upbeat 120-140
TRUE PEAK:      Never exceed -1.5 dBTP
VOICE EQ:       HPF 80Hz, cut 500Hz, boost 2-5kHz, cut 6-8kHz
VOICE COMP:     3:1 ratio, 1-5ms attack, 10-20ms release
TARGET LUFS:    -14 LUFS (YouTube/TikTok/IG) | -16 LUFS (podcasts)
```

## 音频闪避（Ducking）电平

| 元素 | 峰值电平 | 说明 |
|---------|-----------|-------|
| 对白 / 旁白 | -6 dB 至 -12 dB | 主元素 |
| 背景音乐（有人声时） | -18 dB 至 -20 dB | 比对白低 18–20 dB |
| 音效 | -12 dB 至 -18 dB | 介于对白与音乐之间 |
| 最终混音 | -10 dB 至 -20 dB | 不得超过 0 dB |

**闪避规则：**
- W3C 无障碍：音乐须比前景语音**低 20 dB**
- BBC 指南：在你认为「刚好」的基础上，再将音乐**降低 4 dB**
- 旁白播放时，将音乐闪避 **6–12 dB**；复杂教育类内容可闪避至 **22 dB**
- EQ 技巧：在背景音乐上切 **2–4 kHz**，为语音清晰度留出空间
- 测试时以 -20 dB 为基准，以 **1 dB** 为步进向上微调

## 按内容类型选音乐

| 内容类型 | BPM 范围 | 情绪 |
|-------------|-----------|------|
| 平静讲解 / 教程 | 60-80 | 沉思、专注、建立信任 |
| 企业 / 客户证言 | 60-100 | 专业、沉稳、可信 |
| 标准讲解 / 教育 | 90-110 | 稳定、有吸引力、不抢戏 |
| 活泼讲解 / 推广 | 110-130 | 热情、亲和 |
| 高能量 / 产品演示 | 120-140 | 兴奋、紧迫、动感 |
| 动作 / 快节奏 | 140-200 | 肾上腺素、强度 |

**讲解类视频的流派建议：**
- Lo-fi（稳定、不分散注意力、现代感）
- Ambient（氛围感、退居背景）
- 轻型原声吉他纯音乐（温暖、亲和）
- 当代流行纯音乐（活泼、熟悉感）
- 励志配乐 / 轻 cinematic（营造情绪而不压过人声）

**关键规则：**
- 有旁白时务必使用**纯音乐**——歌词会与旁白争抢注意力
- 选择动态**平稳**的曲目——避免戏剧性渐强或 beat drop
- 能量匹配学习情境：「令人兴奋的新概念」用活泼曲风，严肃话题用柔和

## 音效（SFX）放置

### 讲解类视频常用 SFX 类别

| SFX 类型 | 使用场景 | 时长 | 电平 |
|----------|----------|----------|-------|
| Whoosh / Swish | 场景转场、换页 | 400-500ms | -18 至 -12 dB |
| Pop / Pluck | 文字出现、要点条目 | <200ms | -15 至 -12 dB |
| Click / Tap | UI 交互、按钮 | <100ms | -20 至 -15 dB |
| Riser / Swell | 引向揭示或重点 | 1-3s | -18 至 -12 dB |
| Impact / Hit | 关键揭示、重要数据 | <300ms | -12 至 -6 dB |
| 轻微 whoosh | 元素滑入/滑出 | 200-400ms | -20 至 -15 dB |

### 时间规则
- Whoosh 在画面转场**前 10–20ms** 开始（大脑处理音频更快）
- Whoosh 能量峰值应对齐**画面变化最大**的瞬间
- 以**逐帧**微调同步
- 叠加多个 whoosh 时，让它们分布在不同频段

## 平台响度目标（2025）

| 平台 | 综合 LUFS | True Peak | 说明 |
|----------|----------------|-----------|-------|
| YouTube | -14 LUFS | -1.5 dBTP | 向下归一化，不向上 |
| YouTube Shorts | -14 LUFS | -1.5 dBTP | 与长视频相同 |
| TikTok | -14 LUFS | -1 dBTP | 手机扬声器优先 2–4 kHz |
| Instagram Reels | -14 LUFS | -1 dBTP | 同样针对移动端优化 |
| Spotify | -14 LUFS | -2 dBTP | True peak 更严 |
| Apple Podcasts | -16 LUFS | -1 dBTP | 语音留更多余量 |

### 按内容类型的 LUFS

| 内容类型 | 综合 LUFS | 动态范围 |
|-------------|----------------|---------------|
| 对白为主 / 教育 | -16 至 -14 LUFS | 6-12 dB |
| 音乐视频 | -14 至 -12 LUFS | 6-10 dB |
| 游戏内容 | -14 至 -12 LUFS | 8-12 dB |

### 技术规格
- 采样率：优先 **48 kHz**
- 位深：优先 **24-bit**
- 码率：至少 **192 kbps**
- 本底噪声：低于 **-60 dB**
- 余量：最终混音至少 **-6 dB** headroom

## AI TTS（ElevenLabs）混音

### 处理链

1. **高通滤波：** 80–100 Hz（24 dB/oct 斜率）——去除 rumble 与 TTS 低频伪影
2. **EQ：**
   - 切约 500 Hz：减少浑浊/箱感
   - 提升 2–5 kHz（+2–3 dB）：增加 presence 与清晰度
   - 切 6–8 kHz（温和）：减轻 AI 人声常见齿音/刺耳感
   - 可选：对偏薄的 AI 人声提升 120–250 Hz
3. **压缩：**
   - 比率：**3:1**（范围 2:1 至 4:1）
   - Attack：**1–5 ms**
   - Release：**10–20 ms**（若有 pumping 可增至 30ms）
   - 阈值：**-26 dB**（目标 -4 至 -6 dB 增益衰减）
   - 输出增益：**+6 dB**
4. **De-esser：** 若仍有齿音，针对 **6–8 kHz**
5. **Limiter：** 上限 **-1.5 dBTP**

### AI 专用提示
- AI TTS 动态不一致——压缩比真人语音更重要
- ElevenLabs 可能在 4–6 kHz 有轻微伪影；若检测到可用窄 notch 切除
- 将背景音乐 sidechain 到旁白轨以实现自动闪避
- 在音乐 bed 上切 2–4 kHz，为语音「可懂度频段」让路
- 务必在手机扬声器上试听——若人声消失，更大力提升 2–4 kHz

## 在 OpenMontage 中的应用

在 compose 阶段使用 **audio_mixer** 工具时：

1. 旁白设为主轨，音乐为次轨
2. 应用闪避：有人声时音乐比对白低 -18 至 -20 dB
3. 根据 playbook 情绪从上表选择音乐 BPM
4. 在转场点放置 SFX，音频领先画面 10–20ms
5. YouTube 输出目标综合 **-14 LUFS**
6. True peak 保持在 **-1.5 dBTP** 以下
7. AI TTS 旁白在混音前先走上述处理链
8. 在手机扬声器上试听最终混音——多数观众在移动端观看
