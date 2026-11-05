# 提供商与模型更新计划 — 2026 年 10 月 3 日

## 实施状态

已在 `codex/provider-model-refresh` 分支实现，基于 main `08e2151f`。
下文研究内容保留为原始计划；本表记录实际实现情况，并取代原先提议的文件名或未确认的端点。

| 系列 | 已实现的工具与行为 |
| --- | --- |
| Avatar V（Avatar 5） | `heygen_avatar`：v3 形象发现、资格校验、显式 V/IV 引擎、脚本或 supplied audio、同组参考形象、轮询/下载/恢复。已加入 avatar-spokesperson。 |
| Eleven v4 / Turbo | `elevenlabs_tts`：精确 model ID、输入上限、连续性字段、正确的 PCM 转 WAV 封装。`fal_elevenlabs_tts`：精确 v4 端点与 schema，不支持 speed/style，持久化队列任务与恢复。 |
| Wan 3.0 | `wan_fal_video`、`wan_atlas_video`、`wan_replicate_video`：各宿主独立契约。fal 与 Atlas 支持 text/image/reference；Replicate 仅 text/image。Atlas 为独立适配器，以保留既有 Atlas 目录行为。 |
| GPT Image 2.5 | `openai_image`：两种变体，generate/edit，本地 references/masks、透明度、usage metadata。`openai_fal_image` 与 `atlas_refresh_image`：两种变体及 edit 路由。 |
| Google Pro image | `google_imagen`：Gemini 3 Pro Image 与 3.1 Flash Image，本地 references 与 resolution。Nano Banana Pro 亦经 `gemini_fal_image`、`gemini_replicate_image`、`atlas_refresh_image`。Replicate 回退已显式禁用。 |
| Ideogram 4.5 | `ideogram_image`：直连 generation/edit/Precise Edit 与 dry-run 报价。`ideogram_fal_image`：generation/edit，Precise Edit 映射为已验证的 `edit_precision=high`。 |
| 其他视频 | `h3_max_video`：fal text/image/reference 路由。`ltx_api_video`：直连 Fast/Pro text/image/audio 生成，精确 duration/FPS/resolution 限制与恢复。 |
| 其他音频 | `gemini_tts`：3.8 Flash/Flash-Lite，单/多说话人 Interactions，WAV，API-key 音色库发现。`google_music`：显式 Lyria 3.5。`cartesia_tts`：Sonic 3.6，API 版本 2026-08-14。`inworld_tts`：TTS-2 与 Flash，含 usage metadata。 |
| 本地 | `qwen_image_21`：官方本地 Diffusers generation/edit/RGBA，无隐式权重下载。`comfyui_video` 仅在有 supplied API workflow 时识别 `ltx_2.5_local`；拒绝旧模型回退。 |
| 路由 | 显式 tool/host/model 过滤，同 host 工具按 tool 名排序，不支持的 edit 请求拒绝，未知价格不再计为免费。 |

校验使用 mock API 请求与抓取的官方 input schema。未运行付费生成、声音克隆、avatar 创建或模型权重下载。
`cost_usd=null` 表示未报价/未对账，而非免费；生产环境仍需核对当前价格与账户权益。OpenAI token usage 与 Inworld usage 已保留；未声称完整账单对账。

仍待外部条件：Kling 4/Flash 在本研究中无已验证的公开执行契约；本地 LTX-2.5 需已安装权重与导出 workflow；Qwen 需兼容 CUDA/Diffusers 与已下载权重。Gemini Live 仍为原计划中单独范围的 streaming/session 集成。

契约来源：[fal OpenAPI](https://fal.ai/api/openapi/queue/openapi.json)、
[Atlas model pages](https://www.atlascloud.ai/models)、
[Replicate Wan schema](https://replicate.com/alibaba/wan-3/api/schema)、
[Replicate Nano Banana Pro schema](https://replicate.com/google/nano-banana-pro/api/schema)、
[LTX OpenAPI](https://docs.ltx.io/openapi.json)、
[Ideogram 4.5](https://developer.ideogram.ai/api-reference/images/generate/ideogram-4-5)、
[HeyGen Avatar V](https://developers.heygen.com/avatar-v)、
[Cartesia TTS](https://docs.cartesia.ai/api-reference/tts/bytes)、
[Inworld model IDs](https://docs.inworld.ai/docs/tts/tts-models)、
[Qwen model card](https://huggingface.co/Qwen/Qwen-Image-2.1)。

研究窗口：**2026 年 9 月 3 日–10 月 3 日**，相邻/更早发布见下文区分。范围：媒体生成、编辑、旁白、音乐、avatar 及有用的本地替代方案。通用对话模型不在本次 provider-update 范围内。

基线：`main` 自 `51330d17` fast-forward 至 `08e2151f`（123 次提交）。已完成 registry 发现与实现检查。本文为经调研的实施计划，并非声称新集成已在付费 API 上实测。优先级反映生产实用性与接入广度；无全面可比的用量排名，故「热门」为短名单而非实测市场份额。

## 1. 超出请求模型的新增项

| 优先级 | 模型 | 发布依据 | 提供商路径 | 工作与价值 |
|---|---|---|---|---|
| P1 | **Qwen Image 2.1** | 9 月 20 日，Qwen 官方公告 | 优先通过 local/ComfyUI 评估官方权重。在宣传 cloud 支持前验证具名 DashScope 或聚合端点。 | 统一 generation/editing 与原生透明度：利于可复用前景素材、叠加与 targeted edits。当前 `dashscope_image` 列出 2.0 Pro；未发现显式 2.1 集成。 |
| P1 | **Gemini 3.8 Flash TTS + Flash-Lite TTS** | 9 月 22 日 GA，Gemini changelog | Google Gemini API | 新增独立适配器 `gemini_tts`。当前 `google_tts` 使用 Cloud Text-to-Speech，仅改 model 字符串不足。增加音色发现、speaker turns、delivery controls 与 audio-format 处理。 |
| P1 | **Lyria 3.5** | 9 月 3 日 GA，Gemini changelog | Google Gemini API | 升级 `google_music`（现围绕 `lyria-3-pro-preview`）。显式 model 选择；对照新契约校验 duration、structure、vocals、image conditioning、输出编码与成本。 |
| P1 调研；门控实施 | **Kling 4.0 + 4.0 Flash** | 9 月下旬公告；fal 页日期 9 月 29 日 | Kling 直连与 fal early access；Atlas 须在端点验证后 | 规划 text/image/reference 生成与 video editing。变体区分。账户访问与精确 request schema 未验证前勿标为普遍可用。 |
| P3 / 独立产品范围 | **Gemini 3.8 Live + Live Extended Thinking** | 9 月 15 日 GA，Gemini changelog | Google Live API | 适用于交互语音/avatar 体验，非离线视频旁白必需。需 session lifecycle 与 streaming audio；排在 batch TTS 之后。 |

来源：[Qwen Image 2.1](https://qwen.ai/blog?id=qwen-image-2.1)、[Gemini release notes](https://ai.google.dev/gemini-api/docs/changelog)、[Gemini TTS guide](https://ai.google.dev/gemini-api/docs/speech-generation)、[Lyria music guide](https://ai.google.dev/gemini-api/docs/music-generation)、[Kling official release](https://kling.ai/dev/model-release/kling-4)、[fal Kling 4 early-access status](https://fal.ai/kling-4)。

Kling 说明：fal 明确其展示片段来自 Kling，而非 fal API。early-access 页可作规划依据，不能证明公开端点可用。将宣传的 future 4K/HDR/extension 与当前能力分开对待。

## 2. 请求模型：具体集成映射

| 系列 | 已验证提供商面 | 仓库缺口 | 实施 |
|---|---|---|---|
| **HeyGen Avatar V** | HeyGen 开发者索引文档化 Avatar V 与 v3 rendering | Registry 无 HeyGen avatar 适配器。`heygen_video` 为通用 video-model 网关，非 Avatar V 实现。 | 新建 `tools/avatar/heygen_avatar.py`；发现合格 avatar/looks，显式选引擎，提交/轮询/下载 v3 任务，支持 supplied audio 与 scripts。校验 look 资格并拒绝 silent IV 回退。 |
| **Eleven v4 + v4 Turbo** | ElevenLabs 直连 API；fal 文档 `elevenlabs/tts/eleven-v4` | 直连适配器接受任意 model ID 但默认 v2；非已验证 v4 支持。fal 适配器目录仅 v3/v2/v2.5。 | 更新 `elevenlabs_tts` 与 `fal_elevenlabs_tts`：精确 model ID、每模型设置、定价、voice 兼容、长文本拼接。直连 Turbo 已由发布确认；fal Turbo 为单独验证任务。 |
| **Wan 3.0** | fal、Replicate、Atlas Cloud | `wan_video` 为本地 GPU 路径。Atlas 目录无 Wan 3。 | 新增 `wan_fal_video`、`wan_replicate_video`；扩展 `atlas_models.py`/`atlas_video.py`。本地 Wan 工具保持独立。逐条验证 text/image/reference 路由，含 native audio 与长 duration。 |
| **GPT Image 2.5 Flare + Sunburst** | OpenAI API；Atlas 宣传两变体 API 可用 | `openai_image` 仅声明 GPT Image 2 并实现 generation；Atlas 目录亦仅 Image 2。 | 直连与 Atlas 适配器加入两精确变体。实现直连 editing（references/masks）、模型专属 size/quality/transparency 与真实 usage 成本对账。 |
| **Ideogram 4.5 + Precise Edit** | Ideogram 直连 v2 API；fal generation/edit 端点 | 未发现专用 Ideogram 适配器 | 新增直连 `ideogram_image` 与 fal `ideogram_fal_image`。generation、普通 edit 与 Precise Edit 为显式操作。在声称与直连 parity 前验证 fal 是否提供 precise mode。 |

主要参考：

- [HeyGen developer index](https://developers.heygen.com/llms.txt) — Avatar V 按 look opt-in；索引称 Avatar IV 为默认 v3 引擎。[4 月研究文](https://www.heygen.com/research/avatar-v-model) 表明 Avatar V 早于本研究窗口，尽管 launch 页在 9 月更新。
- [Eleven v4 release, September 28](https://elevenlabs.io/blog/eleven-v4)、[fal v4 schema](https://fal.ai/models/elevenlabs/tts/eleven-v4/api)。勿通过盲目保留旧 `fal-ai/` 前缀推导新端点。
- [fal Wan 3](https://fal.ai/wan-3)、[Replicate Wan 3](https://replicate.com/alibaba/wan-3)、[Atlas Wan 3](https://www.atlascloud.ai/models/wan-3.0)。fal 发布 `alibaba/wan-3.0/text-to-video`、`/image-to-video`、`/reference-to-video`；Replicate 发布 `alibaba/wan-3`。可用性已验证；此处未确立原始 9 月发布日。
- [OpenAI Image 2.5 release, September 8](https://openai.com/index/introducing-chatgpt-images-2-5/)、[Sunburst model contract](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)、[Atlas availability](https://www.atlascloud.ai/free-gpt-image-2.5-generator)。实施前仍须抓取精确 Atlas route ID 与 schema。
- [Ideogram model page](https://ideogram.ai/models/4.5/)、[direct API overview](https://developer.ideogram.ai/ideogram-api/api-overview)、[fal generation](https://fal.ai/models/ideogram/v4.5)、[fal edits](https://fal.ai/models/ideogram/v4.5/edit/api)。模型与 API 可用性已确认；精确 9 月 30 发布日见于二次报道，非 dated 一手公告。

## 3. 严格窗口外的重要补漏

**Google 图像跟进：**「Google image pro 3」最可能指 **Gemini 3 Pro Image / Nano Banana Pro**。Google 公告日期为 2025 年 11 月 20 日，故作为请求覆盖缺口而非 9 月 launch。当前 Google 文档标识 `gemini-3-pro-image`；使用当前文档 ID，勿假设旧 preview 后缀。[Google announcement](https://blog.google/innovation-and-ai/products/nano-banana-pro/)、[current image API guide](https://ai.google.dev/gemini-api/docs/image-generation)。

**P1 提供商映射：** 优先 Google 直连（`google_imagen` 已有 Gemini 后端，但声明的 Gemini model 仅 `gemini-2.5-flash-image` 且请求传 text prompt）。增加显式 Pro 支持、reference-image editing、resolution 控制及 per-model 验证/定价。在 Atlas 目录增加 Pro generation/edit 路由；已 catalog 的 Nano Banana 2 不覆盖 Pro。fal 与 Replicate 适配器作额外 host 覆盖：[fal Pro API](https://fal.ai/models/fal-ai/nano-banana-pro/api)、[Replicate Pro](https://replicate.com/google/nano-banana-pro)、[Atlas model index](https://www.atlascloud.ai/docs/en/openapi-index)。确认各 host 上 generation/edit parity。勿将 Nano Banana Pro 与 Nano Banana 2 混为一谈，即便旧聚合营销互换名称。

| 优先级 | 模型 | 提供商 | 建议 |
|---|---|---|---|
| P1 | **MiniMax H3 Max** | fal | 在 `minimax_fal_video` 增加 distinct variant；当前代码指向 Hailuo-03 路由。Max 为独立 post-trained 模型，非 base H3 别名。[Announcement dated August 27](https://blog.fal.ai/introducing-h3-max-by-fal/)；[exact API route](https://fal.ai/models/minimax/h3-max/text-to-video/api)。 |
| P2 | **LTX-2.5 Fast / Pro** | LTX 直连；workflow 验证后 local/ComfyUI | 新建直连 LTX 适配器；单独更新本地 model/runtime 契约。当前 local/Modal 工具暴露 LTX-2。[Model docs](https://docs.ltx.io/models/ltx-2-5)；[September 2 update](https://docs.ltx.io/api-changelog/2026/9/2) 增加 resolution/frame-rate 选项，非初始模型发布。 |
| P2 | **Cartesia Sonic 3.6** | Cartesia 直连 | 新 TTS 提供商作额外旁白选项；在推荐现有 voice 前衡量 quality/latency/cost。[Official blog](https://www.cartesia.ai/ja/blog) 有 9 月 listing，但 [original announcement](https://t.co/lYA5Ym6hCX) 为 8 月 27 日。勿标为 9 月新模型。 |
| P2 调研 | **Inworld TTS-2 / Flash** | Inworld 直连 | 可用且相关，但未验证原始 9 月 launch 日。验证 API 契约，仅在 voice quality/language 覆盖 justify 时再增适配器。[Provider pricing and availability](https://inworld.ai/pricing)。 |

勿将 **Seedance 2.5、MiniMax H3、Seedream 5 Pro、Gemini Omni 或 Nano Banana 2** 计为完全缺失：已拉代码已有集成。应审计 operation 覆盖与 provider parity。Qwen Image 3 与 Krea 2 亦早于本窗口；属后续覆盖审计，非 9 月发布列表。[Qwen Image 3 announcement](https://qwen.ai/blog?id=qwen-image-3.0)、[Krea technical report](https://www.krea.ai/blog/krea-2-technical-report)。

## 4. 交付顺序与验收标准

### PR 1 — 模型契约与路由正确性

扩展现有 catalog 方式，而非在各 tool 散落 model 名列表。分别记录 model family 与 hosting provider、精确 endpoint、operation、access status、verified-on 日期、supported media、duration/resolution 约束与 pricing basis。保留 provider 专属 schema；model 名一致不保证 input 一致。

审计 `image_selector`、`video_selector`、`tts_selector` 的 operation-aware 路由与显式 tool/host 选择。Registry 发现已存在。尤其 direct 与 fal MiniMax 工具均报告 `provider="minimax"`；须测试 hosting preference 无歧义。经 selector 保留 references、masks、audio flags 与精确 model 选择。不支持特性须明确失败，而非在适配中消失。

### PR 2 — 图像升级

GPT Image 2.5 直连 + Atlas，Gemini 3 Pro Image 直连 + Atlas，Ideogram 直连 + fal，随后 Qwen 2.1 local/workflow 验证。add/edit schema、支持处 alpha-preserving 输出、reference/mask 验证与 model-specific 成本估计。将 OpenAI 通用 FLUX skill 指针换为适用 provider 指引。随后 fal/Replicate Pro 覆盖。fal [current model index](https://fal.ai/explore/search) 亦列出 Image 2.5 Flare/Sunburst edit 路由：抓取各精确 generation/edit schema 后纳入 fal Image 2.5 适配器。

验收：每条路由 mock payload 测试；五步 edit 序列检查 subject/layout 保持；masked-edit 与 transparent-output 检查；selector 保留全部 conditioning input；legacy GPT Image 2 仍可用。

### PR 3 — 语音与音乐

Eleven v4/v4 Turbo 直连与 fal v4，新 Gemini TTS 适配器，Lyria 3.5 更新。Cloud TTS 与 Gemini TTS 保持区分。对照各 provider 验证 voice ID/settings、dialogue alignment 与 stitching、声明输出格式及 duration/cost 报告。

验收：短/长旁白 fixture、支持处 two-speaker fixture、decoding/sample-rate 检查、若暴露则 timestamp 检查，及基于 captured usage 响应的定价测试。付费样本仅作单独范围验证运行。

### PR 4 — 跨聚合器的 Wan，及 H3 Max

实现 fal 与 Replicate 适配器，随后 Atlas 目录增补。仅在契约真正一致处共享 job-lifecycle helper。存储 task ID 并支持 polling timeout 后 resume，避免重试盲目再建付费任务。

验收：各 host 的 submit/poll/error/download fixture；text/image/reference 路由测试；native audio 与实际 duration/resolution 验证；provenance 与 cost 记录保留 host+model+operation。

### PR 5 — Avatar V

实现直连 avatar 适配器并在 avatar pipeline tool 菜单暴露。将 avatar discovery/eligibility 与 generation 分离。尊重现有账户资产及任何新 identity enrollment 的 provider consent 要求。

验收：合格与不合格 look fixture、显式 engine 选择、audio-driven 与 script-driven 请求、失败任务处理，及长形式使用前批准的短 lip-sync 样本。

### PR 6 — 访问门控与次要提供商

Kling 4/Flash 在 schema 与 access 可用后；LTX-2.5 直连/local；Cartesia 与 Inworld 在对比样本后。Gemini Live 仍为独立交互特性提案。勿因这些依赖阻塞可用模型更新。

每项集成同时更新 `docs/PROVIDERS.md`、相关 Layer 2/3 skills、registry metadata、cost handling 与 contract tests。普通 provider 新增无需生产 pipeline  redesign。

## 5. 验证与剩余研究

- 公开文档验证可用性，非本账户是否 entitled。未做付费生成或凭据检查。
- 实施前抓取 Atlas Image 2.5/Wan、直连 Eleven v4/Turbo、Ideogram Precise Edit、HeyGen Avatar V 的精确 route schema/定价。HeyGen 详细 Markdown 页本次未能抓取；官方 index 可读。
- Qwen 2.1 cloud hosting、fal v4 Turbo、Atlas Kling 4 仍未验证。勿凭命名惯例臆造 ID。
- 对比 like-for-like prompt、duration、resolution 与 native audio。Provider 营销排名非 OpenMontage 独立评估。
- 先跑 targeted adapter/selector 测试。跨 provider 付费样本需具体成本测试批次；本规划任务不执行。

## 6. Pull 与本地工作保留

更新最初与本地 provider 文档及较旧未跟踪 Atlas 文件冲突。命名 stash `codex-before-provider-research-main-update-2026-10-03` 仍完整。原冲突文件亦在 `.tmp/provider-update-backup-2026-10-03/`。

本地架构与 Google TTS 编辑已重新应用。Provider 文档已与当前 upstream catalog 对账，保留 setup 指引而非恢复过时 route 声称。冲突 Atlas 代码/测试/skill 的 upstream 版本仍活跃；较旧本地版本保存在 backup 与 stash。无未解决 Git 冲突。其他既有工作保持不动。
