---
name: video-toolkit
description: 使用 claude-code-video-toolkit 自主创建专业视频 — AI 旁白、图像生成、音乐、数字人说话与 Remotion 渲染。
metadata:
  openclaw:
    emoji: "🎬"
    skillKey: "video-toolkit"
    os: ["darwin", "linux"]
    requires:
      bins: ["node", "python3", "ffmpeg", "npm"]
---

# Video Toolkit

根据文字简报创建专业讲解类视频。工具包在云端 GPU（Modal 或 RunPod）上使用开源 AI 模型完成旁白、图像生成、音乐与数字人动画；Remotion（React）负责合成与渲染。

## 关键：工具包路径

工具包位于固定路径。**运行任何工具命令前必须先 `cd` 到该目录。**

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
```

**切勿在项目目录内运行工具命令。** 工具路径均相对于工具包根目录解析。

## 设置

### 步骤 1：检查当前状态

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/verify_setup.py
```

若全部显示 `[x]`，可跳至下文「快速测试」。否则继续完成设置。

### 步骤 2：安装 Python 依赖

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
pip3 install --break-system-packages -r tools/requirements.txt
```

说明：在 Debian/Ubuntu 等受管 Python（PEP 668）环境下需要 `--break-system-packages`。在容器内使用是安全的。

### 步骤 3：配置云端 GPU 端点

工具包需在 `.env` 中配置云端 GPU 端点 URL。检查 `.env` 是否存在且包含 Modal 端点：

```bash
cat ~/.openclaw/workspace/claude-code-video-toolkit/.env | grep MODAL
```

若已配置 Modal 端点，即可继续。若未配置，**请用户提供 Modal 端点 URL**，或自行搭建 Modal：

```bash
pip3 install --break-system-packages modal
python3 -m modal setup   # Opens browser for authentication

# Deploy each tool — capture the endpoint URL from output
cd ~/.openclaw/workspace/claude-code-video-toolkit
modal deploy docker/modal-qwen3-tts/app.py
modal deploy docker/modal-flux2/app.py
modal deploy docker/modal-music-gen/app.py
modal deploy docker/modal-sadtalker/app.py
modal deploy docker/modal-image-edit/app.py
modal deploy docker/modal-upscale/app.py
modal deploy docker/modal-propainter/app.py
modal deploy docker/modal-ltx2/app.py      # Requires: modal secret create huggingface-token HF_TOKEN=hf_...
```

**LTX-2 前提条件：** 部署 LTX-2 前，创建 HuggingFace secret 并接受 [Gemma 3 许可](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized)：
```bash
modal secret create huggingface-token HF_TOKEN=hf_your_read_access_token
```

将各 URL 写入 `.env`：
```
MODAL_QWEN3_TTS_ENDPOINT_URL=https://...modal.run
MODAL_FLUX2_ENDPOINT_URL=https://...modal.run
MODAL_MUSIC_GEN_ENDPOINT_URL=https://...modal.run
MODAL_SADTALKER_ENDPOINT_URL=https://...modal.run
MODAL_IMAGE_EDIT_ENDPOINT_URL=https://...modal.run
MODAL_UPSCALE_ENDPOINT_URL=https://...modal.run
MODAL_DEWATERMARK_ENDPOINT_URL=https://...modal.run
MODAL_LTX2_ENDPOINT_URL=https://...modal.run
```

可选但推荐 — 使用 Cloudflare R2 实现可靠文件传输：
```
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=video-toolkit
```

### 步骤 4：验证与快速测试

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/verify_setup.py
```

所有工具应显示 `[x]`。随后运行快速测试确认 GPU 流水线可用：

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/qwen3_tts.py --text "Hello, this is a test." --speaker Ryan --tone warm --output /tmp/video-toolkit-test.mp3 --cloud modal
```

若得到有效 `.mp3` 文件，则设置完成。若失败，请检查：
- `.env` 中 `MODAL_QWEN3_TTS_ENDPOINT_URL` 是否正确
- 运行 `python3 tools/verify_setup.py --json`，查看 `modal_tools` 中缺少哪些端点

**费用：** Modal 含每月 $30 免费算力。典型 60 秒视频约 $1–3。

---

## 创建视频

### 步骤 1：创建项目

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
cp -r templates/product-demo projects/PROJECT_NAME
cd projects/PROJECT_NAME
npm install
```

模板：`product-demo`（营销/讲解）、`sprint-review`、`sprint-review-v2`（可组合场景）。

### 步骤 2：编写配置

编辑 `projects/PROJECT_NAME/src/config/demo-config.ts`：

```typescript
export const demoConfig: ProductDemoConfig = {
  product: {
    name: 'My Product',
    tagline: 'What it does in one line',
    website: 'example.com',
  },
  scenes: [
    { type: 'title', durationSeconds: 9, content: { headline: '...', subheadline: '...' } },
    { type: 'problem', durationSeconds: 14, content: { headline: '...', problems: ['...', '...'] } },
    { type: 'solution', durationSeconds: 13, content: { headline: '...', highlights: ['...', '...'] } },
    { type: 'stats', durationSeconds: 12, content: { stats: [{value: '99%', label: '...'}, ...] } },
    { type: 'cta', durationSeconds: 10, content: { headline: '...', links: ['...'] } },
  ],
  audio: {
    backgroundMusicFile: 'audio/bg-music.mp3',
    backgroundMusicVolume: 0.12,
  },
};
```

场景类型：`title`、`problem`、`solution`、`demo`、`feature`、`stats`、`cta`。

**时长规则：** 估算 `durationSeconds` 为 `ceil(word_count / 2.5) + 2`。在步骤 4 生成音频后需再调整。

### 步骤 3：撰写旁白脚本

创建 `projects/PROJECT_NAME/VOICEOVER-SCRIPT.md`：

```markdown
## Scene 1: Title (9s, ~17 words)
Build videos with AI. The product name toolkit makes it easy.

## Scene 2: Problem (14s, ~30 words)
The problem statement goes here. Keep it punchy and relatable.
```

**每场景字数预算：** `(durationSeconds - 2) * 2.5` 词。减 2 秒用于 1 秒音频延迟 + 1 秒留白。

### 步骤 4：生成素材

**关键：以下所有命令必须在工具包根目录运行，而非项目目录。**

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
```

#### 4a. 背景音乐

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/music_gen.py \
  --preset corporate-bg \
  --duration 90 \
  --output projects/PROJECT_NAME/public/audio/bg-music.mp3 \
  --cloud modal
```

预设：`corporate-bg`、`upbeat-tech`、`ambient`、`dramatic`、`tension`、`hopeful`、`cta`、`lofi`。

#### 4b. 旁白（按场景）

**每个场景生成一个 `.mp3` 文件。** 不要生成单一整段旁白文件。

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit

# Scene 01
python3 tools/qwen3_tts.py \
  --text "The voiceover text for scene one." \
  --speaker Ryan --tone warm \
  --output projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --cloud modal

# Scene 02
python3 tools/qwen3_tts.py \
  --text "The voiceover text for scene two." \
  --speaker Ryan --tone warm \
  --output projects/PROJECT_NAME/public/audio/scenes/02.mp3 \
  --cloud modal

# ... repeat for each scene
```

**说话人：** `Ryan`、`Aiden`、`Vivian`、`Serena`、`Uncle_Fu`、`Dylan`、`Eric`、`Ono_Anna`、`Sohee`  
**语气：** `neutral`、`warm`、`professional`、`excited`、`calm`、`serious`、`storyteller`、`tutorial`

语音克隆（需参考录音）：
```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/qwen3_tts.py \
  --text "Text to speak" \
  --ref-audio assets/voices/reference.m4a \
  --ref-text "Exact transcript of the reference audio" \
  --output projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --cloud modal
```

#### 4c. 场景图像

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/flux2.py \
  --prompt "Dark tech background with blue geometric grid, cinematic lighting" \
  --width 1920 --height 1080 \
  --output projects/PROJECT_NAME/public/images/title-bg.png \
  --cloud modal
```

图像预设（用 `--preset` 代替 `--prompt --width --height`）：  
`title-bg`、`problem`、`solution`、`demo-bg`、`stats-bg`、`cta`、`thumbnail`、`portrait-bg`

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/flux2.py \
  --preset title-bg \
  --output projects/PROJECT_NAME/public/images/title-bg.png \
  --cloud modal
```

#### 4d. 视频片段 — B-Roll 与动态背景（可选）

生成 AI 视频片段，用于 B-roll 插入、幻灯片动态背景或片头片尾：

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit

# B-roll clip from text
python3 tools/ltx2.py \
  --prompt "Aerial drone shot over a European city at golden hour, cinematic wide angle" \
  --output projects/PROJECT_NAME/public/videos/broll-europe.mp4 \
  --cloud modal

# Animate a slide/screenshot (image-to-video)
python3 tools/ltx2.py \
  --prompt "Gentle particle effects, soft ambient light shifts, very slight camera drift" \
  --input projects/PROJECT_NAME/public/images/title-bg.png \
  --output projects/PROJECT_NAME/public/videos/animated-title.mp4 \
  --cloud modal

# Abstract intro/outro background
python3 tools/ltx2.py \
  --prompt "Dark moody abstract background with flowing blue light streaks, bokeh particles, cinematic" \
  --output projects/PROJECT_NAME/public/videos/intro-bg.mp4 \
  --cloud modal
```

在 Remotion 合成中使用 `<OffthreadVideo>`：
```tsx
<OffthreadVideo src={staticFile('videos/broll-europe.mp4')} />
```

**LTX-2 规则：**
- 每段最长约 8 秒（24fps 下 193 帧）。默认约 5 秒（121 帧）。
- 宽/高须能被 64 整除。默认：768x512。
- 每段约 $0.20–0.25，生成约 2.5 分钟。
- 冷启动约 60–90 秒。GPU 预热后续片段更快。
- 生成音频仅为环境声 — 语音与音乐请用旁白/音乐工具。
- 约 30% 生成结果可能含训练数据伪影（logo/文字）。可用 `--seed` 重跑以变化结果。

#### 4e. 数字人讲解（可选）

生成主持人肖像，再按场景生成动画片段：

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit

# 1. Generate portrait
python3 tools/flux2.py \
  --prompt "Professional presenter portrait, clean style, dark background, facing camera, upper body" \
  --width 1024 --height 576 \
  --output projects/PROJECT_NAME/public/images/presenter.png \
  --cloud modal

# 2. Generate per-scene narrator clips (one per scene, NOT one long video)
python3 tools/sadtalker.py \
  --image projects/PROJECT_NAME/public/images/presenter.png \
  --audio projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --preprocess full --still --expression-scale 0.8 \
  --output projects/PROJECT_NAME/public/narrator-01.mp4 \
  --cloud modal

# Repeat for each scene that needs a narrator
```

**SadTalker 规则 — 请严格遵循：**
- **始终** 使用 `--preprocess full`（默认 `crop` 输出为正方形，宽高比错误）
- **始终** 使用 `--still`（减少头部晃动，更专业）
- **始终** 按场景生成片段（每段 6–15 秒），**不要** 生成一条长视频
- 处理速度：Modal A10G 上约每 10 秒音频 3–4 分钟
- `--expression-scale 0.8` 使表情更 subtle（范围 0.0–1.5）

#### 4e. 图像编辑（可选）

基于现有图像创建场景变体：

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/image_edit.py \
  --input projects/PROJECT_NAME/public/images/title-bg.png \
  --prompt "Make it darker with red tones, more ominous" \
  --output projects/PROJECT_NAME/public/images/problem-bg.png \
  --cloud modal
```

#### 4f. 超分辨率（可选）

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/upscale.py \
  --input projects/PROJECT_NAME/public/images/some-image.png \
  --output projects/PROJECT_NAME/public/images/some-image-4x.png \
  --scale 4 --cloud modal
```

### 步骤 5：同步时长

**生成旁白后必须执行。** 实际音频时长与估算会有差异。

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
for f in projects/PROJECT_NAME/public/audio/scenes/*.mp3; do
  echo "$(basename $f): $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")s"
done
```

在 `demo-config.ts` 中将各场景 `durationSeconds` 更新为：`ceil(actual_audio_duration + 2)`。

示例：若 `01.mp3` 为 6.8s，则场景 1 的 `durationSeconds` 设为 `9`（ceil(6.8 + 2) = 9）。

### 步骤 6：预览静帧

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit/projects/PROJECT_NAME
npx remotion still src/index.ts ProductDemo --frame=100 --output=/tmp/review-scene1.png
npx remotion still src/index.ts ProductDemo --frame=400 --output=/tmp/review-scene2.png
```

检查：文字截断、动画时序、数字人画中画位置、背景对比度。

### 步骤 7：渲染

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit/projects/PROJECT_NAME
npm run render
```

**输出：** `out/ProductDemo.mp4`

---

## 合成模式

### 按场景音频

按场景音频，延迟 1 秒（`from={30}` = 30 帧 = 30fps 下 1 秒）：

```tsx
<Sequence from={30}>
  <Audio src={staticFile('audio/scenes/01.mp3')} volume={1} />
</Sequence>
```

### 按场景数字人画中画

```tsx
<Sequence from={30}>
  <OffthreadVideo
    src={staticFile('narrator-01.mp4')}
    style={{ width: 320, height: 180, objectFit: 'cover' }}
    muted
  />
</Sequence>
```

**始终使用 `<OffthreadVideo>`，不要用 `<video>`。** Remotion 需要该组件以实现逐帧精确渲染。

### 转场

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { glitch } from '../../../lib/transitions/presentations/glitch';
import { lightLeak } from '../../../lib/transitions/presentations/light-leak';
```

**切勿从 `lib/transitions` barrel 导入** — 自定义转场请直接从 `lib/transitions/presentations/` 导入。

---

## 错误恢复

| 问题 | 解决方案 |
|---------|----------|
| 工具命令失败并提示 "No module named..." | 在工具包根目录运行 `pip3 install --break-system-packages -r tools/requirements.txt` |
| "MODAL_*_ENDPOINT_URL not configured" | 检查 `.env` 是否含端点 URL。运行 `python3 tools/verify_setup.py` |
| SadTalker 输出为正方形/被裁剪 | 忘记加 `--preprocess full`。用该参数重新运行 |
| 音频相对场景过短/过长 | 重新执行步骤 5（同步时长）并更新配置 |
| `npm run render` 失败 | 确保在项目目录而非工具包根目录。先运行 `npm install` |
| Remotion 中 "Cannot find module" | 检查 import 路径。自定义组件使用 `../../../lib/` 相对路径 |
| Modal 冷启动超时 | 空闲后首次调用需 30–120 秒。重试一次 — 第二次会使用预热 GPU |

---

## 费用估算（Modal）

| 工具 | 典型费用 | 说明 |
|------|-------------|-------|
| Qwen3-TTS | ~$0.01/场景 | 预热 GPU 上约 20 秒/场景 |
| FLUX.2 | ~$0.01/张 | 预热约 3 秒，冷启动约 30 秒 |
| ACE-Step | ~$0.02-0.05 | 取决于时长 |
| SadTalker | ~$0.05-0.20/场景 | 约每 10 秒音频 3–4 分钟 |
| Qwen-Edit | ~$0.03-0.15 | 冷启动约 8 分钟（25GB 模型） |
| RealESRGAN | ~$0.005/张 | 非常快 |
| LTX-2.3 | ~$0.20-0.25/片段 | 约 5 秒片段 2.5 分钟，A100-80GB |

**60 秒视频合计：** 约 $1–3，取决于场景数与数字人片段。

Modal Starter 计划：每月 $30 免费算力。空闲时应用缩容至零。
