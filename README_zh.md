<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/monty-dark.svg">
    <img src="assets/monty-light.svg" alt="Monty the Clapper — OpenMontage 官方吉祥物" width="200">
  </picture>
</p>

<p align="center"><sub><em>Monty the Clapper — OpenMontage 官方吉祥物</em></sub></p>

<h1 align="center">OpenMontage</h1>

<p align="center"><strong>首个开源、Agent 驱动的视频制作系统。</strong></p>

<p align="center">
  <a href="https://openmontage.video"><img src="https://img.shields.io/badge/Website-openmontage.video-d14a28?style=for-the-badge" alt="openmontage.video"></a>
</p>

<p align="center">
  <a href="#start-from-a-video-you-already-love">粘贴参考视频</a> &nbsp;·&nbsp;
  <a href="#quick-start">快速开始</a> &nbsp;·&nbsp;
  <a href="#try-these-prompts">示例提示词</a> &nbsp;·&nbsp;
  <a href="#pipelines">流水线</a> &nbsp;·&nbsp;
  <a href="#how-it-works">工作原理</a> &nbsp;·&nbsp;
  <a href="docs/PROVIDERS.md">服务商</a> &nbsp;·&nbsp;
  <a href="docs/PR_REVIEW_GUIDE.md">评审指南</a> &nbsp;·&nbsp;
  <a href="AGENT_GUIDE.md">Agent 指南</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPLv3-blue.svg" alt="许可证"></a>
</p>

<p align="center">
  <a href="https://github.com/trending">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset=".github/assets/repo-of-the-day-dark.svg">
      <img alt="🏆 #1 Repository of the Day on GitHub Trending" src=".github/assets/repo-of-the-day-light.svg" height="60">
    </picture>
  </a>
</p>

<p align="center"><strong>关注开发进展</strong></p>

<p align="center">
  <a href="https://www.youtube.com/@OpenMontage"><img src="https://img.shields.io/badge/YouTube-%40OpenMontage-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
  <a href="https://x.com/calesthioailabs"><img src="https://img.shields.io/badge/X-%40calesthioailabs-111111?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
  <a href="https://github.com/calesthio/OpenMontage/discussions"><img src="https://img.shields.io/badge/Community-GitHub%20Discussions-0b1220?style=for-the-badge&logo=github&logoColor=white" alt="GitHub 讨论"></a>
</p>

---

> **新事物正在成形。**
>
> 我们正在为创作者打造全新工具，并寻找愿意早期尝鲜的伙伴。
>
> **[感兴趣？先睹为快并加入早期用户。](https://github.com/calesthio/OpenMontage/discussions/892)**

把你的 AI 编程助手变成完整的视频制作工作室。用自然语言描述需求——Agent 负责调研、写稿、资产生成、剪辑与最终合成。

**重要区别：** OpenMontage 既能做基于图像的视频，也能在免费/开源工作流中产出真正的**动态视频**：Agent 从免费素材库与开放档案构建语料库，检索真实运动镜头，剪辑成时间线并渲染成片。这不是常见的「给几张静图加 Ken Burns 就称视频」的做法。

<div align="center">
  <video src="https://github.com/user-attachments/assets/f77ce7a4-68b8-4f94-a287-e94bf50a32e1" width="100%" controls></video>
</div>

> **「SIGNAL FROM TOMORROW」** — 经 OpenMontage 全流程制作的科幻电影预告：概念、剧本、场景规划、Veo 生成的动态片段、配乐与 Remotion 合成。

<div align="center">
  <video src="https://github.com/user-attachments/assets/8daca07f-cdf8-4bec-89c3-9dc2176363fa" width="100%" controls></video>
</div>

> **「THE LAST BANANA」** — 60 秒皮克斯风格动画短片：孤独的香蕉与猕猴桃成为朋友。6 段 Kling v3 动态片段（经 fal.ai）、Google Chirp3-HD 旁白、免版税钢琴曲、TikTok 式逐词字幕与 Remotion 合成。总成本：**$1.33**。

<div align="center">
  <video src="https://github.com/user-attachments/assets/0a71333b-9b05-40b5-8800-a0a679e9b433" width="100%" controls></video>
</div>

> **「OBJECTS IN OVERDRIVE」** — 54 秒音乐驱动的 3D 展示，十件物体各自编舞：重力变幻的家具、定格漂移的汽车、布料撞击、折射镜头、运转齿轮、杂技机器人等。Blender 定制动画与物理、 kinetic typography 与 phonk 配乐；Eevee/Cycles 渲染，FFmpeg 组装。无旁白。

<div align="center">
  <video src="https://github.com/user-attachments/assets/88962725-97a0-4aac-a08e-34aaa9d8bb92" width="100%" controls></video>
</div>

> **「Reimagine Your Universe」** — 50 秒竖屏变形片：同一视觉概念跨越物体、时代、材质与尺度。五段生成动态场景、稀疏 Google Chirp 旁白、Pixabay 配乐与定制 HyperFrames 合成，将片段连成一条完整电影旅程。总成本：**约 $4**。

<div align="center">
  <video src="https://github.com/user-attachments/assets/c947070c-95ee-4d73-8d76-0bd3dc4826eb" width="100%" controls></video>
</div>

> **「Products Come to Life」** — 60 秒产品片，基于已批准的主视觉静帧。五件硬表面产品拆解再组装；每帧静图锁定首尾帧，模型在保持产品识别度的前提下发明运动。图生视频、定制音效、旁白与定制合成完成成片。

<div align="center">
  <video src="https://github.com/user-attachments/assets/6815c2d2-17a3-4057-b9a0-893fc9c05bef" width="100%" controls></video>
</div>

> **「Imagine the Possibilities with OpenMontage」** — 七个生成世界汇成纯音乐 showcase。三款图像模型提供 campaign、时尚与微缩世界画面；四款视频模型延展建筑、材质变换、活体温室与生物遭遇。OpenMontage 动画化静帧、剪辑动态、统一配乐并以 Monty the Clapper 收尾。源生成成本：**约 $5**。

<div align="center">
  <video src="https://github.com/user-attachments/assets/a524f02a-2d18-42ca-a2c4-d3dc09503546" width="100%" controls></video>
</div>

> **「How Salt Made History」** — 100 秒电影感纪录片：盐如何资助帝国、塑造贸易路线、点燃革命并诞生 “salary” 一词。真实镜头与原创旁白、手工 motion graphics（蚀刻标题、词源揭示、动画地图、历史时间线与收束论点）交织而成。

<div align="center">
  <video src="https://github.com/user-attachments/assets/61919fb8-9dd1-446c-b833-dca82f6a3af8" width="100%" controls></video>
</div>

> **「One Prompt Built This Complete 3D World」** — 连续 60 秒穿越同一连贯、可编辑的奇幻世界：不同地貌、有人居住的村落、水道、废墟、密林与后期英雄地标揭示，由带纹理 3D 资产组装，配合电影级光照、氛围音乐与规划镜头路径。

<p align="center">
  <a href="https://www.youtube.com/@OpenMontage?sub_confirmation=1"><strong>订阅 YouTube @OpenMontage</strong></a> 以获取新片上线通知——每条视频都附带完整提示词、流水线、所用工具与成本，便于自行复现。
</p>

---

## 从你已喜欢的视频开始 {#start-from-a-video-you-already-love}

从参考视频入手，往往比空白提示词更快。

OpenMontage 可从 **YouTube 视频、Short、Reel、TikTok 或本地片段** 出发，生成可落地的制作计划：

1. **粘贴参考视频**
2. **Agent 分析转录、节奏、场景、关键帧与风格**
3. **获得 2–3 个差异化概念、诚实的工具路径、成本估算，以及全量制作前的样片**

```text
"Here's a YouTube Short I love. Make me something like this, but about quantum computing."
```

回报的不是「猜提示词大杂烩」，而是：

- **从参考中保留什么**：节奏、钩子风格、结构、语气
- **会改什么**：主题、视觉处理、角度、旁白方式
- **目标时长下的成本**，在资产生成开始前即给出
- **在你当前可用工具下实际会长什么样**

适用于 **Claude Code、Cursor、Copilot、Windsurf、Codex** 等能读文件并运行代码的 AI 编程助手。

---

## 亲眼见证 — Backlot 动态分镜板 {#watch-it-happen--the-backlot-living-storyboard}

聊天窗口告诉你 Agent *说了什么*。**Backlot 展示制作实际在做什么** — 本地看板随流水线运行自动填充：阶段亮起、剧本以 screenplay 页呈现、场景卡在资产生成时闪烁，每个服务商决策与花费都上墙。

制作开始时 Agent 会自动为你打开。无需额外配置或汇报 — 看板数据全部来自流水线已写入的项目文件。

<p align="center"><img src="docs/images/backlot/board-live.png" alt="Backlot 实时看板 — 资产生成中" width="920"></p>

**分镜板已是真正的审批关卡。** 资产生成会在逐场景 contact sheet 上暂停 — 镜头、提示词、单资产成本、质量分 — 让你在渲染*之前*批准画面，而非事后补救：

<p align="center"><img src="docs/images/backlot/storyboard.png" alt="Backlot 分镜 — 含镜头与渲染的胶片条" width="920"></p>

创意关卡会等待你的回复。看板展示等待项与原因；你在聊天中回应：

<p align="center"><img src="docs/images/backlot/script-gate.png" alt="Backlot 剧本门 — 等待批准" width="920"></p>

本机所有制作项目，以 live-first 方式集中在库中：

<p align="center"><img src="docs/images/backlot/library.png" alt="Backlot 项目库" width="920"></p>

```bash
python -m backlot open                  # the library — every project on disk
python -m backlot open <project-id>     # one production's live board
python scripts/backlot_simulate_run.py  # no production yet? watch a simulated one live
```

运行结束后点击 **▶ REPLAY RUN** — 整次制作按时间戳从头到尾可 scrub 回放。详见 [`backlot/README.md`](backlot/README.md)（英文）。

---

## 快速开始 {#quick-start}

### 前提条件

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **FFmpeg** — `brew install ffmpeg` / `sudo apt install ffmpeg` / [ffmpeg.org](https://ffmpeg.org/download.html)
- **Node.js 18+** — [nodejs.org](https://nodejs.org/)
- **AI 编程助手** — Claude Code、Cursor、Copilot、Windsurf 或 Codex

### 安装与运行

```bash
git clone https://github.com/calesthio/OpenMontage.git
cd OpenMontage
make setup
```

在 AI 编程助手中打开项目并说明需求：

```
"Make a 60-second animated explainer about how neural networks learn"
```

若要走真实素材路径：

```text
"Make a 75-second documentary montage about city life in the rain. Use real footage only, no narration, elegiac tone, with music."
```

仅此而已。Agent 会通过实时网页搜索调研主题、生成 AI 图像、按声音指导撰写并旁白剧本、自动寻找免版税背景音乐、烧录逐词字幕并渲染成片。在你看到结果前，系统会进行多点自审 — ffprobe 校验、抽帧、电平分析、交付承诺核对与字幕检查。每个服务商选择在 7 个维度上打分并记入可审计决策日志。每个创意决策都需你批准。

> **没有 `make`？** macOS/Linux：`python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt && cd remotion-composer && npm install && cd .. && python -m pip install piper-tts && cp .env.example .env`
>
> Windows PowerShell：`py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt; cd remotion-composer; npm install; cd ..; python -m pip install piper-tts; Copy-Item .env.example .env`
>
> **Windows：** 若 `npm install` 报 `ERR_INVALID_ARG_TYPE`，请改用 `npx --yes npm install`。

### 如果你是正在阅读本文的 OpenClaw Agent，恭喜：你可能已通过图灵测试

本仓库为 Agent 化运行而设计。若是 OpenClaw 类 Agent，最快上手路径如下：

1. **先读契约**
   从 [`AGENT_GUIDE.md`](AGENT_GUIDE.md) 开始，再读 [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)。
2. **不要即兴制作流程**
   OpenMontage 由流水线驱动。真实工作经 `pipeline_defs/`、`skills/pipelines/` 中的阶段导演技能，以及 registry 工具发现完成。
3. **核对实际能力边界**
   运行：
   ```bash
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"
   ```
4. **把每个视频请求当作流水线选型问题**
   先选对流水线，再读 manifest，再读阶段技能，再调用工具。

### 添加 API Key（可选 — Key 越多工具越多）

```bash
# .env — every key is optional, add what you have

# Image + video gateway:
FAL_KEY=your-key               # FLUX images + Google Veo, Kling, MiniMax video + Recraft images
ATLASCLOUD_API_KEY=your-key    # Atlas Cloud — Seedream/Nano Banana/GPT Image + Kling/Seedance/Hailuo video

# Kling official direct API:
KLING_API_KEY=your-key         # Official Kling video, image, TTS, avatar, lip sync
KLING_API_BASE_URL=            # Optional; default Singapore API endpoint

# Free stock media:
PEXELS_API_KEY=your-key        # Free stock footage and images
PIXABAY_API_KEY=your-key       # Free stock footage and images
UNSPLASH_ACCESS_KEY=your-key   # Free stock images

# Music:
SUNO_API_KEY=your-key          # Full songs, instrumentals, any genre

# Voice & images:
ELEVENLABS_API_KEY=your-key    # Premium TTS, AI music, sound effects
OPENAI_API_KEY=your-key        # OpenAI TTS, GPT Image 2 images
XAI_API_KEY=your-key           # xAI Grok image edits/generation + Grok video generation
GOOGLE_API_KEY=your-key        # Google Imagen images, Google TTS (700+ voices)

# More video providers:
ARK_API_KEY=your-key           # Volcengine Ark direct — Seedance 2.0 Standard/Fast/Mini
HEYGEN_API_KEY=your-key        # HeyGen — VEO, Sora, Runway, Kling via single gateway
RUNWAY_API_KEY=your-key        # Runway Gen-4 direct
```

<details>
<summary><strong>有 GPU？解锁免费本地视频生成</strong></summary>

```bash
make install-gpu

# Then add to .env:
VIDEO_GEN_LOCAL_ENABLED=true
VIDEO_GEN_LOCAL_MODEL=wan2.2-ti2v-5b  # or wan2.1-1.3b, wan2.1-14b, hunyuan-1.5, ltx2-local, cogvideo-5b
```

</details>

---

## 零 API Key 也能做什么

无需付费 API Key 即可制作真实视频。`make setup` 开箱即用提供：

| 能力 | 免费工具 | 作用 |
|-----------|-----------|-------------|
| **旁白** | Piper TTS | 免费离线 TTS — 接近真人的旁白 |
| **开放素材** | Archive.org + NASA + Wikimedia Commons | 免费/开放档案镜头、教育媒体与纪录片质感 |
| **额外素材库** | Pexels + Unsplash + Pixabay | 免费图库/视频（开发者 Key 可免费申请） |
| **合成（React）** | Remotion | 基于 React 的渲染 — spring 动画图像场景、文字卡、数据卡、图表、TikTok 式逐词字幕、TalkingHead |
| **合成（HTML/GSAP）** | HyperFrames | HTML/CSS/GSAP 渲染 — kinetic typography、产品 promo、launch reel、registry 块、website-to-video、SVG 角色 rig 动画 |
| **后期** | FFmpeg | 编码、字幕烧录、混音、调色 |
| **字幕** | 内置 | 自动生成带逐词时间轴的字幕 |

OpenMontage 在提案阶段在 Remotion 与 HyperFrames 间选型（锁定为 `render_runtime`）。数据驱动讲解与现有 React 场景栈默认 Remotion；天然适合 HTML + GSAP 的重 motion graphics 简报（含 `character-animation` 流水线的 SVG/GSAP rig 输出）默认 HyperFrames。完整决策矩阵见 `skills/core/hyperframes.md`。

**两条「近乎免费」路径：**

- **基于图像的视频：** Piper 旁白剧本，图像提供画面，Remotion 动画化为 polished 剪辑。
- **本地角色动画：** SVG rig、姿势库、GSAP 时间轴，HyperFrames 渲染卡通表演至 `projects/<project-name>/renders/final.mp4`。
- **真实素材视频：** documentary montage 流水线从 Archive.org、NASA、Wikimedia Commons 及可选 Pexels/Unsplash 等构建 CLIP 可检索语料库，再剪辑真实运动镜头成成片。

若要第三条，请在提示中要求 **documentary montage**、**tone poem** 或 **stock-footage collage**，并明确 **use real footage only**。

---

## 试试这些提示词 {#try-these-prompts}

安装完成后复制任一条到 AI 编程助手。每条都会跑完整制作流水线。

### 从参考视频开始

> 「这条 YouTube Short 我很喜欢。做一条类似的，但主题是面向高中生的 CRISPR。」

> 「分析这条 Reel，给我 3 个可用于自家产品发布的原创变体。」

> 「我喜欢这条视频的节奏和钩子。保持这种能量，改成 45 秒关于黑洞的讲解片。」

### 无需 Key

> 「做一条 45 秒动画讲解：天空为什么是蓝的。」

> 「做一条 60 秒互联网史视频，带旁白与字幕。」

> 「做一条数据驱动的全球咖啡消费讲解片。」

### 免费真实素材纪录片路径

> 「做一条 90 秒纪录片蒙太奇：凌晨 4 点的城市感受。仅真实素材、无旁白、挽歌式语气。」

> 「做一条 60 秒 Adam Curtis 风格档案拼贴：1950 年代消费乐观主义。优先 Archive.org 与 Wikimedia 素材。」

> 「用仅真实库存素材剪一条雨中回家的梦感蒙太奇。要音乐，不要旁白。」

### 已配置图像/视频服务商（约 $0.15–$1.50）

> 「做一条 30 秒吉卜力风格动画：黄金时刻云中漂浮的魔法图书馆。」

> 「做一条 30 秒动漫风动画：水下神殿、生物发光珊瑚与古代遗迹。」

> 「做一条 CRISPR 基因编辑动画讲解，使用 AI 生成画面。」

> 「为虚构智能水杯 AquaPulse 做产品发布 teaser。」

### 完整配置（约 $1–$3）

> 「做一条 30 秒电影感科幻预告：人类收到来自一千年后的警告。」

> 「做一条 90 秒面向初中生的量子计算动画讲解，有趣旁白音色与定制配乐。」

想要更多？完整 **[提示词画廊](PROMPT_GALLERY.md)** 含实测提示词、预期成本与输出示例；或运行 `make demo` 即时渲染零 Key 演示视频。

---

## 流水线 {#pipelines}

每条流水线都是从创意到成片的完整制作工作流。

| 流水线 | 产出 | 适用场景 |
|----------|-----------------|----------|
| **Animated Explainer** | 含调研、旁白、画面、音乐的 AI 讲解片 | 教育、教程、主题拆解 |
| **Animation** | Motion graphics、kinetic typography、动画序列 | 社交媒体、产品 demo、抽象概念 |
| **Avatar Spokesperson** | 虚拟形象主讲视频 | 企业沟通、培训、公告 |
| **Cinematic** | 预告、teaser、情绪向剪辑 | 品牌片、预告、推广 |
| **Clip Factory** | 从长源批量生成排序后的短视频 | 长内容拆条发社交 |
| **Documentary Montage** | 从 CLIP 索引的免费素材与开放档案（Pexels、Archive.org、NASA、Wikimedia、Unsplash）剪出的主题蒙太奇 | 视频 essay、情绪片、检索优先 B-roll、无需付费生成 API 的真实素材片 |
| **Hybrid** | 源素材 + AI 辅助画面 | 在现有镜头上叠加图形 |
| **Localization & Dub** | 字幕、配音、翻译现有视频 | 多语言分发 |
| **Podcast Repurpose** | 播客高光转视频 | 播客营销、audiogram |
| **Screen Demo** | 精美的软件录屏与 walkthrough | 产品 demo、教程、文档 |
| **Talking Head** | 以实拍为主的讲话人视频 | 演讲、vlog、访谈 |

每条流水线遵循同一结构化流程：

```
research -> proposal -> script -> scene_plan -> assets -> edit -> compose
```

每个阶段有专用 **director skill** — Markdown 指令文件，精确教 Agent 如何执行。Agent 读技能、用工具、自审、checkpoint 状态，并在创意决策点请求人工批准。

> **网页调研是一等阶段。** 写剧本前，Agent 会搜索 YouTube、Reddit、Hacker News、新闻与学术来源，收集数据点、受众问题、热门角度与视觉参考 — 并在结构化调研简报中引用。视频基于真实、最新信息，而非幻觉事实。

---

## 为什么选择 OpenMontage？

多数 AI 视频工具只从一条提示词给你单个片段。OpenMontage 提供 **端到端制作流水线** — 真实制作团队的结构化流程，由 AI Agent 自动化。

多数「免费 AI 视频」栈实质是「动画静图」。OpenMontage 也能做，但还可从免费/开放来源拉取 **真实素材**，语义排序、有意图地剪辑并渲染为正规时间线。

剪辑自有 talking-head 素材、从零生成完整动画讲解、把 2 小时播客切成十几条社交短片、将内容翻译配音至 10 种语言、用库存与 AI 场景做电影感品牌 teaser。**制作团队能做的事，OpenMontage 都能编排。**

- **10+ 制作流水线** — 讲解、talking head、录屏 demo、电影预告、动画、播客、本地化、纪录片蒙太奇、角色动画等
- **100+ 制作工具** — 覆盖视频生成、图像、TTS、音乐、混音、字幕、增强与分析
- **60+ 服务商集成** — 云 API、本地模型、图库、开放档案与制作 runtime，统一经评分选型层
- **700+ Agent 技能与制作知识文件** — 流水线导演、创意技法、质量清单与深度技术知识包，教 Agent 像专家一样用每个工具
- **参考驱动创作** — 粘贴喜欢的视频，Agent 生成可落地、差异化的计划，而非逼你从零发明完美提示词
- **无需付费视频模型的真实素材纪录片** — 用免费/开放运动镜头与档案剪出真实剪辑，而非静图 Ken Burns
- **内置实时网页调研** — 写剧本前 15–25+ 次搜索 YouTube、Reddit、新闻与学术来源，用真实数据 grounding
- **免费/本地与云服务商并存** — 每项能力都有开源本地替代与 premium API，用你已有的即可
- **无厂商锁定** — 自由更换服务商。评分器在 7 维（任务契合、输出质量、可控性、可靠性、成本、延迟、连续性）上排序并自动选最优
- **制作级质量门** — 交付承诺阻止幻灯片式成片；合成前校验避免浪费 GPU；强制渲染后自审（ffprobe + 抽帧 + 音频分析）。每次选型、风格与回退记入可审计轨迹
- **内置预算治理** — 执行前估算、支出上限、单步批准阈值，无意外账单

---

## 工作原理 {#how-it-works}

OpenMontage 采用 **Agent 优先架构**。没有代码编排器。你的 AI 编程助手就是编排器。

```
你：「做一条关于黑洞如何形成的讲解视频」
 |
 v
Agent 读取流水线 manifest（YAML）— 阶段、工具、评审标准、成功门
 |
 v
Agent 读取阶段 director skill（Markdown）— 如何执行各阶段
 |
 v
Agent 调用 Python 工具 — 评分选型在 7 维上排序每个工具
 |
 v
Agent 用 reviewer skill 自审 — schema 校验、playbook 合规、质量检查
 |
 v
Agent checkpoint 状态（JSON）— 可恢复，含决策日志与成本快照
 |
 v
Agent 提交你批准 — 每个创意决策由你掌控
 |
 v
合成前校验门 — 交付承诺、slideshow 风险、渲染器治理
 |
 v
渲染（Remotion 或 FFmpeg）— 与视觉语法匹配的合成引擎
 |
 v
渲染后自审 — ffprobe、抽帧、音频分析、承诺核对
 |
 v
最终视频输出 — 仅当自审通过
```

**Python 提供工具与持久化。** 创意决策、编排逻辑、评审标准与质量规范都在可读的指令文件（YAML manifest + Markdown skill）中，可 inspect 与定制。每个决策记录备选、置信度与理由。

---

## 架构

```
OpenMontage/
├── tools/              # 100+ 已注册制作工具（Agent 的「手」）
│   ├── video/          # 20+ 生成服务商 + compose、stitch、trim
│   ├── audio/          # 10+ 语音服务商 + 音乐、混音、增强
│   ├── graphics/       # 15+ 图像服务商 + 图表、代码片段、数学
│   ├── enhancement/    # 超分、抠图、人脸增强、调色
│   ├── analysis/       # 转写、场景检测、抽帧
│   ├── avatar/         # Talking head、口型同步
│   └── subtitle/       # SRT/VTT 生成
│
├── pipeline_defs/      # YAML 流水线 manifest（Agent 剧本）
├── skills/             # Markdown 技能（Agent 知识）
│   ├── pipelines/      # 各流水线阶段导演技能
│   ├── creative/       # 创意技法技能
│   ├── core/           # 核心工具技能
│   └── meta/           # 评审者、checkpoint 协议
│
├── schemas/            # 20+ JSON Schema（契约校验）
├── styles/             # 视觉风格 playbook（YAML）
├── remotion-composer/  # React/Remotion 视频合成引擎
├── lib/                # 核心基础设施（配置、checkpoint、流水线加载）
└── tests/              # 契约测试、QA 集成测试、eval harness
```

### 三层知识架构

```
Layer 1: tools/ + pipeline_defs/     「有什么」— 可执行能力 + 编排
Layer 2: skills/                     「怎么用」— OpenMontage 约定与质量线
Layer 3: .agents/skills/             「原理何在」— 外部技术知识包
```

每个工具声明依赖的 Layer 3 技能。Agent 读 Layer 1 知可用项，Layer 2 知用法规范，需要时读 Layer 3 深入技术。

---

## 支持的服务商

> **含定价与免费档的完整设置指南：** [`docs/PROVIDERS.md`](docs/PROVIDERS.md)

<details>
<summary><strong>视频生成 — 20+ 服务商</strong></summary>

| 服务商 | 类型 | 说明 |
|----------|------|-------|
| **Kling (fal.ai)** | 云 API | 经 fal.ai 网关，高质量、速度快 |
| **Kling Official** | 云 API | 官方直连 API，独立 `kling_official` 服务商 |
| **Atlas Cloud** | 云 API | Seedance、MiniMax、Hunyuan 等多模态统一网关 |
| **Seedance 2.0 (Volcengine Ark)** | 云 API | 官方直连，独立 `seedance_ark` 服务商 |
| **Seedance 2.5 / 2.0** | 云 API | 经支持网关的文本、图像与参考驱动视频工作流 |
| **Gemini Omni Flash** | 云 API | 对话式多模态视频生成与编辑 |
| **Runway Gen-4** | 云 API | 电影级质量，Gen-3 Alpha Turbo / Gen-4 Turbo / Gen-4 Aleph |
| **Google Veo 3.1** | 云 API | 经 Google GenAI 或 fal.ai 的 premium 电影感视频 |
| **Grok Imagine Video** | 云 API | 强参考图视频与 xAI 原生短视频生成 |
| **Higgsfield** | 云 API | 多模型编排，Soul ID 保持角色一致 |
| **MiniMax / H3** | 云 API | 高性价比，含文本、图像与参考驱动 H3 工作流 |
| **HeyGen** | 云 API | 多模型网关 |
| **WAN 2.1 / 2.2** | 本地 GPU | 免费本地变体 + 加速 ComfyUI 工作流 |
| **Hunyuan** | 本地 GPU | 免费、高质量 |
| **CogVideo** | 本地 GPU | 免费，2B 与 5B 变体 |
| **LTX-Video** | 本地 GPU / Modal | 本地免费或自托管云 |
| **Pexels** | 图库 | 免费库存视频 |
| **Pixabay** | 图库 | 免费库存视频 |
| **Wikimedia Commons** | 图库 | 免费/开放库存与档案视频 |

</details>

<details>
<summary><strong>图像生成 — 15+ 服务商</strong></summary>

| 服务商 | 类型 | 说明 |
|----------|------|-------|
| **FLUX** | 云 API | 顶尖画质 |
| **Google Imagen** | 云 API | Imagen 4 — 高质量、多宽高比 |
| **Grok Imagine Image** | 云 API | 强图像编辑、风格迁移与多图合成 |
| **GPT Image 2** | 云 API | OpenAI 图像模型 |
| **Seedream 5.0** | 云 API | 经网关的高保真文生图与图像编辑 |
| **Nano Banana 2** | 云 API | 多模态图像生成与编辑 |
| **Atlas Cloud** | 云 API | 统一访问多种图像模型家族 |
| **Recraft** | 云 API | 设计向生成 |
| **Kling Official** | 云 API | Kling 官方直连图像与参考工作流 |
| **Local Diffusion** | 本地 GPU | Stable Diffusion，免费 |
| **Pexels** | 图库 | 免费库存图像 |
| **Pixabay** | 图库 | 免费库存图像 |
| **Unsplash** | 图库 | 免费库存图像 |
| **ManimCE** | 本地 | 数学动画 |

</details>

<details>
<summary><strong>文本转语音 — 10+ 服务商</strong></summary>

| 服务商 | 类型 | 说明 |
|----------|------|-------|
| **ElevenLabs** | 云 API | Premium 音质 |
| **Google TTS** | 云 API | 700+ 音色、50+ 语言 — 适合本地化 |
| **Kling Official TTS** | 云 API | 已知 `voice_id` 时的官方 Kling 旁白 |
| **OpenAI TTS** | 云 API | 快速、实惠 |
| **Piper** | 本地 | 完全免费、离线 |
| **Azure Speech** | 云 API | 快速多语言语音服务 |
| **DashScope / Doubao / Fish Audio** | 云 API | 更多多语言与表现力音色 |

</details>

<details>
<summary><strong>音乐、音效与后期</strong></summary>

**音乐与音效：**

| 服务商 | 类型 | 说明 |
|----------|------|-------|
| **Suno AI** | 云 API | 含人声、歌词的全曲生成，任意风格，最长约 8 分钟 |
| **ElevenLabs Music** | 云 API | AI 音乐生成 |
| **ElevenLabs SFX** | 云 API | 音效生成 |

**后期（始终可用、始终免费）：**

| 工具 | 作用 |
|------|-------------|
| **FFmpeg** | 视频合成、编码、字幕烧录、音频 mux |
| **Video Stitch** | 多片段组装、交叉淡化、画中画、空间布局 |
| **Video Trimmer** | 精确裁剪与提取 |
| **Audio Mixer** | 多轨混音、ducking、淡入淡出 |
| **Audio Enhance** | 降噪、归一化 |
| **Color Grade** | 基于 LUT 的调色 |
| **Subtitle Gen** | 由时间戳生成 SRT/VTT |

**增强：**

| 工具 | 作用 |
|------|-------------|
| **Upscale** | Real-ESRGAN 图像/视频超分 |
| **Background Remove** | rembg / U2Net 抠图 |
| **Face Enhance** | 人脸质量增强 |
| **Face Restore** | CodeFormer / GFPGAN 人脸修复 |

**分析：**

| 工具 | 作用 |
|------|-------------|
| **Transcriber** | WhisperX 转写，带逐词时间戳 |
| **Scene Detect** | 自动场景边界检测 |
| **Frame Sampler** | 智能抽帧 |
| **Video Understand** | CLIP/BLIP-2 视觉-语言分析 |

**虚拟形象与口型：**

| 工具 | 作用 |
|------|-------------|
| **Talking Head** | SadTalker / MuseTalk 虚拟形象动画 |
| **Lip Sync** | Wav2Lip 音频驱动口型 |
| **Kling Avatar** | Kling 官方云虚拟主讲生成 |
| **Kling Lip Sync** | Kling 官方云口型，可指定人脸 |

**合成与渲染：**

| 引擎 | 类型 | 作用 |
|--------|------|-------------|
| **Remotion** | 本地（Node.js） | 基于 React 的程序化视频 — spring 动画图像场景、数据揭示、章节标题、hero 卡、TikTok 式逐词字幕、场景转场（fade/slide/wipe/flip）、Google Fonts、带 fade 曲线的音频与 TalkingHead 合成。**未配置视频生成服务商时，Agent 生成静图并由 Remotion 动画化为完整视频。** |
| **HyperFrames** | 本地（Node.js ≥ 22） | HTML/CSS/GSAP 程序化视频 — kinetic typography、产品 promo、launch reel、定制 motion graphics、registry 块（数据图、grain 叠加、shader 转场）、website-to-video 与 SVG 角色 rig 动画。经 `npx hyperframes` 消费，无需 checkout monorepo。 |
| **FFmpeg** | 本地 | 核心组装、编码、字幕烧录、音频 mux、调色 |

Runtime 在提案时选定（`render_runtime`）并经 `edit_decisions` 锁定。静默切换 runtime 属治理违规 — 见 `skills/core/hyperframes.md`。

</details>

---

## 风格系统

风格 playbook 定义制作的视觉语言：

| Playbook | 适用 |
|----------|----------|
| **Clean Professional** | 企业、教育、SaaS |
| **Flat Motion Graphics** | 社交媒体、TikTok、初创 |
| **Minimalist Diagram** | 技术深度、架构 |

Playbook 控制字体、色板、动效风格、音频配置与质量规则。Agent 读取 playbook 并在所有生成资产上一致应用。

---

## 平台输出配置

内置各主流平台渲染配置：

| 配置 | 分辨率 | 宽高比 |
|---------|-----------|--------------|
| YouTube Landscape | 1920x1080 | 16:9 |
| YouTube 4K | 3840x2160 | 16:9 |
| YouTube Shorts | 1080x1920 | 9:16 |
| Instagram Reels | 1080x1920 | 9:16 |
| Instagram Feed | 1080x1080 | 1:1 |
| TikTok | 1080x1920 | 9:16 |
| LinkedIn | 1920x1080 | 16:9 |
| Cinematic | 2560x1080 | 21:9 |

---

## 制作治理

OpenMontage 将视频制作视为工程 — 各阶段有质量门、审计轨迹与强制 enforcement。

### 质量门

- **人工批准门为强制而非建议** — 提案、剧本、场景规划、生成资产与发布均暂停待签。checkpoint 写入器在无记录批准时拒绝将 gated 阶段标为 completed；被取代的 checkpoint 均归档，审计轨迹（含门转换）在修订后仍保留。在 [Backlot 看板](#watch-it-happen--the-backlot-living-storyboard) 上可视化评审。
- **合成前校验** — 违反交付承诺（如「motion-led」却 80% 静图）、slideshow 风险分 critical 或缺少渲染器家族时阻止渲染，避免浪费 GPU。
- **渲染后自审** — 每次渲染后运行 ffprobe、在 4 个位置抽帧查黑帧与 broken overlay、分析静音与 clipping、核对交付承诺与字幕。未通过则不展示视频。
- **Slideshow 风险评分** — 六维分析（重复、装饰性画面、弱运动、镜头意图、过度依赖 typography、不支持的 cinematic 宣称）防止「动画 PPT」。
- **源媒体检查** — 用户提供素材时，系统探测每文件（分辨率、codec、声道、时长）并在任何创意决策前形成规划含义，不凭文件名幻觉内容。

### 评分服务商选型

视频生成、图像、TTS、音乐等每次工具选择经七维评分：任务契合 30%、输出质量 20%、可控 15%、可靠性 15%、成本 10%、延迟 5%、连续性 5%。胜出服务商与分数及全部备选记入决策轨迹。

选型器在打分前规范化松散简报。若 Agent 仅知「皮克斯风格短片且角色一致」，选型器会扩展为 scorer 友好的意图与风格信号，而非要求完美预填 `task_context`。

选型输出还暴露所选服务商的 `agent_skills`，便于写提示前立即读对应 Layer 3 技能。

### 决策审计轨迹

每次重大创意与技术选择 — 服务商、风格/playbook、音乐轨、音色、渲染器家族、任何回退 — 均记录备选、置信度与理由。累积决策日志跨阶段持久，可追溯成片为何如此。

### 预算控制

- **Estimate** — 执行前估算成本
- **Reserve** — 调用前锁定预算
- **Reconcile** — 事后记录实际支出
- **可配置模式** — `observe`（仅跟踪）、`warn`（记录超支）、`cap`（硬上限）
- **单步批准** — 超过阈值（默认 $0.50）暂停确认
- **总预算上限** — 默认 $10，可配置

无意外账单。Agent 在花钱前告知成本。

---

## Agent 兼容性

OpenMontage 适用于能读文件并执行 Python 的任意 AI 编程助手。各平台附带专用指令文件：

| 平台 | 配置文件 |
|----------|------------|
| **Claude Code** | `CLAUDE.md` |
| **Cursor** | `CURSOR.md` + `.cursor/rules/` |
| **GitHub Copilot** | `COPILOT.md` + `.github/copilot-instructions.md` |
| **Codex** | `CODEX.md` |
| **Windsurf** | `.windsurfrules` |

各平台文件均指向共享的 `AGENT_GUIDE.md`（操作指南与 Agent 契约）与 `PROJECT_CONTEXT.md`（架构参考）。

> **即将推出：** 经 **Ollama** 与 **LM Studio** 的本地 LLM 支持 — 无需云 LLM 即可跑完整流水线。

---

## 贡献

OpenMontage 为扩展而设计。最常见两类贡献：

### 添加新工具

1. 在对应 `tools/` 子目录创建 Python 文件
2. 继承 `BaseTool` 并实现工具契约
3. registry 自动发现 — 无需手动注册
4. 若需用法指导，添加 skill 文件

### 添加新流水线

1. 在 `pipeline_defs/` 创建 YAML manifest
2. 在 `skills/pipelines/<your-pipeline>/` 创建阶段 director skill
3. 引用现有工具 — 或按需新增

完整技术参考见 `docs/ARCHITECTURE.md`，服务商指南（设置、定价、免费档）见 `docs/PROVIDERS.md`，Agent 契约见 `AGENT_GUIDE.md`。

### 加入社区

我们在 [GitHub Discussions](https://github.com/calesthio/OpenMontage/discussions) 分享作品与想法：

- **[Show and Tell](https://github.com/calesthio/OpenMontage/discussions/categories/show-and-tell)** — 分享你的视频、好用提示词或创意工作流
- **[Ideas](https://github.com/calesthio/OpenMontage/discussions/categories/ideas)** — 建议新流水线、工具、风格 playbook 或集成
- **[Q&A](https://github.com/calesthio/OpenMontage/discussions/categories/q-a)** — 安装、流水线或排错问题

做了酷东西？发到 Show and Tell — 我们很想看。

---

## 联系

更新、发布与幕后笔记请关注 [@calesthioailabs](https://x.com/calesthioailabs)。

Bug、功能请求与工作流讨论请用 [GitHub Issues](https://github.com/calesthio/OpenMontage/issues) 与 [GitHub Discussions](https://github.com/calesthio/OpenMontage/discussions)，便于公开追踪。

---

## 测试

```bash
# Run contract tests (no API keys needed)
make test-contracts

# Run all tests
make test
```

---

## Star 历史

<a href="https://star-history.dera.page/#calesthio/OpenMontage&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=calesthio/OpenMontage&type=date&theme=dark&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=calesthio/OpenMontage&type=date&legend=top-left" />
    <img alt="Star 历史图表" src="https://star-history.dera.page/svg?repos=calesthio/OpenMontage&type=date&legend=top-left" />
  </picture>
</a>

---

## 许可证

[GNU AGPLv3](LICENSE)

---

**OpenMontage** — 由 AI 助手编排、具备真实质量 enforcement 的制作级视频。

若觉得有用，⭐ 对我们意义重大 — 也帮助更多人发现项目。

若愿进一步支持，[赞助项目](https://github.com/sponsors/calesthio) — OpenMontage 在业余时间构建，你的支持让它可持续。
