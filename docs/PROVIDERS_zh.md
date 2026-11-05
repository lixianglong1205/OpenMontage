# OpenMontage 提供商指南
## 2026年10月的提供商更新

请参阅 [实施状态和验证模型地图](provider-update-plan-2026-10-03.md) 和 [适配器使用](../.agents/skills/provider-model-refresh/SKILL.md)。

新路线覆盖HeyGen Avatar V、Eleven v4/Turbo、Wan 3.0 on fal/Atlas/Replicate、GPT Image 2.5 Flare/Sunburst、Gemini 3 Pro Image (Nano Banana Pro)、Ideogram 4.5 和 Precise Edit、H3 Max、Gemini 3.8 TTS、Lyria 3.5、LTX-2.5、Sonic 3.6、Inworld TTS-2/Flash 和本地 Qwen Image 2.1。每个模型都使用相同的 API 主机合同；API 密钥不建立账户权利。

对于图像/视频选择器使用 `model`、`hosting_provider` 和可选的 `preferred_tool`。语音使用 `model_id`。明确的工具、主机和模型约束从未默默地退回。遗留的 `preferred_provider`仍然是排名偏好。多个工具可能共享一个主机；排名选择实际工具名称。

新异步图像/视频工具返回 `resume_job` 并可选地保存 `job_path`。在等待超时后重启同一任务，而不是提交另一个付费请求。未计价的调用返回 `cost_usd: null` 并可选地返回 `cost_status`，不是零。Ideogram 直接支持一个未计价的 `dry_run`价格报价。

Kling 4/Flash 仍然封装，直到验证公开的结构和账户访问。LTX-2.5 本地执行需要提供的 ComfyUI API 工作流和安装的权重；LTX 的直接 API 已独立实现。GPU 和付费 API 输出质量需要在预期环境中进行现场验证。

---

## 快速开始：我应该设置什么？

**开始免费，按需添加付费提供商。** 这是推荐的顺序：

| 步骤 | 成本 | 设置 |解锁能力|
|------|------|----------------|-----------------|
| 1 | **$0** | Pexels + Pixabay | 版权照片和视频 — 生产基本视频的足够数量 |
| 2 | **$0** | Google API 密钥 | 700多种 TTS 声音（每月免费1M字符）+ $300新账户信用 |
| 3 | **$0** | ElevenLabs | 优质 TTS + 音乐 + SFX（每月免费10K字符） |
| 4 | **$0** | Piper (本地安装) | 完全无网络的 TTS — 无 API 密钥、无成本、无网络 |
| 5 | **~$0.03/图像** | fal.ai | FLUX 图像 + Kling/Veo/MiniMax 视频 + Recraft — 广泛单键图像+视频覆盖 |
| 6 | **~$0.05/图像** | OpenAI | GPT Image 2 图像 + OpenAI TTS |
| 7 | **~$0.04/图像** | Google Imagen | Imagen 4 图像（共享 Google API 密钥） |
| 8 | **付费** | Kling 官方 | 官方直接 Kling 视频、图像、TTS、头像和 Lip-sync API，独立于 fal.ai Kling |
| 9 | **付费** | Volcengine Ark | 官方直接 Seedance 2.0 标准/快速/小 API |
| 10 | **$12/月** | Runway | Gen-4 视频 — 最佳的 AI 视频 |
| 11 | **付费** | Hunyuan 云视频 | 中文友好的 T2V + I2V |
| 12 | **pay-as-you-go** | HeyGen | Avatar videos, multi-model video gateway |
| 13 | **pay-as-you-go** | Suno | Full song generation with vocals and lyrics |
| 14 | **$0 + GPU** | Local video gen | WAN 2.1, Hunyuan, CogVideo, LTX — free, offline |
| 15 | **$0 + GPU** | Local Diffusion | Stable Diffusion images — free, offline |

### 环境变量概述

```bash
# .env — add your keys here

# FREE (no cost, ever)
PEXELS_API_KEY=              # Stock photos + videos
PIXABAY_API_KEY=             # Stock photos + videos

# GOOGLE (one key, multiple tools, generous TTS free tier)
GOOGLE_API_KEY=              # Google TTS + Imagen + Lyria music + Gemini Omni/Veo video

# VOICE + MUSIC
ELEVENLABS_API_KEY=          # TTS, music, sound effects (10K chars/month free)
FISH_AUDIO_API_KEY=          # fish.audio TTS (voice cloning via reference_id, inline emotion tags)
OPENAI_API_KEY=              # OpenAI TTS + GPT Image 2 images
XAI_API_KEY=                 # xAI Grok image generation/editing + Grok video generation
DOUBAO_SPEECH_API_KEY=       # Volcengine Doubao Speech TTS (strong Mandarin narration)
DOUBAO_SPEECH_VOICE_TYPE=    # Default Doubao speaker/voice type
DASHSCOPE_API_KEY=           # Alibaba DashScope (Qwen image gen, TTS, ASR with word timestamps)

# AZURE AI SPEECH (optional cloud STT + TTS; one key unlocks both directions)
AZURE_SPEECH_KEY=            # Azure AI Speech — azure_stt (Fast Transcription) + azure_tts (neural narration)
AZURE_SPEECH_REGION=         # Speech resource region, e.g. eastus

# MULTI-MODEL GATEWAY (one key, 6+ tools)
FAL_KEY=                     # FLUX, Recraft, Kling, Veo, MiniMax video
MINIMAX_API_KEY=             # MiniMax first-party image + MiniMax H3 video generation
ATLASCLOUD_API_KEY=          # Atlas Cloud image/video gateway

# KLING OFFICIAL DIRECT API
KLING_API_KEY=               # Official Kling video, image, TTS, avatar, lip sync
KLING_API_BASE_URL=          # Optional; default https://api-singapore.klingai.com

# VOLCENGINE ARK DIRECT SEEDANCE 2.0 / 2.5 API
ARK_API_KEY=                 # API key body only; do not include the "Bearer " prefix

# VIDEO
HEYGEN_API_KEY=              # HeyGen avatar video gateway
RUNWAY_API_KEY=              # Runway native + Seedance 2.5, Gemini Omni, MiniMax H3
SUNO_API_KEY=                # Suno music generation

# TENCLOUD HUNYUAN VIDEO
TENCENT_TOKENHUB_API_KEY=    # Tencent Hunyuan cloud video via TokenHub API

# LOCAL (no keys needed — just GPU + install)
VIDEO_GEN_LOCAL_ENABLED=     # Set to "true" for local video gen
VIDEO_GEN_LOCAL_MODEL=       # wan2.2-ti2v-5b, wan2.1-1.3b, wan2.1-14b, hunyuan-1.5, ltx2-local, cogvideo-5b

# COMFYUI (optional overrides; localhost:8188 is the default)
COMFYUI_SERVER_URL=          # Local ComfyUI server for shared workflows
COMFYUI_VIDEO_SERVER_URL=    # Optional video-specific ComfyUI server
```

## 当前视频模型覆盖

以下的集成是基于已知、当前可用的模型标识符。没有公开的API契约的提供者页面没有给出假设的模型字符串。

| 模型 | 直接提供商 | fal.ai | Runway | ComfyUI 伙伴节点 | 本地 ComfyUI |
|------|------------|-------|--------|------------------|--------------|
| **Gemini Omni Flash** | Google `gemini_omni_video` (`gemini-omni-1.1-flash`) | `gemini_omni_fal` (T2V, I2V, references, editing) | `runway_video` 模型 `gemini_omni_flash` | 传统 `GeminiVideoOmni`映射不是一个稳定的 1.1 备选方案；单独迁移到 `GeminiVideoOmniV2` | 不可用作为本地权重 |
| **Seedance 2.5** | Volcengine `seedance_ark` 模型变体 `2.5` | `seedance_video` 模型版本 `2.5` | `runway_video` 模型 `seedance2_5` | `ByteDance2TextToVideoNode` (hosted, paid credits) | 不可用作为本地权重 |
| **MiniMax H3** | `minimax_video` 模型 `MiniMax-H3` | `minimax_fal_video` (`hailuo-03`) | `runway_video` 模型 `hailuo3` | `MinimaxHailuo03TextToVideoNode` (hosted, paid credits) | 支持官方开放权重和一个导出API工作流程 |

ComfyUI 伙伴节点运行在 ComfyUI 图形中，但调用远程服务；它们需要网络访问、登录的 Comfy 账户和预付费信用。只有 MiniMax H3 开放权重的工作流程在此表中是本地模型路径。

Replicate, HeyGen, 和 Higgsfield 没有更新到这些精确的模型版本，因为它们的公共 API 文档没有在此更新时提供一个当前、稳定的契约。

---

## 云提供商

### xAI — Grok 图像 + 视频

> **最好是想要一个提供商来编辑图像和参考条件的短视频。** Grok 既覆盖图像生成/编辑，也覆盖视频生成。

**解锁的工具:** `grok_image`, `grok_video`
**环境变量:** `XAI_API_KEY`

#### 设置

1. 创建一个 xAI 开发者账户
2. 在 xAI 开发者控制台中生成 API 密钥
3. 添加到 `.env`: `XAI_API_KEY=xai-...`

#### 最适合的用途

- 图像编辑和风格转移
- 将多个图像合并到一个生成的帧中
- 需要将人、衣物或产品带入运动的参考图像视频

#### 价格

当前 xAI 文档的 Grok 像素媒体模型的价格：

| 模型 | 价格 |
|------|------|
| `grok-imagine-image` | 每生成像素 $0.02 |
| `grok-imagine-image` 输入图像（编辑/合并） | 每输入像素 $0.002 |
| `grok-imagine-video` 480p | 每秒 $0.05 |
| `grok-imagine-video` 720p | 每秒 $0.07 |
| `grok-imagine-video` 输入图像 | 每输入像素 $0.002 |

现在，OpenMontage 在 Grok 工具估算器中使用这些公开的价格。

---

### Volcengine Jimeng — 即梦 AI 视频生成

> **直接通过 V4 签名调用 ByteDance API。** 使用 IAM AK/SK 认证的 HMAC-SHA256 请求签名调用 Volcengine 的视觉 API（visual.volcengineapi.com），支持文本到视频和图像到视频的 Jimeng 3.0 Pro。

**解锁的工具:** `jimeng_video`
**环境变量:** `VOLC_ACCESSKEY` (Access Key ID) + `VOLC_SECRETKEY` (Secret Access Key)

#### 设置

1. 前往 [console.volcengine.com/iam/keymanage](https://console.volcengine.com/iam/keymanage)
2. 创建一个Volcengine账户，如果你没有的话
3. 创建一个访问密钥对（AK + SK）
4. 确保你的账户可以访问Jimeng AI（即梦）视频生成服务
5. 添加到`.env`: `VOLC_ACCESSKEY=...` 和 `VOLC_SECRETKEY=...`

#### 最适合的用途

- 直接ByteDance/Volcengine API 计量使用
- Jimeng 3.0 Pro 文本到视频和图像到视频
- 中文语言提示理解
- 可配置的帧数（121=5s, 241=10s）和宽高比

#### API 说明

认证使用Volcengine IAM V4 签名（HMAC-SHA256），不是Bearer токен。签名过程构建一个规范请求，导出签名密钥（SK → 日期 → 地区 → 服务），并签署请求。

API 流程：`POST ?Action=CVSync2AsyncSubmitTask` → 监控`POST ?Action=CVSync2AsyncGetResult` → 下载`video_url`。

实现使用兼容的generic`CVSync2Async*`路由（API 版本`2022-08-31`），而不是在公共 API 探索中呈现的model-specific`2024-06-06`动作。这是有意为之的——generic route 支持Jimeng 3.0 Pro 模型通过`req_key`而保持在模型更新时的稳定性。

Video`req_key`的`jimeng_ti2v_v30_pro`。成功代码是`10000`。任务状态：`in_queue`,`generating`,`done`,`not_found`,`expired`。

**权威的API 参考:** [Jimeng TI2V V30 Pro SubmitTask](https://api.volcengine.com/api-docs/view?action=JimengTI2VV30PROSubmitTask&serviceCode=cv&version=2024-06-06)

**schema 约束**（通过`input_schema`来防止付费调用失败）：
- `prompt`：最大800个字符
- `frames`：必须是`121`（5s）或`241`（10s）在24fps下
- `seed`：`-1`用于随机，或任何非负整数

#### 价格

| 模型 | 价格 |
|------|-------|
| Jimeng 3.0 Pro（视频） | ~$0.05/秒（请在Volcengine 控制台查看实际速率） |

---

### Volcengine Ark — 直接Seedance 2.0 和 2.5 视频生成

> **官方直接Seedance API。** 调用Volcengine Ark，而不通过fal.ai或Replicate路由，尽管保留这些现有提供者路径作为独立的备选。

**工具解锁：** `seedance_ark`

**环境变量：** `ARK_API_KEY`

#### 设置

1. 打开[Volcengine Ark API 密钥控制台](https://console.volcengine.com/ark/region:cn-beijing/apiKey)
2. 启用Seedance 模型家族并确认账户有余额或有效资源包
3. 创建一个长期有效的API 密钥
4. 将密钥主体添加到`.env`: `ARK_API_KEY=...`

不要在环境值中包含`Bearer `前缀。工具在发送请求时添加了授权方案。

可选的超出：```bash
ARK_SEEDANCE_MODEL=doubao-seedance-2-0-260128
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_CNY_PER_USD=7.2
```

#### 模型和能力

| 变体 | 默认模型ID | 输出 |
|------|------------|------|
| 2.5 | `doubao-seedance-2-5-260628` | 480p 或 720p; 4–30 秒 |
| 标准 | `doubao-seedance-2-0-260128` | 480p, 720p, 1080p 或 4K |
| 快速 | `doubao-seedance-2-0-fast-260128` | 480p 或 720p |
| 小 | `doubao-seedance-2-0-mini-260615` | 480p 或 720p |

适配器支持：

- 文本到视频，第一帧图像到视频，和多模态参考到视频
- 受验证数据 URI 形式的本地图像和音频输入
- 参考图像、视频和音频 URL
- 创建、查询、取消和有界定期的任务
- 同步音频，选项性最后一帧返回，文本请求的网页搜索，和输出下载
- 提交前的干预测试和基于token的成本估算

Seedance 2.5 允许最多30张图片、10个视频和10个音频参考。
选择它时用 `model: "2.5"`（或其精确的模型ID）。因为公共文档没有为此模型确立稳定的默认token价格，
OpenMontage 需要 `custom_price_cny_per_million_tokens`在呈现成本估算之前；未知价格从未报告为免费的。

本地参考视频是故意拒绝的，因为公共API 没有文档支持视频 Data URI 支持。使用一个可以访问的HTTPS URL 或 Ark资产参考代替。

#### API 和账单说明

异步 API 流程如下：

`POST /contents/generations/tasks` → `GET /contents/generations/tasks/{id}` → 下载成功结果URL。

已排队的任务可以用 `DELETE /contents/generations/tasks/{id}`取消。任务记录保留有限时间，成功结果URL 是短暂的，所以工具立即下载输出。

Ark 通过完成tokenbilling 以billing Seedance。模型、分辨率和是否包含参考视频在请求中都会影响费用。OpenMontage 在提交前估算成本，并在可用时与提供商返回的使用量进行匹配。检查 Ark 控制台以获取当前费用之前进行付费运行；定制端点ID 和 Seedance 2.5 需要明确的定制价格，所以未知价格从未被认为是免费的。

官方参考： [Seedance 模型列表](https://www.volcengine.com/docs/82379/1366799)，[创建任务](https://www.volcengine.com/docs/82379/1520757?lang=zh)，[查询任务](https://www.volcengine.com/docs/82379/1521309?lang=zh)。

---

### Alibaba DashScope — Qwen Image + TTS + ASR

> **最佳适用于中文语言生产。** 一个关键可以解锁 Qwen-Image 生成、Qwen-TTS 的普通话叙述和 Qwen-ASR 的单词级时间戳——唯一的 DashScope 路径为字幕同步提供单词级细节。

**解锁的工具：** `dashscope_image`, `dashscope_tts`, `dashscope_asr`
**环境变量：** `DASHSCOPE_API_KEY`

#### 设置

1. 访问 [dashscope.aliyun.com](https://dashscope.aliyun.com/)
2. 如果没有创建 Alibaba Cloud 账户，则创建一个
3. 在 DashScope 控制台生成 API 密钥
4. 添加到 `.env`: `DASHSCOPE_API_KEY=sk-...`

#### 最适用的场景

- 使用强大的提示理解进行中文语言图像生成（Qwen-Image）
- 自然普通话叙述（Qwen-TTS，Cherry voice）
- 用于字幕同步的单词级时间戳转录文件（Qwen-ASR filetrans）
- 替换了已故的 `whisperx` 位置的 ASR

#### API 注释
DashScope's `/compatible-mode/v1/` only supports `/chat/completions` and `/embeddings`. Image gen, TTS, and ASR all use DashScope-native endpoints with nested `{model, input, parameters}` request shape — not OpenAI-compatible paths.

The ASR tool (`qwen3-asr-flash-filetrans`) uses an async submit-poll pattern. Audio must be at a publicly accessible URL (local files are not supported). Word timestamps are in milliseconds, normalized to seconds by the tool.

#### 价格

| 模型 | 价格 |
|------|-------|
| `qwen-image-2.0-pro` | ~$0.02 per image (检查控制台获取当前率) |
| `qwen3-tts-flash` | ~$0.000015 per character |
| `qwen3-asr-flash-filetrans` | 每分钟计费 (检查控制台) |

---

### 腾讯云 — 图像生成

> **中文友好第一方图像生成。** `hunyuan_image`通过腾讯 TokenHub访问Hunyuan Image 3.0，并使用Bearer-Token认证。它支持带有种子文本的图像生成，最多三个参考图像，定制分辨率，提示重写和水印控制。

**工具解锁:** `hunyuan_image`

**环境变量:** `TENCENT_TOKENHUB_API_KEY`

在腾讯云 TokenHub控制台生成API密钥，并将其添加到
`.env`。该工具报告大约每生成一个图像花费0.08美元，基于TokenHub的信用价格。它通过`image_selector`可用；共享参考图像输入被规范化为提供者的`images`数组。

---

### fal.ai — 多模型入口

> **广泛单键覆盖。** 一个API密钥解锁了多个图像和视频提供商。

**解锁的工具:** `flux_image`, `recraft_image`, `seedream_image`,
`kling_video`, `veo_video`, `seedance_video`, `gemini_omni_fal`,
`minimax_fal_video`, `fal_elevenlabs_tts`, `fal_elevenlabs_music`
**环境变量:** `FAL_KEY`

#### 设置

1. 访问[fal.ai](https://fal.ai/)并点击**注册**（GitHub或Google）
2. 导航到[fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)
3. 点击**创建密钥**，复制它
4. 添加到`.env`: `FAL_KEY=your-key-here`

#### 价格

无订阅 — 纯按需支付，无最低支出。

**图像生成:**

| 模型 | 价格 | 每1美元 |
|-------|-------|--------|
| FLUX Pro v1.1 | $0.05/image | 20 images |
| FLUX Dev | $0.03/image | 33 images |
| Recraft v3 | ~$0.04/image | 25 images |
| Seedream 5 Pro (最大1536x1536) | $0.0675/image | ~14 images |
| Seedream 5 Pro (最大2048x2048) | $0.135/image | ~7 images |

**视频生成:**

| 模型 | 价格 | 每1美元 |
|-------|-------|--------|
| Kling 2.5 Turbo Pro | $0.07/sec | 14 seconds |
| Seedance 2.5 | endpoint-dependent | 4–30 seconds |
| Gemini Omni Flash | endpoint-dependent | 3–10 seconds |
| MiniMax H3 (`hailuo-03`) | endpoint-dependent | 4–15 seconds |
| Veo 3 | $0.40/sec | 2.5 seconds |
| WAN 2.5 | $0.05/sec | 20 seconds |

**免费通道:** 无 — 但$0起步，您只需支付您使用的费用。

同一个密钥还可以通过fal.ai访问ElevenLabs的语音和音乐。使用
`fal_elevenlabs_tts`当ElevenLabs的直接凭证不可用时，或
通过`tts_selector`选择它并使用`preferred_provider: "fal.ai"`。

---

### MiniMax — 官方直接图像和视频API

> **第一方图像和视频生成。** MiniMax官方直接API支持
**工具解锁：** `minimax_image`, `minimax_video`

**环境变量：** `MINIMAX_API_KEY`

**可选区域：** `MINIMAX_REGION=global`（默认）或 `cn`

#### 设置

1. 创建一个MiniMax开源平台账户。
2. 在账户的API密钥页面生成API密钥。
3. 将`MINIMAX_API_KEY=...`添加到`.env`。
4. 对于大陆中国账户，还需设置`MINIMAX_REGION=cn`。

`MINIMAX_BASE_URL`可用于文档化的私有/企业端点重定向。默认的全球和大陆中国主机由`MINIMAX_REGION`选择。

#### MiniMax H3 视频

使用`minimax_video`和`model: "MiniMax-H3"`。该工具使用v2任务合同（`POST /v2/video_generation`，然后`GET /v2/query/video_generation/{task_id}`），支持4–15秒的2K视频剪辑。较旧的hailuo模型继续使用v1 API。MiniMax H3参考生成可以结合图像、视频和音频；音频参考需要视觉参考。

#### 定价

| 模型 | 全球按用费价格 |
|------|------------------|
| `image-01`, `image-01-live` | 每生成图像 $0.0035 |

MiniMax还提供订阅token计划，包含每日图像配额。OpenMontage谨慎地在成本估算和生成结果中报告标准按用费金额。

工具可以通过图像和视频选择器自动发现；选择它们时使用`preferred_provider: "minimax"`。

---

### Atlas 云 — 图像和视频入口

**工具：** `atlas_image`, `atlas_video`
**环境变量：** `ATLASCLOUD_API_KEY`（别名：`ATLAS_CLOUD_API_KEY`, `ATLAS_API_KEY`）
**技能：** `.agents/skills/atlas-cloud/SKILL.md`

Atlas Cloud提供一个入口和密钥，用于以下明确列出的路线。OpenMontage验证每个模型的实际schema，而不是将任务后缀或参数名称视为可互换。

| 家族 | 支持路线 | 当前Atlas费率 |
|------|-----------|------------------|
| Seedance 2.5 | 文本/图像/参考到视频 | $0.134/秒 |
| Seedance 2.0 | 文本/图像/参考到视频 | $0.112/秒 |
| Gemini Omni Flash | 文本/图像/参考到视频；视频编辑；开发人员文本/图像/参考 | $0.112–$0.140/秒 |
| MiniMax H3 | 文本/图像/参考到视频 | $0.100/秒 |
| Seedream 5.0 Pro | 文本到图像；编辑；层分解 | $0.022–$0.045/图像 |
| GPT Image 2 | 文本到图像；编辑 | $0.009–$0.010/图像 |
| Nano Banana 2 | 文本到图像；编辑 | $0.080/图像 |

查看`get_info()["model_catalog"]`以获取精确ID、操作、媒体形状、持续时间和分辨率。价格是从每个模型的Atlas页面中获取的机器可读页面的估计，并应在付费批次前再次确认。

---

### Kling 官方 — 直接API

> **官方Kling路径。** 这是与`kling_video`通过fal.ai不同的`Authorization: Bearer <KLING_API_KEY>`API，它使用Kling的官方`kling_official`API，提供者名称`kling_official_video`，并直接使用Classic/Turbo/Omni任务协议。

**解锁的工具：** `kling_official_video`, `kling_official_image`, `kling_tts`, `kling_avatar`, `kling_lip_sync`
**环境变量：** `KLING_API_KEY`，可选`KLING_API_BASE_URL`

#### 设置

1. 创建或打开一个Kling AI开源平台账户。
2. 在 Kling API 控制台生成官方 API 密钥。
3. 添加到 `.env`：```bash
   KLING_API_KEY=your-key-here
   # Optional, defaults to Singapore:
   KLING_API_BASE_URL=https://api-singapore.klingai.com
   ```

#### 这是最适合的

- Kling 官方 API 的直接官方来源，而不是 fal.ai 路由
- `kling_official_video` 通过 Text-to-video、image-to-video 和 Deep Video Omni 参考工作流
- `kling_official_image` 通过 Text-to-image、image edit/reference 和 Image Omni 多参考或系列工作流
- `kling_tts` 通过 Text-to-speech，当你已经知道 Kling 的官方`voice_id`
- `kling_avatar` 通过 Cloud avatar presenter clips，既不替代本地`talking_head`
- `kling_lip_sync` 通过 Cloud lip-sync，具有明确的面部选择用于多个人视频
- 需要使用 Kling 官方模型的权限、资源包或区域端点的账户

#### 注意事项

- `provider="kling_official"` 不是 fal.ai 的 `provider="kling"`。
- Kling 官方是一个付费远程 API。OpenMontage 使用保守的成本估计，并包括高成本因素，如 Omni 参考、系列输出、4k 模式和原生声音。
- 支持 Classic/图像生成字段的本地图像路径以原始 base64 形式发送。Turbo image-to-video 需要 URL 并不会默默地通过 fal.ai 上传。
- Video Omni 和 Image Omni 可以通过 `element_id` 参考通过 `element_list` 传递；Elements 保持为 Kling 官方的内部助手，不是 OpenMontage 的独立能力。
- Account Usage 可作为低频诊断辅助工具，使用 `tools/_kling/account.py`；它不是选择器或管道工具。
- `callback_url` 通过并记录传递，但 OpenMontage 仍然默认通过任务进行监控。
- `kling_tts` 需要明确的 `voice_id`；OpenMontage 不会猜测默认的官方声音。
- `kling_avatar` 和 `kling_lip_sync` 注册在现有 `avatar` 能力下并与本地 SadTalker/Wav2Lip 工具共存。当前的 avatar 流程必须明确地选择它们；注册发现本身不能替代本地工具。
- Kling 官方的音效和视频效果已被记录，但尚未注册为 OpenMontage 工具，因为当前的流程没有一个稳定的音效或视频效果能力槽供它们使用。

---

### ElevenLabs — 声音、音乐、音效

> **优质的语音质量。** 最佳用于叙述性视频的 TTS。还生成音乐和音效。

**解锁的工具:** `elevenlabs_tts`, `music_gen`
**环境变量:** `ELEVENLABS_API_KEY`

#### 设置

1. 访问 [elevenlabs.io](https://elevenlabs.io) 并点击 **注册**
2. 访问 **个人资料**（底部左侧）> **API 密钥**，或访问 [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys)
3. 点击 **创建 API 密钥**，命名它，复制它
4. 添加到 `.env`: `ELEVENLABS_API_KEY=xi_your-key-here`

#### 价格表

| 计划 | 价格 | 每月字符 | 关键特性 |
|------|-------|-----------|----------|
| **免费** | $0 | 10,000 | 3 个自定义声音，API 访问，需提供归属 |
| Starter | $5/月 | 30,000 | 无归属 |
| Creator | $22/月 | 100,000 | 专业语音克隆 |
| Pro | $99/月 | 500,000 | 96kbps 音频，使用分析 |
| Scale | $330/月 | 2,000,000 | 优先支持 |
**免费使用:** 每月10,000个字符（大约2-3分钟的叙述）。API 访问包含在内。音乐生成和音效也可在免费使用期间使用，但限额有限。

---

### fish.audio — 表情丰富的TTS+语音克隆

> **高情感叙述和可重用的克隆语音。** S2生成模型支持内联情感标签（`[laugh]`, `[whispers]`）和80多种语言。使用fish.audio Playground创建的语音在运行期间通过`reference_id`重用。

**解锁的工具：** `fish_audio_tts`
**环境变量：** `FISH_AUDIO_API_KEY`

#### 设置

1. 在[fish.audio](https://fish.audio)注册账号。
2. 在[fish.audio/go-api/api-keys](https://fish.audio/go-api/api-keys/)创建API密钥。
3. 将`.env`添加到：`FISH_AUDIO_API_KEY=your-key-here`
4. （可选）在fish.audio Playground中构建或选择一个语音模型，并将其id传递为`reference_id`重用一个克隆语音。

#### 后端模型

`model`是**必须的 — 没有默认值。** 选择其中之一：

| 模型 | 最适用情况 |
|------|------------|
| `s2.1-pro` | 最新旗舰 — 内联情感标签，80多种语言，英雄叙述 |
| `s2.1-pro-free` | s2.1-pro的免费试用 — 草稿，样本，验证运行（见下方的 Caveats） |
| `s2-pro` | 第一个S2生成模型 — 高质量稳定，情感标签支持 |
| `s1` | 保持兼容的前旗舰，已被移除（不支持情感标签） |

**`s2.1-pro-free` Caveats — 促销，不是长期免费使用。** 根据[fish.audio公告](https://fish.audio/ko/blog/s2-1-pro-free-api/?articleLocale=en)，免费API访问将在**2026年8月31日**结束，并且受Fair Use限制，提供**无保证的服务水平或延迟**，请求**可能会被fish.audio保留**，并且**商业用途受限**。不要将客户工作或生产叙述通过它路由，计划长期成本为$0 — `fish_audio_tts.estimate_cost()`在促销窗口结束后回到付费`s2.1-pro`价格。

已移除的`speech-1.x` Legacy-tier和`s1-mini`已从fish.audio API中移除，并不再被支持。

#### 价格

billing是**按UTF-8字符的输入文本**（不按字符）计费 — CJK文本和emoji成本3-4倍于同长度的ASCII字符。当前的列表价格：`s1` / `s2-pro` / `s2.1-pro` = 每1M字节$15；`s2.1-pro-free`仅在促销期间（通过2026年8月31日 — 见上面的 Caveats）为$0。请在[官方价格指南](https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits)中核实当前价格，之前进行大批量操作。

---

### Doubao Speech — 普通话TTS

> **强大的普通话叙述。** Volcengine Doubao Speech是一个适合中文解释语音和需要字幕时间戳的长篇叙述的好选择。

**解锁的工具：** `doubao_tts`
**环境变量：** `DOUBAO_SPEECH_API_KEY`, `DOUBAO_SPEECH_VOICE_TYPE`

#### 设置

1. 在Volcengine Doubao Speech控制台打开并启用Speech Synthesis 2.0。
2. 创建一个新的控制台API密钥。
3. 选择一个Speech 2.0的语音类型，例如`zh_female_vv_uranus_bigtts`。
4. 将`.env`添加：```bash
   DOUBAO_SPEECH_API_KEY=your-api-key
   DOUBAO_SPEECH_VOICE_TYPE=zh_female_vv_uranus_bigtts
   ```

#### API 说明

OpenMontage 使用新式 API 密钥流：

0```text
X-Api-Key: ${DOUBAO_SPEECH_API_KEY}
X-Api-Resource-Id: seed-tts-2.0
```Do not pass a new-console API Key as `X-Api-App-Id` or `X-Api-Access-Key`. That mismatch can produce `load grant: requested grant not found`.

#### What It Is Best For

- Natural Mandarin narration for Chinese-language explainers
- Async long-form narration via `/api/v3/tts/submit` and `/api/v3/tts/query`
- Character-level timing metadata for subtitle alignment
- Calm educational pacing where the video duration can follow the approved voice rhythm

#### Pacing

Start with `speech_rate: 0` for natural Mandarin delivery. If the approved format needs a tighter runtime, compare short samples at `speech_rate: 25` or `50` before generating the full narration. Do not force Doubao to match another provider's duration unless the user explicitly wants that tradeoff.

#### Pricing

Doubao Speech 2.0 is billed by character package or usage in Volcengine. OpenMontage estimates cost from text length and prefers provider-returned usage metadata when available.

---

### Tencent Hunyuan Cloud — Video Generation

> **Tencent Hunyuan (腾讯混元) cloud video generation via TokenHub API.** Generates
> videos from text or images using Tencent's Hunyuan models through the Tencent
> TokenHub API — an OpenAI-compatible gateway (tokenhub.tencentmaas.com) with
> simple Bearer-token authentication. No TC3-HMAC-SHA256 signing required.

**Tools unlocked:** `hunyuan_cloud_video`
**Env var:** `TENCENT_TOKENHUB_API_KEY`

#### Setup

1. Go to the [Tencent Cloud TokenHub console](https://console.cloud.tencent.com/tokenhub).
2. Create an application or navigate to the **API Key** section.
3. Generate an API key and copy its value.
4. Add to `.env`:```bash
   TENCENT_TOKENHUB_API_KEY=your-tokenhub-api-key
   ```

#### 最适用场景

- **中文友好的提示理解** — Hunyuan 模型比大多数西方 API 更好地理解中文提示
- **简单的认证** — Bearer 键，无需复杂的签名（只需 HTTP 认证头）
- **直接的腾讯云计量** — 使用自己的腾讯云信用，非第三方门槛标记
- **文本到视频和图像到视频** — 一个 API 键解开了文本到视频和图像到视频

#### API 注记

TokenHub 使用一个 **提交-然后等待** 模式：```text
# Submit a generation task
POST https://tokenhub.tencentmaas.com/v1/api/video/submit
Authorization: Bearer ${TENCENT_TOKENHUB_API_KEY}

# Poll for results
POST https://tokenhub.tencentmaas.com/v1/api/video/query
Authorization: Bearer ${TENCENT_TOKENHUB_API_KEY}
```| 模型 | 类型 | 价格 |
|------|------|------|
| `hy-video-1.5` | 文本到视频 | 1.5 租金 (~$0.25) |
| `yt-video-2.0` | 图片到视频 | 2–5 租金 (~$0.33–0.83) |

分辨率选项：**720p**（默认）或 **1080p**。

默认情况下，添加了水印 (`logo_add`)。将 `logo_add: 0` 设置为禁用它（需要腾讯的_console 认可）。

**schema 约束：**
- **提示:** 最大200个 UTF-8字符
- **图片:** 最大10MB，50–5000 px 每边，比例范围为1:4到4:1
- **格式:** jpg, png, jpeg, webp, bmp, tiff

#### 备用工具

如果 `hunyuan_cloud_video` 返回错误，代理可能会重试： `jimeng_video`, `kling_official_video`, `minimax_video`

#### 价格

腾讯 TokenHub 使用基于租金的价格系统（1 租金 = 1.2 RMB ≈ $0.167 USD）：

| 模型 | 分辨率 | 租金 | 估计美元 |
|------|--------|------|---------|
| HY-Video-1.5 | 任何 | 1.5 | ~$0.25 |
| YT-Video-2.0 | 480p | 2 | ~$0.33 |
| YT-Video-2.0 | 720p / 1080p | 5 | ~$0.83 |

> **免费套餐:** 腾讯偶尔为 TokenHub 新用户提供租金。请查看 [TokenHub_console](https://console.cloud.tencent.com/tokenhub) 以获取当前促销。

---

### Azure AI Speech — 声音到文本

> **云转录。** Azure AI Speech Fast Transcription 将本地音频转化为文本，提供每个词的时间戳，交叉识别发言者和多语言识别——无需GPU。可选：本地更快的-whisper `transcriber`仍然是默认的离线 STT 路径。当 `AZURE_SPEECH_KEY` 设置时，代理偏好 `azure_stt` 进行云转录。

**解锁的工具：** `azure_stt`
**环境变量：** `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`（或 `AZURE_SPEECH_ENDPOINT`）

#### 设置

1. 在 [Azure门户](https://portal.azure.com) 中创建一个 **Speech** 资源（Azure AI 服务 → Speech服务）。
2. 打开资源的 **Keys and Endpoint** 页面。
3. 将 **KEY 1** 和 **Location/Region**（例如 `eastus`）复制到 `.env` 中：```bash
   AZURE_SPEECH_KEY=your-speech-resource-key
   AZURE_SPEECH_REGION=eastus
   # AZURE_SPEECH_ENDPOINT=https://<custom>...  # optional, overrides region
   ```

#### API 说明

OpenMontage 使用 **快速转录** REST 端点，该端点接受直接（multipart）上传本地音频文件，并返回同步结果 — 无 Azure Blob 存储、 SAS URL 或异步任务监控：```text
POST https://{region}.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15
Ocp-Apim-Subscription-Key: ${AZURE_SPEECH_KEY}
```

#### 适合什么

- 云端转录，包含音标时间戳，不需要本地GPU
- 跨语言自动检测，覆盖候选语言集
- 不需要 HuggingFace token 的说话者分割
- `subtitle_gen`的字幕时间标注数据直接流入`subtitle_gen`

#### 价格

Azure AI Speech Standard (S0)按音频小时计费（大约每小时1美元，写时的价格；免费F0级别包括有限的每月额度）。OpenMontage估算费用来自转录的音频时长。查看[Azure AI Speech 价格](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)以获取当前的费用。

---

### Azure AI Speech — Text-to-Speech

> **云端神经叙述。** Azure 神经TTS 提供高质量的多语言声音，包含 SSML 语音控制和表达方式 — 与 `azure_stt` 的同一个语音资源相同，因此一个键/区域可以解锁两种方向。可选：`piper_tts`仍然是默认的本地TTS路径。当`AZURE_SPEECH_KEY`设置时，代理可能会优先选择`azure_tts`进行云端叙述。

**解锁的工具：** `azure_tts`
**环境变量：** `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`（或 `AZURE_TTS_ENDPOINT`）

#### 配置

与上面提到的 STT 配置相同 — 同一个 Speech 资源键和区域适用于两者。如果您已经配置了 `azure_stt`，`azure_tts`现在可用。```bash
AZURE_SPEECH_KEY=your-speech-resource-key
AZURE_SPEECH_REGION=eastus
# AZURE_TTS_ENDPOINT=https://<region>.tts.speech.microsoft.com  # optional, overrides region
```

#### API 说明

OpenMontage 使用同步 REST v1 端点，带有 SSML 身份证 — 无身份验证、 Blob 存储或任务监控：

Note: TTS 服务器 (`<region>.tts.speech.microsoft.com`) 与 STT 端点不同，因此可选的替换变量是 `AZURE_TTS_ENDPOINT`，不是 `AZURE_SPEECH_ENDPOINT`。```text
POST https://{region}.tts.speech.microsoft.com/cognitiveservices/v1
Ocp-Apim-Subscription-Key: ${AZURE_SPEECH_KEY}
Content-Type: application/ssml+xml
X-Microsoft-OutputFormat: audio-48khz-192kbitrate-mono-mp3
```

#### 声音短名单的替代名称： `andrew` (默认 — 温暖、自信)， `brandon`
（更深）， `ava` (明亮的女性)， `guy` (权威)， `jenny` (友好)。任何 Azure 声音短名都可以接受字面上的使用。请参阅 `azure-text-to-speech`
技能以获取 SSML `rate`/`pitch`/`style`的指导。

#### 何时最好使用

- Azure Azure 账户的现有神经叙述的高质量
- 温暖、自信的解释者 / 创始人注册发音
- 多语言叙述通过 *多语言* 声音家族
- 确定性重渲染（固定声音 + SSML → 相同的音频）

不适用于：完全离线生产（使用 `piper_tts`）或声音克隆（使用 `elevenlabs_tts`）。

#### 价格

Azure 神经 TTS 标准 (S0) 大约每 1M 个字符收费 **$16**（F0 级别包括有限的每月月度额度）。一个 150 个单词的叙述段落大约花费 $0.015。OpenMontage 根据字符数估算成本。参阅 [Azure AI Speech 价格](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/) 获取当前费用。

---

### Google — TTS + Imagen + Music + Video (共享密钥)

> **一个密钥，五个工具。** Google Cloud TTS 有 700+ 声音在 50+ 语言中 — 最强的本地化选项。 `google_imagen` 支持 Imagen 4 和 Gemini 2.5 Flash Image，包括没有 Imagen 目录访问的项目。Google Lyria 生成高质量背景音乐。Gemini Omni Flash 支持对话视频编辑，直接 Veo 生成覆盖高质量短视频片段。

**解锁的工具：** `google_tts`, `google_imagen`, `google_music`, `gemini_omni_video`, `veo_video`
**环境变量：** `GOOGLE_API_KEY` (或 `GEMINI_API_KEY` — 两者都可以； `GEMINI_API_KEY` 具有优先权)

#### 设置

1. 访问 [Google AI Studio](https://aistudio.google.com/) 并登录
2. 导航到 [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
3. 点击 **创建 API 密钥**，选择一个 Google Cloud 项目
4. 拷贝密钥
5. 添加到 `.env`: `GOOGLE_API_KEY=AIza...` (或 `GEMINI_API_KEY=AIza...`)

**对于 TTS 特别而言，你还需要启用 Text-to-Speech API：**
1. 访问 [console.cloud.google.com/apis/library/texttospeech.googleapis.com](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com)
2. 点击 **启用**
3. 确保你的 API 密钥的限制允许 Text-to-Speech API

**对于 Imagen, Lyria Music, Gemini Omni 视频和直接 Veo 视频，启用 Generative Language API：**
1. 访问 [console.cloud.google.com/apis/library/generativelanguage.googleapis.com](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com)
2. 点击 **启用**

#### Google TTS 价格

| 声音类型 | 免费层 | 每 1M 个字符的付费 | 注释 |
|-----------|-----------|---------------------|-------|
| **标准** | 1M 个字符/月 | $4.00 | 基础质量，快速 |
| **WaveNet** | 1M 个字符/月 | $16.00 | 自然发音 |
| **Neural2** | 1M 个字符/月 | $16.00 | 最佳质量 |
| **Studio** | — | $24.00 | 专业录音室声音 |
| **Chirp** | — | $4.00 | 交谈风格 |

免费层是独立的 — 你每月免费获得 1M 标准和 1M WaveNet 以及 1M Neural2 个字符。大约每月 250+ 分钟的叙述，每月零成本。

#### Google Imagen 价格

| 模型 | 每张图片的价格 |
|-------|----------------|
| Imagen 4 Fast | $0.02 |
| Imagen 4 Standard | $0.04 |
| Imagen 4 Ultra | $0.06 |
| Gemini 2.5 Flash Image (`gemini-2.5-flash-image`) | $0.039 |

**免费通道:** 无。付费通道仅有。

通过通过governed `image_selector`来选择Gemini后端，传递`preferred_provider: "google_imagen"`和`model_name: "gemini-2.5-flash-image"`。选择器将其中立`model_name`字段映射到提供商的`model`输入。

#### Gemini Omni 视频价格

| 模型 | 价格 | 注释 |
|-------|-------|-------|
| `gemini-omni-1.1-flash` | ~$0.10 每秒视频 | 标准输入：$1.50/1M 词汇。输出：$9.00/1M 文本词汇和$17.50/1M 视频词汇；720p 视频发出5,792个词汇/秒 |

直接使用OpenMontage转换器生成3–10秒的720p/24fps视频，配有合成音频，以及状态性对话编辑（`edit_video`通过`previous_interaction_id`）。`duration`输入仅仅是计划/提示：转换器不发送它，模型选择实际持续时间，提示不限制账单。`ToolResult.cost_usd`使用可用的提供商`usage`：所有输入模式均为$1.50/1M 词汇，输出文本为$9.00/1M，视频及未知或未分类输出被保守地$17.50/1M；单独报告的思维词汇也以$17.50/1M的价格计费。如果使用缺失或不正确，转换器假设10秒输出的最大持续时间，并加上一个保守的输入词汇估计，因此短时提示不能降低备用。

设置`store=false`用于一次性生成，应该不应留存在后续编辑回调中。如果付费生成成功但下载失败，结果包括`output_uri`，使用有效使用的费用（否则是保守的备用），以及`resume_download`的payload；重新执行该payload来进行GET单独恢复，而无需提交或收费第二次生成。**付费通道仅有。**实际720p视频输出大约为每秒$0.10，前任何输入和任何文本/思维输出；每次编辑回调生成一个新片段并再次计费。

#### Google 音乐 (Lyria) 价格

| 模型 | 每生成请求价格 |
|-------|-----------------------------|
| `lyria-3-pro-preview` | $0.08（固定费率，最长184秒持续时间） |

**免费通道:** 无。付费通道仅有。

**新账户优惠:** Google Cloud 提供 **每个通道300美元的免费信用**（90天试用期），适用于TTS、Imagen、音乐、Gemini Omni视频、以及直接使用Veos视频。

#### Google TTS 声音类型

Google TTS 提供超过700种声音，超过50种语言。声音名称遵循`{language}-{type}-{letter}`的模式：

| 类型 | 示例 | 质量 | 成本 |
|------|---------|---------|------|
| **Chirp 3 HD** | `en-US-Chirp3-HD-Orus` | **最佳（2024，最自然）** | **中等 — 默认** |
| 标准 | `en-US-Standard-A` | 好 | 最便宜 |
| WaveNet | `en-US-WaveNet-D` | 非常好 | 中等 |
| Neural2 | `en-US-Neural2-D` | 非常好 | 中等 |
| 工作室 | `en-US-Studio-O` | 专业 | 最贵 |
| Journeys | `en-US-Journey-D` | Conversational (long-form) | Mid |

**Recommended voices:** `en-US-Chirp3-HD-Orus` (male, rich/cinematic), `en-US-Chirp3-HD-Aoede` (female, warm). These are Google's newest tier — most natural-sounding, uses the v1beta1 endpoint automatically.

**Languages include:** English (US, UK, AU, IN), Spanish, French, German, Italian, Portuguese, Japanese, Korean, Chinese (Mandarin, Cantonese), Arabic, Hindi, Russian, Dutch, Polish, Turkish, Vietnamese, Thai, Indonesian, and 30+ more.

---

### OpenAI — TTS + Image Generation

> **Solid all-rounder.** GPT Image 2 handles complex multi-element compositions and in-image text well. TTS is fast and affordable.

**Tools unlocked:** `openai_tts`, `openai_image`
**Env var:** `OPENAI_API_KEY`

#### Setup

1. Go to [platform.openai.com/signup](https://platform.openai.com/signup) and create an account
2. Add a payment method at [platform.openai.com/account/billing](https://platform.openai.com/account/billing)
3. Navigate to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Click **Create new secret key**, name it, copy it
5. Add to `.env`: `OPENAI_API_KEY=sk-...`

#### TTS Pricing

| Model | Price per 1M characters |
|-------|------------------------|
| tts-1 | $15.00 |
| tts-1-hd | $30.00 |
| gpt-4o-mini-tts | $12.00 |

#### Image Pricing

| Model | Size | Quality | Price per image |
|-------|------|---------|----------------|
| GPT Image 2 | 1024x1024 | low | $0.006 |
| GPT Image 2 | 1024x1024 | medium | $0.053 |
| GPT Image 2 | 1024x1024 | high | $0.211 |
| GPT Image 2 | 1024x1536 / 1536x1024 | low | $0.005 |
| GPT Image 2 | 1024x1536 / 1536x1024 | medium | $0.041 |
| GPT Image 2 | 1024x1536 / 1536x1024 | high | $0.165 |

> **注意：** DALL-E 2/3 were shut down by OpenAI on 2026-05-12, and the `gpt-image-1` family (`gpt-image-1-mini`, `gpt-image-1.5`) retires 2026-12-01 — `gpt-image-2` is OpenAI's recommended replacement ([deprecations](https://developers.openai.com/api/docs/deprecations)).

**Free tier:** None. Requires prepaid billing. Previously offered $5 in free credits for new accounts (discontinued for most signups).

---

### Runway — Native and Third-Party Video Models

> **Multi-model production API.** OpenMontage supports current Runway-native
> models plus documented third-party Seedance 2.5, Gemini Omni Flash, and
> MiniMax H3/Hailuo 3.0 routes.

**Tools unlocked:** `runway_video`
**Env var:** `RUNWAY_API_KEY`

#### Setup

1. Go to [dev.runwayml.com](https://dev.runwayml.com/) and create a developer account
2. Subscribe to a paid plan (Standard or above — API requires subscription)
3. Generate an API key from the developer portal
4. Add to `.env`: `RUNWAY_API_KEY=key_...`

#### Pricing

| Plan | Price | Credits/month | Video capacity |
|------|-------|---------------|----------------|
| **Free** | $0 | 125 one-time | ~5 seconds Gen-4 |
| Standard | $12/mo | 625 | ~25 seconds Gen-4 |
| Pro | $28/mo | 2,250 | ~90 seconds Gen-4 |
| Unlimited | $76/mo | Unlimited (Explore Mode) | Unlimited Gen-4 Turbo |

**API pricing (Runway credits are $0.01 each):**

| Model | Price per second |
|-------|-----------------|
| Gen-4 Turbo | ~$0.05 |
| Gen-4.5 | ~$0.12 |
| Seedance 2.5 | ~$0.20 at 480p / ~$0.30 at 720p |
| Gemini Omni Flash | ~$0.10 generation / ~$0.11 video editing |
| MiniMax H3 (`hailuo3`) | ~$0.10 at 768P / ~$0.15 at 2K |

Seedance 2.5 supports text, image, and video inputs, 4–30 second outputs, and
up to 30 image, 10 video, and 10 audio references. Gemini Omni Flash supports
3–10 second text/image generation plus video editing with up to five image
references. Hailuo 3.0 is Runway's MiniMax H3 route and supports 5–15 second
outputs at 768P or 2K. The adapter maps each model to its exact request field
names instead of sending a generic payload.

Gen-3 Alpha Turbo and Gen-4 Aleph were removed from the Runway API on
2026-07-30 and are not offered by the tool.

**Free tier:** 125 one-time credits (no monthly renewal). Enough for about 5 seconds of Gen-4 video. API access requires a paid subscription.

---

### Higgsfield — Multi-Model Video Orchestrator

> **Multi-model video platform.** Routes to Kling 3.0, Veo 3.1, Sora 2, WAN 2.5, and proprietary Soul Cinema through a single API. Includes Soul ID for character consistency across clips.

**Tools unlocked:** `higgsfield_video`
**Env vars:** `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` (or combined `HIGGSFIELD_KEY=key:secret`)

#### Setup

1. Go to [cloud.higgsfield.ai](https://cloud.higgsfield.ai/) and create an account
2. Subscribe to a plan (Starter or above for API access)
3. Navigate to API Keys section at [cloud.higgsfield.ai/api-keys](https://cloud.higgsfield.ai/api-keys)
4. Generate an API key and secret
5. Add to `.env`:```
   HIGGSFIELD_API_KEY=your-api-key
   HIGGSFIELD_API_SECRET=your-api-secret
   ```

#### 价格

| 计划 | 价格 | 注释 |
|------|-------|-------|
| 免费 | $0 | 限制的信用 |
|starter| $15/mo | 基本分配 |
| Plus | $34/mo | 中等级别，~33-56 Kling 3.0 片 |
| Ultra | $84/mo | 高量 |

**每个生成成本（大致，使用信用）：**

| 模型 | 每片成本 |
|-------|--------------|
| Kling 3.0 | ~$0.10（最便宜） |
| WAN 2.5 | ~$0.10 |
| Soul Cinema | ~$0.15 |
| Veo 3.1 | ~$0.50 |
| Sora 2 | ~$0.50 |

**免费计划:** 注册时有限制的信用。无需月度续费的免费计划。

---

### HeyGen — Avatar 视频门户

> **多模型视频门户。** 通过单个 API 访问 VEO, Sora, Runway, Kling, 和 Seedance。

**解锁的工具:** `heygen_video`
**环境变量:** `HEYGEN_API_KEY`

#### 设置

1. 访问 [app.heygen.com/register](https://app.heygen.com/register) 并创建账户
2. 在设置中导航到 API 部分
3. 生成 API 密钥
4. 添加 API 余额（预付费，分离于网页计划的信用）
5. 添加到 `.env`: `HEYGEN_API_KEY=your-key-here`

#### 价格

| 服务 | 价格 |
|---------|-------|
| Avatar 视频 (Engine III) | $0.017/秒 |
| Avatar 视频 (Engine IV) | $0.10/秒 |
| Prompt to Video | $0.033/秒 |
| 视频翻译 (速度) | $0.05/秒 |
| 视频翻译 (精确度) | $0.10/秒 |

**网页计划：**

| 计划 | 价格 | 注释 |
|------|-------|-------|
| 免费 | $0 | 1 个信用（演示） |
| Creator | $24/mo | 限制的信用 |
| Business | $72/mo | API 访问，更多信用 |

**免费计划:** 1 个信用在网页平台上。API 是按预付费余额支付的。

---

### Suno — AI 音乐生成

> **完整的歌曲，包括歌词和声乐。** 所有风格，最长 8 分钟。乐器轨或声乐轨。

**解锁的工具:** `suno_music`
**环境变量:** `SUNO_API_KEY`

#### 设置

1. 访问 [suno.com](https://suno.com) 并创建一个 Suno 账户
2. 为 API 访问，访问 [sunoapi.org](https://sunoapi.org) 并创建账户
3. 导航到控制台并复制 API 密钥
4. 添加信用（1 个信用 = $0.005 美元）
5. 添加到 `.env`: `SUNO_API_KEY=your-key-here`

#### 价格

**Suno 平台：**

| 计划 | 价格 | 信用 | 注释 |
|------|-------|---------|-------|
| 免费 | $0 | 50/天 | ~10 歌曲/天，仅非商业用途 |
| Pro | $10/mo | 2,500/mo | 商业许可证 |
| Premier | $30/mo | 10,000/mo | 商业许可证 |

**API（通过 sunoapi.org）：**按需支付，1 个信用 = $0.005。每个生成产生 2 个轨道。

---

### Pexels — 免费库存媒体

> **完全免费。** 无成本，无需归属，允许商业使用。

**解锁的工具:** `pexels_image`, `pexels_video`
**环境变量:** `PEXELS_API_KEY`

#### 设置

1. 访问 [pexels.com/join](https://www.pexels.com/join/) 并创建一个免费账户
2. 导航到 [pexels.com/api](https://www.pexels.com/api/)
3. 点击 **Your API Key** 或请求 API 访问
4. 从控制台复制密钥
5. 添加到 `.env`: `PEXELS_API_KEY=your-key-here`

#### 价格

**完全免费。** 没有付费等级。无需归属。允许商业使用。

- 每小时 200 请求
- 每月 20,000 请求
- 照片和视频搜索 + 下载

---

### Pixabay — 免费的图像和视频媒体

> **完全免费。** 5M+ 的无版权的图像和视频。

**解锁的工具：** `pixabay_image`, `pixabay_video`
**环境变量：** `PIXABAY_API_KEY`

#### 配置

1. 前往 [pixabay.com/accounts/register](https://pixabay.com/accounts/register/) 创建一个免费账户
2. 导航到 [pixabay.com/api/docs](https://pixabay.com/api/docs/)
3. 登录后，docs 页面顶部显示的 API 密钥
4. kopieren Sie den Schlüssel
5. 加入到 `.env`: `PIXABAY_API_KEY=your-key-here`

#### 价格

**完全免费。** 没有付费层次，没有需要的归属权。商业用途允许。

- ~100 请求/分钟
- 5,000 请求/小时
- 照片和视频搜索 + 下载
- 标准 API 限制为 1280 像素的图像（完整分辨率需要编辑器 API）

---

## 本地提供商（免费，无 API 密钥）

这些提供商完全运行在您的机器上。无需网络、无 API 密钥、无成本。某些需要显卡。

### Remotion — 计划性视频组合

> **基于 React 的视频渲染。** 将静态图像转换为带弹性物理学的动画视频，带有动画文本卡、统计卡、图表、过渡和动画。**这是配置没有视频生成提供商时的关键备选方案——代理生成图像并使用 Remotion 将其动画成专业的视频。**

**工具：** `video_compose`（带 `operation="render"` — 自动路由到 Remotion 当需要时）
**运行时：** CPU（Node.js 需要）
**环境变量：** 无

#### 配置

```bash
# Included in make setup, or install manually:
cd remotion-composer && npm install && cd ..
```

## 需要 **Node.js 18+** 和 `npx`。 `remotion-composer/` 项目包含在此repo中。

#### Remotion 何时渲染

| 元素 | 生产的内容 |
|------|---------|
| **TextCard** | spring physics entrance 的动画标题/主体文本 |
| **StatCard** | animated statistics 的 animated count-up animations |
| **ProgressBar** | animated progress indicators |
| **CalloutBox** | animated icon 的 callout panels |
| **ComparisonCard** | side-by-side comparison 的 layout |
| **BarChart / LineChart / PieChart** | animated data visualizations |
| **KPIGrid** | multi-metric dashboard cards |
| **Image scenes** | spring-animated motion 的 still images (替代 Ken Burns) |

#### Remotion 何时激活？

`video_compose` 工具的 `render` 操作自动检测 Remotion 是否需要：
- 切片包含静态图像 (`.png`, `.jpg` 等)
- 切片设置 `type` 为 `text_card`, `stat_card`, `chart` 等
- 切片指定 `animation` 或 `transition_in`/`transition_out`

如果 Remotion 没有安装，组合会退回到 FFmpeg Ken Burns pan-and-zoom — 功能性但不那么吸引人。

**成本:** 免费。始终本地。

---

### HyperFrames - HTML/CSS/GSAP 视频组合

> **GSAP-native 本地渲染。** HyperFrames 是 HTML 组合中重度使用动画图像的首选运行时和 `character-animation` 线框的特定 SVG 人物。

**工具:** `hyperframes_compose` 直接使用，或 `video_compose` 通过 `edit_decisions.render_runtime="hyperframes"`
**运行时:** CPU (Node.js >= 22, FFmpeg, 和 `npx` 需要)
**环境变量:** 无

#### 设置

```bash
node --version
ffmpeg -version
npx --yes hyperframes doctor
```The CLI is consumed as `npx hyperframes`. Do not use `npx @hyperframes/cli`; that package name is not the OpenMontage runtime path.

#### What HyperFrames Renders

| 用例 | 產生 |
|------|------|
| **动态文字** | 基於 GSAP 時軸駐蹔的 HTML/CSS文字動畫 |
| **產品 / 發行影片** | 構建好的 HTML 圧縮區塊、registry 核心和轉換 |
| **網站到影片** | 使用 HyperFrames 验證的瀏覽器捕捉的網站組成 |
| **角色動畫** | SVG 角色架構、POSE/ACTION 時軸和 GSAP 行動節拍，渲染到 `renders/final.mp4` |

HyperFrames 工作區域生活在 `projects/<project-name>/hyperframes/`。最終影片仍然遵循 OpenMontage 的常規： `projects/<project-name>/renders/final.mp4`。

**成本:** 免费。始终本地。

---

### Piper TTS — Offline Text-to-Speech

> **完全免費的全時機式 TTS。** 没有網絡需求。適合草稿和預算有限的項目。

**工具:** `piper_tts`
**運行時程:** CPU（不需要 GPU）
**環境變數:** 沒有

#### 配置

```bash
# Install via pip
pip install piper-tts

# Or download the binary from GitHub
# https://github.com/rhasspy/piper/releases

# Download a voice model (first run downloads automatically)
piper --download-dir ~/.piper/models --model en_US-lessac-medium
```**可用声音:** ~30 英语声音及德语、法语、西班牙语、意大利语等其他语言的声音。比云提供商少，但完全免费且无需联网。

**质量:** 用于草稿、内部视频和预算项目。对于面向客户的叙述，使用 ElevenLabs 或 Google TTS。

---

### ComfyUI 视频 — 本地工作流程和合作伙伴节点

**工具:** `comfyui_video`

**可选环境变量:** `COMFYUI_SERVER_URL`（默认值为`http://localhost:8188`）和 `COMFYUI_VIDEO_SERVER_URL`（视频特定的超时）。

Bundled WAN 2.2 工作流程和来自调用者的本地工作流程在 ComfyUI 机器上执行。MiniMax H3 是一个官方的开放权本地工作流程；使用 export 以 API 格式的官方工作流程（`workflow_json` 或 `workflow_path`），以及其 `output_node`。

MiniMax H3 本地堆栈包括 prune INT8 传播模型、Qwen3-VL 文本编码器、视频 VAE 和音频 VAE。OpenMontage 公开了官方下载的 URL 和目的目录，而不是默默地下载大模型。

该工具还支持 ComfyUI 的合作伙伴节点：

| `model_family` | 节点 | 执行 | 大致成本 |
|----------------|------|-----------|------------------|
| `gemini_omni_flash`（过时预览） | `GeminiVideoOmni` | 由合作伙伴节点远程执行；与稳定的直接 `gemini_omni_video` 适配器分开 | 每秒约 $0.146 |
| `seedance_2.5` | `ByteDance2TextToVideoNode` | 由合作伙伴节点远程执行 | 每秒约 $0.148（480p）；每秒约 $0.333（720p） |
| `minimax_h3_api` | `MinimaxHailuo03TextToVideoNode` | 由合作伙伴节点远程执行 | 每秒约 $0.129（768P）；每秒约 $0.186（2K） |
| `minimax_h3_local` | 官方 MiniMax H3 图形 | 本地 GPU | 无 APIcharges |

合作伙伴节点不是本地化的：它们需要当前的 ComfyUI、网络访问、登录的 Comfy 账户和预付费信用。价格是从 Comfy kredits（211 kredits = $1）的估算转换；实际计费的使用量是最终的。

官方参考：[合作伙伴节点概述](https://docs.comfy.org/tutorials/partner-nodes/overview)，[价格](https://docs.comfy.org/tutorials/partner-nodes/pricing)，和
[MiniMax H3 本地教程](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)。

---

### 本地视频生成（GPU 需要）

> **免费 AI 视频生成。** 需要一个具有足够 VRAM 的 NVIDIA GPU。

**工具:** `wan_video`, `hunyuan_video`, `cogvideo_video`, `ltx_video_local`
**运行时间:** 本地 GPU（CUDA 需要）
**环境变量:** `VIDEO_GEN_LOCAL_ENABLED=true`, `VIDEO_GEN_LOCAL_MODEL=<model>`

#### 设置

```bash
# 1. Install the GPU stack
make install-gpu
# Or manually:
pip install diffusers transformers accelerate torch pillow requests

# 2. Enable local generation in .env
VIDEO_GEN_LOCAL_ENABLED=true

# 3. Choose a model based on your GPU VRAM
VIDEO_GEN_LOCAL_MODEL=wan2.2-ti2v-5b   # 12GB+ VRAM (default; 720p @ 24fps, T2V+I2V+V2V)
VIDEO_GEN_LOCAL_MODEL=wan2.1-1.3b      # 6GB+ VRAM (entry-level, text-to-video only)
VIDEO_GEN_LOCAL_MODEL=wan2.1-14b       # 24GB+ VRAM (best Wan 2.1 quality)
VIDEO_GEN_LOCAL_MODEL=hunyuan-1.5      # 12GB+ VRAM
VIDEO_GEN_LOCAL_MODEL=ltx2-local       # 8GB+ VRAM (fastest)
VIDEO_GEN_LOCAL_MODEL=cogvideo-5b      # 10GB+ VRAM
VIDEO_GEN_LOCAL_MODEL=cogvideo-2b      # 6GB+ VRAM (lightest)
```

#### 模型比较

| 模型 | VRAM | 品质 | 速度 | 最适用 |
|------|------|------|------|------|
| **WAN 2.2 TI2V (5B)** | 12GB | 优秀 | 中等 | 默认。720p @ 24fps，T2V/I2V/V2V的一个检查点 |
| **WAN 2.1 (1.3B)** | 6GB | 好 | 快速 | 入门级GPU，快速迭代（文本到视频） |
| **WAN 2.1 (14B)** | 24GB | 优秀 | 慢 | Wan 2.1的最佳质量 |
| **Hunyuan 1.5** | 12GB | 非常好 | 中等 | 中等GPUs |
| **LTX-2** | 8GB | 好 | 最快 | 快速草稿，最低延迟 |
| **CogVideo (5B)** | 10GB | 好 | 中等 | 平衡选项 |
| **CogVideo (2B)** | 6GB | 平庸 | 快速 | 低VRAM实验 |

**所有本地模型支持：** 文本到视频，离线生成，重现性。

#### WAN 2.2 — 全局操作矩阵

`wan_video`驱动Wan任务中的每个检查点。`operation`输入选择了diffusers的流派；工具拒绝执行该选择的流派没有权重。

| `operation` | 作用 | 附加输入 |
|-------|------|---------|
| `text_to_video` | 按照剪辑 | — |
| `image_to_video` | 动画静态 | `reference_image_path` / `reference_image_url` |
| `video_to_video` | 重塑现有的剪辑 | `source_video_path`, `strength` |
| `first_last_frame` | 两个静态之间的插值 | `reference_image_*` + `last_image_*` |
| `text_to_image` | 单个帧，保存为PNG | — |

几何被捕捉到VAE可以编码的范围内，所以你可以要求任何尺寸：帧数落在`4k + 1`，宽度/高度落在TI2V线的32倍（其16x VAE + 2x修补是为什么720p是**1280x704**，不是1280x720）或其他地方。

#### 长于五秒的剪辑

Wan被训练为大约五秒的通行。用`duration_seconds`请求更多内容，工具链会将每个延续段落：每个延续段落的最后一个帧作为其自己的帧0重新生成，并在接缝处删除该副本。```python
wan_video.execute({
    "prompt": "A red convertible on a coastal road at golden hour",
    "duration_seconds": 30,          # -> 720 frames @ 24fps -> 6 chained segments
    "width": 704, "height": 480,
    "num_inference_steps": 20,
    "offload_mode": "sequential",
    "segment_prompts": [...],        # optional shot list, one entry per segment
})
```Chaining drifts: every hop conditions on already-generated pixels, so contrast and colour
`correct_drift` (on by default) re-grades each segment to the opening segment's
channel statistics. Pass `segment_prompts` to steer the clip through a shot list instead of
repeating one prompt six times.

#### Fitting a 12GB card

`precision` (`auto`/`bf16`/`int8`/`int4`) and `offload_mode` (`auto`/`model`/`sequential`)
both default to `auto` and are picked from visible VRAM.

A bf16 5B transformer is ~10GB resident. With `offload_mode="model"` that leaves almost
nothing for activations on a 12GB card — measured peak was 10.85GB at just 512x320.
`offload_mode="sequential"` streams one submodule at a time: the same card then peaks at
**1.97GB** and renders 704x480 comfortably, at the cost of ~4s per denoising step of PCIe
traffic. On a 12GB GPU `auto` selects it for you.

> **NVIDIA driver note.** If the loaded kernel module and the installed userspace libraries
> are different versions, `nvmlInit` fails. CUDA compute still runs, but PyTorch calls NVML
> while composing an out-of-memory report — so real OOMs surface as an internal assert, and
> bitsandbytes (`int8`/`int4`) cannot load at all. Compare `cat /proc/driver/nvidia/version`
> with `nvidia-smi`; if they disagree, reboot. `wan_video` detects this and says so.

Image-to-video is *not* universal — Wan 2.1 never shipped 1.3B I2V weights and CogVideo is
text-only. Each variant's real capability list is `operations` in `tools/video/_shared.py`,
and `wan_video` refuses an operation the selected checkpoint cannot do.

---

### Local Diffusion — Offline Image Generation (GPU Required)

> **Free Stable Diffusion image generation.** No API cost, fully offline.

**Tool:** `local_diffusion`
**Runtime:** Local GPU (CUDA required)
**Env var:** None (enable by installing dependencies)

#### Setup

```bash
pip install diffusers transformers accelerate torch
```第一次运行下载模型（约4GB）。后续运行使用缓存模型。

**VRAM需求：** 4GB+（推荐8GB用于1024x1024像素）

**支持：** 降低提示、种子、定制尺寸。质量低于FLUX或GPT Image 2，但完全免费且无需网络。

---

### LTX-2 on Modal — 自主云GPU

> **运行LTX-2 on Modal的云GPU。** 你的自己的端点，自己的规模。比本地GPU更一致，便宜于商业API。

**工具：** `ltx_video_modal`
**运行时间：** 云（自主）
**环境变量：** `MODAL_LTX2_ENDPOINT_URL`

#### 设置

1. 创建一个[Modal](https://modal.com)账户
2. 部署LTX-2端点（参见Modal文档）
3. 将端点URL设置在`.env`: `MODAL_LTX2_ENDPOINT_URL=https://your-modal-endpoint`

**Modal定价：** 每小时大约0.99美元用于A100 GPU时间。视频生成时间的成本取决于视频生成时间。

---

### 其他本地工具（总是可用）

这些工具只需要FFmpeg或Python包 — 无需GPU、无需API密钥。

| 工具 | 安装 | 该工具做什么 |
|------|---------|-------------|
| **FFmpeg工具**（视频组合、视频拼接、视频裁剪、音频混音、音频增强、颜色校准、面部增强、帧采样器、场景检测） | `brew install ffmpeg` / `sudo apt install ffmpeg` / `winget install FFmpeg` | 视频编辑、音频处理、颜色校准、分析 |
| **转录器** | `pip install faster-whisper` | 语音转文字，单词级别时间戳 |
| **背景移除** | `pip install rembg`（CPU）或 `pip install rembg[gpu]` | 移除图片/视频背景 |
| **增强** | `pip install realesrgan`（需要PyTorch + CUDA） | RealesRGAN图像/视频增强 |
| **面部恢复** | `pip install gfpgan`（需要PyTorch） | CodeFormer/GFPGAN面部恢复 |
| **代码片段** | `pip install Pygments Pillow` | 语法高亮的代码图像 |
| **图表生成** | `npm install -g @mermaid-js/mermaid-cli` | Mermaid图表生成 |
| **数学动画** | `pip install manim` | ManimCE数学动画 |
| **字幕生成** | 无安装需要 | SRT/VTT字幕文件生成 |
| **视频理解** | `pip install transformers torch` | CLIP/BLIP-2视觉分析 |
| **说话头** | 克隆[SadTalker](https://github.com/OpenTalker/SadTalker) | 基于照片+音频的头像动画 |
| **同步嘴巴** | 克隆[Wav2Lip](https://github.com/Rudrabha/Wav2Lip) | 音频驱动嘴巴同步 |

---

## 提供者到工具映射

| 提供者 | 环境变量 | 工具解锁 | 成本 |
|----------|---------|---------------|------|
| **Pexels** | `PEXELS_API_KEY` | `pexels_image`, `pexels_video` | 免费 |
| **Pixabay** | `PIXABAY_API_KEY` | `pixabay_image`, `pixabay_video` | 免费 |
| **Piper** | —（仅安装） | `piper_tts` | 免费 |
| **Azure AI Speech** | `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` | `azure_stt`, `azure_tts` | 免费版 + 付费 |
| **Google** | `GOOGLE_API_KEY`（或 `GEMINI_API_KEY`） | `google_tts`, `google_imagen`, `google_music`, `gemini_omni_video`, `veo_video` | 免费版（TTS） + 付费 |
| **ElevenLabs** | `ELEVENLABS_API_KEY` | `elevenlabs_tts`, `music_gen` | 免费版 + 付费 |
| **fish.audio** | `FISH_AUDIO_API_KEY` | `fish_audio_tts` | 免费版（s2.1-pro-free） + 付费 |
| **fal.ai** | `FAL_KEY` | `flux_image`, `recraft_image`, `kling_video`, `veo_video`, `seedance_video`, `gemini_omni_fal`, `minimax_fal_video` | 付费使用 |
| **Atlas Cloud** | `ATLASCLOUD_API_KEY` | `atlas_image`, `atlas_video` | 付费使用 |
| **Kling Official** | `KLING_API_KEY` | `kling_official_video`, `kling_official_image`, `kling_tts`, `kling_avatar`, `kling_lip_sync` | 付费使用 |
| **Volcengine Ark** | `ARK_API_KEY` | `seedance_ark` | 付费使用 |
| **MiniMax direct** | `MINIMAX_API_KEY` | `minimax_image`, `minimax_video` | Pay-as-you-go |
| **OpenAI** | `OPENAI_API_KEY` | `openai_tts`, `openai_image` | Paid only |
| **xAI** | `XAI_API_KEY` | `grok_image`, `grok_video` | Paid only |
| **Runway** | `RUNWAY_API_KEY` | `runway_video` | Free trial + paid |
| **Higgsfield** | `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` | `higgsfield_video` | Subscription ($15-84/mo) |
| **HeyGen** | `HEYGEN_API_KEY` | `heygen_video` | Pay-as-you-go |
| **Suno** | `SUNO_API_KEY` | `suno_music` | Pay-as-you-go |
| **Tencent Hunyuan** | `TENCENT_TOKENHUB_API_KEY` | `hunyuan_cloud_video` | Pay-as-you-go (~$0.25–0.83/gen) |
| **Local GPU** | `VIDEO_GEN_LOCAL_ENABLED` | `wan_video`, `hunyuan_video`, `cogvideo_video`, `ltx_video_local` | Free (GPU required) |
| **Local Diffusion** | — (install only) | `local_diffusion` | Free (GPU required) |
| **Modal** | `MODAL_LTX2_ENDPOINT_URL` | `ltx_video_modal` | Self-hosted cloud |
| **ComfyUI** | optional server URL overrides | `comfyui_video` | Local GPU, or paid Partner Node credits |

---

## 具备能力覆盖

每个能力的供应商覆盖情况：

| 能力 | 云供应商 | 本地供应商 | 免费选项 |
|------|--------|--------|--------|
| **图像生成** | FLUX, Kling 官方, Grok, Google Imagen, GPT Image 2, Recraft | 本地 Diffusion | Pexels, Pixabay (库存) |
| **视频生成** | Grok, Kling 官方, fal.ai, Seedance via Volcengine Ark, Runway, Veo, Gemini Omni, Higgsfield, MiniMax, HeyGen, Tencent Hunyuan, ComfyUI Partner Nodes | WAN, Hunyuan, CogVideo, LTX, ComfyUI WAN, ComfyUI MiniMax H3 | Pexels, Pixabay (库存) |
| **文本到语音** | Azure AI Speech, ElevenLabs, fish.audio, Google TTS, Kling 官方, OpenAI | Piper | Piper, Google free tier, ElevenLabs free tier, Azure free tier, fish.audio s2.1-pro-free |
| **音乐生成** | ElevenLabs, Suno, Google Lyria | — | ElevenLabs free tier |
| **后期制作** | — | FFmpeg (组合、拼接、裁剪、混合、增强、校准) | 所有免费 |
| **分析** | — | WhisperX, Scene Detect, Frame Sampler, CLIP/BLIP-2 | 所有免费 |
| **增强** | — | Upscale, BG Remove, Face Enhance, Face Restore | 所有免费 |
| **头像** | Kling 官方 | SadTalker, Wav2Lip | 本地工具免费 |

---

## 常见问题解答

**Q: 我需要多少东西才能制作视频？**
A: FFmpeg + Node.js (两者都是免费，本地)。FFmpeg处理视频组装、音频混合和字幕。使用 Node.js，Remotion将静态图像转换为动画视频——即使没有任何视频生成API，代理生成图像，Remotion将它们转化为专业的视频，配有弹簧动画、文本卡片和过渡。添加 Piper TTS以免费叙述和Pexels/Pixabay以免费库存素材。

**Q: 我没有任何视频生成供应商。还可以制作视频吗？**
是的。代理生成静态图像（使用任何图像提供商——包括免费Pexels/Pixabay）并将其编入Remotion使用弹性物理过渡、文本卡、统计卡和图表的动画视频中。这是当没有视频生成配置时的默认路径，对于解释和动画流程。

**Q: 有一种低阻碍的方式来获取AI生成的图像和视频吗？**
A: fal.ai (`FAL_KEY`) 是一种付费使用的选项，具有广泛的单键覆盖。它解锁了FLUX图像以及多个视频提供商。无需订阅——只需为生成支付费用。

**Q: 我有一个GPU。要在本地免费运行什么？**
A: 设置`VIDEO_GEN_LOCAL_ENABLED=true`并安装`diffusers`。你将获得WAN 2.1、Hunyuan、CogVideo和LTX视频生成以及Stable Diffusion图像生成——所有免费且都可以在本地运行。

**Q: 哪个TTS提供商我应该使用？**
A: 对于质量 → ElevenLabs。对于多语言（50+语言）→ Google TTS。对于预算 → Google免费版（每月1M个字符）。对于离线 → Piper。

**Q: 我需要所有这些提供商吗？**
A: 不需要。先从你有的开始。选择器模式自动将流量路由到可用的任何东西。如果缺少一个提供商，系统会自动落到下一个提供商。

## 2026年10月23日的添加和迁移

请参阅[当前整合指南](../.agents/skills/provider-refresh-oct23/SKILL.md)以获取精确的工具/模型/主机选择、设置、限制和主要来源。

添加了HeyGen Voice1/Turbo/Free和目录TTS、时序保留的HeyGen语音转换、xAI语音生成TTS、Voxtral3 TTS/STT、MAI Voice2.1/Flash、ElevenLabs视频配乐、Nano Banana2.1（Google/fal/Replicate）、FLUX3图像（BFL/fal/Replicate）、FLUX3 Max视频(fal)、Vidu Q4（fal）、Grok Imagine1.5/Lite、Fibo2（Bria/fal）、MAI图像2.6/Flash，以及用于Grok语音3、Eleven Realtime Mini/Max和MAI实时转录的单独实时传输。没有Kling4或实时翻译的整合。

Gemini Omni使用gemini-omni-1.1-flash。Gemini Veo/Imagen调用失败，迁移指导已提供；Vertex和聚合路由处理独立。

Eleven v4现在使用对话合同，Turbo使用其WebSocket传输。新提供商的可用性基于凭证，而不是实时的授权检查。定价需要当前报价，除非Explicitly dated HeyGen免费促销。